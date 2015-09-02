CXX = g++
CXXFLAGS = -g -Wall -fPIC
LD = g++
LDFLAGS = -g
SOFLAGS = -shared

DIRNAME = ${PWD}
# Base directory where the EvtGen libraries are
BASEDIR = ${DIRNAME}/../

# Specify the base location for the Pythia 8 libraries.
# PYTHIA8DATA is the location of the xmldoc Pythia 8 directory.
# Include files/libraries are usually located in the same main directory.
PYTHIADIR = ${PYTHIA8DATA}/..

# Base directory location of the Photos library
PHOTOSDIR = ${DIRNAME}/../../photos_215_5/share

# Define the path to all required libraries
LIBS = -L${BASEDIR}/lib/archive -L${PHOTOSDIR}/lib/archive -L${PYTHIADIR}/lib/archive \
	-lEvtGen -lphotos -lpythia8 -llhapdfdummy -lgfortran

# CERN configuration - need to find out where Pythia 8 libraries are installed...
#CERNLIBDIR = /afs/cern.ch/sw/lcg/external/cernlib/2006b/x86_64-slc5-gcc41-opt
#LIBS = -L${BASEDIR}/lib/archive -L${CERNLIBDIR}/lib \
#        -lEvtGen -lphotos202 -lpythia6205 -lgfortran

INCLUDEDIR = ${BASEDIR}

# ROOT
#ifndef ROOTSYS
  ROOTSYS = $(shell root-config --prefix)
  ifeq ($(ROOTSYS), )
    $(error running of root-config failed or reported null value)
  endif
#endif

# CERN configuration
#ROOTSYS = /afs/cern.ch/sw/lcg/external/root/5.21.04/slc4_amd64_gcc34/root

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
