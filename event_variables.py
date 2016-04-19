"""
A script to generate histograms for all possible event variables
to compare MC data for ALEPH.
"""

from info import *
from ROOT import TFile, TTree, TH1D, TCanvas, TLegend

mc_files = [TFile(data_dir + x + ".root") for x in mc_filenames]
mc_trees = [f.Get('h100') for f in mc_files]
mc_n = len(mc_trees)

cut = "Nefl<=14&&Egood<=63.5&&Eec<=70.2"
#cut = ""

for variable_name, variable_info in event_variables.iteritems():
    variable_caption, n_bins, x_min, x_max, logscale = variable_info
    c = TCanvas("c", variable_name, 600, 400)
    c.cd()

    if logscale:
        c.SetLogy()

    hists = []
    leg = TLegend(0.91,0.11,1.0,0.89);

    for i in range(mc_n):
        hists.append(TH1D("h{}".format(i),variable_caption,n_bins,x_min,x_max))
        if variable_name == "pcha":
            mc_trees[i].Draw("TMath::Sqrt({0}[][0]**2 + {0}[][1]**2)>>h{1}".format(variable_name, i), cut)
        else:
            mc_trees[i].Draw("{0}>>h{1}".format(variable_name, i), cut)
        # Number of events assuming the experimental luminosity
        N = luminosity["91.29"] * sigma[mc_filenames[i]]
        # N = 1
        hists[-1].Scale(1/float(mc_trees[i].GetEntries()) * N);
        hists[-1].SetLineColor(i+1)

    # Find out which histogram has the highest bins, to use this as the
    # reference for the y-axis. In other words: to plot it before the others.
    maxima = [h.GetMaximum() for h in hists]
    max_i = maxima.index(max(maxima))

    hists[max_i].GetYaxis().SetTitle(variable_caption)
    hists[max_i].GetYaxis().SetTitleOffset(1.4)
    hists[max_i].GetXaxis().SetTitle(variable_name)

    # The indices rearranged from 0 to mc_n with max_i as the first entry
    r = range(mc_n)
    r.insert(0, r.pop(max_i))
    for i, j in enumerate(r):
        if i == 0:
            hists[j].Draw("")
        else:
            hists[j].Draw("same")
        leg.AddEntry(hists[j],mc_filenames[j][5:],"l")
        c.Update()

    leg.Draw()

    c.Print(output_dir+variable_name.lower()+".pdf")
