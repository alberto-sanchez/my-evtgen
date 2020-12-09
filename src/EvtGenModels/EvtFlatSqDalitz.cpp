
/***********************************************************************
* Copyright 1998-2020 CERN for the benefit of the EvtGen authors       *
*                                                                      *
* This file is part of EvtGen.                                         *
*                                                                      *
* EvtGen is free software: you can redistribute it and/or modify       *
* it under the terms of the GNU General Public License as published by *
* the Free Software Foundation, either version 3 of the License, or    *
* (at your option) any later version.                                  *
*                                                                      *
* EvtGen is distributed in the hope that it will be useful,            *
* but WITHOUT ANY WARRANTY; without even the implied warranty of       *
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        *
* GNU General Public License for more details.                         *
*                                                                      *
* You should have received a copy of the GNU General Public License    *
* along with EvtGen.  If not, see <https://www.gnu.org/licenses/>.     *
***********************************************************************/

#include "EvtGenModels/EvtFlatSqDalitz.hh"

#include "EvtGenBase/EvtDiracSpinor.hh"
#include "EvtGenBase/EvtGenKine.hh"
#include "EvtGenBase/EvtPDL.hh"
#include "EvtGenBase/EvtParticle.hh"
#include "EvtGenBase/EvtPatches.hh"
#include "EvtGenBase/EvtReport.hh"
#include "EvtGenBase/EvtTensor4C.hh"
#include "EvtGenBase/EvtVector4C.hh"

#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include <string>
using std::fstream;

EvtFlatSqDalitz::~EvtFlatSqDalitz()
{
}

std::string EvtFlatSqDalitz::getName()
{
    return "FLATSQDALITZ";
}

EvtDecayBase* EvtFlatSqDalitz::clone()
{
    return new EvtFlatSqDalitz;
}

void EvtFlatSqDalitz::initProbMax()
{
    setProbMax( 1. );
}

void EvtFlatSqDalitz::init()
{
    // check that there are 0 arguments
    checkNArg( 0 );

    //check there are 3 daughters
    checkNDaug( 3 );
}

void EvtFlatSqDalitz::decay( EvtParticle* p )
{
    p->initializePhaseSpace( getNDaug(), getDaugs() );

    double mB = p->mass();
    double m1 = p->getDaug( 0 )->mass();
    double m2 = p->getDaug( 1 )->mass();
    double m3 = p->getDaug( 2 )->mass();

    EvtVector4R p4_1 = p->getDaug( 0 )->getP4();
    EvtVector4R p4_2 = p->getDaug( 1 )->getP4();
    EvtVector4R p4_3 = p->getDaug( 2 )->getP4();

    EvtVector4R p4_12 = p4_1 + p4_2;
    EvtVector4R p4_13 = p4_1 + p4_3;
    // do not compute p4_23 to avoid breaking p4 conservation ???
    EvtVector4R p4_23 = p4_2 + p4_3;

    double m12 = p4_12.mass();
    double m13 = p4_13.mass();
    double m23 = p4_23.mass();

    double m12norm = 2 * ( ( m12 - ( m1 + m2 ) ) / ( mB - ( m1 + m2 + m3 ) ) ) -
                     1;
    double mPrime = acos( m12norm ) / EvtConst::pi;
    double thPrime = acos( ( m12 * m12 * ( m23 * m23 - m13 * m13 ) -
                             ( m2 * m2 - m1 * m1 ) * ( mB * mB - m3 * m3 ) ) /
                           ( sqrt( pow( m12 * m12 + m1 * m1 - m2 * m2, 2 ) -
                                   4 * m12 * m12 * m1 * m1 ) *
                             sqrt( pow( -m12 * m12 + mB * mB - m3 * m3, 2 ) -
                                   4 * m12 * m12 * m3 * m3 ) ) ) /
                     EvtConst::pi;

    double p3st = sqrt( pow( mB * mB - m3 * m3 - m12 * m12, 2 ) -
                        pow( 2 * m12 * m3, 2 ) ) /
                  ( 2 * m12 );
    double p1st = sqrt( pow( m2 * m2 - m1 * m1 - m12 * m12, 2 ) -
                        pow( 2 * m12 * m1, 2 ) ) /
                  ( 2 * m12 );

    double jacobian = 2 * pow( EvtConst::pi, 2 ) * sin( EvtConst::pi * mPrime ) *
                      sin( EvtConst::pi * thPrime ) * p1st * p3st * m12 *
                      ( mB - ( m1 + m2 + m3 ) );

    double prob = 1. / jacobian;    //pow(1./(jacobian),2);

    //  std::cout << mB << " " << mPrime << " " << thPrime << " " << prob << std::endl;

    setProb( prob );

    if ( prob < 1 )
        setProb( prob );
    else
        setProb( 1. );

    return;
}
