
# coding: utf-8

# In[ ]:




import os
import sys

from pylab import *
import pandas, numpy
import matplotlib.pyplot as plt
from scipy import stats

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import KFold
from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier

from hep_ml import uboost, gradientboosting as ugb, losses

print('importing rep')
from rep.estimators import TMVAClassifier, SklearnClassifier, XGBoostClassifier
from rep.report.metrics import RocAuc
from rep.metaml import ClassifiersFactory
print('rep imported')

print('importing Root and root_pandas')
from root_pandas import read_root, to_root
from ROOT import TGraphErrors, TCanvas
print('root imported')




foldList = [0,1,2,3,6,7,8,9]
for n in foldList:
    print('processing fold number '+str(n))
    foldname = ('/disk/users/odahme/KstarSelection/folds/fold'+ str(n) +'/clas_fold'+ str(n) +'.root')
    temp = read_root(foldname,'default')
    bdt = temp['bdt']
    bdtHist = plt.figure(n)
    plt.hist(bdt, bins=100, label='bdt', range=[0.0,1.0])
    bdtHist.savefig('/disk/users/odahme/KstarSelection/folds/fold'+ str(n) +'/bdtHist'+ str(n) +'.png')
    del temp
    del bdtHist

