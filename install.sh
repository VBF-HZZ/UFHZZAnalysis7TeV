#!/bin/sh


scramv1 project CMSSW CMSSW_4_4_5
cd CMSSW_4_4_5/src
eval `scramv1 runtime -sh`
git clone https://github.com/VBF-HZZ/UFHZZAnalysis7TeV.git
cd UFHZZAnalysis7TeV
git checkout -b testProd origin/testProd
cd ../
tar xvzf UFHZZAnalysis7TeV/requiredPackages.tgz
scram b -j12

# aslo install submit scripts
#cd ../../
#git clone https://github.com/VBF-HZZ/SubmitArea_7TeV.git
#cd SubmitArea_7TeV
#git checkout -b testProd origin/testProd


