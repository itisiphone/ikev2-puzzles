"""
Cost measurements for the IKEv2 / RFC 8019 PRISM models.

Measures, on this machine, the cost constants used by the models, and
writes:
  costs_results.csv    one row per operation: mean and standard deviation
  puzzle_results.csv   one row per solved puzzle: k, seconds, PRF calls
  costs_summary.txt    environment, summary, and a PRISM constants block

Every measurement is repeated (default 30 times). Fast operations are timed
in batches so that timer resolution does not matter.

Usage:  python measure_costs.py            (full run, about 2-4 minutes)
        python measure_costs.py --quick    (smoke test, a few seconds)
"""

import argparse
import csv
import hashlib
import hmac
import os
import platform
import random
import ssl
import statistics
import sys
import time

# ---------------------------------------------------------------- settings
REPS = 30                       # repetitions per measurement (per measurement)
PUZZLE_KS = [8, 10, 12, 14, 16, 18]   # difficulties solved REPS times each
PUZZLE_K_SLOW = 20              # solved fewer times (each solve takes seconds)
PUZZLE_REPS_SLOW = 5
SEED = 20261120                 # fixed seed: cookies and key counters reproducible

# RFC 3526 group 14 (2048-bit MODP), generator 2
P14 = int((
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1"
    "29024E088A67CC74020BBEA63B139B22514A08798E3404DD"
    "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245"
    "E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED"
    "EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3D"
    "C2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F"
    "83655D23DCA3AD961C62F356208552BB9ED529077096966D"
    "670C354E4ABC9804F1746C08CA18217C32905E462E36CE3B"
    "E39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9"
    "DE2BCBF6955817183995497CEA956AE515D2261898FA0510"
    "15728E5A8AACAA68FFFFFFFFFFFFFFFF"), 16)


# ---------------------------------------------------------------- helpers
def cpu_name():
    """Best-effort CPU model string."""
    if sys.platform.startswith("win"):
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                 r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
            name, _ = winreg.QueryValueEx(key, "ProcessorNameString")
            mhz, _ = winreg.QueryValueEx(key, "~MHz")
            return f"{name.strip()} (~{mhz} MHz reported)"
        except OSError:
            pass
    if os.path.exists("/proc/cpuinfo"):
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
    return platform.processor() or "unknown"


def time_batch(fn, batch, reps):
    """Run fn() `batch` times per repetition; return per-call seconds for each rep."""
    fn()  # warm-up
    out = []
    for _ in range(reps):
        t0 = time.perf_counter()
        for _ in range(batch):
            fn()
        out.append((time.perf_counter() - t0) / batch)
    return out


class Recorder:
    def __init__(self):
        self.rows = []

    def add(self, name, per_call, batch, note=""):
        mean = statistics.mean(per_call)
        sd = statistics.stdev(per_call) if len(per_call) > 1 else 0.0
        self.rows.append({"operation": name, "reps": len(per_call), "batch": batch,
                          "mean_s": mean, "std_s": sd, "note": note})
        print(f"  {name:<40s} {mean*1e6:12.2f} us  (sd {sd*1e6:9.2f} us, n={len(per_call)})")
        return mean


# ---------------------------------------------------------------- RFC 8019 puzzle
def solve_puzzle(cookie, k, start):
    """Find 4 different equal-size keys K with PRF(K, cookie) ending in >= k zero bits
    (RFC 8019 s7.1.3, PRF = HMAC-SHA-256). Returns (keys, PRF calls)."""
    mask = (1 << k) - 1
    digest = hmac.digest
    from_bytes = int.from_bytes
    keys, ctr, tries = [], start, 0
    while len(keys) < 4:
        key = ctr.to_bytes(8, "big")
        ctr += 1
        tries += 1
        if from_bytes(digest(key, cookie, "sha256")[-4:], "big") & mask == 0:
            keys.append(key)
    return keys, tries


def verify_puzzle(cookie, keys, k):
    mask = (1 << k) - 1
    return all(int.from_bytes(hmac.digest(key, cookie, "sha256")[-4:], "big") & mask == 0
               for key in keys) and len(set(keys)) == 4


# ---------------------------------------------------------------- IKEv2 key derivation (RFC 7296 s2.13, s2.14)
def prf_plus(key, seed, length):
    out, t, i = b"", b"", 1
    while len(out) < length:
        t = hmac.digest(key, t + seed + bytes([i]), "sha256")
        out += t
        i += 1
    return out[:length]


def derive_sk(ni, nr, shared, spii, spir):
    skeyseed = hmac.digest(ni + nr, shared, "sha256")
    # SK_d, SK_pi, SK_pr (32 B each), SK_ei, SK_er (AES-256, 32 B), SK_ai, SK_ar (32 B)
    return prf_plus(skeyseed, ni + nr + spii + spir, 7 * 32)


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="smoke test with tiny repetitions")
    args = ap.parse_args()

    reps = 3 if args.quick else REPS
    ks = [8, 10, 12] if args.quick else PUZZLE_KS
    k_slow, reps_slow = (14, 2) if args.quick else (PUZZLE_K_SLOW, PUZZLE_REPS_SLOW)
    scale = 0.05 if args.quick else 1.0          # shrinks batch sizes in quick mode

    def b(n):
        return max(1, int(n * scale))

    rng = random.Random(SEED)

    def rb(n):  # random bytes, reproducible, works on Python < 3.9
        return rng.getrandbits(8 * n).to_bytes(n, "big")

    rec = Recorder()
    t_start = time.time()

    env = [
        f"date        : {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"cpu         : {cpu_name()}",
        f"logical cpus: {os.cpu_count()}",
        f"os          : {platform.platform()}",
        f"python      : {sys.version.split()[0]} ({platform.python_implementation()})",
        f"openssl     : {ssl.OPENSSL_VERSION}",
        f"mode        : {'QUICK smoke test' if args.quick else 'full'}  reps={reps}",
    ]
    print("\n".join(env))

    # -------------------------------------------- 1 PRF and cookie
    print("\n[1] PRF (HMAC-SHA-256) and cookie")
    cookie = rb(32)
    key8 = rb(8)
    t_prf = rec.add("prf_hmac_sha256_8B_key_32B_msg",
                    time_batch(lambda: hmac.digest(key8, cookie, "sha256"), b(100000), reps), b(100000),
                    "one PRF call as used by the puzzle (C-level hmac.digest)")
    secret, ni, ip, spii = rb(32), rb(32), rb(4), rb(8)
    t_cookie = rec.add("cookie_sha256",
                       time_batch(lambda: hashlib.sha256(ni + ip + spii + secret).digest(), b(100000), reps),
                       b(100000), "RFC 7296 s2.6: Hash(Ni | IPi | SPIi | secret)")

    # -------------------------------------------- 2 puzzles
    print("\n[2] RFC 8019 puzzles (4 keys each)")
    puzzle_rows = []

    def run_puzzles(k, n):
        for rep in range(n):
            c = rb(32)
            start = rng.getrandbits(48)
            t0 = time.perf_counter()
            keys, tries = solve_puzzle(c, k, start)
            dt = time.perf_counter() - t0
            assert verify_puzzle(c, keys, k)
            puzzle_rows.append({"k": k, "rep": rep + 1, "seconds": dt, "prf_calls": tries})
        sel = [r for r in puzzle_rows if r["k"] == k]
        secs = [r["seconds"] for r in sel]
        calls = sum(r["prf_calls"] for r in sel)
        per_try = sum(secs) / calls
        print(f"  k={k:2d}: mean {statistics.mean(secs):9.4f} s  "
              f"(sd {statistics.stdev(secs) if len(secs) > 1 else 0:8.4f}, n={len(secs)})  "
              f"PRF calls/puzzle {calls/len(sel):12.0f} (expected {4*2**k})  "
              f"time per call {per_try*1e6:.3f} us")

    for k in ks:
        run_puzzles(k, reps)
    run_puzzles(k_slow, reps_slow)

    all_calls = sum(r["prf_calls"] for r in puzzle_rows if r["k"] >= ks[-1])
    all_secs = sum(r["seconds"] for r in puzzle_rows if r["k"] >= ks[-1])
    t_try = all_secs / all_calls       # per-call cost inside the solver loop, large k only
    c_verify = rb(32)
    keys_v, _ = solve_puzzle(c_verify, 8, 0)
    rec.add("puzzle_verify_4_keys",
            time_batch(lambda: verify_puzzle(c_verify, keys_v, 8), b(20000), reps), b(20000),
            "responder checks a PS payload (4 PRF calls)")

    # -------------------------------------------- 3 key derivation
    print("\n[3] IKEv2 key derivation (SKEYSEED + prf+ for 7 x 32 bytes)")
    nr, spir, shared = rb(32), rb(8), rb(256)
    t_derive = rec.add("sk_derivation_prfplus",
                       time_batch(lambda: derive_sk(ni, nr, shared, spii, spir), b(20000), reps),
                       b(20000), "RFC 7296 s2.13/s2.14")

    # -------------------------------------------- 4 DH and signatures
    have_crypto = True
    try:
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import dh, ec, padding, rsa, x25519
    except ImportError:
        have_crypto = False
        print("\n[4] SKIPPED: the 'cryptography' package is not installed "
              "(pip install cryptography), DH and signature costs not measured")

    results = {}
    if have_crypto:
        print("\n[4] Diffie-Hellman")
        peer_x = x25519.X25519PrivateKey.generate().public_key()
        results["x25519_keygen"] = rec.add("x25519_keygen",
            time_batch(lambda: x25519.X25519PrivateKey.generate().public_key(), b(2000), reps), b(2000))
        sk_x = x25519.X25519PrivateKey.generate()
        results["x25519_shared"] = rec.add("x25519_shared_secret",
            time_batch(lambda: sk_x.exchange(peer_x), b(2000), reps), b(2000))

        peer_e = ec.generate_private_key(ec.SECP256R1()).public_key()
        results["p256_keygen"] = rec.add("ecdh_p256_keygen",
            time_batch(lambda: ec.generate_private_key(ec.SECP256R1()).public_key(), b(2000), reps), b(2000))
        sk_e = ec.generate_private_key(ec.SECP256R1())
        results["p256_shared"] = rec.add("ecdh_p256_shared_secret",
            time_batch(lambda: sk_e.exchange(ec.ECDH(), peer_e), b(2000), reps), b(2000))

        params14 = dh.DHParameterNumbers(P14, 2).parameters()
        peer_m = params14.generate_private_key().public_key()
        results["modp_keygen"] = rec.add("modp2048_keygen",
            time_batch(lambda: params14.generate_private_key().public_key(), b(100), reps), b(100))
        sk_m = params14.generate_private_key()
        results["modp_shared"] = rec.add("modp2048_shared_secret",
            time_batch(lambda: sk_m.exchange(peer_m), b(100), reps), b(100))

        print("\n[5] Signatures over a 300-byte AUTH input")
        msg = rb(300)
        ek = ec.generate_private_key(ec.SECP256R1())
        esig = ek.sign(msg, ec.ECDSA(hashes.SHA256()))
        results["ecdsa_sign"] = rec.add("ecdsa_p256_sign",
            time_batch(lambda: ek.sign(msg, ec.ECDSA(hashes.SHA256())), b(2000), reps), b(2000))
        results["ecdsa_verify"] = rec.add("ecdsa_p256_verify",
            time_batch(lambda: ek.public_key().verify(esig, msg, ec.ECDSA(hashes.SHA256())), b(2000), reps), b(2000))
        rk = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        rsig = rk.sign(msg, padding.PKCS1v15(), hashes.SHA256())
        results["rsa_sign"] = rec.add("rsa2048_sign",
            time_batch(lambda: rk.sign(msg, padding.PKCS1v15(), hashes.SHA256()), b(200), reps), b(200))
        results["rsa_verify"] = rec.add("rsa2048_verify",
            time_batch(lambda: rk.public_key().verify(rsig, msg, padding.PKCS1v15(), hashes.SHA256()), b(2000), reps), b(2000))

    # -------------------------------------------- write files
    with open("costs_results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["operation", "reps", "batch", "mean_s", "std_s", "note"])
        w.writeheader()
        w.writerows(rec.rows)
    with open("puzzle_results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["k", "rep", "seconds", "prf_calls"])
        w.writeheader()
        w.writerows(puzzle_rows)

    lines = ["Cost measurements", "=" * 25, *env, ""]
    lines.append(f"PRF call (hmac.digest, C level)      : {t_prf*1e6:.3f} us")
    lines.append(f"PRF call inside Python solver loop   : {t_try*1e6:.3f} us "
                 f"(ratio {t_try/t_prf:.2f}; fitted on k >= {ks[-1]})")
    lines.append("Puzzle cost law check (mean seconds vs 4*2^k*t_try):")
    for k in sorted({r['k'] for r in puzzle_rows}):
        secs = [r["seconds"] for r in puzzle_rows if r["k"] == k]
        lines.append(f"   k={k:2d}  measured {statistics.mean(secs):9.4f} s   "
                     f"predicted {4*2**k*t_try:9.4f} s   n={len(secs)}")
    lines.append("")

    if have_crypto:
        lines += [
            "PRISM constants (suite A = X25519 + ECDSA P-256; suite B in comments = MODP-2048 + RSA-2048)",
            "// paste into ikev2_rq1.sm and ikev2_rq2.sm, replacing the earlier values",
            f"const double t_PRF     = {t_prf:.6e};   // HMAC-SHA-256, one call",
            f"const double t_cookie  = {t_cookie:.6e};   // SHA-256 cookie",
            f"const double t_dh_gen  = {results['x25519_keygen']:.6e};   // X25519 key pair"
            f"   (B: {results['modp_keygen']:.6e})",
            f"const double t_dh_auth = {results['x25519_shared'] + t_derive:.6e};   // X25519 shared + SK_* derivation"
            f"   (B: {results['modp_shared'] + t_derive:.6e})",
            f"const double t_sig     = {(results['ecdsa_sign'] + results['ecdsa_verify'])/2:.6e};"
            f"   // ECDSA P-256, mean of sign and verify"
            f"   (B: {(results['rsa_sign'] + results['rsa_verify'])/2:.6e})",
        ]
    else:
        lines.append(f"const double t_PRF = {t_prf:.6e};   // install 'cryptography' for the other constants")

    lines.append("")
    lines.append(f"total run time: {time.time() - t_start:.1f} s")
    with open("costs_summary.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n" + "\n".join(lines))
    print("\nWritten: costs_results.csv, puzzle_results.csv, costs_summary.txt")


if __name__ == "__main__":
    main()
