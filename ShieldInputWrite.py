'''
Writing into files module

'''

import numpy as np
from os import listdir
from shutil import copy

import InitShield as insh
import ShieldGeometry as shgeo
from FOR23Make import for023make
from FOR22Make import for022make


def headerWrite(file1, file2, file3, lstBody, nZones):

	nTargetBlocks = insh.nBlocks + insh.nFrontBlocks + insh.nBackBlocks
	if insh.bIsCuboid:
		xBlocks = [lstBody[0].geompos[0] + (i+0.5) * lstBody[0].geompos[3] for i in range(insh.nXBlocks)]
		if insh.nFrontBlocks:
			zBlocks = [lstBody[1].geompos[2] + (i+0.5) * lstBody[1].geompos[5] for i in range(insh.nFrontBlocks)]
		else:
			zBlocks = []
		zBlocks += [lstBody[0].geompos[2] + (i+0.5) * lstBody[0].geompos[5] for i in range(insh.nZBlocks)]
		lstWork = [str(x)+'\t' for x in xBlocks]
		lstWork.append('\n') 
		lstWork = lstWork + [str(x)+'\t' for x in zBlocks]
		lstWork.append('\n')
		if insh.alphaDeg:
			strWork = '    0    6             Cuboid H2O,{: 4d} zones in target (DxL{: 5.1f}x{:4.1f}cm) and {: 4d} zones overall; rotated by{: 5.2f}deg\n'
			strWork = strWork.format(nTargetBlocks, insh.xTargetWidth, insh.zTargetLength, nZones, insh.alphaDeg)
		else:
			strWork = '    0    6             Cuboid H2O,{: 4d} zones in target (DxL{: 5.1f}x{:4.1f}cm) and {: 4d} zones overall\n'
			strWork = strWork.format(nTargetBlocks, insh.xTargetWidth, insh.zTargetLength, nZones)
	else:
		xBlocks = [(x+0.5) * lstBody[0].geompos[2] for x in range(insh.nXBlocks)]
		if insh.nFrontBlocks:
			zBlocks = [lstBody[1].geompos[0] + (i+0.5) * lstBody[1].geompos[1] for i in range(insh.nFrontBlocks)]
		else:
			zBlocks = []
		zBlocks += [lstBody[0].geompos[0] + (i+0.5) * lstBody[0].geompos[1] for i in range(insh.nZBlocks)]
		lstWork = [str(x)+'\t' for x in xBlocks]
		lstWork.append('\n') 
		lstWork = lstWork + [str(x)+'\t' for x in zBlocks]
		lstWork.append('\n')
		strWork = '    0    0             Cylinder H2O, DxL{: 5.1f}x{:4.1f}cm, step {: 3.2f}cm,{:4d} zones\n'
		strWork = strWork.format(nTargetBlocks, 2*insh.xTargetWidth, insh.zTargetLength, nZones)
	file1.write(strWork)
	file2.write('ZONE MED VOL(cm3) MASS(g)\n')

	strWork = ''.join(lstWork)
	file3.write(strWork)
	file3.write('ZONE VOL(cm3)\t MASS(g)\tEDGEX\tEDGEY\tEDGEZ\tSIZEX\tSIZEY\tSIZEZ\tXINDEX\tZINDEX\n')
	return [xBlocks, zBlocks]

def orthogonalizeVectors_debug (vMat, noEr, listOrth, maxVal, iMax, out):
	out.write('maxVal = {: 12.8e}\n'.format(maxVal))
	out.write('iMax = {}\n'.format(iMax))
	strWork = 'listOrth = ' + 3*'{: 12.8f}' + '\n'
	out.write(strWork.format(*listOrth))
	for i in range(3):
		strWork = 'vMat {:d} = ' + 3*'{: 12.8f}' + '\n'
		out.write(strWork.format(i, *vMat[i]))
	flagIsNotOrthogonalized = True
	workVec = np.array([vMat[iMax-1], vMat[iMax]])
	workMax = abs(maxVal)
	workVariate = np.zeros(6)
	workOrth = listOrth
	for i in range(2):
		strWork = 'workVec {: d} = ' + 3*'{: 12.8f}' + '\n'
		out.write(strWork.format(i, *workVec[i]))
	cnt = 0
	while (workMax > noEr) & flagIsNotOrthogonalized:
		out.write('orthogonalization attempt {}:\n'.format(cnt+1)) 
		for k in range(2):
			for i in range(3):
				workVec[k][i] -= np.sign(maxVal) * noEr
				workVariate[k*3+i] = workVec[0] @ workVec[1]
				workVec[k][i] += np.sign(maxVal) * noEr
		strWork = 'workVariate = ' + 6*'{: 12.8f}' + '\n'
		out.write(strWork.format(*workVariate))
		iMin = np.argmin(np.absolute(workVariate))
		out.write('iMinVar = {}\n'.format(iMin))
		out.write('maxVar = {: 12.8e}\n'.format(workVariate[iMin]))
		if (workVariate[iMin] < abs(maxVal)) and (cnt<100):
			ik = iMin // 3
			ii = iMin % 3
			workVec[ik][ii] -= np.sign(maxVal)*noEr
			workOrth[iMax] = workVec[0] @ workVec[1]
			workOrth[iMax-1] = vMat[iMax+1] @ workVec[0]
			workOrth[iMax+1] = workVec[1] @ vMat[iMax+1]
			#flagIsNotOrthogonalized = False
		else:
			print ('couldn\'t orthogonalize vectors')
			flagIsNotOrthogonalized = False                                                   
		for i in range(2):
			strWork = 'workVec {: d} = ' + 3*'{: 12.8f}' + '\n'
			out.write(strWork.format(i, *workVec[i]))
		workMax = max(np.absolute(workOrth))
		out.write('newMax = : {: 12.8e}\n'.format(workMax))
		out.write('\n')
		cnt += 1
	out.write('END ORTHOGONALIZATION\n')
	out.write(120*'-'+'\n')
	#return workVec

def orthogonalizeVectors (vMat, noEr, listOrth, maxVal, iMax):
	flagIsNotOrthogonalized = True
	workVec = np.array([vMat[iMax-1], vMat[iMax]])
	workMax = abs(maxVal)
	workVariate = np.zeros(6)
	workOrth = listOrth
	cnt = 0
	while (workMax > noEr) & flagIsNotOrthogonalized:
		for k in range(2):
			for i in range(3):
				workVec[k][i] -= np.sign(maxVal)*noEr
				workVariate[k*3+i] = workVec[0] @ workVec[1]
				workVec[k][i] += np.sign(maxVal)*noEr
		iMin = np.argmin(np.absolute(workVariate))
		if (workVariate[iMin] < abs(maxVal)) and (cnt<100):
			ik = iMin // 3
			ii = iMin % 3
			workVec[ik][ii] -= np.sign(maxVal)*noEr
			workOrth[iMax] = workVec[0] @ workVec[1]
			workOrth[iMax-1] = vMat[iMax+1] @ workVec[0]
			workOrth[iMax+1] = workVec[1] @ vMat[iMax+1]
			#flagIsNotOrthogonalized = False
		else:
			print ('couldn\'t orthogonalize vectors')
			flagIsNotOrthogonalized = False                                                   
		workMax = max(np.absolute(workOrth))
		cnt += 1
	return workVec

def orthogonalizeCheck (sides, noEr, ind):
	strWork = 3*[3*'{: 12.7f}']
	for i in range(3):
		strWork[i] = strWork[i].format(*sides[i])
	workMat = np.zeros((3,3))
	for i in range(3):
		workMat[i] = [float(s) for s in strWork[i].split()]
	listOrth = []
	for i in range(3):
		listOrth.append(workMat[i-1] @ workMat[i])
	maxOrth = max(listOrth)
	minOrth = min(listOrth)
	if maxOrth > noEr:
		iM = listOrth.index(maxOrth)
		[workMat[iM-1], workMat[iM]] = orthogonalizeVectors(workMat, noEr, 
															listOrth, maxOrth, iM)
		print ('for body {: d} the pair of vectors {: d} won\'t pass the othogonality check in gemca'.format(ind, iM))
	elif abs(minOrth) > noEr:
		iM = listOrth.index(minOrth)
		[workMat[iM-1], workMat[iM]] = orthogonalizeVectors(workMat, noEr, 
															listOrth, minOrth, iM)
		print ('for body {: d} the pair of vectors {: d} won\'t pass the othogonality check in gemca'.format(ind, iM))
	
	return workMat

def smallBlockWrite (b, f1, f2, f3, lZ):
	dz = 0
	i = b.nfirst[1]+1
	j = b.nfirst[2]
	if insh.bIsCuboid:
		dx = b.geompos[3]
		volume = b.geompos[3] * b.geompos[4] * b.geompos[5]
		mass = volume * b.med[1]
		strWork = b.type[0].format(b.nfirst[0],
									b.geompos[0], b.geompos[0] + b.geompos[3],
									b.geompos[1], b.geompos[1] + b.geompos[4],
									b.geompos[2], b.geompos[2] + b.geompos[5])
		f1.write(strWork)
		lZ.append([b.nfirst[0], volume, mass] + b.geompos + b.nfirst[1:])
		f3.write(b.type[3].format(*lZ[-1]))
	else:
		volume = np.pi * b.geompos[2] ** 2
		mass = volume * b.med[1]
		strWork = b.type[0].format(b.nfirst[0], b.geompos[0], b.geompos[1])
		strWork += b.type[1].format(b.geompos[2])
		f1.write(strWork)
		lZ.append([b.nfirst[0], volume, mass,
				  -b.geompos[-1], -b.geompos[-1], b.geompos[0],
				   b.geompos[-1]*2, b.geompos[-1]*2, b.geompos[1],
				   b.nfirst[1], b.nfirst[2]])
		f3.write(b.type[3].format(*lZ[-1]))

	strWork = b.type[2].format(b.nfirst[0], b.med[0], volume, mass)
	f2.write(strWork)

	for cnt in range(1, b.ncopy):
		if i > insh.nXBlocks:
			if insh.bIsCuboid:
				dx = 0;
				dz += b.geompos[5]
			else:
				dz += b.geompos[1]
			i = b.nfirst[1]
			j += 1
		if insh.bIsCuboid:
			strWork = b.type[1].format(b.nfirst[0] + cnt, b.nfirst[0], dx, dz)
			f1.write(strWork)
			lZ.append([b.nfirst[0] + cnt, volume, mass,
					   dx + b.geompos[0], b.geompos[1], dz + b.geompos[2],
					   b.geompos[3] , b.geompos[4], b.geompos[5],
					   i, j])
			f3.write(b.type[3].format(*lZ[-1]))
			dx += b.geompos[3]
		else:
			strWork = b.type[0].format(b.nfirst[0] + cnt, dz + b.geompos[0] , b.geompos[1])
			strWork += b.type[1].format(i * b.geompos[2])
			f1.write(strWork)
			lZ.append([b.nfirst[0] + cnt, volume, mass,
					  -i * b.geompos[-1], -i * b.geompos[-1], dz + b.geompos[0],
					   i * b.geompos[-1]*2, i * b.geompos[-1]*2, b.geompos[1],
					   i, j])
			f3.write(b.type[3].format(*lZ[-1]))
		strWork = b.type[2].format(b.nfirst[0] + cnt, b.med[0], volume, mass)
		f2.write(strWork)
		i += 1

def filterWrite (b, f1, f2, f3, lZ, noEr, matRotation):
	xSide = np.linalg.norm(b.geompos[1])
	ySide = np.linalg.norm(b.geompos[2])
	zSide = np.linalg.norm(b.geompos[3])  
	volume = xSide * ySide * zSide
	mass = volume * b.med[1]
	if insh.alphaDeg:
		[b.geompos[1], b.geompos[2], b.geompos[3]] = orthogonalizeCheck([b.geompos[i] for i in range(1,4)], 
																		noEr, b.nfirst)
		vecShift = np.array([insh.fOneWidth, 0.0, 0.0])
		vecShift = vecShift @ matRotation
		vecPivShift = vecShift
		strWork = b.type[0].format(b.nfirst, *b.geompos[0], *b.geompos[1])
		f1.write(strWork)
		strWork = b.type[1].format(*b.geompos[2], *b.geompos[3])
		f1.write(strWork)
		strWork = b.type[2].format(b.nfirst, b.med[0], volume, mass)
		f2.write(strWork)
		lZ.append([b.nfirst, volume, mass] + b.geompos[0] + b.geompos[1] + b.geompos[2] + b.geompos[3])
		f3.write(b.type[3].format(*lZ[-1]))
		for cnt in range(1,b.ncopy+1):
			strWork = b.type[0].format(b.nfirst + cnt, *(b.geompos[0] + vecPivShift), *b.geompos[1])
			f1.write(strWork)
			strWork = b.type[1].format(*b.geompos[2], *b.geompos[3])
			f1.write(strWork)
			strWork = b.type[2].format(b.nfirst + cnt, b.med[0], volume, mass)
			f2.write(strWork)
			workPiv = b.geompos[0]+vecPivShift
			lZ.append([b.nfirst + cnt, volume, mass] + workPiv + b.geompos[1] + b.geompos[2] + b.geompos[3])
			f3.write(b.type[3].format(*lZ[-1]))
			vecPivShift = vecPivShift + vecShift
	else:
		dx=insh.fOneWidth
		strWork = b.type[0].format(b.nfirst,
								   b.geompos[0][0], b.geompos[0][0] + b.geompos[1][0],
								   b.geompos[0][1], b.geompos[0][1] + b.geompos[2][1],
								   b.geompos[0][2], b.geompos[0][2] + b.geompos[3][2])
		f1.write(strWork)
		strWork = b.type[2].format(b.nfirst, b.med[0], volume, mass)
		f2.write(strWork)
		lZ.append([b.nfirst, volume, mass, 
				   b.geompos[0][0], b.geompos[0][1], b.geompos[0][2],
				   b.geompos[1][0], b.geompos[2][1], b.geompos[3][2]])
		f3.write(b.type[3].format(*lZ[-1]))
		for cnt in range(1,b.ncopy+1):
			strWork = b.type[1].format(b.nfirst + cnt, b.nfirst, dx)
			f1.write(strWork)
			strWork = b.type[2].format(b.nfirst + cnt, b.med[0], volume, mass)
			f2.write(strWork)
			lZ.append([b.nfirst + cnt, volume, mass,
					  dx + b.geompos[0][0], b.geompos[0][1], b.geompos[0][2],
					  b.geompos[1][0], b.geompos[2][1], b.geompos[3][2]])
			f3.write(b.type[3].format(*lZ[-1]))
			dx += insh.fOneWidth

def rotatedWrite (b, f1, f2, f3, lZ, noEr):
	xSide = np.linalg.norm(b.geompos[1])
	ySide = np.linalg.norm(b.geompos[2])
	zSide = np.linalg.norm(b.geompos[3])  
	volume = xSide * ySide * zSide
	mass = volume * b.med[1]
	if insh.alphaDeg:
		[b.geompos[1], b.geompos[2], b.geompos[3]] = orthogonalizeCheck([b.geompos[i] for i in range(1,4)], 
																				 noEr, b.nfirst)
		strWork = b.type[0].format(b.nfirst, *b.geompos[0], *b.geompos[1])
		f1.write(strWork)
		strWork = b.type[1].format(*b.geompos[2], *b.geompos[3])
		f1.write(strWork)
		strWork = b.type[2].format(b.nfirst, b.med[0], volume, mass)
		f2.write(strWork)
		lZ.append([b.nfirst, volume, mass] + b.geompos[0] + b.geompos[1] + b.geompos[2] + b.geompos[3])
		f3.write(b.type[3].format(*lZ[-1]))
	else:
		strWork = b.type[0].format(b.nfirst,
								   b.geompos[0][0], b.geompos[0][0] + b.geompos[1][0],
								   b.geompos[0][1], b.geompos[0][1] + b.geompos[2][1],
								   b.geompos[0][2], b.geompos[0][2] + b.geompos[3][2])
		f1.write(strWork)
		strWork = b.type[1].format(b.nfirst, b.med[0], volume, mass)
		f2.write(strWork)
		lZ.append([b.nfirst, volume, mass, 
				   b.geompos[0][0] , b.geompos[0][1], b.geompos[0][2],
				   b.geompos[1][0] , b.geompos[2][1], b.geompos[3][2]])
		f3.write(b.type[2].format(*lZ[-1]))

def simpleWrite (b, f1, f2, f3, lZ):
	if insh.bIsCuboid:
		volume = b.geompos[3] * b.geompos[4] * b.geompos[5]
		mass = volume * b.med[1]
		strWork = b.type[0].format(b.nfirst,
								   b.geompos[0], b.geompos[0] + b.geompos[3],
								   b.geompos[1], b.geompos[1] + b.geompos[4],
								   b.geompos[2], b.geompos[2] + b.geompos[5])
		f1.write(strWork)
		lZ.append([b.nfirst, volume, mass] + b.geompos + [b.nfirst])
		f3.write(b.type[2].format(*lZ[-1]))
	else:
		volume = np.pi * (b.geompos[2] ** 2)
		mass = volume * b.med[1]
		strWork = b.type[0].format(b.nfirst, *b.geompos[:2])
		strWork = strWork + b.type[1].format(b.geompos[2])
		f1.write(strWork)
		lZ.append([b.nfirst, volume, mass,
				  -b.geompos[-1], -b.geompos[-1], b.geompos[0],
				   b.geompos[-1]*2, b.geompos[-1]*2, b.geompos[1]])
		f3.write(b.type[3].format(*lZ[-1]))
	strWork = b.type[-2].format(b.nfirst, b.med[0], volume, mass)
	f2.write(strWork)

def environmentWrite (b, f1):
	if insh.bIsCuboid:
		strWork = b.type[0].format(b.nfirst-1, -0.5*insh.xTargetWidth, insh.xTargetWidth,
								   insh.zTargetInit, insh.zTargetInit + insh.zTargetLength)
	else:
		strWork = b.type[0].format(b.nfirst-1, insh.zTargetInit, insh.zTargetLength)
		strWork = strWork + b.type[1].format(insh.xTargetWidth)
	f1.write(strWork)
	strWork = b.type[-2].format(b.nfirst, b.geompos[5])
	f1.write(strWork)
	strWork = b.type[-1].format(b.geompos[6])
	f1.write(strWork)
	f1.write('  END\n')

def bodyDeclare (file1, file2, file3, lstBody, matRotation):
	dNonOrthogonalError = 1e-7
	res = []
	for b in lstBody:
		key = b.name[0:5]
		if key == 'Main ':
			smallBlockWrite(b, file1, file2, file3, res)
		elif insh.bWithFilter and (key == 'Step '):
			filterWrite(b, file1, file2, file3, res, dNonOrthogonalError, matRotation)
		elif insh.bWithFilter and (key == 'Coppe'):
			rotatedWrite(b, file1, file2, file3, res, dNonOrthogonalError)
		elif key == 'Envir':
			environmentWrite(b, file1)
		else:
			simpleWrite(b, file1, file2, file3, res)
	
	return res

def zoneDeclare (file1, nZones, nFirst = 0):
	if nZones > 4095:
		print('Zones should be renamed')
	for nCurZone in range(1, nZones+1):
		strWork = '  {0:03X}{0:+12d}\n'.format(nCurZone)
		file1.write(strWork)
	nCurZone += 1
	strWork = '  OUT{:+12d}{:+7d}'.format(nCurZone+1, -nCurZone)
	file1.write(strWork)
	if insh.bWithFilter:
		for cnt in range(1 + insh.nSteps * insh.nRepeat):  
			if cnt >= insh.nRepeat * insh.nSteps or ((cnt+3) % 9)==0:
				strWork = '{:+7d}\n'.format(-(nFirst+cnt))
				file1.write(strWork)
			elif ((cnt+3) % 9) == 1:
				strWork = 10*' ' + '{:+7d}'.format(-(nFirst+cnt))
				file1.write(strWork)
			else:
				strWork = '{:+7d}'.format(-(nFirst+cnt))
				file1.write(strWork)
	else:
		file1.write('\n')
	file1.write('  END\n')    

def mediumDeclare (file1, b, nZones):
	numOfColumns = 14
	for k in range(1, nZones+1):
		if k % numOfColumns > 0:
			file1.write('{: 5d}'.format(k+1))
		else:
			file1.write('{: 5d}\n'.format(k+1))
	k += 2
	file1.write('{: 5d}\n'.format(k))
	i = 0
	for k in range(1, nZones+1):
		if k >= b[i+1].nfirst:
			i += 1
		if k % numOfColumns > 0:
			file1.write('{: 5d}'.format(b[i].med[0]))
		else:
			file1.write('{: 5d}\n'.format(b[i].med[0]))    
	file1.write('{: 5d}\n'.format(b[-1].med[0]))

def stdInputMake (strDir):
	lstWork = insh.strAnswers.copy()
	lstWork.append(insh.strAnswers[-1])
	if insh.bWithFilter:
		for i in range(insh.nMedia-2):
			lstWork.append(insh.strAnswers[0])
		strWork = ''.join(lstWork)
	else:
		strWork = ''.join(lstWork)
	open(strDir + 'ShieldInput.txt', 'w+').write(strWork)

def PrepareInput (strDirName, lstDir):
	lstBody, matRotation = shgeo.GeometryMake()

	output1 = open(strDirName + 'pasin.dat', 'w+')
	output2 = open(strDirName + 'zones.dat', 'w+')
	output3 = open(strDirName + 'zones.geo', 'w+')
	nZones = lstBody[-1].nfirst-2
	res = headerWrite(output1, output2, output3, lstBody, nZones)

	res += bodyDeclare(output1, output2, output3, lstBody, matRotation)
	output2.close()
	output3.close()

	if insh.bWithFilter:
		i = [b.name[0:5] for b in lstBody].index('Coppe')
		zoneDeclare(output1, nZones, lstBody[i].nfirst)
	else:
		zoneDeclare(output1, nZones)
	mediumDeclare(output1, lstBody, nZones)
	output1.close()

	for022make(strDirName)
	for023make(lstDir)
	stdInputMake(strDirName)
	
	for dir in lstDir:
		for f in [strDirName + s for s in listdir(strDirName)] :
			copy(f, dir)
	return res