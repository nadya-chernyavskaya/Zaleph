"""
This script generates an efficiency vs purity plot
"""

from info import *
from ROOT import TFile, TCanvas, TH1D, TGraph
import numpy as np

# Filename of what you try to separate from the rest
separate = "zdec_hadr"

# The same code appears in event_variables.py
# TODO: find a way to not have this code duplicated
mc_files = [TFile(data_dir + x + ".root") for x in mc_filenames]
mc_trees = [f.Get('h100') for f in mc_files]
mc_n = len(mc_trees)

# idx correspond to indices in mc_filenames/mc_trees
idx_bg = range(mc_n)
idx_sig = idx_bg.pop(mc_filenames.index(separate))
s = "Nch>=0&&Ech>0"
t = "&&Nch>=8"
N_bg = [mc_trees[i].GetEntries(s) for i in idx_bg]
N_sig = mc_trees[idx_sig].GetEntries(s)

eff = mc_trees[idx_sig].GetEntries(s+t) / float(N_sig)
eff_bg = [mc_trees[j].GetEntries(s+t) for j in idx_bg]
eff_bg = np.array(eff_bg) / np.array(N_bg, dtype=np.float)
# calculate number of sinal and background events above cut
# normalized to luminosity 1
S = eff * sigma[separate]
B = sum(eff_bg * np.array([sigma[x] for x in mc_filenames])[idx_bg])
if S + B != 0:
    pur = S/(S+B)
else:
    pur = 0

best_idx = np.argmax(pur * eff)
print("Investigating cuts separate {}".format(separate[5:]))
print("Efficiency: {}".format(eff))
print("Purity: {}".format(pur))
