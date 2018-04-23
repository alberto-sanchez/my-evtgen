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
// Module: EvtCBTo3piMPP.cc
//
// Description: Routine to decay B+/-->pi+ pi- pi+/-
//              and has CP violation.
//
// Modification history:
//
//    MK               September, 2016     Reimplementation to C++
//    RYD/Versille     May 6, 1997         Module created
//
//------------------------------------------------------------------------
//
#include "EvtGenBase/EvtPatches.hh"
#include <stdlib.h>
#include "EvtGenBase/EvtParticle.hh"
#include "EvtGenBase/EvtGenKine.hh"
#include "EvtGenBase/EvtPDL.hh"
#include "EvtGenBase/EvtReport.hh"
#include "EvtGenBase/EvtId.hh"
#include "EvtGenModels/EvtCBTo3piMPP.hh"
#include <string>

EvtCBTo3piMPP::~EvtCBTo3piMPP() {}

std::string EvtCBTo3piMPP::getName(){

  return "CB3PI-MPP";     

}


EvtDecayBase* EvtCBTo3piMPP::clone(){

  return new EvtCBTo3piMPP;

}

void EvtCBTo3piMPP::init(){

  // check that there are 1 argument
  checkNArg(1);
  checkNDaug(3);

  checkSpinParent(EvtSpinType::SCALAR);

  checkSpinDaughter(0,EvtSpinType::SCALAR);
  checkSpinDaughter(1,EvtSpinType::SCALAR);
  checkSpinDaughter(2,EvtSpinType::SCALAR);

}

void EvtCBTo3piMPP::initProbMax(){

  setProbMax(1.5);

}

void EvtCBTo3piMPP::decay( EvtParticle *p ){

  //added by Lange Jan4,2000
  static EvtId BM=EvtPDL::getId("B-");
  static EvtId BP=EvtPDL::getId("B+");

  EvtParticle *pi1,*pi2,*pi3;

  p->makeDaughters(getNDaug(),getDaugs());
  pi1=p->getDaug(0);
  pi2=p->getDaug(1);
  pi3=p->getDaug(2);

  EvtVector4R p4[3];
  double alpha = getArg(0);

  int iset;

  static int first=1;

  if (first==1) {
    iset=10000;
    first=0;
  }
  else{
    iset=0;
  }

  double realA,imgA,realbarA,imgbarA;

  generator.Evt3piMPP(alpha, iset, p4[0], p4[1], p4[2], 
                  realA, imgA, realbarA, imgbarA);

  pi1->init( getDaug(0), p4[0] );
  pi2->init( getDaug(1), p4[1] );
  pi3->init( getDaug(2), p4[2] );

  EvtComplex A(realA,imgA);
  EvtComplex Abar(realbarA, imgbarA);

   //amp is filled just to make sure the compiler will
   //do its job!! but one has to define amp differently
   // if one wants the B+ or the B- to decay to 3pi!
   // 


   EvtComplex  amp;
   if(p->getId()==BP)
     {
       amp = A;
     }
   if(p->getId()==BM)
     {
       amp = Abar;
     }  

   vertex(amp);

  return ;
}


