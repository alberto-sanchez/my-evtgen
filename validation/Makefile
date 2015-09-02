# Base directory where the EvtGen libraries are
BASEDIR = ../

# Read in the config.mk file in the base directory to extract where
# the external libraries are as well as setting other compiler flags/variables
include ${BASEDIR}/config.mk
include extraConfig.mk

# Need to first add EvtGen libraries, then HepMC, then Photos, Tauola and Pythia,
# since Photos depends on HepMC etc..

GENLIBS = -L${BASEDIR}/lib/archive -L${HEPMCLIBDIR} -L${PHOTOSLIBDIR} \
	-L${TAUOLALIBDIR} -L${PYTHIALIBDIR} -lEvtGen -lgfortran \
	${HEPMCLIBLIST} ${PHOTOSLIBLIST} ${TAUOLALIBLIST} ${PYTHIALIBLIST}

INCLUDEDIR = ${BASEDIR}

CXXFLAGS      += $(ROOTCFLAGS)
LIBS           = $(ROOTLIBS)
NGLIBS         = $(ROOTGLIBS)
NGLIBS        += -lMinuit
GLIBS          = $(filter-out -lNew, $(NGLIBS))

.SUFFIXES: .cc

# ================================================================================
default: genExampleRootFiles compareRootFiles testCPVDecays

genExampleRootFiles: genExampleRootFiles.o
	$(CXX) $(CXXFLAGS) -o genExampleRootFiles genExampleRootFiles.o $(GENLIBS) $(LIBS)

compareRootFiles: compareRootFiles.o
	$(CXX) $(CXXFLAGS) -o compareRootFiles compareRootFiles.o $(LIBS)

testCPVDecays: testCPVDecays.o
	$(CXX) $(CXXFLAGS) -o testCPVDecays testCPVDecays.o $(GENLIBS) $(LIBS)

.cc.o:
	$(CXX) $(CXXFLAGS) -c -o $@ $< -I$(INCLUDEDIR) -I$(HEPMCINCDIR)

clean:
	rm -f genExampleRootFiles compareRootFiles testCPVDecays *.o
