import numpy as np

from DrawingGeom import DrawGeom
import InitShield as insh

class GeoBody:

	def __init__ (self, strName, iFirst, numCopy = 1):
		self.name = strName
		self.nfirst = iFirst
		self.ncopy = numCopy
	def SetType (self, strType):
		self.type = strType
	def SetGeometry (self, lstSize):
		self.geompos = lstSize
	def SetMedium (self, lstMedType):
		self.med = lstMedType

def MakeSteps():
	if sum(insh.lstStepsWidth) != insh.fOneWidth:
		mult = 10000
		res = [np.trunc(x * insh.fOneWidth * mult / sum(insh.lstStepsWidth)) / mult for x in insh.lstStepsWidth]
	else:
		res = insh.lstStepsWidth[:]
	res[0] = 0
	res[0] = round(insh.fOneWidth - sum(res),4)
	return res

def CheckSize(alpha = 0):
	if insh.bWithFilter:
		c, s = np.cos(alpha), np.sin(alpha)
		if insh.zTargetInit < ((max(insh.lstStepsLength) + insh.zScatererThickness) * c + 
								insh.xTargetWidth * s):
			raise Warning('Ridge filter is in the target!')
	if (insh.zTargetInit + insh.zTargetLength + 10) > insh.fTotalLength - 10:
		raise Warning('Target is sticking out!')

def makeGeo(alpha = None, mRotation = None, lstWSteps = None):
	res=[]
	iBod = 0

	#Main Small Peak Blocks
	res.append(GeoBody('Main Target Block', [1, 1, 1], insh.nXBlocks * insh.nZBlocks))
	if insh.bIsCuboid:
		res[iBod].SetType(['  RPP{: 5d}' + 6*'{: 10.5f}' + '\n',
						   '  MOV{0: 5d}{1: 10.1f}{2: 10.5f}       0.0{3: 10.5f}\n',
						   '{:d}\t{:d}\t{: 8.4f}{: 10.4f}\n',
						   '{:d}\t' + 2*'{:8.4f}\t' + 6*'{:5.3f}\t' + 2*'{:4d}\t' + '\n'])
		res[iBod].SetGeometry([-insh.xTargetWidth*0.5, -insh.xTargetWidth*0.5, 
							   insh.zTargetInit + insh.zBegin[0], insh.xTargetWidth / insh.nXBlocks, 
							   insh.xTargetWidth, (insh.zBegin[1] - insh.zBegin[0]) / insh.nZBlocks])
	else:
		res[iBod].SetType(['  RCC{:5d}' + 2*'     0.000' + '{: 10.3f}' + 2*'     0.000' + '{: 10.3f}\n',
							12*' ' + '{: 8.3f}\n',
							'{:d}\t{:d}\t{: 8.4f}{: 10.4f}\n',
							'{:d}\t' + 2*'{:8.4f}\t' + 6*'{:5.3f}\t' + 2*'{:4d}\t' + '\n'])
		res[iBod].SetGeometry([insh.zTargetInit + insh.zBegin[0], 
							   (insh.zBegin[1] - insh.zBegin[0]) / insh.nZBlocks, 
							   insh.xTargetWidth / insh.nXBlocks])
	res[iBod].SetMedium([1, insh.lstMediaDensity[0]])
	nZones = 1+res[iBod].ncopy
	iBod+=1

	#Front Block
	if insh.nFrontBlocks:
		res.append(GeoBody('Front Target Block', nZones, insh.nFrontBlocks))
		if insh.bIsCuboid:
			res[iBod].SetType(['  RPP{: 5d}' + 6*'{: 10.5f}' + '\n',
								'{:d}\t{:d}\t{: 8.4f}{: 10.4f}\n',
								'{:d}\t' + 2*'{:8.4f}\t' + 6*'{:5.3f}\t' + '\n'])
			res[iBod].SetGeometry([-insh.xTargetWidth*0.5, -insh.xTargetWidth*0.5, 
									insh.zTargetInit, insh.xTargetWidth, 
									insh.xTargetWidth, insh.zBegin[0] / insh.nFrontBlocks])
		else:
			res[iBod].SetType(['  RCC{:5d}' + 2*'     0.000' + '{: 10.3f}' + 2*'     0.000' + '{: 10.3f}\n',
								12*' ' + '{: 8.3f}\n',
								'{:d}\t{:d}\t{: 8.4f}{: 10.4f}\n',
								'{:d}\t' + 2*'{:8.4f}\t' + 3*'{:5.3f}\t' + '\n'])
			res[iBod].SetGeometry([insh.zTargetInit, 
								   insh.zBegin[0] / insh.nFrontBlocks,
								   insh.xTargetWidth])
		res[iBod].SetMedium([1, insh.lstMediaDensity[0]])
		nZones += res[iBod].ncopy
		iBod+=1

	#Back Block
	if insh.nBackBlocks:
		res.append(GeoBody('Back Target Block', nZones))
		if insh.bIsCuboid:
			res[iBod].SetType(['  RPP{: 5d}' + 6*'{: 10.5f}' + '\n',
								'{:d}\t{:d}\t{: 8.4f}{: 10.4f}\n',
								'{:d}\t' + 2*'{:8.4f}\t' + 6*'{:5.3f}\t' + '\n'])
			res[iBod].SetGeometry([-insh.xTargetWidth*0.5, -insh.xTargetWidth*0.5, 
									insh.zTargetInit + insh.zBegin[1], insh.xTargetWidth, 
									insh.xTargetWidth, insh.zTargetLength - insh.zBegin[1]])
		else:
			res[iBod].SetType(['  RCC{:5d}' + 2*'     0.000' + '{: 10.3f}' + 2*'     0.000' + '{: 10.3f}\n',
								'{: 20.3f}\n',
								'{:d}\t{:d}\t{: 8.4f}{: 10.4f}\n',
								'{:d}\t' + 2*'{:8.4f}\t' + 3*'{:5.3f}\t' + '\n'])
			res[iBod].SetGeometry([insh.zTargetInit + insh.zBegin[1], 
								   insh.zTargetLength - insh.zBegin[1],
								   insh.xTargetWidth])
		res[iBod].SetMedium([1, insh.lstMediaDensity[0]])
		nZones+=1
		iBod+=1

	#Copper Scaterrer
	if insh.bWithFilter:
		res.append(GeoBody('Copper Scatterer', nZones))
		xSide=np.array([insh.xTargetWidth, 0.0, 0.0])
		ySide=np.array([0.0, insh.xTargetWidth, 0.0])
		zSide=np.array([0.0, 0.0, insh.zScatererThickness])
		if abs(alpha) <= (np.pi*0.5 - 0.1):
			rPiv = np.array([-insh.xTargetWidth*0.5, -insh.xTargetWidth*0.5, insh.xTargetWidth*0.5 * np.tan(abs(alpha))+0.1 / np.cos(alpha)])
			vecCompensate = np.array([-np.sin(alpha) * rPiv[2], 0.0, 0.0])
		elif abs(alpha-np.pi*0.5) < 0.1:
			rPiv = np.array([-insh.xTargetWidth*0.5, -insh.xTargetWidth*0.5, 0.0])
			vecCompensate = np.array([0.0, 0.0, insh.xTargetWidth*0.5 + 0.1])
		else:
			rPiv = np.array([-insh.xTargetWidth*0.5, -insh.xTargetWidth*0.5, 0.0])
			vecCompensate = np.array([0.0, 0.0, (max(max(insh.lstStepsLength), insh.xTargetWidth*0.5) * abs(mRotation[0, 0]) +
												 insh.xTargetWidth*0.5 * abs(mRotation[0, 2]) + 0.1)])
		zPiv = rPiv[2] + zSide[2]
		if alpha:
			rPiv = rPiv @ mRotation + vecCompensate
			xSide = xSide @ mRotation
			zSide = zSide @ mRotation
			if min(rPiv[2], rPiv[2] + xSide[2], rPiv[2] + zSide[2], rPiv[2] + xSide[2] + zSide[2])  < 0.0:
				raise Warning('Filter moved behind the source')
			res[iBod].SetType(['  BOX{: 5d}'+3*'{: 10.6f}'+3*'{: 10.7f}'+'\n',
								10*' '+3*'{: 10.5f}'+3*'{: 10.7f}'+'\n',
								'{:d}\t{:d}\t{:8.4f}{: 10.4f}\n',
								'{:d}\t'+2*'{:8.4f}\t'+12*'{:5.3f}\t'+'\n'])
		else:
			res[iBod].SetType(['  RPP{: 5d}'+6*'{: 10.5f}'+'\n',
								'{:d}\t{:d}\t{: 8.4f}{: 10.4f}\n',
								'{:d}\t'+2*'{:8.4f}\t'+6*'{:5.3f}\t'+'\n'])
		res[iBod].SetGeometry(np.array([rPiv, xSide, ySide, zSide]))
		res[iBod].SetMedium([3, insh.lstMediaDensity[2]])
		nZones+=1
		iBod+=1

	#Steps
	if insh.bWithFilter:
		for cnt in range(1, insh.nSteps+1):
			res.append(GeoBody('Step {}'.format(cnt), nZones, insh.nRepeat))
			rPiv=np.array([-insh.xBeamSize*0.5 + sum(lstWSteps[:cnt]), 
						   -insh.xTargetWidth*0.5, 
						   zPiv])
			xSide=np.array([lstWSteps[cnt], 0.0, 0.0])
			zSide=np.array([0.0, 0.0, insh.lstStepsLength[cnt]])
			if alpha:
				rPiv = rPiv @ mRotation + vecCompensate
				xSide = xSide @ mRotation
				zSide = zSide @ mRotation
				res[iBod].SetType(['  BOX{: 5d}'+3*'{: 10.6f}'+3*'{: 10.7f}'+'\n',
									10*' '+3*'{: 10.5f}'+3*'{: 10.7f}'+'\n',
									'{:d}\t{:d}\t{:8.4f}{: 10.4f}\n',
									'{:d}\t'+2*'{:8.4f}\t'+12*'{:5.3f}\t'+'\n'])
			else:
				res[iBod].SetType(['  RPP{: 5d}'+6*'{: 10.5f}'+'\n',
									'  MOV{: 5d}{: 10.1f}{: 10.5f}       0.0       0.0\n',
									'{:d}\t{:d}\t{: 8.4f}{: 10.4f}\n',
									'{:d}\t'+2*'{:8.4f}\t'+6*'{:5.3f}\t'+'\n'])
			res[iBod].SetGeometry(np.array([rPiv, xSide, ySide, zSide]))
			res[iBod].SetMedium([4, insh.lstMediaDensity[3]])
			nZones += res[iBod].ncopy+1
			iBod+=1

	#Environment
	res.append(GeoBody('Environment', nZones+1))
	if insh.bIsCuboid:
		res[iBod].SetType(['  RPP{0: 5d}{1: 10.5f}{2: 10.5f}{1: 10.5f}{2: 10.5f}{3: 10.5f}{4: 10.5f}\n',
							'  RCC{: 5d}       0.0       0.0     -10.0       0.0       0.0{: 10.5f}\n',
							'{: 20.5f}\n'])
	else:
		res[iBod].SetType(['  RCC{:5d}' + 2*'       0.0       0.0{: 10.1f}' + '\n',
							'{: 20.1f}\n',
							'  RCC{: 5d}' +2*'       0.0' + '     -10.0' + 2*'       0.0' + '{: 10.5f}\n',
							'{: 20.5f}\n'])
	res[iBod].SetGeometry([0, 0, -10, 0, 0, insh.fTotalLength, insh.fTotalRadius])
	res[iBod].SetMedium([2, insh.lstMediaDensity[1]])

	return res

def GeometryMake():
	dRotAngle = (insh.alphaDeg/180 % 2) * np.pi                                     #Rotation angle in radians
	if dRotAngle:                                                                   #In rad; >0 the longest step on the way, <0 the shortest step on the way (clockwise/counterclockwise rotation)
		c, s = np.cos(dRotAngle), np.sin(dRotAngle)
		mRotation = np.array([[c, 0.0, -s],
							  [0.0, 1.0, 0.0],
							  [s, 0.0, c]])
	else:
		#change to np's identity matrix
		mRotation = np.array([[1.0, 0.0, 0.0],
							  [0.0, 1.0, 0.0],
							  [0.0, 0.0, 1.0]])
	if insh.bWithFilter:
		dWSteps = MakeSteps()
	CheckSize(dRotAngle)
	if insh.bWithFilter:
		lstBody = makeGeo(dRotAngle, mRotation, dWSteps)
	else:
		lstBody = makeGeo()

#!!check how mRotation variable is used in DrawGeom to change it to only when with filter use
	DrawGeom(lstBody, mRotation)

	return lstBody, mRotation