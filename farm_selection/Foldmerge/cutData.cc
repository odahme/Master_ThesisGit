


#include <iostream>
#include <sstream>

#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TChain.h>










using namespace std;




int main(int argc, char const *argv[]) {

  if(argc != 2)
  {

    cout<<"Wrong number of arguments"<<endl;
    cout<<"Usage: ./cudData <year=2015 2016>"<<endl;
    return -1;

  }

  int year=atoi(argv[1]);

  TChain *chData = new TChain();

  if(year==2015)
    {
      chData->Add("/disk/lhcb_data/mchrzasz/Kstarmumu/data/Run2_S28_TISTOSFIX/Kstarmumu_Data_2015_MagDown.root/B2XMuMu_Line_Tuple/DecayTree");
      chData->Add("/disk/lhcb_data/mchrzasz/Kstarmumu/data/Run2_S28_TISTOSFIX/Kstarmumu_Data_2015_MagUp.root/B2XMuMu_Line_Tuple/DecayTree");
    }
  else if(year==2016)
    {
      chData->Add("/disk/lhcb_data/mchrzasz/Kstarmumu/data/Run2_S28_TISTOSFIX/Kstarmumu_Data_2016_MagDown.root/B2XMuMu_Line_Tuple/DecayTree");
      chData->Add("/disk/lhcb_data/mchrzasz/Kstarmumu/data/Run2_S28_TISTOSFIX/Kstarmumu_Data_2016_MagUp.root/B2XMuMu_Line_Tuple/DecayTree");
    }
  else
    {
      cout<<"Wrong year!"<<endl;
      return 0;

    }
  std::cout << "********************************************************" << '\n';
  cout<<"ENTRIES Data: "<<chData->GetEntries()<<endl;
  size_t nentries = chData->GetEntries();
  std::cout << "********************************************************" << '\n';
  chData->SetBranchStatus("*",1);


  string cut_string = "B0_M>4960&&B0_M<5700&&J_psi_M>(3097-60)&&J_psi_M<(3097+60) && Kstar_M>795.9 && Kstar_M < 995.9";




  // TTree *t = chData->CopyTree(cut_string.c_str());
  TTree *tt = chData->CloneTree(0);

  double B0_M = 0;
  double J_psi_M = 0;
  double Kstar_M = 0;
  chData->SetBranchAddress("B0_M",&B0_M);
  chData->SetBranchAddress("J_psi_M",&J_psi_M);
  chData->SetBranchAddress("Kstar_M",&Kstar_M);
  for (size_t i = 0; i < nentries; i++) {
    chData->GetEntry(i);
    if (B0_M>4960 && B0_M<5700 && J_psi_M>(3097-60) && J_psi_M<(3097+60) && Kstar_M>795.9 && Kstar_M < 995.9){
      tt->Fill();
    }
    if (i % 100000 == 0) {
      std::cout << "at entry "<< i << '\n';
    }
    B0_M = 0;
    J_psi_M = 0;
    Kstar_M = 0;
  }
  std::cout << "********************************************************" << '\n';
  cout<<"ENTRIES: Data reduced: "<<tt->GetEntries()<<endl;
  std::cout << "********************************************************" << '\n';
  // tt->Print();

  stringstream sssxx;

if(year==2015)
  {
    sssxx<<"/disk/users/odahme/KstarSelection/reducedData2015.root";
  }
if(year==2016)
  {
    sssxx<<"/disk/users/odahme/KstarSelection/reducedData2016.root";
  }
  TFile *ff = new TFile( sssxx.str().c_str(), "RECREATE");
  ff->cd();

  tt->Write();
  ff->Close();







  return 1;
}
