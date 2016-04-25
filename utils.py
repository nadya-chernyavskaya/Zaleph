"""
Useful functions which can be used in the analysis
"""

from info import *
from ROOT import TFile, TCanvas, TH1D, TGraph
from numpy import array, linspace, zeros, argmax

# Read in the monte carlo data
mc_files = [TFile(data_dir + x + ".root") for x in mc_filenames]
mc_trees = [f.Get('h100') for f in mc_files]
mc_n = len(mc_trees)

# This is internally used by get_effput for calculating efficiency and purity
# for one single cut.
def _get_single_effpur(sep, cut, idx_bg, idx_sig, N_sig, N_bg):

    # Number of events after the cut
    n_sig = mc_trees[idx_sig].GetEntries(cut)
    n_bg = [mc_trees[j].GetEntries(cut) for j in idx_bg]

    # Calculate efficiency
    eff = n_sig / float(N_sig)
    eff_bg = n_bg / array(N_bg, dtype=float)

    # Number of events devided by number of mc events and multiplied with the
    # theoretical crosssection
    S = eff * xsec["zdec_{}".format(sep)]
    B = sum(eff_bg * array([xsec[x] for x in mc_filenames])[idx_bg])

    # Calculate Purity
    if S + B != 0:
        pur = S/(S+B)
    else:
        pur = 0

    return eff, pur

# Returns efficiency and purity of a given cut to sep a given channel.
# The parameter cut is either a string, or a list of strings.
# In the latter case, eff and pur are also arrays.
def get_effpur(sep, cut):

    # idx correspond to indices in mc_filenames/mc_trees
    idx_bg = range(mc_n)
    idx_sig = idx_bg.pop(mc_filenames.index("zdec_{}".format(sep)))

    # Number of signal and background events before the cut
    N_sig = mc_trees[idx_sig].GetEntries()
    N_bg = [mc_trees[i].GetEntries() for i in idx_bg]

    args = [idx_bg, idx_sig, N_sig, N_bg]

    if isinstance(cut, basestring):
        return _get_single_effpur(sep, cut, *args)
    else:
        eff, pur = array([_get_single_effpur(sep, c, *args) for c in cut]).T
        return array(eff, dtype=float), array(pur, dtype=float)
