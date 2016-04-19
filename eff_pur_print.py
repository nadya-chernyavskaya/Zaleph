from info import *
from ROOT import TFile, TCanvas, TH1D, TGraph
from numpy import array, linspace, zeros, argmax

# Filename of what you try to separate from the rest
separate = "zdec_taus"

# The same code appears in event_variables.py
# TODO: find a way to not have this code duplicated
mc_files = [TFile(data_dir + x + ".root") for x in mc_filenames]
mc_trees = [f.Get('h100') for f in mc_files]
mc_n = len(mc_trees)

# idx correspond to indices in mc_filenames/mc_trees
idx_bg = range(mc_n)
idx_sig = idx_bg.pop(mc_filenames.index(separate))

#cut = "Nefl>13" # our cut for hadrons
#cut = "Nefl<=4&&Nplanes>2&&Egood>61.5" # our cut for muons
cut = "Nefl<=14&&Egood<=63.5&&Eec<=70.2" # our cut for taus
#cut = "Nefl<=6&&Nplanes<=0&&Eec>39" # our cut for electrons

# Number of signal and background events before the cut
N_sig = mc_trees[idx_sig].GetEntries()
N_bg = [mc_trees[i].GetEntries() for i in idx_bg]

# Number of events after the cut
n_sig = mc_trees[idx_sig].GetEntries(cut)
n_bg = [mc_trees[j].GetEntries(cut) for j in idx_bg]

# Calculate efficiency
eff = n_sig / float(N_sig)

# Number of events devided by number of mc events and multiplied with theoretical crosssection
S = eff * sigma[separate]
B = sum(n_bg * array([sigma[x] for x in mc_filenames])[idx_bg] / array(N_bg, dtype=float))

# Calculate Purity
if S + B != 0:
    pur = S/(S+B)
else:
    pur = 0

print("Efficiency: {}".format(eff))
print("Purity: {}".format(pur))
