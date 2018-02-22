#ifndef __CINT__
#endif
#include <iostream>
#include "TTree.h"
#include "TH1D.h"
#include "TRandom.h"
#include "RooRealVar.h"
#include "RooDataHist.h"
#include "RooGlobalFunc.h"
#include "RooBreitWigner.h"
#include "RooGaussian.h"
#include "RooVoigtian.h"
#include  "RooCBShape.h"
#include "RooFFTConvPdf.h"
#include "RooPlot.h"
#include "RooAddPdf.h"
#include  "RooFitResult.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TPaveLabel.h"
#include "TPave.h"
#include "TStyle.h"
#include "TROOT.h"


using namespace RooFit ;

void Convolution(){
  RooRealVar x("x","mu+mu- Inv. Mass (in GeV)",60,120,"GeV");
  TFile *inputfile = new TFile("MyAn.root","READ");
  inputfile->cd();
  
  TH1F *heg  = (TH1F*)inputfile->Get("h4");
  RooDataHist dh("dh","dh",x,Import(*heg)) ;
  RooPlot* frame = x.frame(Title("M_{eg}")) ;
  dh.plotOn(frame,Name("dh")) ;
    
  RooRealVar mBW("mBW","mean BW",91.1875,60,120) ;
  RooRealVar sBW("sBW","sigma BW",2.4952,0.0,10.0) ;
  RooBreitWigner brietwigner("BW","BW",x,mBW,sBW) ;

  RooRealVar mCB("mCB", "mCB" ,0,0,1.0) ;
  RooRealVar sCB("sCB", "sCB" ,2.3 , 0.0, 5.0)  ;
  RooRealVar nCB("nCB","", 10,0.,200.0);
  //RooRealVar nCB("nCB","", 1.42,0.001,50);
  RooRealVar alphaCB("alphaCB","", 0.93,0.1,5.0);
  //RooRealVar alphaCB("alphaCB","", 0.93,0.1 , 50);
  RooCBShape cball("cball","cball",x,mCB,sCB, alphaCB, nCB);

  RooRealVar lambda("lambda", "slope", -0.1, -5.0, 0.0);
  RooExponential shape("expo", "exponential PDF", x, lambda);

  RooFFTConvPdf bwcball("BWxcball","BW(X)cball",x,brietwigner, cball) ;
  RooRealVar nsig("nsig","signal events",50000,0,80000);
  RooRealVar nbkg("nbkg","signal background events",1000,0,2000);

  RooAddPdf  model("model","bwcball+shape",RooArgList(bwcball,shape),RooArgList(nsig,nbkg)) ; 

  //model.fitTo(dh,Range(60,120));                                                                                
  model.fitTo(dh,Extended(),Range(60,120));                                                                                
  // model.plotOn(frame); 
  // model.fitTo(dh,Extended(),Range(60,120));                                                                                
  model.plotOn(frame,Name("model"));
  model.plotOn(frame,Components(shape),LineStyle(kDashed)) ;
  model.plotOn(frame,Components(bwcball),LineColor(kGreen),LineStyle(kDashed)) ;
  model.paramOn(frame,Layout(0.62,0.90),Format("NEU",AutoPrecision(1))) ;
  frame->getAttText()->SetTextSize(0.026) ;
  
  TCanvas* c = new TCanvas("c","Inv. Mass Hist.",800,800) ;
  c->cd();
  gPad->SetLeftMargin(0.19) ; frame->GetYaxis()->SetTitleOffset(1.8) ;
  gPad->SetRightMargin(0.10) ; frame->GetXaxis()->SetTitleOffset(1.2) ;

  frame->Draw();
  // c->SaveAs("hello.png")  ;
  //  inputfile->Close();
 
}
