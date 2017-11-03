#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <math.h>
#include <Rtypes.h>
#include <TSystem.h>
#include <TROOT.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TChain.h>
#include <TTree.h>
#include <TF1.h>
#include <TCut.h>
#include <TString.h>
#include <TMath.h>
#include <TH1F.h>
#include <TF1.h>
#include <TCut.h>
#include <TString.h>
#include <TMath.h>
#include <TH1F.h>
#include <TH2F.h>
#include <TGraphErrors.h>
#include "math.h"
#include "RooCBShape.h"
#include "RooRealVar.h"
#include "RooAbsReal.h"
#include "RooExponential.h"
#include "RooDataSet.h"
#include "RooPlot.h"
#include "TFile.h"
#include <iostream>
#include <fstream>
#include "RooGenericPdf.h"
#include "RooPolynomial.h"
#include "RooAddPdf.h"
#include "RooExtendPdf.h"
#include <vector>
#include "RooGaussian.h"
#include <unistd.h>
#include "RooStats/SPlot.h"
#include "RooDataHist.h"
#include "RooGenericPdf.h"
#include "RooPolynomial.h"
#include "RooAddPdf.h"
#include "RooExtendPdf.h"
#include <vector>
#include "RooGaussian.h"
#include <unistd.h>
#include "RooStats/SPlot.h"
#include "RooDataHist.h"
#include "RooAbsReal.h"
#include "RooMinuit.h"
#include "TLorentzVector.h"
#include "TDirectoryFile.h"

#include <TH3F.h>
using namespace std;



void plot_comparistion()
{

  vector<string> names={"nTracks", "B0_PT", "B0_ENDVERTEX_CHI2", "B0_DIRA_OWNPV", "B0_IP_OWNPV", "B0_FD_OWNPV", "B0_FDCHI2_OWNPV", "B0_IPCHI2_OWNPV"};
  vector<string> names_nice={"nTracks", "B0_PT", "B0_ENDVERTEX_CHI2" , "B0_DIRA_OWNPV", "B0_IP_OWNPV", "B0_FD_OWNPV", "B0_FDCHI2_OWNPV", "B0_IPCHI2_OWNPV"};
  vector<string>  ranges={"(100,0,600)", "(100,0,30000)", "(25,0,25)", "(50,0.9999,1)", "(100,0,0.15)", "(100,0,50)", "(100,0,10000)",        "(40,0,20)"};

  TFile *fmc = new TFile("/media/oliver/USB-HDD/ntupels/MC/Run2_S28_TISTOSFIX/B2KstarJpsi_MC_2016.root");

  TFile *fd =  new TFile("/media/oliver/USB-HDD/ntupels/Splot/KstarJpsi_2016_Splot.root");

  TTree *tmc = (TTree*)fmc->Get("DecayTree");
  TTree *td= (TTree*)fd->Get("data");

  string weight_name="DATAMC_weight_1";

  TCanvas *c1 = new TCanvas("c1","c1", 600,400);

  gStyle->SetOptStat(kFALSE);

  cout<<"Checking: "<<names.size()<<" "<<names_nice.size()<<"  "<<ranges.size()<<endl;


  for(int i=0;i<names.size(); i++)
    {

      stringstream ss;
      ss<<names[i]<<">>hist"<<ranges[i];


      stringstream ss1;
      ss1<<names[i]<<">>hist1"<<ranges[i];

      stringstream ss2;
      ss2<<names[i]<<">>hist2"<<ranges[i];


      tmc->Draw(ss.str().c_str());
      tmc->Draw(ss1.str().c_str(), weight_name.c_str() );

      td->Draw(ss2.str().c_str());

      TH1F *histmc= (TH1F*)gROOT->FindObject("hist");
      TH1F *histmcw= (TH1F*)gROOT->FindObject("hist1");

      TH1F *histd = (TH1F*)gROOT->FindObject("hist2");

      histmc->SetLineColor(kRed+2);
      histmcw->SetLineColor(kGreen+2);
      histd->SetLineColor(kCyan+2);

      histmc->SetLineWidth(3);
      histmcw->SetLineWidth(3);
      histd->SetLineWidth(3);

      histmc->GetXaxis()->SetTitle(names[i].c_str());
      histmcw->GetXaxis()->SetTitle(names[i].c_str());
      histd->GetXaxis()->SetTitle(names[i].c_str());


      histmcw->SetTitle("");
      histmc->SetTitle("");
      histd->SetTitle("");

      histd->DrawNormalized();

      histmc->DrawNormalized("SAME");
      histmcw->DrawNormalized("SAME");


      //
      TLegend *leg = new TLegend(0.5, 0.8, 0.75, 0.9);
      leg->AddEntry(histmc, "MC", "f");
      leg->AddEntry(histmcw, "MC weighted", "f");
      leg->AddEntry(histd, "Data", "f");

      leg->Draw();

      //saving
      stringstream ss10;
      ss10<<"plots/"<<names[i]<<".png";
      c1->SaveAs(ss10.str().c_str());

      //saving
      stringstream ss11;
      ss11<<"plots/root_files/"<<names[i]<<".root";
      c1->SaveAs(ss11.str().c_str());



    }


}
