import ROOT
doFit = True

w = ROOT.RooWorkspace("w")


w.factory("Exponential:bkg1_pdf(x[0,10], a1[-0.5,-2,-0.2])")
w.factory("Gaussian:sig_pdf(x, mass[2], sigma[0.3])")
w.factory("prod:nsig1(mu[1,0,5],xsec1[50])")
w.factory("SUM:model1(nsig1*sig_pdf, nbkg1[1000,0,10000]*bkg1_pdf)")

w.factory("Exponential:bkg2_pdf(x, a2[-0.25,-2,-0.2])")
w.factory("prod:nsig2(mu,xsec2[30])")
w.factory("SUM:model2(nsig2*sig_pdf, nbkg2[100,0,10000]*bkg2_pdf)")

w.factory("index[channel1,channel2]")
w.factory("SIMUL:jointModel(index,channel1=model1,channel2=model2)")

pdf = w.pdf("jointModel")
x = w.var("x")
index = w.cat("index")

x.setBins(50)
data = pdf.generate(ROOT.RooArgSet(x,index))
data.SetName("data")
getattr(w,'import')(data)
data.Print()

c = ROOT.TCanvas()
plot1 = x.frame(ROOT.RooFit.Title("Channel 1"))
plot2 = x.frame(ROOT.RooFit.Title("Channel 2"))
data.plotOn(plot1,ROOT.RooFit.Cut("index==index::channel1"))
data.plotOn(plot2,ROOT.RooFit.Cut("index==index::channel2"))
c.Divide(1,2)
c.cd(1)
plot1.Draw()
c.cd(2)
plot2.Draw()
c.SaveAs("Simultaneous_data.png")

if(doFit):
    r = pdf.fitTo(data, ROOT.RooFit.Save(True), ROOT.RooFit.Minimizer("Minuit2","Migrad"))
    r.Print()
    c = ROOT.TCanvas()
    plot1 = x.frame(ROOT.RooFit.Title("Channel 1"))
    plot2 = x.frame(ROOT.RooFit.Title("Channel 2"))
    data.plotOn(plot1,ROOT.RooFit.Cut("index==index::channel1"))
    data.plotOn(plot2,ROOT.RooFit.Cut("index==index::channel2"))
    
    pdf.plotOn(plot1,ROOT.RooFit.ProjWData(data),ROOT.RooFit.Slice(w.cat("index"),"channel1"))
    pdf.plotOn(plot2,ROOT.RooFit.ProjWData(data),ROOT.RooFit.Slice(w.cat("index"),"channel2"))
    
    #pdf.paramOn(plot1,ROOT.RooFit.Layout(0.65,0.85,0.85),ROOT.RooFit.Parameters(ROOT.RooArgSet(w.var("a1"),w.var("nbkg1"))))
    #pdf.paramOn(plot2,ROOT.RooFit.Layout(0.65,0.85,0.85),ROOT.RooFit.Parameters(ROOT.RooArgSet(w.var("a2"),w.var("nbkg2"))))
    #pdf.paramOn(plot2,ROOT.RooFit.Layout(0.65,0.85,0.7),ROOT.RooFit.Parameters(ROOT.RooArgSet(w.var("mu"))))
    
    c.Divide(1,2)
    c.cd(1)
    plot1.Draw()
    c.cd(2)
    plot2.Draw()
    c.SaveAs("SimultaneousFit.png")
    
    mc = ROOT.RooStats.ModelConfig("ModelConfig",w)
    mc.SetPdf(pdf)
    mc.SetParametersOfInterest(ROOT.RooArgSet(w.var("mu")))
    mc.SetObservables(ROOT.RooArgSet(w.var("x"),w.cat("index")))
    w.defineSet("nuisParams","a1,nbkg1,a2,nbkg2")
    mc.SetNuisanceParameters(w.set("nuisParams"))
    mc.SetSnapshot(ROOT.RooArgSet(w.var("mu")))
    getattr(w,'import')(mc)
    w.writeToFile("SimultaneousModel.root",True)
