from ROOT import TFile
from info import *

files = [TFile(data_dir + x + ".root") for x in data_filenames]
trees = [f.Get('h100') for f in files]
n_trees = len(trees)

cuts = {"hadr": "Nefl>13",
        "muon": "Nefl<=4&&Nplanes>2&&Egood>61.5",
        "taus": "Nefl<=14&&Egood<=63.5&&Eec<=70.2",
        "bhab": "Nefl<=6&&Nplanes<=0&&Eec>39"}

eff = {"hadr": 0.998653509918,
       "muon": 0.918196509049,
       "taus": 0.931470083745,
       "bhab": 0.840443523772}

pur = {"hadr": 0.99885095464,
       "muon": 0.9905708718,
       "taus": 0.842816803352,
       "bhab": 0.951152731451}

for i in range(n_trees):
    print "Energy: {}".format(data_energies[i])
    N = trees[i].GetEntries("Nhits>0&&Cthr>-1&&Cthr<1&&Thruv>0.1")
    print "Total number of events: {}".format(N)
    for branch in cuts:
        print "{}:".format(branch)
        n = trees[i].GetEntries(cuts[branch]+"&&Nhits>0&&Cthr>-1&&Cthr<1&&Thruv>0.1")
        print "Number of Events left: {}".format(n)
        print "Branching ratio: {}".format(n/float(N) * pur[branch])
    print ""
