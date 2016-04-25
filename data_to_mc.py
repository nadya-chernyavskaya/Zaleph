"""
A script to generate histograms for all possible event variables
to compare MC data for ALEPH.
"""

from info import *
from ROOT import TFile, TTree, TH1D, TCanvas, TLegend

# Read in monte carlo
mc_files = [TFile(data_dir + x + ".root") for x in mc_filenames]
mc_trees = [f.Get('h100') for f in mc_files]
mc_n = len(mc_trees)

# Read in data
data_files = [TFile(data_dir + x + ".root") for x in data_filenames]
data_trees = [f.Get('h100') for f in data_files]
data_n = len(data_trees)

cut = "Nefl<=14&&Nhits>3&&Ech<=62"
cut = ""

for variable_name, variable_info in event_variables.iteritems():
    variable_caption, n_bins, x_min, x_max, logscale = variable_info
    c = TCanvas("c", variable_name, 600, 400)
    c.cd()

    if logscale:
        c.SetLogy()

    mc_hists = []
    data_hists = []

    leg = TLegend(0.91,0.11,1.0,0.89);

    for i in range(mc_n):
        mc_hists.append(TH1D("hmc{}".format(i),variable_caption,n_bins,x_min,x_max))
        if variable_name == "pcha":
            mc_trees[i].Draw("TMath::Sqrt({0}[][0]**2 + {0}[][1]**2)>>h{1}".format(variable_name, i), cut)
        else:
            mc_trees[i].Draw("{0}>>hmc{1}".format(variable_name, i), cut)
        # Number of events assuming the experimental luminosity
        N = luminosity["91.29"] * xsec[mc_filenames[i]]
        # N = 1
        mc_hists[-1].Scale(1/float(mc_trees[i].GetEntries()) * N);
        mc_hists[-1].SetLineColor(i+1)

    mc_hist = TH1D("hmc",variable_caption,n_bins,x_min,x_max)

    for h in mc_hists:
        mc_hist = mc_hist + h

    for i in range(data_n):
        data_hists.append(TH1D("hd{}".format(i),variable_caption,n_bins,x_min,x_max))
        data_trees[i].Draw("{0}>>hd{1}".format(variable_name, i), "Cthr>0")

    mc_hist.Draw("")
    leg.AddEntry(mc_hist,"mc","l")
    c.Update()

    for i in range(data_n):
        data_hists[i].Draw("same")
        data_hists[i].SetLineColor(i+2)
        leg.AddEntry(data_hists[i],"data{}".format(i),"l")
        c.Update()

    leg.Draw()
    c.Update()

    c.Print(output_dir+variable_name.lower()+".pdf")
