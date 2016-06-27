sudo apt-get install git

echo "mkdir GritRenaissance && cd GritRenaissance"
mkdir GritRenaissance && cd GritRenaissance

echo "git clone --recursive https://github.com/bitcoinsoftware/openMVG.git"
git clone --recursive https://github.com/bitcoinsoftware/openMVG.git

echo "git clone https://github.com/bitcoinsoftware/mve.git"
git clone https://github.com/bitcoinsoftware/mve.git

echo "git clone https://github.com/bitcoinsoftware/mvs-texturing.git"
git clone https://github.com/bitcoinsoftware/mvs-texturing.git

echo "git clone https://github.com/bitcoinsoftware/3Drecon"
git clone https://github.com/bitcoinsoftware/3Drecon

#echo "##### NOW CLIENT STUFF #####"
#echo "Downloading CloudCompare:\n git clone https://github.com/bitcoinsoftware/trunk.git"
#git clone https://github.com/bitcoinsoftware/trunk.git
#echo "cd trunk/plugins"
#cd trunk/plugins
#echo "git clone https://github.com/bitcoinsoftware/qPhotogrammetry"
#git clone https://github.com/bitcoinsoftware/qPhotogrammetry
#echo "cd .."
#cd ..
##TODO automate this stuff
#echo "cmake-gui" 
#echo cmake-gui
#cd ../..
#make -j$CORE_NUM

