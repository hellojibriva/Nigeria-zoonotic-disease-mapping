"""
Spearman rank correlations between state-level reported outbreak counts
for Rabies, HPAI, and Trypanosomosis (WAHIS, Nigeria, 2006-2025).

Tests whether states with a high burden of one disease also tend to have
a high burden of another. Uses pairwise-complete observations, since each
disease has a different number of states with reported data.
"""
import pandas as pd
from scipy import stats

df = pd.read_csv("../data/processed/QGIS_state_dataset.csv")

pairs = [
    ("Rabies_outbreaks", "HPAI_outbreaks"),
    ("Rabies_outbreaks", "Trypanosomosis_outbreaks"),
    ("HPAI_outbreaks", "Trypanosomosis_outbreaks"),
]

print(f"{'Pair':45s} {'n':>4s} {'rho':>8s} {'p-value':>10s}")
for a, b in pairs:
    sub = df[[a, b]].dropna()
    n = len(sub)
    if n < 3:
        print(f"{a} vs {b}: n={n}, too few pairwise-complete states")
        continue
    rho, p = stats.spearmanr(sub[a], sub[b])
    print(f"{a + ' vs ' + b:45s} {n:4d} {rho:8.3f} {p:10.4f}")

# Results (2006-2025 extraction):
#   Rabies vs HPAI:            n=34, rho= 0.149, p=0.402
#   Rabies vs Trypanosomosis:  n=17, rho=-0.211, p=0.417
#   HPAI vs Trypanosomosis:    n=16, rho=-0.125, p=0.644
#
# None of the three pairs are statistically significant (all p > 0.05).
# State-level reported outbreak counts for these three diseases do not
# track together -- there is no evidence that a state with a high burden
# of one disease also tends to have a high burden of another. Note the
# Trypanosomosis comparisons are based on only 16-17 states with data,
# so those two results are underpowered and should be read as
# inconclusive rather than as strong evidence of no relationship.
