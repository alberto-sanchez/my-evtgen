CXX = g++
CXXFLAGS = -g -Wall -fPIC
LD = g++
LDFLAGS = -g
SOFLAGS = -shared

DIRNAME = ${PWD}
# Base directory where the EvtGen libraries are
BASEDIR = ${DIRNAME}/../
# Directory locations of the photos and pythia libraries
PHOTOSDIR = ${DIRNAME}/../../photos_215_5/share
PYTHIADIR = ${DIRNAME}/../../pythia6_420/share
LIBS = -L${BASEDIR}/lib/archive -L${PHOTOSDIR}/lib/archive -L${PYTHIADIR}/lib/archive \
	-lEvtGen -lphotos -lpythia6 -lpythia6_dummy -lgfortran
INCLUDEDIR = ${BASEDIR}

.SUFFIXES: .cc

# ================================================================================
default: evt_dalitz example1

evt_dalitz: evt_dalitz.o
	$(LD) $(LDFLAGS) -o evt_dalitz evt_dalitz.o $(LIBS)

example1: example1.o
	$(LD) $(LDFLAGS) -o example1 example1.o $(LIBS)

.cc.o:
	$(CXX) $(CXXFLAGS) -c -o $@ $< -I$(INCLUDEDIR)

clean:
	rm -f evt_dalitz example1 *.o
