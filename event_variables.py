"""
A script to generate histograms for all possible event variables
to compare MC data for ALEPH.
"""

# set the location of the data files and an output directory for the histograms
data_dir = "../data/"
output_dir = "../output/"

# comment out the data sets you don't want to look at
mc_filenames = [
        "zdec_bhab",
        "zdec_hadr",
        "zdec_muon",
        "zdec_taus",
        #"zdec_gge",
        #"zdec_ggm",
        #"zdec_ggt",
        #"zdec_ggv",
        #"zdec_ggh",
        ]

# A list of event variables with branch name, description,
# histogram bin number, histogram limits, and log-scale flag.
# Comment out the variables which you don't want to process.
# See http://ihp-lx.ethz.ch/Stamet/varhelp-all.php for more info.
event_variables = [
        #("Run",     "Run number",                                100,1800, 1850., False)],
        #("Evt",     "Event number",                              100, 0  ,100000, False)],
        #("Clas",    "preclassification of event",                100, 0  , 2.2e6, False)],
        ("Ngood",   "Number of good charged tracks",              50,  0.,   50., True ),
        #("Elep",    "centre-of-mass energy (GeV)",               100, 91.,  92.3, True ),
        ("Cthr",    "Cosine of the thrust axis polar angle",     100, -1.,    1., False),
        ("Thruv",   "Thrustvalue",                               100,  0.,    1., True ),
        ("Egood",   "sum of energy (GeV) of good charged tracks",100,  0.,  205., True ),
        ("Nch",     "Number of all charged tracks",              102,  0.,  102., True ),
        ("Ech",     "Energy sum (GeV) of all charged tracks",    100,  0.,  200., True ),
        #("pcha"
        #("Qcha"
        #("D0"
        #("Z0"
        #("Nhits",
        ("Nplanes", "Number of hits in the last planes of HCAL", 12,    0.,  12., False),
        ("Nefl",    "Number of energy flow objects",             85,    0.,  85., True ),
        #("pefl"
        #("Typeefl"
        #("Nec"
        ("Eec",     "Energy sum (GeV) of all objects in ECAL",  100,   0.,  130., True ),
        #("Eecal"
        #("Tecal", "Theta of the ECAL object (radians)"
        #("Pecal"
        ("Nhc",     "Number of all objects in HCAL",             20,   0.,   20., True ),
        ("Ehc",     "Energy sum (GeV) of all objects in HCAL",  100,   0.,  130., True ),
        #("Ehcal"
        #("Thcal", "Theta of the HCAL object (radians)"
        #("Phcal"
        ("Njet",    "Number of jets found",                       6,   0.,    6., True ),
        #("pjet"
        ]

# Now the real script begins
from ROOT import TTree, TFile, TH1D, TCanvas, gStyle, kFALSE, TLegend, gROOT

gROOT.SetBatch()
gStyle.SetOptStat(kFALSE);
gStyle.SetLegendBorderSize(0);

mc_files = [TFile(data_dir + x + ".root") for x in mc_filenames]
mc_trees = [f.Get('h100') for f in mc_files]
mc_n = len(mc_trees)

for variable_name, variable_caption, n_bins, x_min, x_max, logscale in event_variables:
    c = TCanvas("c", variable_name, 600, 400)
    c.cd()

    if logscale:
        c.SetLogy()

    hists = []
    leg = TLegend(0.91,0.11,1.0,0.89);

    for i in range(mc_n):
        hists.append(TH1D("h{}".format(i),variable_caption,n_bins,x_min,x_max))
        mc_trees[i].Draw("{0}>>h{1}".format(variable_name, i))
        hists[-1].Scale(1/hists[-1].GetEntries());
        hists[-1].SetLineColor(i+1)

    # Find out which histogram has the highest bins, to use this as the
    # reference for the y-axis. In other words: to plot it before the others.
    maxima = [h.GetMaximum() for h in hists]
    max_i = maxima.index(max(maxima))

    hists[max_i].GetYaxis().SetTitle(variable_caption);
    hists[max_i].GetYaxis().SetTitleOffset(1.4);
    hists[max_i].GetXaxis().SetTitle(variable_name);

    # The indices rearranged from 0 to mc_n with max_i as the first entry
    r = range(mc_n)
    r.insert(0, r.pop(max_i))
    for i, j in enumerate(r):
        if i == 0:
            hists[j].Draw("")
        else:
            hists[j].Draw("same")
        leg.AddEntry(hists[j],mc_filenames[j][5:],"l");
        c.Update()

    leg.Draw();

    c.Print(output_dir+variable_name.lower()+".pdf")
