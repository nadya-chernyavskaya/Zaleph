from ROOT import TFile, TTree
import ROOT

data_dir = "../data/"
output_dir = "../output/"

monte_carlo_filenames = ["zdec_bhab", "zdec_hadr", "zdec_muon", "zdec_taus"]

monte_carlo_files = [TFile(data_dir + x + ".root") for x in monte_carlo_filenames]
output_files = [TFile(output_dir + x + "-output.root", "recreate") for x in monte_carlo_filenames]


t = monte_carlo_files[2].Get('h100')
print(t)

t.Print()
hist1 = ROOT.TH1F("hist1","",100,0.,1.)
t.Draw("Cthr>>hist1")
output_files[2].cd()
hist1.Write("Cthr")
