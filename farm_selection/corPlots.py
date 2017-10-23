
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



print('reading root file')
data = read_root('/disk/users/odahme/KstarSelection/class_data.root')
print('finished reading')

cuts = [1.0,0.8,0.6]

def rms(x) :
    q = np.square(x)
    s = np.sum(q)
    sol = sqrt(s/len(x))
    return sol

cor_params = ['B0_M', "B0_ThetaK", "B0_ThetaL","B0_Phi"]
bins = 10
classNames = ['sk_bdt', 'uBoost']

for cn in classNames:
    for cut in cuts:
        cutData = data[(data[cn] <= cut)]
        bdt = cutData[cn]
        for p in cor_params:
            title = 'corPlot_'+str(cn)+'(<'+str(cut)+')_vs_'+p
            c = TCanvas('c',title,1920,1080)
            plot_p = cutData[p]
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
            fnpdf = '/home/uzh/odahme/Master_Thesis/farm_selection/plots/'+title+'.pdf'
            fnroot = '/home/uzh/odahme/Master_Thesis/farm_selection/plots/root_files/'+title+'.root'
            c.SaveAs(fnpdf)
            c.SaveAs(fnroot)
            del c



