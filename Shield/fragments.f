C This BLOCK DATA defines the next conditions of the SHIELD-HIT output:
C 1.Energy grid EGRIDL(70) for all energy distributions.
C 2.Limits of intervals of stopping power (i.e.LET) STPL(21)
C   for scoring of dose in dependence on values of LET.   ! KI07#1
C 3.Set of ten fragments BOOKED(2,10), which the user can book
C   for simultaneous scoring of:
C      2.1. Track length estimation over all target zones.
C      2.2. Double differential yield from forward end of the target.
C      2.3. Dose distribution over all target zones.
C      2.4. Dose distribution according to intervals of LET.   ! KI07#1
C      2.5. Estimation of fluencies on intersections (for cylindrical targets only!).
C 
      BLOCK DATA GRIDOUT                      ! 2004c
      COMMON /EGRIDL/ EGRIDL(70),NG70               ! KI05NG
C Booked fragments  (Zi,Ai)x10, Zi>2 or Pi+/- = (-3.,-3.)
      COMMON /BOOKED/ BOOKED(2,10)
C
C------------------------------ KI07#1 ---------------------------------
      COMMON /STPLIMS/ STPL(21),ELIM1(21),ELIM2(21),E1234(4,20),DLE(20),
     *                          IFL1(20),IFL2(20),NSTP
      REAL*8 STPL,ELIM1,ELIM2,E1234,DLE
C        NSTP - number of specified STP-intervals (2<=NSTP<=20)
C        STPL(21) - limits of specified STP-intervals
C        ATTENTION: 1) STPL(1)<STPL(2)<...STPL(21)
C                   2) STPL(1)=0.0
C                   3) STPL(NSTP+1) must exceed maximal dE/dX(E) in the task!
C                   4) Be careful about increasing of dE/dX(E) for pions at high E
C------------------------------ end KI07#1 -----------------------------
C
      DATA EGRIDL /
     * .000E+00, .215E-06, .464E-06, .100E-05, .215E-05,
     * .464E-05, .100E-04, .215E-04, .464E-04, .100E-03, 
     * .215E-03, .464E-03, .100E-02, .215E-02, .464E-02, 
     * .100E-01, .215E-01, .464E-01, .100E+00, .215E+00, 
     * .464E+00, .100E+01, .147E+01, .215E+01, .316E+01, 
     * .464E+01, .562E+01, .681E+01, .825E+01, .100E+02, 
     * .121E+02, .145E+02, .178E+02, .215E+02, .261E+02, ! WARNING: 14.5 MeV
     * .316E+02, .383E+02, .464E+02, .511E+02, .562E+02, ! instead of 14.7 !
     * .619E+02, .681E+02, .750E+02, .825E+02, .909E+02, 
     * .100E+03, .110E+03, .121E+03, .133E+03, .147E+03, 
     * .162E+03, .178E+03, .196E+03, .215E+03, .237E+03, 
     * .261E+03, .287E+03, .316E+03, .348E+03, .383E+03, 
     * .422E+03, .464E+03, .511E+03, .562E+03, .619E+03, 
     * .681E+03, .750E+03, .825E+03, .909E+03, .100E+04/
C
      DATA BOOKED /
C      (Zi,Ai), Zi>2.  Ai=1000 means all A
     *  3., 6.,
     *  4., 7.,
     *  4., 10.,
     *  5., 10.,
     *  6., 10.,
     *  6., 11.,
     *  7., 1000.,
     *  8., 1000.,
     * -3., -3.,      ! Charged pions
     * -2., -2./      ! Secondary protons
C
C------------------------------ KI07#1 ---------------------------------
c      DATA NSTP /20/
c      DATA STPL /   ! an example of detailed step in LET
c     *     0.0,    5.0,   10.0,   20.0,   30.0,
c     *    40.0,   50.0,   60.0,   80.0,  100.0,
c     *   120.0,  150.0,  200.0,  250.0,  350.0,
c     *   500.0,  700.0, 1000.0, 2000.0, 4000.0,
c     *  8000.0/
C
*      DATA NSTP /7/
*      DATA STPL /    ! an example of crude step in LET
*     *    0.0, 5.0, 20.0, 50.0, 200.0, 600.0, 1000.0, 2000.0, 13*0.0/
C
      DATA NSTP /13/
      DATA STPL /   ! an example of the step in LET acceptable for both protons and C12
     *     0.0,    5.0,   20.0,   40.0,   60.0,
     *    80.0,  100.0,  150.0,  200.0,  400.0,
     *   600.0, 1000.0, 2000.0, 4000.0,  7*0.0/
C
      DATA ELIM1 /21*0.0/
      DATA ELIM2 /21*0.0/
      DATA E1234 /80*0.0/
      DATA DLE /20*0.0/
      DATA IFL1 /20*0/
      DATA IFL2 /20*0/
C------------------------------ end KI07#1 -----------------------------
C
      END
