"""
This script generates an efficiency vs purity plot
"""

from info import *
from ROOT import TFile, TCanvas, TH1D, TGraph
from numpy import array, linspace, zeros, argmax
from utils import get_effpur

# Branch name of the variable you want to cut
# The range for the efficiency vs purity plot is automatically
# gathered from config.py
variable = "Nefl"

# Filename of what you try to separate from the rest
separate = "taus"

variable_caption, n_bins, x_min, x_max, logscale = event_variables[variable]

previous_cut = "Nefl>13" # our cut for hadrons
previous_cut = "Nefl<=4&&Nplanes>2&&Egood>61.5" # our cut for muons
previous_cut = "Nefl<=14&&Egood<=63.5&&Eec<=70.2" # our cut for taus
previous_cut = "Nefl<=6&&Nplanes<=0&&Egood>49.2" # our cut for electrons
previous_cut = "Nefl<=6&&Nplanes<=0&&Eec>39" # our cut for electrons
previous_cut = "Nefl<=13&&Nhits>3&&Ech<=62&&Ehc>1.6"

if variable == "pcha":
    t = "TMath::Sqrt({0}[][0]**2 + {0}[][1]**2)<={1}"+previous_cut
else:
    t = previous_cut+"&&{0}<={1}"

# Create an array with all the cuts to try out and loop over it
cut_range = linspace(x_min, x_max, n_bins+1, dtype=float)
eff, pur = get_effpur(separate, [t.format(variable, c) for c in cut_range])

best_idx = argmax(pur * eff)

print("Investigating cuts on {0} to separate {1}".format(variable, separate))
print("Best cut: {}".format(cut_range[best_idx]))
print("Efficiency: {}".format(eff[best_idx]))
print("Purity: {}".format(pur[best_idx]))

#eff = array(eff, dtype=float)
#pur = array(pur, dtype=float)

# Purity vs efficiency plot
c1 = TCanvas("c1","A Simple Graph Example",200,10,700,500);
c1.cd()
gr1 = TGraph(len(cut_range),eff,pur);

gr1.SetTitle("p vs. e for {0} cut to separate {1}".format(variable, separate))
gr1.GetYaxis().SetTitle("purity")
gr1.GetXaxis().SetTitle("efficiency")

gr1.SetMarkerStyle(2)
gr1.Draw("AP")
c1.Draw()
c1.Print(output_dir+variable.lower()+"_"+separate+"_pur_vs_eff_"+".pdf")

# Purity * efficiency plot
c2 = TCanvas("c1","A Simple Graph Example",200,10,700,500);
c2.cd()
gr2 = TGraph(len(cut_range),cut_range,pur * eff);

gr2.SetTitle("p * e for {0} cut to separate {1}".format(variable, separate))
gr2.GetYaxis().SetTitle("purity * efficiency")
gr2.GetXaxis().SetTitle("cut")

gr2.SetMarkerStyle(2)
gr2.Draw("AP")
c2.Draw()
c2.Print(output_dir+variable.lower()+"_"+separate+"_pur_times_eff"+".pdf")
