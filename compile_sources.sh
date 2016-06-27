echo " cd GritRenaissance"
cd GritRenaissance

echo "Install the following libs:"
echo "libpng-dev
libjpeg-dev
libtiff-dev
libxxf86vm1
libxxf86vm-dev
libxi-dev
libxrandr-dev
graphviz"
sudo apt-get install libpng-dev libjpeg-dev libtiff-dev libxxf86vm1 libxxf86vm-dev libxi-dev libxrandr-dev graphviz

echo "MAKE openMVG library"
echo "mkdir openMVG/openMVG_Build && cd openMVG/openMVG_Build"
mkdir openMVG/openMVG_Build && cd openMVG/openMVG_Build
echo "cmake -DCMAKE_BUILD_TYPE=RELEASE . ../src/"
cmake -DCMAKE_BUILD_TYPE=RELEASE . ../src/
echo "make"
CORE_NUM=8
make -j$CORE_NUM
echo "GO BACK TO ROOT FOLDER
cd ../.."
cd ../..

echo "cd mve && make"
cd mve && make -j8
echo "GO BACK TO ROOT FOLDER
cd .."
cd ..

echo "cd mvs-texturing && mkdir build && cd build"
cd mvs-texturing && mkdir build && cd build
echo "cmake .. -DRESEARCH=ON"
cmake .. -DRESEARCH=ON
echo "make"
make -j$CORE_NUM
echo "GO BACK TO ROOT FOLDER
cd ../.."
cd ../..

echo "
ln -s 3Drecon/reconstruction_cmd.py main_cmd.py
ln -s 3Drecon/reconstruction_daemon.py main_daemon.py
"
ln -s 3Drecon/reconstruction_cmd.py main_cmd.py
ln -s 3Drecon/reconstruction_daemon.py main_daemon.py


