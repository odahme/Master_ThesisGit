#ifndef REWEIGHTINGTOOLS_H
#define REWEIGHTINGTOOLS_H



#include<iostream>
#include "TH1D.h"
//#include "usefulFunctions.h"
#include "TTreeFormula.h"
#include<vector>
#include<string>
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
                                          
using namespace std;


void getWeights(string fileMCTree, string fileTargetTree, string nameMCTree, string nameTargetTree, int nBins, vector<string> varsReweight, int nIter,
    string fileHistoName, string dataWeightName = "", string extracut = "", string previousMCWeight = "");
void getWeights(string fileMCTree, string fileTargetTree, string nameMCTree, string nameTargetTree, int nBins, vector<string> varsReweight, int nIter,
    vector<string> fileHistoNames, vector<string> criteria, string dataWeightName = "", string extracut = "", string previousMCWeight = "");


void getWeights(string fileMCTree, string fileTargetTree, string nameMCTree, string nameTargetTree, int nBins, vector<string> varsReweight, int nIter,
    string fileHistoName, string dataWeightName,  string extraMCCut, string extraTargetCut, string previousMCWeight);
void getWeights(string fileMCTree, string fileTargetTree, string nameMCTree, string nameTargetTree, int nBins, vector<string> varsReweight, int nIter,
    vector<string> fileHistoNames, vector<string> criteria, string dataWeightName, string extraMCcut, string extraTargetCut, string previousMCWeight);


void applyWeightsToTree( string fileTree, string nameTree, vector<string> varsReweight, int nIter, string nameHistoFile, string extracut = "", string MCNewWeightName = "DataMCWeight", string previousWeightName = "" );
void applyWeightsToTree( string fileTree, string nameTree,  vector<string> varsReweight, int nIter, vector<string> namesHistoFile, vector<string> criteria, string extracut = "", string MCNewWeightName = "DataMCWeight", string previousWeightName = "" ); //make the reweighting with different histograms produced with different criteria, ie 2012MU, 2012MD, etc.



void getUniformBinning(int nbins, double bins[], TTree* t, string namevar, string extracut = "");
void getUniformBinning(int nbins, double bins[], TTree* t, string namevar, string extracut, string nameWeight);
void updateWeightsAndFillTable(list<double>& weightTab, TTree* MCTree, int nBins, TTreeFormula* MCTtf, TFile* fileHisto, TH1D* targetHisto, string nameHisto, TTreeFormula* MCTtfExtraCut, string previousMCWeight);




#endif
