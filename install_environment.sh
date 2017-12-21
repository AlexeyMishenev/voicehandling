#!/bin/bash
sudo apt install python3-pip
sudo apt install gcc automake autoconf libtool bison swig python3-dev libpulse-dev libgnutls28-dev portaudio19-dev
sudo pip3 install setuptools gtts wave 
pip3 install colorama playsound, numpy

rm -rf sphinx-source
mkdir sphinx-source
cd sphinx-source


#Installing SphinxBase
git clone https://github.com/cmusphinx/sphinxbase.git
cd sphinxbase/

./autogen.sh
./configure.sh
./autogen.sh

make check
make clean
sudo make install

#check this path already in ld.so.cong
if ! grep -q "/usr/local/lib" "/etc/ld.so.conf" ; then
   sudo sh -c "echo '/usr/local/lib' >> /etc/ld.so.conf"
fi

sudo ldconfig
ldconfig -p | grep local


#Installing PocketSphinx
git clone https://github.com/cmusphinx/pocketsphinx.git
cd pocketsphinx/

./autogen.sh
./configure.sh
./autogen.sh

make check
make clean
sudo make install


#Installing SphinxTrain
git clone https://github.com/cmusphinx/sphinxtrain.git
cd sphinxtrain/

./autogen.sh
./configure.sh
./autogen.sh

make check
make clean
sudo make install
sudo make install