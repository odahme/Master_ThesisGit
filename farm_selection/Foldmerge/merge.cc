


#include <iostream>
#include <sstream>

#include <TFile.h>
#include <TTree.h>
#include <TChain.h>










using namespace std;




int main(int argc, char const *argv[]) {

  // if(argc != 3)
  // {
  //
  //   cout<<"Wrong number of arguments"<<endl;
  //   cout<<"Usage: ./merge <year=2015 2016>"<<endl;
  //   return -1;
  //
  // }
  //
  // int year=atoi(argv[1]);
  //
  //
  // if(year==2015)
  //   {
  //     chData->Add("/disk/lhcb_data/mchrzasz/Kstarmumu/data/Run2_S28_TISTOSFIX/Kstarmumu_Data_2015_MagDown.root/DecayTree");
  //     chData->Add("/disk/lhcb_data/mchrzasz/Kstarmumu/data/Run2_S28_TISTOSFIX/Kstarmumu_Data_2015_MagUp.root/DecayTree");
  //   }
  // else if(year==2016)
  //   {
  //     chData->Add("/disk/lhcb_data/mchrzasz/Kstarmumu/data/Run2_S28_TISTOSFIX/Kstarmumu_Data_2016_MagDown.root/DecayTree");
  //     chData->Add("/disk/lhcb_data/mchrzasz/Kstarmumu/data/Run2_S28_TISTOSFIX/Kstarmumu_Data_2016_MagUp.root/DecayTree");
  //   }
  // else
  //   {
  //     cout<<"Wrong year!"<<endl;
  //     return 0;
  //
  //   }
  // cout<<"Entries: "<<chData->GetEntries()<<endl;
  // chData->SetBranchStatus("*",1);

  TChain *foldCh = new TChain();
  //Adding folds
  for (int i = 0; i < 10; i++) {
    stringstream ss;
    ss<<"/disk/users/odahme/KstarSelection/folds/fold"<<i<<"/clas_fold"<<i<<".root/default";
    foldCh->Add(ss.str().c_str());
  }
  std::cout << "Entries: " <<foldCh->GetEntries()<< '\n';
  foldCh->SetBranchStatus("*",0);
  foldCh->SetBranchStatus("uBoost",1);
  foldCh->SetBranchStatus("sk_bdt",1);

  TFile *f = new TFile("/disk/users/odahme/KstarSelection/bdts.root","recreate");
  TTree *t = foldCh->CloneTree();
  t->Write();
  f->Close();







  return 1;
}
