# Artifact: Quantifying the DoS Resistance of IKEv2 Client Puzzles with Probabilistic Model Checking

This repository contains the PRISM models, property files, experiment scripts, raw results,
cost measurements and plotting code behind the paper. It is anonymised for double-blind review.

## Contents

| Path | What it is | Paper |
|---|---|---|
| `ikev2_rq1.sm` | Model M1: one legitimate session, message by message, with the on-path attacker of T1 | Sect. 4.1, RQ1 |
| `ikev2_rq2.sm` | Model M2: responder with aggregated legitimate and attack traffic (T2, T3) | Sect. 4.2, RQ2 |
| `ikev2_rq1_wait.sm` | M1 with the wait-window mitigation (experiment E7) | Sect. 6 |
| `experiments/E7_v1_leastwork/` | First version of the wait-window rule (solve only the cheaper puzzle), its results, and a note on the extra data point cited in Sect. 6 | Sect. 6 |
| `experiments/*.props` | Property files used by the scripts | Sects. 4–6 |
| `run_experiments.bat` | Runs E1–E6 (about 2 hours) and then draws the figures | Sect. 5 |
| `run_E7.bat` | Runs E7, the wait window (about 15 minutes) | Sect. 6 |
| `run_E0.bat` | No-attack baseline of M1 and deadlock checks (a few seconds) | Sect. 4.4 |
| `run_plots.bat`, `experiments/plot_figures.py` | Draws the figures from the CSV results | Sect. 5 |
| `experiments/E*.csv`, `experiments/log_*.txt` | Raw PRISM results and logs | Sects. 4–6 |
| `experiments/figures/` | Figures as used in the paper (PDF and PNG), `key_numbers.txt`, model sizes | Sect. 5 |
| `measure/` | Cost measurement script and results (Table 2), puzzle-solving measurements (Erlang-4 check) | Sects. 4.3, 4.4 |
| `validation/` | M2 steady-state results with Jacobi and with Gauss–Seidel iteration | Sect. 4.4 |

## Experiments

| Id | Model | Question | Constants (see the `.bat` files for exact ranges) |
|---|---|---|---|
| E0 | M1 | No-attack baseline; all deadlocks are final states | `attack=0`, `defense=0..2` |
| E1 | M1 | Forged puzzles vs the initiator's maximum difficulty | `D_max` in {16,18,20,24,none}, `d_f` in {0,20,24,28} |
| E2 | M1 | Attacker speed | `ratio_F` 0.5..5 |
| E3 | M1 | Initiator/attacker CPU (rewards of E1) | — |
| E4 | M2 | No defence / cookies / puzzles under T2 and T3 | `lam_att`, `rho`, `defense` |
| E5 | M2 | Table size and half-open lifetime | `H` 20..100, `tau_R` 2..10, `k` in {18,20} |
| E6 | M2 | Puzzle difficulty | `k` 8..24 |
| E7 | M1 wait | Wait window before solving | `w_I` 0..0.5, `d_f` in {0,16,18,24} |

Note: `experiments/E1_Dmax255_df0.csv` comes from a rerun after a 40-bit cap on the work for a
zero difficulty was added to M1 (the first run underflowed).

## Requirements

- PRISM 4.10.1 (https://www.prismmodelchecker.org/) with Java 11 or later.
- Python 3 with `matplotlib` for the figures; `cryptography` for the cost measurements.

## Running

The `.bat` files are for Windows and expect PRISM in `E:\PRISM\prism-4.10.1`; change `PRISM_DIR` at
the top of each file. On other systems, call PRISM with the model, property file and constants
shown in the `.bat` files, for example

```
prism ikev2_rq1.sm experiments/ikev2_rq1_exp.props \
      -const attack=1,defense=2,d_f=20:4:28,D_max=24,ratio_F=2,T=10:50:60 \
      -exportresults experiments/E1_Dmax24_df20-28.csv:csv
prism ikev2_rq2.sm experiments/ikev2_rq2_exp.props -gs -maxiters 100000 \
      -const attack=2,defense=0:2,lam_att=10:10:200,rho=0.25:0.25:0.75,N_bots=100,H=50,tau_R=2,theta=0,k=18 \
      -exportresults experiments/E4_T2.csv:csv
```

Then run `python experiments/plot_figures.py` from the repository root.

The CSV files contain PRISM's raw results; the paper reports `1 - P(established)` as the probability
of having no IKE SA, and E3 as the ratio of the `init_cpu` and `att_cpu` rewards at T = 60 s.

## Cost measurements

`measure/measure_costs.py` measures the cryptographic costs (HMAC-SHA-256, cookie, X25519, ECDSA
P-256, MODP-2048, RSA-2048, key derivation) and solves puzzles with k = 8..20 to check the
Erlang-4 assumption. `measure/costs_summary.txt` lists the constants used in the models. The PRF
cost is that of a single C-level HMAC call; the same summary also reports the slower cost of a
trial inside a Python solver loop, which the paper discusses.
