
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



foldnameList = []

print('reading root files')
for n in range(0,10):

    foldnameList.append('/disk/users/odahme/KstarSelection/folds/fold'+ str(n) +'/clas_fold'+ str(n) +'.root')

for f in range(0,len(foldnameList)):
    if f==0:
        data = read_root(foldnameList[f],'default')
        continue
    temp = read_root(foldnameList[f],'default')
    data = pandas.concat([data,temp],ignore_index=True)
    print('added fold number '+str(f))
    del temp
print('reading finished')
data = data.reset_index()
data = data.drop('index',axis=1)
data.to_root('/disk/users/odahme/KstarSelection/class_data.root')
