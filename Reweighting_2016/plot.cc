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



void plot()
{

  vector<string> names={"nTracks", "B0_PT", "B0_ENDVERTEX_CHI2"};
  vector<string> names_nice={"nTracks", "B0_PT", "B0_ENDVERTEX_CHI2"};





  TFile *f = new TFile("out/out_1.root");
  //  TCanvas *c1 = new TCanvas("c1","c1", 600,400);

  gStyle->SetOptStat(kFALSE);

  for(int i=0;i<names.size(); i++)
    {
      stringstream ss;
      ss<<"weights_Iter0Var"<<i;

      TH1D *h0_w=(TH1D*)f->Get(ss.str().c_str());
      TH1D *h0_mc=(TH1D*)f->Get(("MC_"+names[i]).c_str());
      TH1D *h0_t=(TH1D*)f->Get(("target_"+names[i]).c_str());


      h0_w->GetXaxis()->SetTitle(names[i].c_str());
      h0_mc->GetXaxis()->SetTitle(names[i].c_str());
      h0_t->GetXaxis()->SetTitle(names[i].c_str());


      h0_mc->Scale(1./h0_mc->GetSumOfWeights());
      h0_t->Scale(1./h0_t->GetSumOfWeights());


      TCanvas *c1 = new TCanvas("c1","c1", 600,400);

      int order=0;
      double max=h0_mc->GetMaximum();
      TH1D *hmax=h0_mc;
      double maxp;

      if(max<h0_t->GetMaximum())
	{
	  max=h0_t->GetMaximum();
	  order=1;
	  hmax=h0_t;
	}
      if(order==0)
	{
	  h0_mc->Draw();
	  c1->Update();
	  maxp=gPad->GetUymax();
	  h0_t->Draw("same");
	}
      else
	{
	  h0_t->Draw();
	  c1->Update();
	  maxp=gPad->GetUymax();
	  h0_mc->Draw("same");
	}


      //scale hint1 to the pad coordinates
      Float_t rightmax = 1.1*h0_w->GetMaximum();
      cout<<rightmax<<endl;
      cout<<gPad->GetUymax()<<endl;
      cout<<maxp<<endl;
      Float_t scale = max/rightmax;
      cout<<scale<<endl;
      h0_w->SetLineColor(kGreen+2);
      h0_w->Scale(scale);
      h0_w->Draw("same");

      maxp=max*1.1;

      //draw an axis on the right side
      TGaxis *axis = new TGaxis(gPad->GetUxmax(),gPad->GetUymin(),
				gPad->GetUxmax(), gPad->GetUymax(),0,rightmax,510,"+L");

      axis->SetLineColor(kGreen+2);
      axis->SetLabelColor(kGreen+2);
      axis->Draw();

      c1->Update();


      //
      TLegend *leg = new TLegend(0.5, 0.8, 0.75, 0.9);
      leg->AddEntry(h0_mc, "MC", "f");
      leg->AddEntry(h0_t, "data", "f");
      leg->AddEntry(h0_w, "weight", "f");

      leg->Draw();

      //saving
      stringstream ss1;
      ss1<<"plots/"<<names[i]<<"w.png";
      c1->SaveAs(ss1.str().c_str());
    }


}
