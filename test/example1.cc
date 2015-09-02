//
//  Sample test program for running EvtGen
//  

#include "EvtGen/EvtGen.hh"

#include "EvtGenBase/EvtParticle.hh"
#include "EvtGenBase/EvtParticleFactory.hh"
#include "EvtGenBase/EvtPatches.hh"
#include "EvtGenBase/EvtPDL.hh"
#include "EvtGenBase/EvtRandom.hh"
#include "EvtGenBase/EvtReport.hh"
#include "EvtGenBase/EvtStdHep.hh"
#include "EvtGenBase/EvtStdlibRandomEngine.hh"

#include <iostream>
#include <string>


//Define random number fcn used by Jetset
extern "C" {
  extern float rlu_();
  extern float begran_(int *);
}

float rlu_(){
  return EvtRandom::Flat();
}
float begran_(int *){
  return EvtRandom::Flat();
}

int main(int argc, char** argv) {

  EvtStdHep evtstdhep;
  EvtParticle* parent(0);

  EvtStdlibRandomEngine eng;
  EvtRandom::setRandomEngine((EvtRandomEngine*)&eng);
   //Initialize the generator - read in the decay table and particle properties
  EvtGen myGenerator("../DECAY.DEC","../evt.pdl", (EvtRandomEngine*)&eng);
  //If I wanted a user decay file, I would read it in now.
  //myGenerator.readUDecay(``../user.dec'');

  static EvtId UPS4 = EvtPDL::getId(std::string("Upsilon(4S)"));

  int nEvents(10000);

  // Loop to create nEvents, starting from an Upsilon(4S)
  int i;
  for (i = 0; i < nEvents; i++) {

    std::cout<<"Event number "<<i<<std::endl;

    // Set up the parent particle
    EvtVector4R pInit(EvtPDL::getMass(UPS4), 0.0, 0.0, 0.0);
    parent = EvtParticleFactory::particleFactory(UPS4, pInit);
    parent->setVectorSpinDensity();      

    // Generate the event
    myGenerator.generateDecay(parent);
    
    // Write out the results
    evtstdhep.init();
    parent->makeStdHep(evtstdhep);
    parent->deleteTree();

  }

  return 0;

}
