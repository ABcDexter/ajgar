import ROOT
import sys

FNAME = "output.root"

f = ROOT.TFile.Open(FNAME)
if not f or f.IsZombie():
	print(f"Failed to open {FNAME}")
	sys.exit(1)

# If user hasn't specified a histogram name, attempt to find one
requested = None
if len(sys.argv) > 1:
	requested = sys.argv[1]

def list_keys(tf):
	print("Contents of", tf.GetName())
	tf.ls()

if requested:
	obj = f.Get(requested)
	if not obj:
		print(f"Object '{requested}' not found in {FNAME}")
		list_keys(f)
		f.Close()
		sys.exit(1)
else:
	# try to find the first histogram-like object
	obj = None
	for k in f.GetListOfKeys():
		name = k.GetName()
		cls = k.GetClassName()
		if cls and cls.startswith("TH"):
			obj = f.Get(name)
			requested = name
			break
	if obj is None:
		print("No histogram (TH*) found in file. Showing file contents:")
		list_keys(f)
		f.Close()
		sys.exit(1)

print(f"Drawing object '{requested}' from {FNAME}")

c = ROOT.TCanvas("c", requested or "c", 800, 600)
try:
	obj.Draw()
except ReferenceError:
	print("Failed to draw object; it may be a null pointer or unsupported type.")
	f.Close()
	sys.exit(1)

out_name = f"{requested}.png" if requested else "output.png"
c.SaveAs(out_name)
print(f"Saved {out_name}")
f.Close()