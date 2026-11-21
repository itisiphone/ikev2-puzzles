"""Compare the Jacobi results in validation/ with the Gauss-Seidel results of E4 and E5.

Run from the repository root:  python validation/compare_jacobi.py
Prints, for each Jacobi file, how many values were compared and the largest absolute
difference; PRISM errors (non-convergence) are listed separately.
"""
import os

PAIRS = [
    ("validation/V_jacobi_E4_baseline.csv", "experiments/E4_baseline.csv", {}),
    ("validation/V_jacobi_E4_T2.csv", "experiments/E4_T2.csv", {"rho": "0.5"}),
    ("validation/V_jacobi_E4_T3.csv", "experiments/E4_T3.csv", {}),
    ("validation/V_jacobi_E5.csv", "experiments/E5_k18.csv", {}),
]


def parse(path):
    """PRISM -exportresults csv: blocks of a quoted property line, a header, rows."""
    out, errors, prop, header = {}, [], None, None
    with open(path, errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('"'):
                prop, header = line, None
                continue
            if line.startswith("Error") or line.startswith("Consider"):
                if line.startswith("Error"):
                    errors.append((prop, line))
                continue
            if header is None:
                header = line.split(",")
                continue
            vals = line.split(",")
            key = tuple(zip(header[:-1], vals[:-1]))
            out[(prop, key)] = float(vals[-1])
    return out, errors


def main():
    for jac, gs, fixed in PAIRS:
        if not (os.path.exists(jac) and os.path.exists(gs)):
            print(f"{jac}: missing file")
            continue
        J, jerr = parse(jac)
        G, _ = parse(gs)
        n, worst = 0, 0.0
        for (prop, key), v in J.items():
            want = dict(key)
            want.update(fixed)
            match = [gv for (gp, gk), gv in G.items()
                     if gp == prop and all(dict(gk).get(a) == b for a, b in want.items())]
            if len(match) != 1:
                print(f"  no unique match for {prop} {key}")
                continue
            n += 1
            worst = max(worst, abs(v - match[0]))
        print(f"{jac}: {n} values compared, max |Jacobi - Gauss-Seidel| = {worst:.2e}")
        for prop, msg in jerr:
            print(f"  {prop}: {msg}")


if __name__ == "__main__":
    main()
