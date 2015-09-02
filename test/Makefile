CXX = g++
CXXFLAGS = -g -Wall -fPIC
LD = g++
LDFLAGS = -g
SOFLAGS = -shared

DIRNAME = ${PWD}
# Base directory where the EvtGen libraries are
BASEDIR = ${DIRNAME}/../
# Base directory location of HepMC
HEPMCDIR = ${DIRNAME}/../../HepMC-2.06.05/build
# Base directory location of Photos
PHOTOSDIR = ${DIRNAME}/../../PHOTOS
# Base directory location of Tauola
TAUOLADIR = ${DIRNAME}/../../TAUOLA
# Base directory location of Pythia 8
PYTHIADIR = ${DIRNAME}/../../pythia8150

# PYTHIA8DATA is the location of the xmldoc Pythia 8 directory.
# Include files/libraries are usually located in the same main directory.
# PYTHIADIR = ${PYTHIA8DATA}/..

# Define the path to all required libraries
LIBS = -L${BASEDIR}/lib/archive -L${HEPMCDIR}/lib -L${PHOTOSDIR}/lib \
       -L${TAUOLADIR}/lib -L${PYTHIADIR}/lib/archive -lEvtGen -lgfortran \
       -lHepMC -lPhotosCxxInterface -lTauolaCxxInterface -lTauolaFortran \
       -lpythia8 -llhapdfdummy -lhepmcinterface

INCLUDEDIR = ${BASEDIR}

# ROOT
#ifndef ROOTSYS
  ROOTSYS = $(shell root-config --prefix)
  ifeq ($(ROOTSYS), )
    $(error running of root-config failed or reported null value)
  endif
#endif

ROOTCFLAGS    = $(shell ${ROOTSYS}/bin/root-config --cflags)
ROOTLIBS      = $(shell ${ROOTSYS}/bin/root-config --libs)
ROOTGLIBS     = $(shell ${ROOTSYS}/bin/root-config --glibs)
CXXFLAGS      += $(ROOTCFLAGS)
LIBS          += $(ROOTLIBS) 
NGLIBS         = $(ROOTGLIBS) 
NGLIBS        += -lMinuit
GLIBS          = $(filter-out -lNew, $(NGLIBS))

.SUFFIXES: .cc

# ================================================================================
default: evtgenlhc_test1 evt_dalitz example1

evtgenlhc_test1: evtgenlhc_test1.o
	$(LD) $(LDFLAGS) -o evtgenlhc_test1 evtgenlhc_test1.o $(LIBS)

evt_dalitz: evt_dalitz.o
	$(LD) $(LDFLAGS) -o evt_dalitz evt_dalitz.o $(LIBS)

example1: example1.o
	$(LD) $(LDFLAGS) -o example1 example1.o $(LIBS)

.cc.o:
	$(CXX) $(CXXFLAGS) -c -o $@ $< -I$(INCLUDEDIR)

clean:
	rm -f evtgenlhc_test1 evt_dalitz example1 *.o
