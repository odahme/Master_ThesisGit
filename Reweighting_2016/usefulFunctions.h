#ifndef USEFUL_FUNCTIONS_H
#define USEFUL_FUNCTIONS_H

#include<sstream>
#include<string>
#include<vector>
#include<fstream>
#include "TCanvas.h"
#include "TH1.h"
#include "TLorentzVector.h"
//#include "KFolder.hpp"
//#include "uKFolder.hpp"
#include "TTreeFormula.h"
//#include "valError.h"

class ValError;

using namespace std;


string getStripping20Cuts();
double s2d(string str); //convert string to double
string d2s(double d);
string dbl2str(double nbr, int nfixed = 0); //convert string to double with fixed precision
string i2s(int i);
vector<string> loadList(ifstream& inf);
void addWeightBranch(string namefile, string nameweight, string formulaweight);
//void addVarKFold(uKFolder& kf, string spectatorList, string trainingList);
double getEntries(TTree* t, string cut = "", string weightName = "");
double getEntries(string filename, string cut = "", string weightName = "", string nametree = "DecayTree");
ValError getEntriesWithError(TTree* t, string cut = "", string weightName = "");
ValError getEntriesWithError(string filename, string cut = "", string weightName = "", string nametree = "DecayTree");
bool setBranchStatusTTF(TTree* t, string cuts);
bool separateString(string& str1, double& min, double& max);
void removeBranchFromTree(string namefile, string namebranch);
double getCorrelationCoefficient(TTree*& t, string var1name, string var2name, string cuts, bool draw = false, string plotname = "");
double getCorrelationCoefficient(string filename, string var1name, string var2name, string cuts, bool draw = false, string plotname = "");
void getCorrelationMatrix(vector<string> vars, string namefile, string nameoutputdir, string cuts, bool draw2d = false);
void addBranchInTree(string namefile, string nameNewBranch, string formulaNewBranch);
void addBranchInTree(string namefile, vector<string> nameNewBranch, vector<string> formulaNewBranch);
void divideByBinWidth(TH1* h);
string cleanNameString(string s);
double gamma(double* x, double* param);

void plotOneVariable(string filename,
      string varname,
      string outputname,
      int nbin = 50,
      string cut = "",
      string weightExpression = "", 
      string legEntry = "",
      string outputlegname = "",
      string drawOptions = "hist",
      bool wantLogPlot = false,
      string nameTree = "DecayTree");

void plotOneVariable(vector<string> const& filenames,
      string varname,
      string outputname,
      int nbin,
      string cut,
      vector<string> weightExpressions = vector<string>(0),
      string outputlegname = "",
      vector<string> legEntries = vector<string>(0),
      string drawOptions = "hist",
      bool wantLogPlot = false,
      string nameTree = "DecayTree");

void plotOneVariable(vector<string> const& filenames,
      string varname,
      string outputname,
      int nbin = 50,
      vector<string> cuts = vector<string>(0),
      vector<string> weightExpressions= vector<string>(0),
      string outputlegname = "",
      vector<string> legEntries = vector<string>(0),
      string drawOptions = "hist",
      bool wantLogPlot = false,
      string nameTree = "DecayTree");





double getCosThetaL(bool bzero,
      const TLorentzVector& muplus,
      const TLorentzVector& muminus,
      const TLorentzVector& kaon);


double gammaDataNorm(double SPDHits);
double gammaMCNorm(double SPDHits);
void getDoubleEvents(vector<pair<unsigned int, unsigned int> >& doubleEntries, vector<int>& notDoubleEntries, string nameTree );
void mergeTrees(string targetName, string treeFile1, string treeFile2 = "", string treeFile3 = "", string treeFile4 = "", string treeFile5 = "", string treeFile6 = "");
void makePull(TH1* pull, TH1 const& h1, TH1 const& h2, bool wantUniform);
void lhcbStyle(double fontsize);




#endif
