from random import randint
import InitShield as insh

#LineTitleLength=20
#DataLength=12
#CommentLength=70
#LineSize=LineTitleLength+DataLength+CommentLength

def RandSeedGen(strPath, numSes):
	maxSessions = 8
	fileRand = open(strPath, 'r+')
	work = randint(1e7,99999999)

	for line in fileRand:
		if abs(work - int(line)) < maxSessions:
			work = randint(1e7,99999999)
			fileRand.seek(0)
	fileRand.write(str(work)+'\n')
	fileRand.close()
	return [work + i for i in range(numSes)]

def for023make (lstDir):

#Type of particles
	strWork = "JPART0  FORMAT(I12):           2              ! Type of incident particle type JPART\n"

#Energy
	strWork += "TMAX0 FORMAT(F12.3):{: 12.1f}{: 12.1f}  ! Incident energy (MeV) and Gaussian energy scatter\n".format(insh.fMaxEnergy, insh.fDeltaEnergy)

#Profile
	strWork += "Beam FORMAT(2E12.5):{: 12.1f}{: 12.1f}  ! Gaussian beam profile (SigmaX,SigmaY) in cm\n".format(insh.fSigmaX, insh.fSigmaY)

#NSTAT
	strWork += "NSTAT  FORMAT(2I12):{:12d}{:12d}  ! Statistics NSTAT and step of saving of results\n".format(insh.nStatistics, insh.nStepofSaving)

#Neutrons cutoff
	strWork += "OLN   FORMAT(E12.4):         0.0              ! Cutoff for neutron transport (MeV)\n"
#Writefile
	strWork += "writefile Frmt(A12):yyyyyynyyyyy              ! Flags for output (yes,no)\n"
#Switchers
	strWork += "MAKELN        (I12):           0              ! Zero always\n"
	strWork += "     Parameters for SWITCH ON/OFF nucl.reactions, straggling and mult.scatt\n"
	strWork += "DELE    FORMAT(I12):        0.05              ! Delta E (relative share ~0.1); keep 0.05 always\n"
	strWork += "STRAGGLING (YES,NO):YES                       ! Simulation of straggling (YES,NO) in capitals\n"
	strWork += "MULTIPLE SCATTERING (YES,NO):YES              ! Simulation of Coulomb scattering (YES,NO) in capitals\n"
	strWork += "ITYPST  FORMAT(I12):           1              ! Type of straggl: 0-Gaussian, 1-Vavilov-Landau\n"
	strWork += "ITYPMS  FORMAT(I12):           1              ! Type of mlt.sct: 0-Gaussian, 1-Moliere\n"
	strWork += "INUCRE  FORMAT(I12):           1              ! Nuclear reaction switcher: 1-ON, 0-OFF\n"
	strWork += "     Incident heavy ion (is used if JPART0.eq.25 only)\n"
	strWork += "APROJ,FORMAT(F12.3):         4.0              ! A of nucleus-projectile\n"
	strWork += "ZPROJ,FORMAT(F12.3):         2.0              ! Z of nucleus-projectile\n"
	strWork += "<------- 20X ------><-- DATA --><----------^----------------- Comments !---------------------------->\n"
#RNG
	nRandSeed = RandSeedGen("Out\Randomness.txt", len(lstDir))
#Writning in files
	for i, f in enumerate([open(dir + "\\for023.dat", 'w') for dir in lstDir]):
#Title
		strOut = 10*' ' + "Input file FOR023.DAT for the SHIELD Transport Code (FORMATTED!)\n"
		strOut += "IXFIRS FORMAT(2I12):{:12d}           0  ! Initial state of random number generator (seed)\n"
		f.write(strOut.format(nRandSeed[i]))
		f.write(strWork)
		f.close()

