"""
This script generates an efficiency vs purity plot
"""

from info import *
from ROOT import TFile, TCanvas, TH1D, TGraph
from numpy import array, linspace, zeros, argmax

# Branch name of the variable you want to cut
# The range for the efficiency vs purity plot is automatically
# gathered from config.py
variable = "Eec"

# Filename of what you try to separate from the rest
separate = "zdec_bhab"

# The same code appears in event_variables.py
# TODO: find a way to not have this code duplicated
mc_files = [TFile(data_dir + x + ".root") for x in mc_filenames]
mc_trees = [f.Get('h100') for f in mc_files]
mc_n = len(mc_trees)

variable_caption, n_bins, x_min, x_max, logscale = event_variables[variable]

# idx correspond to indices in mc_filenames/mc_trees
idx_bg = range(mc_n)
idx_sig = idx_bg.pop(mc_filenames.index(separate))

previous_cut = "Nefl>13" # our cut for hadrons
previous_cut = "Nefl<=4&&Nplanes>2&&Egood>61.5" # our cut for muons
previous_cut = "Nefl<=14&&Egood<=63.5&&Eec<=70.2" # our cut for taus
previous_cut = "Nefl<=6&&Nplanes<=0&&Egood>49.2" # our cut for electrons
previous_cut = "Nefl<=6&&Nplanes<=0&&Eec>39" # our cut for electrons

if variable == "pcha":
    t = "TMath::Sqrt({0}[][0]**2 + {0}[][1]**2)<={1}"+previous_cut
else:
    t = previous_cut+"{0}>{1}"

# Number of signal and background events before the new cut
N_sig = mc_trees[idx_sig].GetEntries()
N_bg = [mc_trees[i].GetEntries() for i in idx_bg]

# Create arrays to store the efficiencies and purities in
eff = zeros(n_bins + 1, dtype=float)
pur = zeros(n_bins + 1, dtype=float)

# Create an array with all the cuts to try out and loop over it
cut_range = linspace(x_min, x_max, n_bins+1, dtype=float)
for i, cut in enumerate(cut_range):

    # Print progress
    if i % 10 == 0:
        print i/float(len(cut_range)) * 100

    # Number of events after the new cut
    n_sig = mc_trees[idx_sig].GetEntries(t.format(variable,cut))
    n_bg = [mc_trees[j].GetEntries(t.format(variable,cut)) for j in idx_bg]

    # Calculate efficiency
    eff[i] = n_sig / float(N_sig)

    # Number of events devided by number of mc events and multiplied with theoretical crosssection
    S = eff[i] * sigma[separate]
    B = sum(n_bg * array([sigma[x] for x in mc_filenames])[idx_bg] / array(N_bg, dtype=float))

    # Calculate Purity
    if S + B != 0:
        pur[i] = S/(S+B)
    else:
        pur[i] = 0


best_idx = argmax(pur * eff)

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
