# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 12:06:14 2017

@author: odahme
"""

from pylab import *
import pandas, numpy
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
# this wrapper makes it possible to train on subset of features
from hep_ml import uboost, gradientboosting as ugb, losses
from root_pandas import read_root, to_root
#from rep.report.metrics import RocAuc
import rep
#from rep.metaml import ClassifiersFactory
#from rep.estimators import TMVAClassifier, SklearnClassifier, XGBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier
from sklearn.model_selection import KFold
from scipy import stats
from ROOT import TGraphErrors, TCanvas
print('import complete')

#view()
used_columns_sig = ["nTracks", "B0_PT", "B0_ENDVERTEX_CHI2", "B0_DIRA_OWNPV", "B0_IP_OWNPV", "B0_FD_OWNPV", "B0_FDCHI2_OWNPV", "B0_IPCHI2_OWNPV" ]

used_columns_bkg = ["nTracks", "B0_PT", "B0_ENDVERTEX_CHI2", "B0_DIRA_OWNPV", "B0_IP_OWNPV", "B0_FD_OWNPV", "B0_FDCHI2_OWNPV", "B0_IPCHI2_OWNPV","DATAMC_weight_1" ]

#path_sig='/disk/lhcb_data/mchrzasz/Kstarmumu/MC/Run2_S28/'

signal_names = [
    #path_mc+'B2KstarMuMu_SM_MC_2016_MagUp_Pythia8_Sim09b_Filtered_11114001.root',
    #path_mc+'B2KstarMuMu_SM_MC_2016_MagDown_Pythia8_Sim09b_Filtered_11114001.root'
    '/media/oliver/USB-HDD/ntupels/Splot/KstarJpsi_2016_Splot.root'
]

#path_dataRun1='/disk/lhcb_data/mchrzasz/Kstarmumu/data/Run1/'
#path_dataRun2_S26='/disk/lhcb_data/mchrzasz/Kstarmumu/data/Run2_S26/'
#path_dataRun2_S28='/disk/lhcb_data/mchrzasz/Kstarmumu/data/'
# path_dataRun2_S28_TISTOSFIX='/disk/lhcb_data/mchrzasz/Kstarmumu/data/Run2_S28_TISTOSFIX/'
#
# bck_names= [
#     #path_dataRun1+'Kstarmumu_Data_2011_MagDown.root',
#     #path_dataRun1+'Kstarmumu_Data_2011_MagUp.root',
#     #path_dataRun1+'Kstarmumu_Data_2012_MagDown.root',
#     #path_dataRun1+'Kstarmumu_Data_2012_MagUp.root',
#
#     #path_dataRun2_S26+'Kstarmumu_Data_2015_MagDown.root',
#     #path_dataRun2_S26+'Kstarmumu_Data_2015_MagUp.root',
#     #path_dataRun2_S26+'Kstarmumu_Data_2016_MagDown.root',
#     #path_dataRun2_S26+'Kstarmumu_Data_2016_MagUp.root',
#
#     #path_dataRun2_S28+'Kstarmumu_Data_2015_MagDown.root',
#     #path_dataRun2_S28+'Kstarmumu_Data_2015_MagUp.root',
#     #path_dataRun2_S28+'Kstarmumu_Data_2016_MagDown.root',
#     #path_dataRun2_S28+'Kstarmumu_Data_2016_MagUp.root'
#
#     path_dataRun2_S28_TISTOSFIX+'Kstarmumu_Data_2015_MagDown.root',
#     path_dataRun2_S28_TISTOSFIX+'Kstarmumu_Data_2015_MagUp.root',
#     path_dataRun2_S28_TISTOSFIX+'Kstarmumu_Data_2016_MagDown.root',
#     path_dataRun2_S28_TISTOSFIX+'Kstarmumu_Data_2016_MagUp.root'
# ]

Sdata = read_root(signal_names,'data',columns=used_columns_sig)
Bdata = read_root("/media/oliver/USB-HDD/ntupels/MC/Run2_S28_TISTOSFIX/B2KstarJpsi_MC_2016.root",'DecayTree',columns=used_columns_bkg)
print('Data reading finished')
#Bdata = Bdata.iloc[range(0,30000)]
#Sdata = Sdata.iloc[range(0,10000)]
Sdata.insert(len(used_columns_sig),'label',1)
Bdata.insert(len(used_columns_bkg),'label',0)
print('Labels added')

for var_name in used_columns_sig:
    Bdata[var_name] = Bdata[var_name] * Bdata['DATAMC_weight_1']
    pass

raw_data = pandas.concat([Sdata,Bdata],ignore_index=True)
data = raw_data.reset_index()
data = data.drop('index',axis=1)


kf = KFold(n_splits=10, shuffle=True, random_state=7103)
print(kf)
n =0
for train_index, test_index in kf.split(data):
    #print('Train_I: '+str(train_index)+' Test_I: '+str(test_index))
    trainX, testX = data.iloc[train_index], data.iloc[test_index]
    testX.to_root('/home/oliver/Master_Thesis/storage/Reweighting_2016_ML_check/folds/fold'+ str(n) +'.root')
    print('fold '+ str(n) +' done.')
    n+=1
