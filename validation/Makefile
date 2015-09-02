CXX = g++
CXXFLAGS = -g -Wall -fPIC
LD = g++
LDFLAGS = -g
SOFLAGS = -shared

DIRNAME = ${PWD}
# Base directory where the EvtGen libraries are
BASEDIR = ${DIRNAME}/../

# Need to first add EvtGen libraries, then HepMC, then Photos and Pythia,
# since Photos depends on HepMC etc..
# Set these environment variables if not previously defined
# HEPMCDIR = <Base directory location of HepMC lib/include>
# PHOTOSDIR = <Base directory location of Photos lib/include>
# TAUOLADIR = <Base directory location of Tauola lib/include>
# PYTHIADIR = <Base directory location of Pythia8 lib/include>

GENLIBS = -L${BASEDIR}/lib/archive -L${HEPMCDIR}/lib -L${PHOTOSDIR}/lib \
	-L${TAUOLADIR}/lib -L${PYTHIADIR}/lib/archive -lEvtGen -lgfortran \
	-lHepMC -lPhotosCxxInterface -lTauolaCxxInterface -lTauolaFortran \
	-lpythia8 -llhapdfdummy -lhepmcinterface

# CERN configuration - to be updated for new pythia, photos etc..
# CERNLIBDIR = /afs/cern.ch/sw/lcg/external/cernlib/2006b/x86_64-slc5-gcc41-opt
# LIBS = -L${BASEDIR}/lib/archive -L${CERNLIBDIR}/lib \
#        -lEvtGen -lphotos202 -lpythia6205 -lgfortran

INCLUDEDIR = ${BASEDIR}

# ROOT
ifndef ROOTSYS
  ROOTSYS = $(shell root-config --prefix)
  ifeq ($(ROOTSYS), )
    $(error running of root-config failed or reported null value)
  endif
endif

# CERN configuration
# ROOTSYS = /afs/cern.ch/sw/lcg/external/root/5.21.04/slc4_amd64_gcc34/root

ROOTCFLAGS    = $(shell ${ROOTSYS}/bin/root-config --cflags)
ROOTLIBS      = $(shell ${ROOTSYS}/bin/root-config --libs)
ROOTGLIBS     = $(shell ${ROOTSYS}/bin/root-config --glibs)
CXXFLAGS      += $(ROOTCFLAGS)
LIBS           = $(ROOTLIBS)
NGLIBS         = $(ROOTGLIBS)
NGLIBS        += -lMinuit
GLIBS          = $(filter-out -lNew, $(NGLIBS))

.SUFFIXES: .cc

# ================================================================================
default: genExampleRootFiles compareRootFiles testCPVDecays

genExampleRootFiles: genExampleRootFiles.o
	$(LD) $(LDFLAGS) -o genExampleRootFiles genExampleRootFiles.o $(GENLIBS) $(LIBS)

compareRootFiles: compareRootFiles.o
	$(LD) $(LDFLAGS) -o compareRootFiles compareRootFiles.o $(LIBS)

testCPVDecays: testCPVDecays.o
	$(LD) $(LDFLAGS) -o testCPVDecays testCPVDecays.o $(GENLIBS) $(LIBS)

.cc.o:
	$(CXX) $(CXXFLAGS) -c -o $@ $< -I$(INCLUDEDIR) -I$(HEPMCDIR)/include

clean:
	rm -f genExampleRootFiles compareRootFiles testCPVDecays *.o
