"""
This script generates an efficiency vs purity plot
"""

from info import *
from ROOT import TFile, TCanvas, TH1D, TGraph
import numpy as np

# Branch name of the variable you want to cut
# The range for the efficiency vs purity plot is automatically
# gathered from config.py
variable = "Eec"

# Filename of what you try to separate from the rest
separate = "zdec_muon"

# The same code appears in event_variables.py
# TODO: find a way to not have this code duplicated
mc_files = [TFile(data_dir + x + ".root") for x in mc_filenames]
mc_trees = [f.Get('h100') for f in mc_files]
mc_n = len(mc_trees)

variable_caption, n_bins, x_min, x_max, logscale = event_variables[variable]

# idx correspond to indices in mc_filenames/mc_trees
idx_bg = range(mc_n)
idx_sig = idx_bg.pop(mc_filenames.index(separate))
s = "{}>=0".format(variable)
#s = "Nch>=6&&{}>=0".format(variable)
t = "&&{0}<{1}"
N_bg = [mc_trees[i].GetEntries(s) for i in idx_bg]
N_sig = mc_trees[idx_sig].GetEntries(s)

cut_range = np.linspace(x_min, x_max, n_bins + 1, dtype=np.float)
eff = np.zeros(n_bins + 1, dtype=np.float)
pur = np.zeros(n_bins + 1, dtype=np.float)
for i, cut in enumerate(cut_range):
    eff[i] = mc_trees[idx_sig].GetEntries(s+t.format(variable,cut)) / float(N_sig)
    eff_bg = [mc_trees[j].GetEntries(s+t.format(variable,cut)) for j in idx_bg]
    eff_bg = np.array(eff_bg) / np.array(N_bg, dtype=np.float)
    # calculate number of sinal and background events above cut
    # normalized to luminosity 1
    S = eff[i] * sigma[separate]
    B = sum(eff_bg * np.array([sigma[x] for x in mc_filenames])[idx_bg])
    if S + B != 0:
        pur[i] = S/(S+B)
    else:
        pur[i] = 0

best_idx = np.argmax(pur * eff) + 19
print("Investigating cuts on {0} to separate {1}".format(variable, separate[5:]))
print("Best cut: {}".format(cut_range[best_idx]))
print("Efficiency: {}".format(eff[best_idx]))
print("Purity: {}".format(pur[best_idx]))

# Purity vs efficiency plot
c1 = TCanvas("c1","A Simple Graph Example",200,10,700,500);
c1.cd()
gr1 = TGraph(len(cut_range),eff,pur);

gr1.SetTitle("p vs. e for {0} cut to separate {1}".format(variable, separate[5:]))
gr1.GetYaxis().SetTitle("purity")
gr1.GetXaxis().SetTitle("efficiency")

gr1.SetMarkerStyle(2)
gr1.Draw("AP")
c1.Draw()
c1.Print(output_dir+variable.lower()+"_"+separate[5:]+"_pur_vs_eff_"+".pdf")

# Purity * efficiency plot
c2 = TCanvas("c1","A Simple Graph Example",200,10,700,500);
c2.cd()
gr2 = TGraph(len(cut_range),cut_range,pur * eff);

gr2.SetTitle("p * e for {0} cut to separate {1}".format(variable, separate[5:]))
gr2.GetYaxis().SetTitle("purity * efficiency")
gr2.GetXaxis().SetTitle("cut")

gr2.SetMarkerStyle(2)
gr2.Draw("AP")
c2.Draw()
c2.Print(output_dir+variable.lower()+"_"+separate[5:]+"_pur_times_eff"+".pdf")
