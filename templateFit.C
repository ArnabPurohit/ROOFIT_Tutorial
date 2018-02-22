#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "TCanvas.h"
#include "RooPlot.h"
#include "TAxis.h"
using namespace RooFit ;


void templateFit()
{
  // S e t u p   m o d e l                                                                                      
  // ---------------------                                                                                      

  // Declare variables x,mean,sigma with associated name, title, initial value and allowed range
  RooRealVar x("x","M_{ee}",60,110, "GeV") ;               
  TFile* file = new TFile("et_vs_mass_DYSample_massrange50_300_datamc_bothHighR9.root", "READ"); 
  TH1* data_hist = (TH1F*) file->Get("Hist4_data");
  TH1* MC_hist = (TH1F*) file->Get("Hist4_MC");
  //  data_hist->Rebin(5);
  // MC_hist->Rebin(5);

  RooDataHist* rdh_data = new RooDataHist("rdh_data","", x, data_hist);
  RooDataHist* rdh_MC = new RooDataHist("rdh_MC","", x, MC_hist);
  RooHistPdf* rdh_pdf = new RooHistPdf("rdh_pdf", "", RooArgSet(x), *rdh_MC );
  //  RooKeysPdf kest1("kest1","kest1",x,*rdh_MC,RooKeysPdf::MirrorBoth) ;

  /*  
  RooRealVar x("x","x",-10,10) ;
  RooRealVar mean("mean","mean of gaussian",1,-10,10) ;
  RooRealVar sigma("sigma","width of gaussian",1,0.1,10) ;

  // Build gaussian p.d.f in terms of x,mean and sigma                                                          
  RooGaussian gauss("gauss","gaussian PDF",x,mean,sigma) ;
  */
  // Construct plot frame in 'x'                                                                                
  RooPlot* xframe = x.frame(Title("Data Hist and Template Fit")) ;
  RooPlot* xframe2 = x.frame(Title("MC Hist")) ;

  // P l o t   m o d e l   a n d   c h a n g e   p a r a m e t e r   v a l u e s   
  // Plot gauss in frame (i.e. in x)                                                                           
 /*
  gauss.plotOn(xframe) ;

  // Change the value of sigma to 3                                                                             
  sigma.setVal(3) ;

  // Plot gauss in frame (i.e. in x) and draw frame on canvas                                                   
  gauss.plotOn(xframe,LineColor(kRed)) ;


  // G e n e r a t e   e v e n t s                                                                              
  // -----------------------------                                                                              

  // Generate a dataset of 1000 events in x from gauss                                                          
  RooDataSet* dataset = gauss.generate(x,100000) ;
  RooDataHist* data = dataset->binnedClone();
  RooHistPdf* rdh = new RooHistPdf("rdh", "", RooArgSet(x), *data,2 );
  // Make a second plot frame in x and draw both the                                                          
  RooRealVar meanP("meanP","Poisson mean", 0.,-2.,2.) ; 
  // data and the p.d.f in the frame                                                                          
  RooPoisson poisson("poisson","Poisson PDF",x,meanP) ;
  //  RooFFTConvPdf* signalShapePdf = new RooFFTConvPdf("signalShapePdf","signalShapePdf", x, (const RooAbsPdf) rdh, poisson);
  RooPlot* xframe2 = x.frame(Title("Gaussian p.d.f. with data")) ;
  // gauss.plotOn(xframe2) ;
  
  //signalShapePdf->plotOn(xframe2) ;
  RooDataSet* datasetm = gauss.generate(x,10000) ;
  RooDataHist* datam = datasetm->binnedClone();
  datam->plotOn(xframe2) ;
 */

  // F i t   m o d e l   t o   d a t a                                                                          
  // -----------------------------                                                                              

  // Fit pdf to data                                                                                            
  //gauss.fitTo(*data) ;
  rdh_data->plotOn(xframe) ;    
  rdh_pdf->fitTo(*rdh_data,Extended()) ;
  //kest1->fitTo(*rdh_data,Extended()) ;
  rdh_pdf->plotOn(xframe) ;
  //kest1->plotOn(xframe) ;
  rdh_MC->plotOn(xframe2);
  // Print values of mean and sigma (that now reflect fitted values and errors)                                
  float chi2PerDof = xframe->chiSquare(1);
  std::cout<<"Chi2perndof = " << chi2PerDof << std::endl;
  //  mean.Print() ;
  //sigma.Print() ;

  // Draw all frames on a canvas                                                                                
  TCanvas* c = new TCanvas("rf101_basics","rf101_basics",800,400) ;
  c->Divide(2) ;
  c->cd(1) ; gPad->SetLeftMargin(0.15) ;  xframe->GetYaxis()->SetTitleOffset(1.6) ; xframe2->Draw() ;
  c->cd(2) ; gPad->SetLeftMargin(0.15) ; xframe2->GetYaxis()->SetTitleOffset(1.6) ; xframe->Draw() ;


}
