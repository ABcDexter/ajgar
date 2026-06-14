# source = https://root.cern/doc/master/group__Python.html

# The entry point to ROOT in Python is one import:

import ROOT
# Every ROOT class and function is available under the ROOT module.

# Now let's create a histogram, fill it from a NumPy array and write it to a file:

import numpy as np
 
# Create a 1D histogram
h = ROOT.TH1D("h", "Gaussian distribution;x;counts", 100, -5, 5)
 
# Fill it from a NumPy array
data = np.random.normal(0, 1, 10000)
h.Fill(data)
 
# Write it to a ROOT file
with ROOT.TFile.Open("output.root", "RECREATE") as f:
    f.WriteObject(h, "my_histogram")

#Now we create an RDataFrame - ROOT's high-level interface for columnar data analysis - from scratch, define a new column and draw a histogram:

import numpy as np
 
# Create an RDataFrame with 10000 rows
rdf = ROOT.RDataFrame(10000)
 
# Define a column x representing a normal distribution
rdf = rdf.Define("x", "gRandom->Gaus(0, 1)")
 
# Draw a histogram of x
rdf.Histo1D("x").Draw()