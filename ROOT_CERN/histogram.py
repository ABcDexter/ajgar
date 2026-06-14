import ROOT
 
# https://root.cern/doc/master/df000__simple_8py.html

# Create a data frame with 100 rows
rdf = ROOT.RDataFrame(100)

# Define a new column `x` that contains random numbers
rdf_x = rdf.Define("x", "gRandom->Rndm()")

# Create a histogram from `x`
h = rdf_x.Histo1D("x")

# Create a canvas and draw the histogram
canvas = ROOT.TCanvas("c1", "Histogram", 800, 600)
h.Draw()
canvas.Update()

# If running interactively, start ROOT's event loop so the window stays open.
# If not, save the canvas to a PNG file as a fallback.
try:
	# gApplication is available when ROOT has GUI support
	if hasattr(ROOT, 'gApplication') and ROOT.gApplication:
		print("Displaying canvas. Close the window to exit, or press Ctrl+C to interrupt.")
		ROOT.gApplication.Run()
	else:
		raise AttributeError
except Exception:
	out_file = "histogram.png"
	print(f"Could not run interactive event loop; saving to {out_file}")
	canvas.SaveAs(out_file)