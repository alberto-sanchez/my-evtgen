//--------------------------------------------------------------------------
//
// Environment:
//      This software is part of the EvtGen package developed jointly
//      for the BaBar and CLEO collaborations.  If you use all or part
//      of it, please give an appropriate acknowledgement.
//
// Copyright Information: See EvtGen/COPYRIGHT
//      Copyright (C) 1998      Caltech, UCSB
//
// Module: EvtGen/EvtVVP.hh
//
// Description: Routine to implement radiative decay
//                   chi_c1 -> psi gamma
//                   chi_c1 -> psi ell ell
//
//
// Modification history:
//
//    DJL/RYD     August 11, 1998         Module created
//	AVL	Oct 10, 2017: chi_c0 -> psi mu mu  mode created
//  AVL Nov 9 2017:   models joined
//
//------------------------------------------------------------------------

#ifndef EVTVVP_HH
#define EVTVVP_HH

#include "EvtGenBase/EvtDecayAmp.hh"

#include <string>

class EvtParticle;
class EvtDecayBase;

class EvtVVP: public EvtDecayAmp  {

public:

  EvtVVP() {}
  virtual ~EvtVVP();
  
  std::string getName();
  EvtDecayBase* clone();

  void initProbMax();
  void init();
  void decay(EvtParticle *p); 

private:
  void decay_2body(EvtParticle *p);
  void decay_3body(EvtParticle *p);
  double delta; // form factor parameter

};

#endif
