from ROOT import TFile
from info import *
from utils import get_effpur

# Read in data trees
files = [TFile(data_dir + x + ".root") for x in data_filenames]
trees = [f.Get('h100') for f in files]
n_trees = len(trees)

# The cuts we found for each decay channel
cuts = {"hadr": "Ech>20&&Nefl>13",
        "muon": "Ech>40&&Nefl<=4&&Nplanes>2&&Egood>61.5",
        #"taus": "Nefl<=14&&Egood<=63.5&&Eec<=70.2",
        "taus": "Ech>10&&Nefl<=13&&Nhits>3&&Ech<=62",
        "bhab": "Ech>40&&Nefl<=6&&Nplanes<=0&&Eec>39"}

# Calculate efficiency and purity for the cuts based on monte carlo
eff, pur = {}, {}
for branch in cuts:
    eff[branch], pur[branch] = get_effpur(branch, cuts[branch])

print eff
print pur

for i in range(n_trees):
    print "Energy: {}".format(data_energies[i])
    N = trees[i].GetEntries()
    print "Total number of events: {}".format(N)
    for branch in cuts:
        print "{}:".format(branch)
        n = trees[i].GetEntries(cuts[branch])
        print "Number of Events left: {}".format(n)
        print "Branching ratio: {}".format(n/float(N) * pur[branch] / eff[branch])
    print ""
