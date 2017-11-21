
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
from ROOT import TGraphErrors, TCanvas
from root_pandas import read_root, to_root
print('root imported')

print("importing completed")

nThreads = 8

used_columns = ["B0_M","J_psi_M","B0_ENDVERTEX_CHI2","B0_IP_OWNPV","B0_IPCHI2_OWNPV", "B0_FD_OWNPV","B0_FDCHI2_OWNPV","B0_P","B0_PT",
                "B0_relinfo_VTXISOBDTHARDFIRSTVALUE",
                "B0_ThetaK", "B0_ThetaL" ]


path_mc='/media/oliver/USB-HDD/ntupels/MC/Run2_S28_TISTOSFIX'

signal_MC_names = [
    path_mc+'B2KstarMuMu_SM_MC_2016_MagUp_Pythia8_Sim09b_Filtered_11114001.root',
    path_mc+'B2KstarMuMu_SM_MC_2016_MagDown_Pythia8_Sim09b_Filtered_11114001.root'
]

path_data='/media/oliver/USB-HDD/ntupels/data/Run2_S28_TISTOSFIX'

bck_names= [
    #path_data+'Kstarmumu_Data_2015_MagDown.root',
    #path_data+'Kstarmumu_Data_2015_MagUp.root',
    path_data+'Kstarmumu_Data_2016_MagDown.root',
    path_data+'Kstarmumu_Data_2016_MagUp.root'
]

Sdata = read_root(signal_MC_names,'B2XMuMu_Line_Tuple/DecayTree',columns=used_columns)
Bdata = read_root(bck_names,'B2XMuMu_Line_Tuple/DecayTree',columns=used_columns)
Bdata = Bdata.iloc[range(0,10000)]
Sdata = Sdata.iloc[range(0,30000)]
Sdata.insert(len(used_columns),'label',1)
Bdata.insert(len(used_columns),'label',0)

raw_data = pandas.concat([Sdata,Bdata],ignore_index=True)
data = raw_data.reset_index()
data = data.drop('index',axis=1)
labels = data['label']
data = data.drop('label',axis=1)
cosThetaK = data["B0_ThetaK"].apply(np.cos)
cosThetaL = data["B0_ThetaL"].apply(np.cos)
data["B0_ThetaK"] = cosThetaK.values
data["B0_ThetaL"] = cosThetaL.values


# In[ ]:


train_features = [ "B0_ENDVERTEX_CHI2","B0_IP_OWNPV","B0_IPCHI2_OWNPV", "B0_FD_OWNPV","B0_FDCHI2_OWNPV","B0_P","B0_PT",
        "B0_relinfo_VTXISOBDTHARDFIRSTVALUE" ]
uniform_features = ['B0_M', "B0_ThetaK", "B0_ThetaL"]
n_estimators = 500
base_estimator = DecisionTreeClassifier(max_depth=6)

reports = []
sig_probs = []
pred_indexs = []

kf = KFold(n_splits=10, shuffle=True, random_state=13)
clasNameList = ['AdaBoost','uGB+knnAda','uBoost','uGB+FL','xgb','sk_bdtg','sk_bdt']
fold = 0
for train_index, test_index in kf.split(data):
    print("TRAIN:", train_index, "TEST:", test_index)
    trainX, testX = data.iloc[train_index], data.iloc[test_index]
    trainY, testY = labels.iloc[train_index], labels.iloc[test_index]

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

    classifiers = ClassifiersFactory()
    base_ada = GradientBoostingClassifier(max_depth=6, n_estimators=n_estimators, learning_rate=0.1,
                                         random_state=13)
    classifiers['AdaBoost'] = SklearnClassifier(base_ada, features=train_features)

    knnloss = ugb.KnnAdaLossFunction(uniform_features, knn=10, uniform_label=1)
    ugbKnn = ugb.UGradientBoostingClassifier(loss=knnloss, max_depth=6, n_estimators=n_estimators,
                                            learning_rate=0.1, train_features=train_features)
    classifiers['uGB+knnAda'] = SklearnClassifier(ugbKnn)

    uboost_clf = uboost.uBoostClassifier(uniform_features=uniform_features, uniform_label=1,
                                         base_estimator=base_estimator,
                                         n_estimators=n_estimators, train_features=train_features,
                                         efficiency_steps=12, n_threads=nThreads)
    classifiers['uBoost'] = SklearnClassifier(uboost_clf)

    flatnessloss = ugb.KnnFlatnessLossFunction(uniform_features, fl_coefficient=3., power=1.3, uniform_label=1)
    ugbFL = ugb.UGradientBoostingClassifier(loss=flatnessloss, max_depth=6,
                                           n_estimators=n_estimators,
                                           learning_rate=0.1, train_features=train_features)
    classifiers['uGB+FL'] = SklearnClassifier(ugbFL)

    classifiers['xgb'] = XGBoostClassifier(features=train_features, random_state=100, max_depth=6,n_estimators=n_estimators,
                                      eta=0.03,subsample=0.5 )
    # Using gradient boosting with default settings
    classifiers['sk_bdtg'] = SklearnClassifier(GradientBoostingClassifier(n_estimators=n_estimators, max_depth=6), features=train_features)

    classifiers['sk_bdt'] = SklearnClassifier( AdaBoostClassifier( n_estimators=n_estimators), features=train_features)

    #classifiers['tmva_BDT'] = TMVAClassifier(method='kBDT', NTrees=50, Shrinkage=0.05,features=train_features,max_depth=6 )

    classifiers.fit(trainX, trainY, parallel_profile='threads-4')
    report = classifiers.test_on(testX, testY)

    reports.append(report)
    roc = report.roc()
    #lc = report.learning_curve(RocAuc(), predict_only_masked=False)
    c1 = roc.plot_tmva(new_plot=True,title='fold_'+str(fold)+'_roc',xlabel='false positive rate',ylabel='true positive rate')
    c1.SaveAs('/home/oliver/Desktop/curves_clas_test/roc/fold_'+str(fold)+'_roc.pdf')
    #c2 = lc.plot_tmva(new_plot=True,title='fold_'+str(fold)+'_learningCurv')
    #c2.SaveAs('/home/uzh/odahme/Master_Thesis/farm_selection/learningCurves/fold_'+str(fold)+'_learningCurv.pdf')
    #lc.plot_bokeh(title='fold_'+str(fold)+'_learningCurv')
    #show()
    #savefig('/home/uzh/odahme/Master_Thesis/farm_selection/learningCurves/fold_'+str(fold)+'_learningCurv.pdf')
    del(c1)
    #del(c2)
    del(roc)
    #del(lc)
    sig_prob = classifiers.predict_proba(testX)
    sig_probs.append(sig_prob)
    pred_indexs.append(test_index)
    fold+=1


ev_DataDic = {}
for clasN in clasNameList:
    pred_index = numpy.array([])
    pred = numpy.array([])
    for i in pred_indexs:
        pred_index = numpy.append(pred_index,i)
    for p in sig_probs:
        pred = numpy.append(pred,p[clasN][:,1])
    predDf = pandas.DataFrame(pred,pred_index,columns=['bdt'])
    ev_Data = pandas.concat([data, predDf], axis=1)
    ev_DataDic[clasN] = ev_Data


# In[ ]:


def rms(x) :
    q = np.square(x)
    s = np.sum(q)
    sol = sqrt(s/len(x))
    return sol

cor_params = ['B0_M', "B0_ThetaK", "B0_ThetaL"]
bins = 10

for clasN in clasNameList:
    bdt = ev_DataDic[clasN]['bdt']
    for p in cor_params:
        title = clasN+'_plot_bdt_vs_'+p
        c = TCanvas('c',title,1920,1080)
        plot_p = ev_DataDic[clasN][p]
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
        if (p == 'B0_M'):
            gr.GetXaxis().SetTitle(p)
        else:
            gr.GetXaxis().SetTitle('cos '+p)
        gr.GetYaxis().SetTitle('bdt')
        gr.SetMarkerStyle(20)
        gr.Draw('AP')
        fn = '/home/oliver/Desktop/curves_clas_test/cor_plots/'+title+'.pdf'
        c.SaveAs(fn)
        del c
bashCommand = "pdfunite /home/oliver/Desktop/curves_clas_test/cor_plots/*.pdf /home/oliver/Desktop/curves_clas_test/Corplots.pdf"
os.system(bashCommand)


# In[ ]:


for clasN in clasNameList:
    ev_DataDic[clasN].to_root('/home/oliver/Desktop/curves_clas_test/root_files/out_'+clasN+'.root')

#fold = 0
#for r in reports:
    #roc = r.roc()
    #lc = r.learning_curve(RocAuc(), predict_only_masked=False)

    ##plot_roc = roc.plot()
    ##plot_roc.show()
    ##plot_roc.savefig('/home/uzh/odahme/Master_Thesis/farm_selection/roc/fold_'+str(fold)+'_roc.pdf')

    ##plot_lc = lc.plot()
    ##plot_lc.show()
    ##plot_lc.savefig('/home/uzh/odahme/Master_Thesis/farm_selection/learningCurves/fold_'+str(fold)+'_learningCurv.pdf')

    ##c1 = TCanvas('c1','fold_'+str(fold)+'_roc',1920,1080)
    ##c2 = TCanvas('c2','fold_'+str(fold)+'_learningCurv',1920,1080)
    #c1 = roc.plot_tmva(new_plot=True,title='fold_'+str(fold)+'_roc',xlabel='false positive rate',xlim=(0.,1.),ylabel='true positive rate',ylim=(0.,1.))
    #c1.SaveAs('/home/uzh/odahme/Master_Thesis/farm_selection/roc/fold_'+str(fold)+'_roc.pdf')
    #c2 = lc.plot_tmva(new_plot=True,title='fold_'+str(fold)+'_learningCurv',xlabel='stage',ylabel='metric')
    #c2.SaveAs('/home/uzh/odahme/Master_Thesis/farm_selection/learningCurves/fold_'+str(fold)+'_learningCurv.pdf')


    ##c1 = TCanvas('c1','fold_'+str(fold)+'_roc',1920,1080)
    ##c2 = TCanvas('c2','fold_'+str(fold)+'_learningCurv',1920,1080)

    ##c1.cd()
    ##multiGr, leg = r.roc().plot_tmva()
    ##multiGr.GetXaxis().SetTitle('false positive rate')
    ##multiGr.GetYaxis().SetTitle('true positive rate')
    ##multiGr.SetTitle('ROC curves')
    ##multiGr.Draw()
    ##leg.Draw()
    ##c1.SaveAs('/home/uzh/odahme/Master_Thesis/farm_selection/roc/fold_'+str(fold)+'_roc.pdf')

    ##c2.cd()
    ##multiGr2, leg2 = r.learning_curve(RocAuc(), steps=1).plot_tmva()
    ##multiGr2.GetXaxis().SetTitle('stage')
    ##multiGr2.GetYaxis().SetTitle('metric')
    ##multiGr2.SetTitle('learning curves')
    ##multiGr2.Draw()
    ##leg2.Draw()
    ##c2.SaveAs('/home/uzh/odahme/Master_Thesis/farm_selection/learningCurves/fold_'+str(fold)+'_learningCurv.pdf')

    #fold+=1
    #del(c1)
    #del(c2)
    #del(roc)
    #del(lc)
    ##del(plot_roc)
    ##del(plot_lc)

bashCommand = "pdfunite /home/oliver/Desktop/curves_clas_test/lc/*.pdf learningCurves.pdf"
os.system(bashCommand)

bashCommand = "pdfunite /home/oliver/Desktop/curves_clas_test/roc/*.pdf ROC.pdf"
os.system(bashCommand)

# In[ ]:





# In[ ]:
