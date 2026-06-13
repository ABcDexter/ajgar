import ROOT
 
# https://root.cern/doc/master/df000__simple_8py.html
# Create a data frame with 100 rows
rdf = ROOT.RDataFrame(100)
 
# Define a new column `x` that contains random numbers
rdf_x = rdf.Define("x", "gRandom->Rndm()")
 
# Create a histogram from `x` and draw it
h = rdf_x.Histo1D("x")
h.Draw()