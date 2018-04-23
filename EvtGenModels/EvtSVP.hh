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
// Module: EvtGen/EvtSVP.hh
//
// Description: Routine to implement radiative decay
//                   chi_c0 -> psi gamma
//                   chi_c0 -> psi ell ell
//
// Modification history:
//	AVL	Jul 6, 2012:	chi_c0 -> gamma psi  mode created
//	AVL	Oct 10, 2017: chi_c0 -> psi mu mu  mode created
//      AVL     Nov 9 2017:   models joined
//
//------------------------------------------------------------------------

#ifndef EvtSVP_HH
#define EvtSVP_HH

#include "EvtGenBase/EvtDecayAmp.hh"
#include <string>

class EvtParticle;
class EvtDecayBase;

class EvtSVP: public EvtDecayAmp  {

public:

  EvtSVP() {}
  virtual ~EvtSVP();

  std::string getName();
  EvtDecayBase* clone();

  void decay(EvtParticle *p);
  void init();

  virtual void initProbMax();

private:

  void decay_2body(EvtParticle *p);
  void decay_3body(EvtParticle *p);
  double delta; // form factor parameter

};

#endif

