import ROOT as r

x = r.RooRealVar("x","x",-10,10)
mean = r.RooRealVar("mean","mean of gaussian",1,-10,10)
sigma = r.RooRealVar("sigma","width of gaussian",1,0.1,10)


gauss = r.RooGaussian("gauss","gaussian PDF",x,mean,sigma)

l = r.RooRealVar("lambda", "slope", -0.1, -5.0, 0.0)
shape = r.RooExponential("expo", "exponential PDF", x, l)

nsig = r.RooRealVar("nsig","signal events",20000,0,80000)
nbkg = r.RooRealVar("nbkg","background events",20000,0,80000)

model = r.RooAddPdf("model","Gauss+shape",r.RooArgList(gauss,shape),r.RooArgList(nsig,nbkg))

xframe = x.frame(r.RooFit.Title("Generated data"))


data = model.generate(r.RooArgSet(x),10000)

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
c.SaveAs("addPdf_plot.png")
