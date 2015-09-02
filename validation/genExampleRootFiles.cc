// Program to create ROOT files for EvtGen validation plots.
// This looks at the 1st generation daughters and stores 4-momenta
// info into a ROOT file for further analysis.
// Useful for Pythia, Photos and Tauola decay tests.

#include "EvtGen/EvtGen.hh"

#include "EvtGenBase/EvtParticle.hh"
#include "EvtGenBase/EvtParticleFactory.hh"
#include "EvtGenBase/EvtPatches.hh"
#include "EvtGenBase/EvtPDL.hh"
#include "EvtGenBase/EvtRandom.hh"
#include "EvtGenBase/EvtStdlibRandomEngine.hh"
//#include "EvtGenBase/EvtHepMCEvent.hh"
#include "HepMC/GenEvent.h"

#include "TFile.h"
#include "TTree.h"

#include <iostream>
#include <string>

using std::cout;
using std::endl;
using std::string;

int main(int argc, char** argv) {

  string decayFileName("../DECAY_2010.DEC");
  if (argc > 1) {decayFileName = argv[1];}
  cout<<"Decay file name is "<<decayFileName<<endl;

  string rootFileName("evtgenTest.root");
  if (argc > 2) {rootFileName = argv[2];}
  cout<<"Root file name is "<<rootFileName<<endl;

  string parentName("Upsilon(4S)");
  if (argc > 3) {parentName = argv[3];}
  cout<<"Parent name is "<<parentName<<endl;

  int nEvents(10);
  if (argc > 4) {nEvents = atoi(argv[4]);}

  cout<<"Number of events is "<<nEvents<<endl;

  TFile* theFile = new TFile(rootFileName.c_str(), "recreate");
  TTree* theTree = new TTree("Data", "Data");
  TTree* nDaugTree = new TTree("nDaugTree", "nDaugTree");

  theTree->SetDirectory(theFile);
  nDaugTree->SetDirectory(theFile);

  int event(0), nDaug(0), daugId(0);
  double E(0.0), p(0.0), px(0.0), py(0.0), pz(0.0);
  double t(0.0), x(0.0), y(0.0), z(0.0);
  double mass(0.0), lifetime(0.0);

  theTree->Branch("event", &event, "event/I");
  theTree->Branch("nDaug", &nDaug, "nDaug/I");
  theTree->Branch("id", &daugId, "id/I");
  theTree->Branch("E", &E, "E/D");
  theTree->Branch("p", &p, "p/D");
  theTree->Branch("px", &px, "px/D");
  theTree->Branch("py", &py, "py/D");
  theTree->Branch("pz", &pz, "pz/D");
  theTree->Branch("t", &t, "t/D");
  theTree->Branch("x", &x, "x/D");
  theTree->Branch("y", &y, "x/D");
  theTree->Branch("z", &z, "x/D");
  theTree->Branch("mass", &mass, "mass/D");
  theTree->Branch("lifetime", &lifetime, "lifetime/D");

  nDaugTree->Branch("event", &event, "event/I");
  nDaugTree->Branch("nDaug", &nDaug, "nDaug/I");

  EvtParticle* baseParticle(0);
  EvtParticle* theParent(0);

  EvtRandomEngine* myRandomEngine = new EvtStdlibRandomEngine();

  // Initialize the generator - read in the decay table and particle properties.
  // For our validation purposes, we just want to read in one decay file and create
  // plots from that.

  EvtGen myGenerator(decayFileName.c_str(), "../evt.pdl", myRandomEngine);

  // If I wanted a user decay file, I would read it in now, e.g:
  // myGenerator.readUDecay(otherFileName);

  EvtId theId = EvtPDL::getId(parentName);
  if (theId.getId() == -1 && theId.getAlias() == -1) {
    cout<<"Error. Could not find valid EvtId for "<<parentName<<endl;
    return -1;
  }

  static EvtId stringId = EvtPDL::getId(std::string("string"));
  // Loop to create nEvents

  int i;
  for (i = 0; i < nEvents; i++) {

    if (i%1000 == 0) {cout<<"Event number = "<<i+1<<" out of "<<nEvents<<std::endl;}

    // Set up the parent particle
    EvtVector4R pInit(EvtPDL::getMass(theId), 0.0, 0.0, 0.0);

    baseParticle = EvtParticleFactory::particleFactory(theId, pInit);
    if (baseParticle->getSpinStates() == 3) {baseParticle->setVectorSpinDensity();}

    // Generate the event
    myGenerator.generateDecay(baseParticle);

    // Alternative way to generate decays and print out information:
    // int PDGId = EvtPDL::getStdHep(theId);
    // EvtVector4R origin(0.0, 0.0, 0.0, 0.0);
    // EvtHepMCEvent* theEvent = myGenerator.generateDecay(PDGId, pInit, origin);
    // HepMC::GenEvent* hepMCEvent = theEvent->getEvent();
    // hepMCEvent->print();
    // Extract other info from the HepMC event. Then delete it:
    // delete theEvent;

    // Now get the particle decay information, looping through daughter tracks (1st generation only)

    // Find out if the first daughter is a string.
    // If so, set this as the new parent particle.

    EvtId daugEvtId = baseParticle->getDaug(0)->getId();

    if (daugEvtId == stringId) {
      theParent = baseParticle->getDaug(0);
    } else {
      theParent = baseParticle;
    }

    nDaug = theParent->getNDaug();
    int iDaug(0);

    nDaugTree->Fill();

    //theParent->printTree();

    // Loop over the daughter tracks
    for (iDaug = 0; iDaug < nDaug; iDaug++) {

      EvtParticle* daug = theParent->getDaug(iDaug);
	
      if (daug != 0) {

	EvtVector4R p4Lab = daug->getP4Lab();	
	EvtVector4R pos4 = daug->get4Pos();
	
	// PDG id
	daugId = EvtPDL::getStdHep(daug->getId());
	
	// 4-momenta
	E = p4Lab.get(0);
	px = p4Lab.get(1);
	py = p4Lab.get(2);
	pz = p4Lab.get(3);
	p = sqrt(px*px + py*py + pz*pz);
	
	// 4-position
	t = pos4.get(0);
	x = pos4.get(1);
	y = pos4.get(2);
	z = pos4.get(3);
	
	mass = daug->mass();
	lifetime = daug->getLifetime();
	
	theTree->Fill();
	
      } // Daughter exists
      
    } // Number of daughters

    // Cleanup    
    baseParticle->deleteTree();

  }


  // Write out the TTree information to the ROOT file

  theFile->cd();
  theTree->Write();
  nDaugTree->Write();

  theFile->Close();

  cout<<"Done."<<endl;

  return 0;

}
