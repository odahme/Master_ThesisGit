#include "RooRealVar.h"
#include "RooDataSet.h"
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
#include "RooAbsReal.h"
#include "RooMinuit.h"
#include "TLorentzVector.h"
#include "TDirectoryFile.h"

#include <TH3F.h>
#include "usefulFunctions.h"
#include "reweightingTools.h"

// use this order for safety on library loading
using namespace RooFit ;
using namespace RooStats ;
using namespace TMVA;
using namespace std;


void create_reweighted_MC() {

  string data_path_splot="/media/oliver/USB-HDD/ntupels/data_reduced/Splot/KstarJpsi_2016_Splot.root";
  string data_path_MC="/media/oliver/USB-HDD/ntupels/data_reduced/Run2/B2KstarJpsi_MC_2016.root";

  TFile f_splot(data_path_splot.c_str());
  TFile f_MC(data_path_MC.c_str());

  TTree *t_sPlot = (TTree*) f_splot.Get("data");
  TTree *t_MC = (TTree*) f_MC.Get("Reduced");

  size_t entries_sPlot = t_sPlot->GetEntries();
  size_t entries_MC = t_MC->GetEntries();
  if (entries_sPlot != entries_MC) {
    std::cout << "Splot and MC have different number of entries!" << '\n';
    return;
  }

  TFile *new_MC = new TFile("out/KstarJpsi_2016_MC_reweighted.root");
  TTree *new_Tree = t_MC->CloneTree(0);
  Event *e_MC = new Event();
  t_MC->SetBranchAddress("e_MC",&e_MC);


  for (size_t i = 0; i < entries_MC; i++) {
    TLeaf *w_leaf = t_sPlot->GetLeaf("DATAMC_weight_1");
    w_leaf->GetBranch()->GetEntry(i);
    t_MC->GetEntry(i);
    Double_t w =w_leaf->GetValue();
    e_MC->SetWeight(w);
    new_Tree->Fill();
    e_MC->Clear();
  }

  new_MC->cd();
  new_Tree->Write();
  new_MC->Write();
  new_MC->Close();
  f_splot.Close();
  f_MC.Close();






}
