      REAL FUNCTION cpdgamma(x)
      COMMON/PAWPAR/PAR(6)

      vector b0b0b(1)

      if ( b0b0b(1).eq.0) b0b0b(1)=1.0

C par1 is a norm
C    2 is tau
C    3 is dgamma
C    4 is qoverp (mag)
C    5 is qoverp (phase)
C    6 is dm

      cpdgamma=par(1)*exp(-abs(x)/PAR(2))*(
          (1+par(4)*par(4))*cosh(par(3)*x/2)
          + 2.0*par(4)*cos(par(5))*sinh(par(3)*x/2)
          + b0b0b(1)*cos(par(6)*x)*(1-par(4)*par(4))
          - b0b0b(1)*2.0*sin(par(6)*x)*par(4)*sin(par(5)))


      END










