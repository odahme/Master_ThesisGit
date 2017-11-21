
# coding: utf-8

# In[ ]:


print("start importing")

import os
import sys

import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt

from pylab import *
import pandas, numpy
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

print("importing completed")

primFoldnumber = int(sys.argv[1])
n_threads = int(sys.argv[2])

foldnameList = []

print('reading root files')
for n in range(0,10):
    if n == primFoldnumber:
        continue
    foldnameList.append('/disk/users/odahme/KstarSelection/folds/fold'+ str(n) +'/fold'+ str(n) +'.root')

for f in range(0,len(foldnameList)):
    if f==0:
        trainD = read_root(foldnameList[f],'default')
        continue
    temp = read_root(foldnameList[f],'default')
    trainD = pandas.concat([trainD,temp],ignore_index=True)
    print('added fold number '+str(f))
    del temp
testD = read_root('/disk/users/odahme/KstarSelection/folds/fold'+ str(primFoldnumber) +'/fold'+ str(primFoldnumber) +'.root')
print('reading finished')
#trainD = trainD.iloc[range(0,0000)]
#testD = testD.iloc[range(0,10000)]
trainY = trainD['label']
testY  = testD['label']
trainX = trainD.drop('label',axis=1)
testX  = testD.drop('label',axis=1)

#print(trainY)
#print(testY)

bool_index = np.logical_or(np.logical_or(
                                        np.logical_or(trainX['B0_M'] >= 6000., trainX['B0_M'] <= 5380.),

                                            np.logical_or(
                                            np.logical_and(trainX['J_psi_M']*trainX['J_psi_M']*1e-6 >= 8.,
                                                            trainX['J_psi_M']*trainX['J_psi_M']*1e-6 <= 11.),
                                            np.logical_and(trainX['J_psi_M']*trainX['J_psi_M']*1e-6 >= 12.5,
                                                            trainX['J_psi_M']*trainX['J_psi_M']*1e-6 <= 15.)
                                                        )
                                    ),
                                    np.logical_or(trainX['J_psi_M']*trainX['J_psi_M']*1e-6 >= 19. , trainX['J_psi_M']*trainX['J_psi_M']*1e-6 <= 0.1)
                           )
cut_indexList = trainX.index[bool_index]
print(str(len(cut_indexList))+' values had been cut off.')
trainX = trainX.drop(cut_indexList)
print(str(len(trainX))+' values remain for training.')
trainY = trainY.drop(cut_indexList)


train_features = [ "B0_ENDVERTEX_CHI2","B0_IP_OWNPV","B0_IPCHI2_OWNPV", "B0_FD_OWNPV","B0_FDCHI2_OWNPV","B0_P","B0_PT",
        "B0_relinfo_VTXISOBDTHARDFIRSTVALUE" ]
uniform_features = ['B0_M', "B0_ThetaK", "B0_ThetaL","B0_Phi"]
n_estimators = 500
base_estimator = DecisionTreeClassifier(max_depth=6)


classifiers = ClassifiersFactory()

uboost_clf = uboost.uBoostClassifier(uniform_features=uniform_features, uniform_label=1,
                                        base_estimator=base_estimator,
                                        n_estimators=n_estimators, train_features=train_features,
                                        efficiency_steps=12, n_threads=n_threads)

classifiers['uBoost'] = SklearnClassifier(uboost_clf)

classifiers['sk_bdt'] = SklearnClassifier( AdaBoostClassifier( n_estimators=n_estimators), features=train_features)



clasNameList = ['uBoost','sk_bdt']


print('start training')
classifiers.fit(trainX, trainY)
sig_prob = classifiers.predict_proba(testX)
report = classifiers.test_on(testX, testY)
n_fig = 1
for clasN in clasNameList:
    pred = sig_prob[clasN][:,1]
    testX.insert(len(testX.iloc[0]),clasN,pred)
    bdtHist = plt.figure(n_fig)
    plt.hist(pred, bins=100, label=clasN, range=[0.0,1.0])
    bdtHist.savefig('/disk/users/odahme/KstarSelection/folds/fold'+ str(primFoldnumber) +'/'+clasN+'Hist_fold'+ str(primFoldnumber) +'.png')
    del bdtHist
    n_fig+=1

testX.to_root('/disk/users/odahme/KstarSelection/folds/fold'+ str(primFoldnumber) +'/clas_fold'+ str(primFoldnumber) +'.root')



c1 = report.roc().canvas(name='c1',size=(1902,1080))
c1.SaveAs('/home/uzh/odahme/Master_Thesis/farm_selection/roc/fold'+ str(primFoldnumber) +'_roc.pdf')

c2= report.learning_curve().canvas(name='c2',size=(1902,1080))
c2.SaveAs('/home/uzh/odahme/Master_Thesis/farm_selection/learningCurves/fold'+ str(primFoldnumber) +'_learningCurve.pdf')
