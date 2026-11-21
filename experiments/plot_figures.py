"""
Stage 5: turn the PRISM experiment results (experiments/*.csv) into the paper's
figures 3-7 and a table of model sizes.

Run from the Research_model folder:   python experiments/plot_figures.py
Outputs go to experiments/figures/:
  fig3_E1_forged_puzzles.pdf/.png      RQ1: unavailability vs D_max
  fig4_E2_attacker_speed.pdf/.png      RQ1: unavailability vs attacker speed
  (version 2: E2 and E3 are panels (a) and (b) of fig4_E2_E3; categorical axes use
   markers only; every figure is drawn at its printed width, so fonts stay >= 6 pt)
  fig5_E4_defences.pdf/.png            RQ2: three defences under T2 and T3
  fig6_E5_table_lifetime.pdf/.png      RQ2: table size x lifetime heat maps
  fig7_E6_difficulty.pdf/.png          RQ2: puzzle difficulty trade-off
  (file numbers follow the figure numbers of the paper)
  model_size.csv/.tex           model size and solution time
  key_numbers.txt                      numbers quoted in the text
"""

import glob
import math
import os
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

HERE = os.path.dirname(os.path.abspath(__file__))           # .../Research_model/experiments
ROOT = os.path.dirname(HERE)                                 # .../Research_model
OUT = os.path.join(HERE, "figures")
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- style
# categorical slots in fixed order (validated palette, light mode); every series
# also gets its own marker and line style, so figures survive grey-scale printing
COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
MARKERS = ["o", "s", "^", "D", "v"]
DASHES = ["-", "--", "-.", ":", (0, (5, 1, 1, 1))]
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e2e1dc"
SEQ = LinearSegmentedColormap.from_list("seq_blue", ["#f3f7fd", "#2a78d6", "#0b2a50"])

plt.rcParams.update({
    "font.family": "serif", "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8,
    "legend.fontsize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7,
    "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2,
    "text.color": INK, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.5, "axes.axisbelow": True,
    "legend.frameon": False, "savefig.bbox": "tight", "savefig.dpi": 300,
    "pdf.fonttype": 42, "ps.fonttype": 42,     # TrueType, not Type 3, in the PDFs
})
FULL_W = 4.8          # LNCS text width in inches (12.2 cm)


def style_series(i, cat=False):
    if cat:     # categorical x axis: markers only, no connecting line
        return dict(color=COLORS[i], marker=MARKERS[i], linestyle="none", markersize=4.5)
    return dict(color=COLORS[i], marker=MARKERS[i], linestyle=DASHES[i],
                linewidth=1.4, markersize=3.5)


JITTER = [-0.18, -0.06, 0.06, 0.18]   # separate series that share a value on a categorical axis


def legend_below(fig, ax, ncol):
    h, l = ax.get_legend_handles_labels()
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.legend(h, l, loc="lower center", ncol=ncol, bbox_to_anchor=(0.5, 0.0))


def save(fig, name):
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(OUT, f"{name}.{ext}"))
    plt.close(fig)
    print("  wrote", name)


def ref_line(ax, x, text, vertical=True, left=False, top=False, below=False):
    if vertical:
        ax.axvline(x, color=INK2, linewidth=0.8, linestyle=(0, (2, 2)), zorder=1)
        ax.annotate(text, (x, 1 if top else 0), xycoords=("data", "axes fraction"), xytext=(2, -2 if top else 2),
                    textcoords="offset points", ha="left", va="top" if top else "bottom", fontsize=6.5, color=INK2)
    else:
        ax.axhline(x, color=INK2, linewidth=0.8, linestyle=(0, (2, 2)), zorder=1)
        ax.annotate(text, (0 if left else 1, x), xycoords=("axes fraction", "data"),
                    xytext=(2 if left else -2, -2 if below else 2), textcoords="offset points",
                    ha="left" if left else "right", va="top" if below else "bottom", fontsize=6.5, color=INK2)


# ---------------------------------------------------------------- reading PRISM exports
def read_prism_csv(path):
    """PRISM -exportresults ...:csv  ->  {property: [ {col: value, ..., 'Result': float} ]}"""
    out, prop, header = {}, None, None
    with open(path, encoding="utf-8", errors="replace") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                prop, header = None, None
                continue
            if line.startswith('"'):
                prop = line[1:-1].replace('""', '"')
                out[prop], header = [], None
                continue
            cells = line.split(",")
            if header is None:
                header = cells
                continue
            row = {}
            for h, c in zip(header, cells):
                try:
                    row[h] = float(c)
                except ValueError:
                    row[h] = float("nan")       # e.g. an error message instead of a number
            out[prop].append(row)
    return out


def load(name):
    path = os.path.join(HERE, f"{name}.csv")
    if not os.path.exists(path):
        print(f"  missing {name}.csv, skipped")
        return None
    return read_prism_csv(path)


def prop(data, key):
    """find a property by a distinctive substring"""
    for p, rows in data.items():
        if key in p:
            return rows
    raise KeyError(key)


def pick(rows, **cond):
    return [r for r in rows if all(abs(r.get(k, float("nan")) - v) < 1e-9 for k, v in cond.items())]


def value(rows, **cond):
    sel = pick(rows, **cond)
    return sel[0]["Result"] if sel else float("nan")


def t_prf_measured():
    path = os.path.join(ROOT, "measure", "costs_summary.txt")
    try:
        txt = open(path, encoding="utf-8").read()
        return float(re.search(r"const double t_PRF\s*=\s*([0-9.eE+-]+)", txt).group(1))
    except (OSError, AttributeError):
        return 1.807093e-06


KEY = []          # lines for key_numbers.txt

D_LIST = [16, 18, 20, 24, 255]
D_LABEL = ["16", "18", "20", "24", "none"]
DF_LIST = [0, 20, 24, 28]
DF_LABEL = ["forged ZBC = 0", "forged $d_f$ = 20", "forged $d_f$ = 24", "forged $d_f$ = 28"]


def e1_table():
    """{(D_max, d_f, T): (P_established, init_cpu, att_cpu)}"""
    tab = {}
    for D in D_LIST:
        for name, dfs in ((f"E1_Dmax{D}_df20-28", [20, 24, 28]), (f"E1_Dmax{D}_df0", [0])):
            data = load(name)
            if data is None:
                continue
            est, ic, ac = prop(data, '"established"'), prop(data, '"init_cpu"'), prop(data, '"att_cpu"')
            for df in dfs:
                for T in (10, 60):
                    cond = dict(T=T) if df == 0 else dict(d_f=df, T=T)
                    tab[(D, df, T)] = (value(est, **cond), value(ic, **cond), value(ac, **cond))
    return tab


# ---------------------------------------------------------------- Fig 3 (E1)
def fig3(tab):
    if not tab:
        return
    fig, axes = plt.subplots(1, 2, figsize=(FULL_W, 2.1), sharey=True)
    for ax, T in zip(axes, (10, 60)):
        for i, df in enumerate(DF_LIST):
            ys = [1 - tab.get((D, df, T), (float("nan"),))[0] for D in D_LIST]
            ax.plot([x + JITTER[i] for x in range(len(D_LIST))], ys, label=DF_LABEL[i], **style_series(i, cat=True))
        ax.set_xticks(range(len(D_LIST)), D_LABEL)
        ax.set_xlabel("initiator's max. difficulty $D_{max}$")
        ax.set_title(f"T = {T} s")
        ax.set_ylim(-0.03, 1.03)
        ref_line(ax, 1, "k = 18", top=True)
    axes[0].set_ylabel("P(no IKE SA within T)")
    fig.set_size_inches(FULL_W, 2.25)
    legend_below(fig, axes[0], 4)
    save(fig, "fig3_E1_forged_puzzles")
    KEY.append("E1  P(no IKE SA within 60 s), rows D_max, columns forged d_f (0 = ZBC 0):")
    KEY.append("      D_max " + "".join(f"{df:>9}" for df in DF_LIST))
    for D, lab in zip(D_LIST, D_LABEL):
        KEY.append(f"      {lab:>5} " + "".join(f"{1 - tab.get((D, df, 60), (float('nan'),))[0]:9.4f}" for df in DF_LIST))


# ---------------------------------------------------------------- Fig 4 (E2 and E3)
def fig4(tab):
    data = load("E2_ratio")
    if data is None or not tab:
        return
    est = prop(data, '"established"')
    fig, (a, b) = plt.subplots(1, 2, figsize=(FULL_W, 2.6), gridspec_kw=dict(width_ratios=[1, 1.05]))
    series = [(24, 60, "$d_f$ = 24, solved, T = 60 s"), (28, 10, "$d_f$ = 28, refused, T = 10 s"),
              (28, 60, "$d_f$ = 28, refused, T = 60 s")]
    for i, (df, T, lab) in enumerate(series):
        rows = sorted(pick(est, d_f=df, T=T), key=lambda r: r["ratio_F"])
        a.plot([r["ratio_F"] for r in rows], [1 - r["Result"] for r in rows], label=lab, **style_series(i))
    a.set_xlabel("attacker speed $\\lambda_F \\cdot RTT$")
    a.set_ylabel("P(no IKE SA within T)")
    a.set_title("(a) E2, $D_{max}$ = 24")
    a.set_ylim(-0.03, 1.03)
    a.axvline(2, color=INK2, linewidth=0.8, linestyle=(0, (2, 2)), zorder=1)
    a.annotate("default", (2, 0.45), xytext=(2, 0), textcoords="offset points", fontsize=6.5, color=INK2, ha="left")
    a.legend(loc="upper center", bbox_to_anchor=(0.5, -0.27), ncol=1)
    d_list, d_label = D_LIST[1:], D_LABEL[1:]          # D_max = 16 < k: no legitimate SA at all
    for i, df in enumerate(DF_LIST):
        ys = []
        for D in d_list:
            p, ic, ac = tab.get((D, df, 60), (float("nan"),) * 3)
            ys.append(ic / ac if ac and ac > 0 else float("nan"))
        b.plot([x + JITTER[i] for x in range(len(d_list))], ys, label=DF_LABEL[i], **style_series(i, cat=True))
    b.set_yscale("log")
    b.set_xticks(range(len(d_list)), d_label)
    b.set_xlabel("initiator's max. difficulty $D_{max}$")
    b.set_ylabel("initiator / attacker CPU")
    b.set_title("(b) E3, over 60 s")
    b.legend(loc="upper center", bbox_to_anchor=(0.5, -0.27), ncol=2)
    fig.tight_layout(w_pad=2.0)
    save(fig, "fig4_E2_E3")
    rows = sorted(pick(est, d_f=24, T=60), key=lambda r: r["ratio_F"])
    KEY.append("E2  P(no IKE SA within 60 s), d_f = 24, D_max = 24, by ratio_F: "
               + ", ".join(f"{r['ratio_F']:g}: {1 - r['Result']:.3f}" for r in rows))


# ---------------------------------------------------------------- Fig 6 (E4)
DEF_LABEL = ["no defence", "cookie only", "cookie + puzzle"]


def fig6():
    t2, t3, base = load("E4_T2"), load("E4_T3"), load("E4_baseline")
    if t2 is None or t3 is None:
        return
    b = prop(base, "legit_success")[0]["Result"] if base else float("nan")
    fig, axes = plt.subplots(2, 2, figsize=(FULL_W, 3.6), sharex="col")
    for col, (data, title, extra) in enumerate(((t2, "T2: IKE_SA_INIT flooding ($\\rho$ = 0.5)", dict(rho=0.5)),
                                                (t3, "T3: junk IKE_AUTH", {}))):
        for row, (key, ylab) in enumerate((("legit_success", "legitimate\nsuccess rate"),
                                           ('"resp_full"', "share of time\ntable full"))):
            ax = axes[row][col]
            rows_all = prop(data, key)
            for d in range(3):
                rows = sorted(pick(rows_all, defense=d, **extra), key=lambda r: r["lam_att"])
                ax.plot([r["lam_att"] for r in rows], [r["Result"] for r in rows], label=DEF_LABEL[d], **style_series(d))
            ax.set_ylim(-0.03, 1.03)
            if row == 0:
                ax.set_title(title)
                if not math.isnan(b):
                    ref_line(ax, b, f"no attack ({b:.3f})" if col == 0 else "", vertical=False, below=True)
            else:
                ax.set_xlabel("attack rate (requests / s)")
            if col == 1:
                ax.annotate("no defence and cookie only coincide", (0.98, 0.36), xycoords="axes fraction",
                            ha="right", va="center", fontsize=6.5, color=INK2)
            if col == 0:
                ax.set_ylabel(ylab)
    fig.set_size_inches(FULL_W, 3.1)
    legend_below(fig, axes[0][0], 3)
    save(fig, "fig5_E4_defences")
    KEY.append(f"E4  no-attack legitimate success rate: {b:.4f}")
    for data, nm, extra in ((t2, "T2", dict(rho=0.5)), (t3, "T3", {})):
        rows_all = prop(data, "legit_success")
        for d in range(3):
            rows = sorted(pick(rows_all, defense=d, **extra), key=lambda r: r["lam_att"])
            KEY.append(f"E4  {nm} {DEF_LABEL[d]:<16} success at max rate {rows[-1]['lam_att']:g}/s: {rows[-1]['Result']:.3f}")


# ---------------------------------------------------------------- Fig 7 (E5)
def fig7():
    sets = [(k, load(f"E5_k{k}")) for k in (18, 20)]
    sets = [(k, d) for k, d in sets if d is not None]
    if not sets:
        return
    fig, axes = plt.subplots(1, len(sets), figsize=(FULL_W, 2.3), sharey=True, squeeze=False)
    axes = axes[0]
    im = None
    for ax, (k, data) in zip(axes, sets):
        rows = prop(data, '"resp_full"')
        Hs = sorted({int(r["H"]) for r in rows})
        taus = sorted({r["tau_R"] for r in rows})
        grid = [[value(rows, H=H, tau_R=t) for t in taus] for H in Hs]
        im = ax.imshow(grid, origin="lower", cmap=SEQ, vmin=0, vmax=1, aspect="auto")
        for yi, H in enumerate(Hs):
            for xi, t in enumerate(taus):
                v = grid[yi][xi]
                ax.text(xi, yi, f"{v:.2f}".replace("0.", "."), ha="center", va="center", fontsize=6,
                        color="white" if v > 0.4 else INK)
        ax.set_xticks(range(len(taus)), [f"{t:g}" for t in taus])
        ax.set_yticks(range(len(Hs)), [str(h) for h in Hs])
        ax.set_xlabel("half-open SA lifetime $\\tau_R$ (s)")
        ax.set_title(f"puzzle difficulty k = {k}")
        ax.grid(False)
        xi = taus.index(2.0) if 2.0 in taus else None
        if xi is not None:
            ax.add_patch(plt.Rectangle((xi - 0.5, -0.5), 1, len(Hs), fill=False, edgecolor=INK, linewidth=1.0))
    axes[0].set_ylabel("table capacity H")
    cb = fig.colorbar(im, ax=list(axes), fraction=0.04, pad=0.02)
    cb.set_label("share of time table full")
    cb.outline.set_visible(False)
    save(fig, "fig6_E5_table_lifetime")


# ---------------------------------------------------------------- Fig 8 (E6)
def fig8():
    t2, t3, base = load("E6_T2"), load("E6_T3"), load("E4_baseline")
    if t2 is None or t3 is None:
        return
    b = prop(base, "legit_success")[0]["Result"] if base else float("nan")
    t_prf = t_prf_measured()
    fig, axes = plt.subplots(1, 3, figsize=(FULL_W, 2.2))
    for i, (data, lab) in enumerate(((t2, "T2 (100 req/s)"), (t3, "T3 (300 req/s)"))):
        succ = sorted(prop(data, "legit_success"), key=lambda r: r["k"])
        rc = {r["k"]: r["Result"] for r in prop(data, '"resp_cpu"')}
        ac = {r["k"]: r["Result"] for r in prop(data, '"att_cpu"')}
        ks = [r["k"] for r in succ]
        axes[0].plot(ks, [r["Result"] for r in succ], label=lab, **style_series(i))
        axes[1].plot(ks, [ac[k] / rc[k] if rc.get(k) else float("nan") for k in ks], label=lab, **style_series(i))
        good = [r["k"] for r in succ if r["Result"] >= 0.95 * b]
        KEY.append(f"E6  {lab}: smallest k with success >= 95% of no-attack level: "
                   f"{int(min(good)) if good else 'none'}; success by k: "
                   + ", ".join(f"{int(r['k'])}: {r['Result']:.3f}" for r in succ))
    ks = list(range(8, 25, 2))
    solve = [4 * 2 ** k * t_prf for k in ks]
    axes[2].plot(ks, solve, **style_series(2))
    KEY.append("E6  legitimate solve time 4*2^k*t_PRF (s): " + ", ".join(f"{k}: {s:.3g}" for k, s in zip(ks, solve)))
    axes[0].set_ylim(-0.03, 1.03)
    axes[0].set_ylabel("legitimate success rate")
    axes[0].set_title("(a) legitimate success")
    axes[1].set_yscale("log")
    axes[1].set_title("(b) attacker / responder\nCPU")
    axes[2].set_yscale("log")
    axes[2].set_title("(c) legitimate\nsolve time (s)")
    ref_line(axes[2], 1.0, "RFC §9: 1 s", vertical=False, left=True)
    for ax in axes:
        ax.set_xlabel("puzzle difficulty k")
        ax.set_xticks(range(8, 25, 4))
        ref_line(ax, 18, "18")
    if not math.isnan(b):
        ref_line(axes[0], b, "no attack", vertical=False, left=True, below=True)
    legend_below(fig, axes[0], 2)
    save(fig, "fig7_E6_difficulty")


# ---------------------------------------------------------------- Table 3
def model_size_table():
    rows = []
    for log in sorted(glob.glob(os.path.join(HERE, "log_*.txt"))):
        txt = open(log, encoding="gbk", errors="replace").read()
        states = [int(x) for x in re.findall(r"States:\s+(\d+)", txt)]
        trans = [int(x) for x in re.findall(r"Transitions:\s+(\d+)", txt)]
        build = [float(x) for x in re.findall(r"Time for model construction:\s+([0-9.]+)", txt)]
        check = [float(x) for x in re.findall(r"Time for model checking:\s+([0-9.]+)", txt)]
        errors = len(re.findall(r"^Error", txt, flags=re.M))
        if not states:
            continue
        name = os.path.basename(log)[4:-4]
        rows.append((name, len(states), max(states), max(trans), sum(build), sum(check),
                     sum(check) / max(len(check), 1), errors))
    if not rows:
        return
    with open(os.path.join(OUT, "model_size.csv"), "w") as f:
        f.write("run,models_built,max_states,max_transitions,build_s_total,check_s_total,check_s_mean,errors\n")
        for r in rows:
            f.write(",".join(str(round(x, 3)) if isinstance(x, float) else str(x) for x in r) + "\n")
    with open(os.path.join(OUT, "model_size.tex"), "w") as f:
        f.write("\\begin{tabular}{lrrrr}\n\\hline\nRun & Models & Max.\\ states & Max.\\ transitions & Mean check (s)\\\\\n\\hline\n")
        for r in rows:
            nm = r[0].replace('_', '\\_')
            f.write(f"{nm} & {r[1]} & {r[2]:,} & {r[3]:,} & {r[6]:.2f}\\\\\n")
        f.write("\\hline\n\\end{tabular}\n")
    print("  wrote model_size")
    bad = [r[0] for r in rows if r[7]]
    KEY.append("Runs with PRISM errors: " + (", ".join(bad) if bad else "none"))


def main():
    print("Reading results from", HERE)
    tab = e1_table()
    fig3(tab)
    fig4(tab)
    fig6()
    fig7()
    fig8()
    model_size_table()
    with open(os.path.join(OUT, "key_numbers.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(KEY) + "\n")
    print("\n".join(KEY))
    print("\nFigures and tables are in", OUT)


if __name__ == "__main__":
    sys.exit(main())
