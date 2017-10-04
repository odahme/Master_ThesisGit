
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


def rms(x) :
    q = np.square(x)
    s = np.sum(q)
    sol = sqrt(s/len(x))
    return sol

cor_params = ['B0_M', "B0_ThetaK", "B0_ThetaL","B0_Phi"]
bins = 10

bdt = data['bdt']
for p in cor_params:
    title = 'corPlot_bdt_vs_'+p
    c = TCanvas('c',title,1920,1080)
    plot_p = data[p]
    if (p == 'B0_M'):
        bin_rms = stats.binned_statistic(plot_p, bdt, statistic=rms,bins=bins)
        bin_mean = stats.binned_statistic(plot_p, bdt, statistic='mean',bins=bins)
    else:
        bin_rms = stats.binned_statistic(plot_p, bdt, statistic=rms,bins=bins,range=(-1.,1.))
        bin_mean = stats.binned_statistic(plot_p, bdt, statistic='mean',bins=bins, range=(-1,1))
    p_mean = (bin_rms[1][1:bins+1] + bin_rms[1][0:bins])/2
    p_er = (bin_rms[1][1:bins+1] - bin_rms[1][0:bins])/2
    gr = TGraphErrors(bins,p_mean,bin_mean[0],p_er,bin_rms[0])
    gr.SetTitle(title)
    if (p == 'B0_M' or p == "B0_Phi"):
        gr.GetXaxis().SetTitle(p)
    else:
        gr.GetXaxis().SetTitle('Cos '+p)
    gr.GetYaxis().SetTitle('bdt')
    gr.SetMarkerStyle(20)
    gr.Draw('AP')
    fn = '/home/uzh/odahme/Master_Thesis/selection/plots/'+title+'.pdf'
    c.SaveAs(fn)
    del c



