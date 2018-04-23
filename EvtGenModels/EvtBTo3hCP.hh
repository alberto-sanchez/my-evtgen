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
// Module: EvtGen/EvtBTo3hCP.hh
//
// Description:
//
// Modification history:
//
//    MK     August 26, 2016         Module created
//
//------------------------------------------------------------------------

#ifndef EVTBTO3HCP_HH
#define EVTBTO3HCP_HH

#include "EvtGenBase/EvtDecayAmp.hh"
#include "EvtGenBase/EvtVector4R.hh"

class EvtParticle;

/*
struct fcomplex {
  double re;
  double im;
};
*/

class EvtBTo3hCP {

public:

  EvtBTo3hCP();
  ~EvtBTo3hCP() {};

  void  EvtKpipi(double alpha, double beta, int iset,
        EvtVector4R& p_K_plus, EvtVector4R& p_pi_minus,
        EvtVector4R& p_gamma_1, EvtVector4R& p_gamma_2,
        double& Real_B0, double& Imag_B0, double& Real_B0bar, 
        double& Imag_B0bar);

  void  Evt3pi(double alpha, int iset,
        EvtVector4R& p_K_plus, EvtVector4R& p_pi_minus,
        EvtVector4R& p_gamma_1, EvtVector4R& p_gamma_2,
        double& Real_B0, double& Imag_B0, double& Real_B0bar, 
        double& Imag_B0bar);

  void  Evt3piMPP(double alpha, int iset,
        EvtVector4R& p_p1, EvtVector4R& p_p2,
        EvtVector4R& p_p3,
        double& Real_B0, double& Imag_B0, double& Real_B0bar, 
        double& Imag_B0bar);

  void Evt3piP00(double alpha, int iset, EvtVector4R &p_p1,
                 EvtVector4R &p_p1_gamma1, EvtVector4R &p_p1_gamma2,
                 EvtVector4R &p_p2_gamma1, EvtVector4R &p_p2_gamma2,
                 double &Real_B0, double &Imag_B0, double &Real_B0bar,
                 double &Imag_B0bar);

private:

  void setConstants(double balpha, double bbeta);
  int computeKpipi(EvtVector4R &p1, EvtVector4R &p2, EvtVector4R &p3,
                       double &real_B0, double &imag_B0, double &real_B0bar,
                       double &imag_B0bar, int set);
  int compute3pi(EvtVector4R &p1, EvtVector4R &p2, EvtVector4R &p3,
                       double &real_B0, double &imag_B0, double &real_B0bar,
                       double &imag_B0bar, int set);
  int compute3piMPP(EvtVector4R &p1, EvtVector4R &p2, EvtVector4R &p3,
                       double &real_B0, double &imag_B0, double &real_B0bar,
                       double &imag_B0bar, int set);
  int compute3piP00(EvtVector4R &p1, EvtVector4R &p2, EvtVector4R &p3,
                       double &real_B0, double &imag_B0, double &real_B0bar,
                       double &imag_B0bar, int set);

  // Modes are : 0 = Kpipi, 1 = 3pi, 2 = MPP, 3 = P00
  void firstStep(EvtVector4R &p1, EvtVector4R &p2, EvtVector4R &p3, int mode);
  void generateSqMasses_Kpipi(double &m12, double &m13, double &m23, double MB2,
                              double m1sq, double m2sq, double m3sq);
  void generateSqMasses_3pi(double &m12, double &m13, double &m23, double MB2,
                            double m1sq, double m2sq, double m3sq);
  void generateSqMasses_3piMPP(double &m12, double &m13, double &m23,
                               double MB2, double m1sq, double m2sq,
                               double m3sq);
  void generateSqMasses_3piP00(double &m12, double &m13, double &m23,
                               double MB2, double m1sq, double m2sq,
                               double m3sq);

  void rotation(EvtVector4R& p, int newRot);
  void gammaGamma(EvtVector4R &p, EvtVector4R &pgamma1,
                     EvtVector4R &pgamma2);
  EvtComplex BreitWigner(EvtVector4R &p1, EvtVector4R &p2, EvtVector4R &p3,
                         int &ierr, double Mass=0, double Width=0);
  EvtComplex EvtRBW(double s, double Am2, double Gam, double Am2Min);
  EvtComplex EvtCRhoF_W(double s);
  EvtComplex EvtcBW_KS(double s, double Am2, double Gam);
  EvtComplex EvtcBW_GS(double s, double Am2, double Gam);
  double d(double AmRho2);
  double k(double s);
  double Evtfs(double s, double AmRho2, double GamRho);
  double h(double s);
  double dh_ds(double s); 

  EvtComplex Mat_S1, Mat_S2, Mat_S3, Mat_S4, Mat_S5, Nat_S1, Nat_S2, Nat_S3,
      Nat_S4, Nat_S5, MatKstarp, MatKstar0, MatKrho, NatKstarp, NatKstar0,
      NatKrho;
  double alphaCP, betaCP, pi, MA2, MB2, MC2, one, eno, Mass_rho, Gam_rho, M_B, M_pip,
      M_pim, M_pi0, DeltaM, Gam_B, xd, M_Upsi, BetaBabar, ptcut, coscut, M_Kp,
      Mass_Kstarp, Mass_Kstar0, Gam_Kstarp, Gam_Kstar0;

  double rotMatrix[3][3];
  double factor_max;
};

#endif
