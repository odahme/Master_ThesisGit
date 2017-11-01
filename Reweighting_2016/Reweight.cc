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
using namespace std;



int main(int argc, char *argv[])
{
  if(argc != 1)
    {

      cout<<"Wrong number of arguments"<<endl;
      cout<<"Usage: ./Reweight.x "<<endl;
      return -1;

    }


  TCanvas *c1 = new TCanvas("c1", "c1", 800,600);

  string MC_path = "/media/oliver/USB-HDD/ntupels/MC/Run2_S28_TISTOSFIX/B2KstarJpsi_MC_2016.root";
  string data_path = "/media/oliver/USB-HDD/ntupels/Splot/KstarJpsi_2016_Splot.root";


  vector<string> names={"nTracks", "B0_PT", "B0_ENDVERTEX_CHI2"};

  int bins=100;
  string dataWeightName="sigB0_sw";

  string selection_MC  ="J_psi_M>(3097-60) && J_psi_M<(3097+60)";
  string selection_DATA="1";

  for(int i=1;i<5;++i)
    {
      stringstream fileHistoName;
      fileHistoName<<"out/out_"<<i<<".root";
      getWeights(MC_path, data_path, "B2XMuMu_Line_Tuple/DecayTree", "data", bins, names, i, fileHistoName.str(),dataWeightName,  selection_MC, selection_DATA, "");

    }


  return 1;
}
