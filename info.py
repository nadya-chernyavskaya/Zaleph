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

data_energies = [89.5, 91.25, 93.00]

data_filenames = [
        "zdec_da8950",
        "zdec_da9125_small",
        "zdec_da9300",
        ]

# A dict of event variables with branch name, description,
# histogram bin number, histogram limits, and log-scale flag.
# Comment out the variables which you don't want to process.
# See http://ihp-lx.ethz.ch/Stamet/varhelp-all.php for more info.
event_variables = {
        #("Run",     "Run number",                                100,1800, 1850., False)],
        #("Evt",     "Event number",                              100, 0  ,100000, False)],
        #("Clas",    "preclassification of event",                100, 0  , 2.2e6, False)],
        "Ngood":   ("Number of good charged tracks",              50,  0.,   50., True ),
        #("Elep",    "centre-of-mass energy (GeV)",               100, 91.,  92.3, True ),
        "Cthr":    ("Cosine of the thrust axis polar angle",     100, -1.,    1., False),
        "Thruv":   ("Thrustvalue",                               100,  0.,    1., True ),
        "Egood":   ("sum of energy (GeV) of good charged tracks",100,  0.,  205., True ),
        "Nch":     ("Number of all charged tracks",              102,  0.,  102., True ),
        "Ech":     ("Energy sum (GeV) of all charged tracks",    100,  0.,  200., True ),
        "pcha":    ("Track momentum (px,py,pz) (GeV/c)",         100,  0.,  200., True ),
        #("Qcha"
        #("D0"
        #("Z0"
        #("Nhits",
        "Nplanes": ("Number of hits in the last planes of HCAL", 12,    0.,  12., False),
        "Nefl":    ("Number of energy flow objects",             85,    0.,  85., True ),
        #("pefl"
        #("Typeefl"
        "Nec":     (" Number of all objects in ECAL",           20,   0,   20., True ),
        "Eec":     ("Energy sum (GeV) of all objects in ECAL",  100,   0.,  130., True ),
        "Eecal":   ("Energy of the ECAL objects (GeV)",         100,   0.,  130., True ),
        #("Tecal", "Theta of the ECAL object (radians)"
        #("Pecal"
        "Nhc":     ("Number of all objects in HCAL",             20,   0.,   20., True ),
        "Ehc":     ("Energy sum (GeV) of all objects in HCAL",  100,   0.,  130., True ),
        "Ehcal":   ("Energy of the HCAL objects (GeV)",         100,   0.,  130., True ),
        #("Thcal", "Theta of the HCAL object (radians)"
        #("Phcal"
        "Njet":    ("Number of jets found",                       6,   0.,    6., True ),
        #("pjet"
        }

# Integrated luminosity of data in nb^-1 for the different energies in GeV
luminosity = {"89.44": 8121.41, "91.29": 3553.53, "92.97": 9372.47}

# Theoretical crosssections for leptons in nb
sigma_leptons = {"ee": 1.219, "mm": 1.481, "tt": 1.478}

# Theoretical hadronic cross sections in nb for different energies
# no QED corrections for initial and final state radiation
sigma_hadr_noqed = {"89.44": 13.56, "91.29": 41.42, "92.97": 13.38}

# Theoretical hadronic cross sections in nb for different energies
# with initial and final state radiation
sigma_hadr_qed = {"89.44": 9.69, "91.29": 30.74, "92.97": 14.06}

# A more useful dictionary for the crosssections at MC-energy (91.2 GeV,
# which we assume to be the same as 91.29 GeV)
sigma = {"zdec_bhab": 1.219, "zdec_hadr": 30.74, "zdec_muon": 1.481, "zdec_taus": 1.478}

# Gamma-gamma background within acceptance
gg_bg = 0.078
# Using this, we don't need go consider the gg monte-carlo files

# Set some general ROOT settings
from ROOT import gROOT, gStyle, kFALSE

gROOT.SetBatch()
gStyle.SetOptStat(kFALSE)
gStyle.SetLegendBorderSize(0)
