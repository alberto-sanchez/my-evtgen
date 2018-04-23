#!/bin/bash

# This script installs EvtGen with all external dependencies. The variable VERSION specifies the
# tag of EvtGen you want to use. The list of available tags can be found by either going to the url
# http://evtgen.hepforge.org/git?p=evtgen.git;a=tags
# or issuing the command (without the need to clone the git repository)
# git ls-remote --tags http://evtgen.hepforge.org/git/evtgen.git | cut -d '/' -f3
# Note that some earlier EvtGen versions will not be compatible with all external dependency
# versions given below, owing to C++ interface differences; see the specific tagged version of
# the EvtGen/README file for guidance.
# To obtain this script, use
# wget -O setupEvtGen.sh "http://evtgen.hepforge.org/git?p=evtgen.git;a=blob_plain;f=setupEvtGen.sh;hb=HEAD"

# Version or tag number. No extra spaces on this line!
VERSION=R01-07-00
# Pythia version number with no decimal points, e.g. 8230 corresponds to version 8.230. This
# follows the naming convention of Pythia install tar files. Again, no extra spaces allowed
PYTHIAVER=8230
PYTHIAPKG="pythia"$PYTHIAVER
PYTHIATAR=$PYTHIAPKG".tgz"
echo Pythia version set to $PYTHIAVER, package tar name $PYTHIATAR

mkdir -p EvtGen
cd EvtGen

INSTALL_BASE=`pwd`

echo Will setup EvtGen $VERSION in $INSTALL_BASE

echo Downloading EvtGen from GIT
git clone -b $VERSION http://evtgen.hepforge.org/git/evtgen.git
# Replace the above line with the following one for the "head" version
#git clone http://evtgen.hepforge.org/git/evtgen.git

osArch=`uname`

echo Downloading external dependencies
mkdir -p external
cd external

# Recommended versions of the external packages. HepMC is mandatory. 
# Later versions should be OK as well, assuming their C++ interfaces do not change
curl -O http://lcgapp.cern.ch/project/simu/HepMC/download/HepMC-2.06.09.tar.gz
curl -O http://home.thep.lu.se/~torbjorn/pythia8/$PYTHIATAR
curl -O http://photospp.web.cern.ch/photospp/resources/PHOTOS.3.61/PHOTOS.3.61.tar.gz
curl -O http://tauolapp.web.cern.ch/tauolapp/resources/TAUOLA.1.1.6c/TAUOLA.1.1.6c.tar.gz

echo Extracting external dependencies
tar -xzf HepMC-2.06.09.tar.gz 
tar -xzf $PYTHIATAR
tar -xzf PHOTOS.3.61.tar.gz
tar -xzf TAUOLA.1.1.6c.tar.gz

# Patch TAUOLA and PHOTOS on Darwin (Mac)
if [ "$osArch" == "Darwin" ]
then
  patch -p0 < $INSTALL_BASE/evtgen/platform/tauola_Darwin.patch
  patch -p0 < $INSTALL_BASE/evtgen/platform/photos_Darwin.patch
fi

echo Installing HepMC in $INSTALL_BASE/external/HepMC
mkdir -p HepMC
cd HepMC
cmake -DCMAKE_INSTALL_PREFIX=$INSTALL_BASE/external/HepMC $INSTALL_BASE/external/HepMC-2.06.09 -Dmomentum:STRING=GEV -Dlength:STRING=MM
make
make install

echo Installing pythia8 in $INSTALL_BASE/external/$PYTHIAPKG
cd ../$PYTHIAPKG
if [ "$PYTHIAVER" -lt "8200" ]
then
  ./configure --with-hepmc=$INSTALL_BASE/external/HepMC --with-hepmcversion=2.06.09 --enable-shared
else
  ./configure --with-hepmc2=$INSTALL_BASE/external/HepMC --enable-shared
fi
make

echo Installing PHOTOS in $INSTALL_BASE/external/PHOTOS
cd ../PHOTOS
./configure --with-hepmc=$INSTALL_BASE/external/HepMC
make

echo Installing TAUOLA in $INSTALL_BASE/external/TAUOLA
cd ../TAUOLA
./configure --with-hepmc=$INSTALL_BASE/external/HepMC
make

echo Building EvtGen
cd $INSTALL_BASE/evtgen
./configure --hepmcdir=$INSTALL_BASE/external/HepMC --photosdir=$INSTALL_BASE/external/PHOTOS --pythiadir=$INSTALL_BASE/external/$PYTHIAPKG --tauoladir=$INSTALL_BASE/external/TAUOLA
make

echo Setup done.
echo To complete, add the following command to your .bashrc file or run it in your terminal before running any programs that use the EvtGen library:
echo LD_LIBRARY_PATH=$INSTALL_BASE/external/HepMC/lib:$INSTALL_BASE/external/$PYTHIAPKG/lib:$INSTALL_BASE/external/PHOTOS/lib:$INSTALL_BASE/external/TAUOLA/lib:$INSTALL_BASE/evtgen/lib:\$LD_LIBRARY_PATH
echo Also set the Pythia8 data path:
if [ "$PYTHIAVER" -lt "8200" ]
then
  echo PYTHIA8DATA=$INSTALL_BASE/external/$PYTHIAPKG/xmldoc
else
  echo PYTHIA8DATA=$INSTALL_BASE/external/$PYTHIAPKG/share/Pythia8/xmldoc
fi
