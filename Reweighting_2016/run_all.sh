#!/bin/bash

#./Reweight_apply.x /storage1/ntuples/lhcb/B2Kemu/preselected/B2KJpsimumu_MC_Run1.root
#./Reweight_apply.x /storage1/ntuples/lhcb/B2Kemu/preselected/B2Kee_MC_2012.root
#./Reweight_apply.x /storage1/ntuples/lhcb/B2Kemu/preselected/B2Kmue_MC_2012.root

for f in /storage1/ntuples/lhcb/B2Kemu/preselected/2015/*MC*.root
do
    echo $f
    ./Reweight_apply.x $f
done
