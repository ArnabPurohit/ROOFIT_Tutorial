import ROOT as r
r.RooRandom.randomGenerator().SetSeed(3001)
wspace = r.RooWorkspace()
wspace.factory("Gaussian::gauss(x[-10,10],mu[1,-10,10],sigma[1,0.1,10])")
wspace.factory("Exponential::shape(x,l[-0.1,-5,5])")
wspace.factory("SUM::model(bkgfrac[0.5,0.,1.]*shape,gauss)");
#wspace.defineSet("poi", "mu")
#wspace.defineSet("obs", "x")
data = wspace.pdf("model").generate(r.RooArgSet(wspace.var("x")), 10000)
getattr(wspace, 'import')(data, r.RooFit.Rename("data"))

x = wspace.var("x")
model = wspace.pdf("model")
gauss = wspace.pdf("gauss")
shape = wspace.pdf("shape")

k = r.RooKeysPdf("k", "k", x, data, r.RooKeysPdf.NoMirror, 0.2)
getattr(wspace, 'import')(k, r.RooFit.RenameAllNodes("workspace"))

wspace.Print()
wspace.writeToFile("addPdf_workspace.root")


xframe = x.frame(r.RooFit.Title("Generated data"))




xframe2 = x.frame(r.RooFit.Title("Gaussian+Exp fit to the data"))

data.plotOn(xframe)


model.fitTo(data)
ras_sig = r.RooArgSet(gauss)
ras_bkg = r.RooArgSet(shape)
data.plotOn(xframe2)
model.plotOn(xframe2)
model.plotOn(xframe2,r.RooFit.Components(ras_sig),r.RooFit.LineColor(r.kRed), r.RooFit.LineStyle(r.kDashed))
model.plotOn(xframe2,r.RooFit.Components(ras_bkg),r.RooFit.LineColor(r.kGreen), r.RooFit.LineStyle(r.kDashed))

c = r.TCanvas("rf101_basics","rf101_basics",800,400)
c.Divide(2)
c.cd(1)
r.gPad.SetLeftMargin(0.15) ; xframe.GetYaxis().SetTitleOffset(1.6) ; xframe.Draw()

c.cd(2) ; r.gPad.SetLeftMargin(0.15) ; xframe2.GetYaxis().SetTitleOffset(1.6) ; xframe2.Draw() ;
#c.Draw()
c.SaveAs("addPdf_withworkspace_plot.png")
