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
mu = wspace.var("mu")
sigma = wspace.var("sigma")
bkgfrac = wspace.var("bkgfrac")

k = r.RooKeysPdf("k", "k", x, data, r.RooKeysPdf.NoMirror, 0.2)
getattr(wspace, 'import')(k, r.RooFit.RenameAllNodes("workspace"))

wspace.Print()
wspace.writeToFile("addPdf_workspace.root")


xframe = x.frame(r.RooFit.Title("Generated data"))




xframe2 = x.frame(r.RooFit.Title("Gaussian+Exp fit to the data"))

data.plotOn(xframe)

result = model.fitTo(data, r.RooFit.Save())
ras_sig = r.RooArgSet(gauss)
ras_bkg = r.RooArgSet(shape)
data.plotOn(xframe2)
model.plotOn(xframe2)
#model.plotOn(xframe2,r.RooFit.Components(ras_sig),r.RooFit.LineColor(r.kRed), r.RooFit.LineStyle(r.kDashed))
#model.plotOn(xframe2,r.RooFit.Components(ras_bkg),r.RooFit.LineColor(r.kGreen), r.RooFit.LineStyle(r.kDashed))

c = r.TCanvas("rf101_basics","rf101_basics",800,400)
c.Divide(2)
c.cd(1)
r.gPad.SetLeftMargin(0.15) ; xframe.GetYaxis().SetTitleOffset(1.6) ; xframe.Draw()

c.cd(2) ; r.gPad.SetLeftMargin(0.15) ; xframe2.GetYaxis().SetTitleOffset(1.6) ; xframe2.Draw() ;
#c.Draw()
c.SaveAs("addPdf_withworkspace_plot.png")


result.Print("v")
hcorr = result.correlationHist()
c = r.TCanvas("c","c",800,400)
hcorr.Draw("colz")
c.SaveAs("corr_matr.png")

# Visualize ellipse corresponding to single correlation matrix element
frame = r.RooPlot(sigma, bkgfrac, 0.95, 1.05, 0.45, 0.55)
frame.SetTitle("Covariance between sigma1 and sig1frac")
result.plotOn(frame, sigma, bkgfrac, "ME12ABHV")
c = r.TCanvas("rf101_basics","rf101_basics",800,400)
frame.Draw()
c.SaveAs("result.png")


nll = r.RooNLLVar("nll", "nll", model, data)
frame2 = sigma.frame(r.RooFit.Range(0.1, 10.),
                  r.RooFit.Title("-log(L) scan vs sigma, regions masked"))
#nll.plotOn(frame2, r.RooFit.PrintEvalErrors(-1), r.RooFit.ShiftToZero(),
#           r.RooFit.EvalErrorValue(nll.getVal() + 10), r.RooFit.LineColor(r.kRed))
nll.plotOn(frame2,r.RooFit.ShiftToZero(),r.RooFit.LineColor(r.kRed))
frame2.SetMaximum(2)
frame2.SetMinimum(0)

c = r.TCanvas("nllerrorhandling",
                 "nllerrorhandling", 1200, 400)
frame2.Draw()

c.SaveAs("nllerrorhandling_sigma.root")

print (xframe2.chiSquare())

hresidual = xframe2.residHist()
hpull = xframe2.pullHist()


frm = x.frame(r.RooFit.Title("Residual Dist."))
frm.addPlotable(hresidual, "P")

frm_p = x.frame(r.RooFit.Title("Pull Dist."))
frm_p.addPlotable(hpull, "P")

c = r.TCanvas("c","c",900,300)

c.Divide(3)
c.cd(1); xframe2.Draw()
c.cd(2); frm.Draw()
c.cd(3); frm_p.Draw()
c.SaveAs("resid_pull_hist.png")


