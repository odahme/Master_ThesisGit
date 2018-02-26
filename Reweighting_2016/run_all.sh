#!/bin/bash

#./Reweight_apply.x /storage1/ntuples/lhcb/B2Kemu/preselected/B2KJpsimumu_MC_Run1.root
#./Reweight_apply.x /storage1/ntuples/lhcb/B2Kemu/preselected/B2Kee_MC_2012.root
#./Reweight_apply.x /storage1/ntuples/lhcb/B2Kemu/preselected/B2Kmue_MC_2012.root

for f in /home/oliver/Master_Thesis/storage/data_reduced/MC/B2KstarJpsi_MC_2016.root
do
    echo $f
    ./Reweight_apply.x $f
done
