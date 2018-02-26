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
  if(argc != 2)
    {

      cout<<"Wrong number of arguments"<<endl;
      cout<<"Usage: ./Reweight_apply.x <STRING>  "<<endl;
      return -1;

    }



  string MC_path=string(argv[1]);
  // string MC_path = "/media/oliver/USB-HDD/ntupels/MC/Run2_S28_TISTOSFIX/B2KstarJpsi_MC_2016.root";
  //string MCKmumu_path="/storage1/ntuples/lhcb/B2KLL/Selection/MC/Kmumu/Kmumu_2012.root";

   string data_path_splot="/home/oliver/Master_Thesis/storage/data_reduced/Splot/KstarJpsi_2016_Splot.root";


  vector<string> names={"nTracks", "B0_PT", "B0_ENDVERTEX_CHI2"};

  int bins=100;
  string dataWeightName="sigB0_sw";

  string selection_MC  = "B0_M>4960 && B0_M<5700 && J_psi_M>(3097-60) && J_psi_M<(3097+60) && Kstar_M>795.9 && Kstar_M < 995.9 && (B0_BKGCAT==0 || B0_BKGCAT==50)";
  // string selection_MC  = "B0_M>6000 && B0_M<5380 && J_psi_M>(3097-60) && J_psi_M<(3097+60) && Kstar_M>795.9 && Kstar_M<995.9";
  string selection_DATA="1";


// #pragma omp parallel for
  for(int i=1;i<5;++i)
    {
      stringstream fileHistoName;
      fileHistoName<<"out/out_"<<i<<".root";
      string cut="";
      stringstream weight_name;
      weight_name<<"DATAMC_weight_"<<i;
      cout<<"Doing: "<<MC_path<<endl;
      applyWeightsToTree(MC_path,  "Reduced", names, i , fileHistoName.str(), cut, weight_name.str(), "");
      //cout<<"Doing: "<<MCKmumu_path<<endl;
      // applyWeightsToTree(MCKmumu_path,  "DecayTree", names, i, fileHistoName.str(), cut, weight_name.str(), "");
      cout<<"Doing: "<<data_path_splot<<endl;
      applyWeightsToTree(data_path_splot, "data", names, i, fileHistoName.str(), cut, weight_name.str(), "");


    }


  return 1;
}
