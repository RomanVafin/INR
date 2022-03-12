import numpy as np
import InitShield as insh

Navog=6.022E-04
def for022make(strDirName):
	lstMedium=['Water', 'Air: 0.755N+0.245O', 'Copper', 'PMMA:C5-H8-O2']

	output=open(strDirName + 'for022.dat', 'w+')
	output.write('NUMMED={:2d}\n'.format(insh.nMedia))

	for iMed in range(insh.nMedia):
		strWork='           MEDIUM NO.{:3d} ( {!s} )\n'
		output.write(strWork.format(iMed+1,lstMedium[iMed]))
		strWork='ICRU_ID={:3d}\n'
		output.write(strWork.format(insh.lstIcruId[iMed]))
		if insh.lstMediaType[iMed]==1:
			strWork='MEDTYP=1\n'
			output.write(strWork)
			strWork='1 NUCLID={:3d}\n'
			output.write(strWork.format(insh.lstNuclId[iMed]))
		elif insh.lstMediaType[iMed]==2:
			if insh.lstMediaDensity[iMed]>0.05:
				strWork='MEDTYP=2 NELEM{:2d} RHO={: 5.2f}\n'
				output.write(strWork.format(len(insh.lstNumComponents[iMed]), insh.lstMediaDensity[iMed]))
			else:
				strWork='MEDTYP=2 NELEM{:2d} RHO={: 8.6f}\n'
				output.write(strWork.format(len(insh.lstNumComponents[iMed]), insh.lstMediaDensity[iMed]))
			for cnt in range(len(insh.lstNuclId[iMed])):
				strWork='{0:d} NUCLID={1:3d} DEL{0:d}={2:3.1f}                                    {3:5.1f}\n'
				output.write(strWork.format(cnt+1, insh.lstNuclId[iMed][cnt], insh.lstNumComponents[iMed][cnt], insh.lstAng[iMed][cnt]))
		elif insh.lstMediaType[iMed]==4:
			fWeight=np.sum(np.multiply(insh.lstNumComponents[iMed], insh.lstAtomicWeight[iMed]))
			if insh.lstMediaDensity[iMed]>0.05:
				strWork='MEDTYP=4 NELEM{:2d} RHO={: 5.2f}\n'
				output.write(strWork.format(len(insh.lstNumComponents[iMed]), insh.lstMediaDensity[iMed]))
			else:
				strWork='MEDTYP=4 NELEM{:2d} RHO={: 8.6f}\n'
				output.write(strWork.format(len(insh.lstNumComponents[iMed]), insh.lstMediaDensity[iMed]))
			for cnt in range(len(insh.lstNuclId[iMed])):
				fWork=insh.lstMediaDensity[iMed]*insh.lstNumComponents[iMed][cnt]/fWeight
				fCon=Navog*fWork
				fDens=insh.lstAtomicWeight[iMed][cnt]*fWork
				strWork='{0:d} NUCLID={1:3d} DEL{0:d}={2: 11.4E} RHO{0:d}={3: 11.4E}{4: 17.2f}\n'
				output.write(strWork.format(cnt+1, insh.lstNuclId[iMed][cnt], fCon, fDens, insh.lstAng[iMed][cnt]))

	output.close()