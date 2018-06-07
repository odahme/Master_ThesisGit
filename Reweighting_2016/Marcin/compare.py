from ROOT import *
import sys

def main(argv):


    gROOT.ProcessLine(".L lhcbStyle.C")

    c1=TCanvas("c1", "c1", 1920,1080)


    fDATA= TFile("/home/oliver/Master_Thesis/storage/data_reduced/Splot/KstarJpsi_2016_Splot.root")
    tDATA = fDATA.Get("data")

    tMC= TChain()
    tMC.Add("/home/oliver/Master_Thesis/storage/data_reduced/MC/B2KstarJpsi_MC_2016_MagDown_Pythia8_Sim09b_Filtered_11144001.root/Reduced")
    tMC.Add("/home/oliver/Master_Thesis/storage/data_reduced/MC/B2KstarJpsi_MC_2016_MagUp_Pythia8_Sim09b_Filtered_11144001.root/Reduced")


    #names = ['costhetak', 'costhetal', 'phi' ]#, 'J_psi_M' ]
    #ranges= ["(100,-1,1)", "(100,-1, 1)", "(100,-3.14, 3.14)"]#, "(100,3037,3157.)" ]

    names_data = ['DATAMC_weight_1'       , 'B0_ENDVERTEX_CHI2' , 'B0_PT', 'B0_P', 'B0_DiraCos' ]
    names_MC   = ['DATAMC_weight_1'       , 'B0_ENDVERTEX_CHI2' , 'B0_PT', 'B0_P', 'B0_DiraCos'  ]
    ranges     = ['(100,-1., 1.)' ,  '(60,0,30)'        ,'(100,0,35000)' , '(100,0,500000)', '(100,0.99998, 1.)']

    names_data += ['B0_IP_OWNPV'  , 'B0_IPCHI2_OWNPV' , 'K_PT'    , 'Pi_PT',            'K_IP_OWNPV',  'Pi_IP_OWNPV']
    names_MC   += ['B0_IP_OWNPV'  , 'B0_IPCHI2_OWNPV' , 'K_PT'    , 'Pi_PT',            'K_IP_OWNPV',  'Pi_IP_OWNPV']
    ranges     += ['(100,0., .1)' , '(100,0., 16.)',   '(100,0,10000)', '(100,0,10000)','(100,0., 5)' ,'(100,0., 5)' ]

    names_data += [ 'mu_minus_PT'    , 'mu_plus_PT',   'mu_minus_IP_OWNPV',  'mu_plus_IP_OWNPV']
    names_MC   += ['mu_minus_PT'    , 'mu_plus_PT',   'mu_minus_IP_OWNPV',  'mu_plus_IP_OWNPV']
    ranges     += [  '(100,0,10000)', '(100,0,10000)','(100,0., 5)' ,'(100,0., 5)' ]

#    names_data += ['B0_relinfo_MU_SLL_ISO_1', 'B0_relinfo_MU_SLL_ISO_2' ]
#    names_MC   += ['B0_relinfo_MU_SLL_ISO_1', 'B0_relinfo_MU_SLL_ISO_2' ]
#    ranges     += ['(100,0,15)', '(100,0,15)']

    names_data += ['mu_plus_PIDmu'       , 'mu_minus_PIDmu'    , 'K_PIDK'       , 'Pi_PIDK'    ]
    names_MC   += ['mu_plus_PIDmu_corr',  'mu_minus_PIDmu_corr', 'K_PIDK_corr'  , 'Pi_PIDK_corr'  ]
    ranges     += ['(100,-3,16)',         '(100,-3,16)'        , '(100,-3,100)' , '(100,-130,20)' ]



    cut_MC= "B0_M>5170 && B0_M<5350 &&  Kstar_M>795.9 && Kstar_M < 995.9 && ( B0_BKGCAT==0 || B0_BKGCAT==50 ) "
    cut_data=''

    fiducial= '( J_psi_M>3037 && J_psi_M <3157. && mu_minus_PT>800 && mu_plus_PT>800 )'


    draw_leg=True


    for nameD ,nameMC, range in zip(names_data, names_MC, ranges):

        tDATA.Draw(nameD+">>histOLD"+range , 'sigB0_sw*'+fiducial  )
        tMC.Draw(nameMC+">>histNEW"+range, "("+fiducial+"&&"+cut_MC +")*DATAMC_weight_1")
        tMC.Draw(nameMC+">>histNEW2"+range, "("+fiducial+"&&"+cut_MC +")")

        histOLD=gROOT.FindObject("histOLD")
        histNEW=gROOT.FindObject("histNEW")
        histNEW2=gROOT.FindObject("histNEW2")

        histOLD.SetLineColor(kMagenta-4)
        histOLD.SetFillColor(0)
        histOLD.SetLineWidth(2)


        histNEW.SetLineColor(kCyan-4)
        histNEW.SetFillColor(0)
        histNEW.SetLineWidth(2)

        histNEW2.SetLineColor(kRed-4)
        histNEW2.SetFillColor(0)
        histNEW2.SetLineWidth(2)


        histOLD.GetXaxis().SetTitle(nameD)
        histNEW.GetXaxis().SetTitle(nameD)
        histNEW2.GetXaxis().SetTitle(nameD)

        '''
        MAX= histOLD.GetMaximum()
        if(MAX< histNEW.GetMaximum() ):
            MAX=histNEW.GetMaximum()
        histOLD.SetMaximum(1.3*MAX)
        histNEW.SetMaximum(1.3*MAX)
        '''

        histOLD.SetMinimum(0.)
        histNEW.SetMinimum(0.)
        histNEW2.SetMinimum(0.)

        histOLD.SetMarkerColor(kMagenta-4)

        histOLD.DrawNormalized("B");
        histNEW.DrawNormalized("SAME hist");
        histNEW2.DrawNormalized("SAME hist");


        if(draw_leg):
            if nameD == 'mu_plus_PIDmu' or nameD == 'mu_minus_PIDmu':
                leg=TLegend(0.25, 0.6 ,0.4 ,0.8)
            else:
                leg=TLegend(0.55, 0.6, .7, .8)
            leg.AddEntry(histOLD, "Data" , "l")
            leg.AddEntry(histNEW, "weighted MC" , "f")
            leg.AddEntry(histNEW2, "original MC", "f")

            leg.Draw()
            #draw_leg=False
        c1.SaveAs(nameD+".pdf")


if __name__=="__main__":
    sys.exit(main(sys.argv))
