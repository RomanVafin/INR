"""
Data visualisation ant export to dat file for Origin

"""

import numpy as np
import os
from shutil import copy

import InitShield as insh
from DrawingGeom import plot_data

class RadiationData:
	
	def doseData (self, file1):
		res = []
		for line in file1:
			if line == '          DISTRIBUTIONS INSIDE TARGET.\n':
				break
		if line == '':
			raise Warning("Dose distribution section is not found")
		file1.readline()
		file1.readline()
		for iZone in range(self.numzone):
			res.append(file1.readline().split())
		return res
	
	def isoData (self, file1):
		res = []
		for line in file1:
			if line == '     Distribution of PET isotopes over target zones\n':
				break
		if line == '':
			raise Warning("Distribution of PET isotopes section is not found")
		self.iso_names = file1.readline()[11:].split()
		for iZone in range(self.numzone):
			res.append(file1.readline().split())
		return res
	
	def __init__ (self, lstZones, file1 = None):
		fConvMult = 1.6e-7
		self.numzone = len(lstZones) - 2			#without environment(air)
		self.dose = np.zeros(self.numzone)
		self.dose_targ = np.zeros((insh.nFrontBlocks + insh.nZBlocks, insh.nXBlocks))
		self.zones = []
		self.nstat = 0
		self.x = np.array(lstZones[0])
		self.z = np.array(lstZones[1])
		
		if file1 is None:
			self.iso_names = insh.lstIsotopes[:-1]
			self.pet = {key: np.zeros(self.numzone) for key in self.iso_names + ['sum']}
			self.pet_targ = {key: np.zeros((insh.nFrontBlocks + insh.nZBlocks, insh.nXBlocks)) for key in self.iso_names + ['sum']}
			for iZ in range(self.numzone):
				self.zones.append([lstZones[iZ + 2][3] + 0.5*lstZones[iZ + 2][6],
								   lstZones[iZ + 2][5] + 0.5*lstZones[iZ + 2][8]])
		else:
			lstD = self.doseData(file1)
			lstI = self.isoData(file1)
			self.pet = {key: np.zeros(self.numzone) for key in self.iso_names + ['sum']}
			self.pet_targ = {key: np.zeros((insh.nFrontBlocks + insh.nZBlocks, insh.nXBlocks)) for key in self.iso_names + ['sum']}
			for iZ in range(self.numzone):
				self.dose[iZ] = fConvMult * float(lstD[iZ][2]) / lstZones[iZ + 2][2]
				lstWork = [float(x) / lstZones[iZ + 2][1] for x in lstI[iZ][2:]]
				for x, key in zip(lstWork, self.iso_names):
					self.pet[key][iZ] = x
					self.pet['sum'][iZ] += x
				self.zones.append([lstZones[iZ + 2][3] + 0.5*lstZones[iZ + 2][6],
								  lstZones[iZ + 2][5] + 0.5*lstZones[iZ + 2][8]])
				if iZ < insh.nBlocks:
					i = int(lstZones[iZ + 2][-2]) - 1
					k = int(lstZones[iZ + 2][-1]) - 1 + insh.nFrontBlocks
					self.dose_targ[k,i] = self.dose[iZ]
					for key in self.iso_names:
						self.pet_targ[key][k,i] = self.pet[key][iZ]
						self.pet_targ['sum'][k,i] += self.pet[key][iZ]
				elif iZ < (insh.nBlocks + insh.nFrontBlocks):
					k = iZ - insh.nBlocks
					self.dose_targ[k,:] = self.dose[iZ]
					for key in self.iso_names:
						self.pet_targ[key][k,:] = self.pet[key][iZ]
						self.pet_targ['sum'][k,:] += self.pet[key][iZ]
	
	def statCheck (self, file1, dir):
		bFlag = False
		for line in file1:
			if line == 45*' ' + 'DISTRIBUTIONS INSIDE TARGET\n':
				bFlag = True
			if bFlag and (line[:24] == ' RANDOM GENERATOR STATUS'):
				break
		if line == '':
			raise Warning("Ending section is not found")
		file1.readline()
		self.nstat = int(file1.readline().split()[3])
		if self.nstat < insh.nStatistics:
			print("Session in ", dir)
			print("hasn't finished and stopped at ", self.nstat, " events")
	
	def update (self, data):
		self.dose += data.dose
		self.dose_targ += data.dose_targ
		for key in data.pet:
			self.pet[key] = self.pet.get(key, 0) + data.pet[key]
			self.pet_targ[key] = self.pet_targ.get(key, 0) + data.pet_targ[key]
		self.nstat += data.nstat
	
	def activ_calc (self):
		ON_SHARE = 0.89								#O13 -> N13 decay probability
		LAMBDA_SEP = np.log(2)/60
		CONV_MULT = 2.7027*1e-8
		self.activity = {}
		self.activity_targ = {}
		dctLambda = {key: np.log(2) / val for key, val in zip(insh.lstIsotopes[:-1], insh.lstHalfLife)}
		for key in self.iso_names:
			if key in insh.lstIsotopes[:-1]:
				self.activity[key] = CONV_MULT * dctLambda[key] * self.pet[key]
				self.activity_targ[key] = CONV_MULT * dctLambda[key] * self.pet_targ[key]
				self.activity['sum'] = self.activity.get('sum', 0) + self.activity[key]
				self.activity_targ['sum'] = self.activity_targ.get('sum', 0) + self.activity_targ[key]
				if dctLambda[key] < LAMBDA_SEP:
					self.activity['long'] = self.activity.get('long', 0) + self.activity[key]
					self.activity_targ['long'] = self.activity_targ.get('long', 0) + self.activity_targ[key]
		if 'O13' in self.iso_names:
			for key in set(insh.lstIsotopes[:-1]) & set(self.iso_names):
				if key == 'N13':
					self.activity['2min'] = (self.activity.get('2min', 0) 
											 + np.exp(-120 * dctLambda[key]) * self.activity[key] 
											 + (ON_SHARE 
												* dctLambda['N13'] 
												* self.activity['O13'] 
												* (np.exp(-120*dctLambda['O13']) - np.exp(-120*dctLambda['N13']))
												/ (dctLambda['N13'] - dctLambda['O13'])
												)
											 )
					self.activity_targ['2min'] = (self.activity_targ.get('2min', 0) 
												 + np.exp(-120 * dctLambda[key]) * self.activity_targ[key] 
												 + (ON_SHARE 
													* dctLambda['N13'] 
													* self.activity_targ['O13'] 
													* (np.exp(-120*dctLambda['O13']) - np.exp(-120*dctLambda['N13']))
													/ (dctLambda['N13'] - dctLambda['O13'])
													)
												  )
				else:
					self.activity['2min'] = self.activity.get('2min', 0) + np.exp(-120*dctLambda[key])*self.activity[key]
					self.activity_targ['2min'] = self.activity_targ.get('2min', 0) + np.exp(-120*dctLambda[key])*self.activity_targ[key]
		else:
			for key in self.iso_names:
				self.activity['2min'] = self.activity.get('2min', 0) + np.exp(-120*dctLambda[key])*self.activity[key]
				self.activity_targ['2min'] = self.activity_targ.get('2min', 0) + np.exp(-120*dctLambda[key])*self.activity_targ[key]


def GetData(lstDir, lstZones):
	#lstZones = open('.\Out\zones.geo','r').readlines()
	res = [RadiationData(lstZones)]
	for dir in lstDir:
		os.chdir(dir)
		workFile = open(dir + '\\for024','r')
		res.append(RadiationData(lstZones, workFile))
		res[-1].statCheck(workFile, dir)
		res[0].update(res[-1])
	res[0].activ_calc()
	return res

def MakeSessionReport(fileRep, radData, strCase = ' '):
	res = []
	if insh.bIsCuboid:
		strWork = 'Cuboid WxL{: 4.1f}x{: 4.1f} cm {: 3d}x{: 3d} zones'.format(insh.zTargetLength, insh.xTargetWidth, insh.nZBlocks, insh.nXBlocks)
	else:
		strWork = 'Cylinder WxL{: 4.1f}x{: 4.1f} cm {: 3d}x{: 3d} zones'.format(insh.zTargetLength, 2*insh.xTargetWidth, insh.nZBlocks, insh.nXBlocks)
	if insh.bWithFilter:
		strWork += ' filter'
	if insh.alphaDeg:
		strWork += ' rotated by{: 4.2} deg'.format(insh.alphaDeg)
	strWork += ' numStat {: 3.0e}\n'.format(radData.nstat)
	fileRep.write(strWork)
	res.append(strWork)
	if strCase == 'sorted':
		strWork = 'z\\x' + (2*insh.numIso + 3)*('\t' + '\t'.join([str(x) for x in radData.x])) + '\n'
		fileRep.write(strWork)
		res.append(strWork)
		strWork = ('z[cm]\tDose[mGy]' 
					+ insh.nXBlocks*'\t' 
					+ (insh.nXBlocks*'\t').join(['Con(' + x + ')[1/cm^3]' for x in insh.lstIsotopes]) 
					+ (insh.nXBlocks*'\t').join(['Act(' + x + ')[mCi]' for x in list(insh.lstIsotopes) + ['long', '2 min']])
					+ '\n'
					)
		fileRep.write(strWork)
		res.append(strWork)
		matConcWork = np.zeros((insh.numIso, insh.nXBlocks))
		matActWork = np.zeros((insh.numIso, insh.nXBlocks))
		for i in range(insh.nFrontBlocks + insh.nZBlocks):
			for id,key in enumerate(insh.lstIsotopes):
				if key in radData.pet_targ:
					matConcWork[id] = radData.pet_targ[key][i]
					matActWork[id] = radData.activity_targ[key][i]
			strWork = ('{: 5.2f}\t' 
					   + insh.nXBlocks * '{: 4.3e}\t' 
					   + insh.nXBlocks * (insh.numIso) * '{: 9.2f}\t' 
					   + insh.nXBlocks * (insh.numIso+2) * '{: 9.2f}\t'
					   + '\n'
					   )
			strWork = strWork.format(radData.z[i], 
									 *radData.dose_targ[i],
									 *matConcWork.flatten(),
									 *matActWork.flatten(),
									 *radData.activity_targ['long'][i],
									 *radData.activity_targ['2min'][i]
									 )
			fileRep.write(strWork)
			res.append(strWork)
	else:
		strWork = (' Zone\tx\tz\tdose\t'
				   + '\t'.join(['Con(' + x + ')' for x in insh.lstIsotopes])
				   + '\t'.join(['Act(' + x + ')' for x in list(insh.lstIsotopes) + ['long', '2 min']])
				   + '\n'
				   )
		fileRep.write(strWork)
		res.append(strWork)
		strWork = '\tcm\tcm\tmGy\t1/cm^3\tmCi\n'
		fileRep.write(strWork)
		res.append(strWork)
		matConcWork = np.zeros(insh.numIso)
		matActWork = np.zeros(insh.numIso)
		for i in range(radData.numzone):
			for id,key in enumerate(insh.lstIsotopes):
				if key in radData.pet:
					matConcWork[id] = radData.pet[key][i]
					matActWork[id] = radData.activity[key][i]
			strWork = ('{: d}\t{: 5.2f}\t{: 5.2f}\t{: 4.3e}\t' 
					   + (insh.numIso) * '{: 9.2f}\t' 
					   + (insh.numIso+2) * '{: 4.3e}\t' 
					   + '\n'
					   )
			strWork = strWork.format(i+1, 
									 *radData.zones[i],
									 radData.dose[i],
									 *matConcWork,
									 *matActWork,
									 radData.activity['long'][i],
									 radData.activity['2min'][i]
									 )
			fileRep.write(strWork)
			res.append(strWork)
	return res

def SumReport(fileS, lstS, radData, strCase = ' '):
	fileS.seek(0)
	fileS.truncate()
	lstHead = lstS[0].split()
	numNewStat = int(float(lstHead[-1])) + radData.nstat
	numSumBlocks = int(lstHead[5][:-1]) * int(lstHead[6])
	#fLenS = len(lstS)
	#fLenA = len(lstA)
	if strCase == 'sorted':
		if (insh.nZBlocks + insh.nFrontBlocks + 3) == len(lstS):
			strWork = ' '.join(lstHead[:-1] + ['{: 3.2e}\n'.format(numNewStat)])
			strWork += lstS[1] + lstS[2]
			fileS.write(strWork)
			for iZ in range(insh.nZBlocks + insh.nFrontBlocks):
				lstWork = lstS[iZ + 3].split()
				z_pos = lstWork.pop(0)
				fWork = [float(x) + y for x, y in zip(lstWork[:insh.nXBlocks], radData.dose_targ[iZ])]
				fWork += [float(x) + y 
						  for i, k in enumerate(insh.lstIsotopes)
						  for x, y in zip(lstWork[(i+1)*insh.nXBlocks:(i+2)*insh.nXBlocks], radData.pet_targ[k][iZ])
						  ]
				fWork += [float(x) + y 
						  for i, k in enumerate(insh.lstIsotopes + ['long', '2min'])
						  for x, y in zip(lstWork[(i+insh.numIso+1)*insh.nXBlocks:(i+insh.numIso+2)*insh.nXBlocks], 
										  radData.activity_targ[k][iZ]
										  )
						  ]
				strWork = (z_pos
						   + insh.nXBlocks * '\t{: 4.3e}' 
						   + insh.nXBlocks * insh.numIso * '\t{: 9.2f}' 
						   + insh.nXBlocks * (insh.numIso+2) * '\t{: 9.2f}'
						   + '\n'
						   )
				fileS.write(strWork.format(*fWork))
		else:
			fileS.close()
			raise Warning("zone number mismatch!")
	else:
		if (radData.numzone + 3) == len(lstS):
			strWork = ' '.join(lstHead[:-1] + ['{: 3.2e}\n'.format(numNewStat)])
			strWork += lstS[1] + lstS[2]
			fileS.write(strWork)
			for iZ in range(radData.numzone):
				lstWork = lstS[iZ + 3].split()
				fWork = [float(lstWork[3]) + radData.dose[iZ]]
				fWork += [float(x) + y 
						  for x, y in zip(lstWork[4:insh.numIso+4], 
										  [radData.pet[k][iZ] for k in insh.lstIsotopes]
										  )
						  ]
				fWork += [float(x) + y 
						  for x, y in zip(lstWork[insh.numIso+4:], 
										  [radData.activity[k][iZ] for k in insh.lstIsotopes + ['long','2min']]
										  )
						  ]
				strWork = ('\t'.join(lstWork[:3])
						   + '\t{: 4.3e}'
						   + (insh.numIso) * '\t{: 9.2f}' 
						   + (insh.numIso+2) * '\t{: 4.3e}' 
						   + '\n'
						   )
				fileS.write(strWork.format(*fWork))
		else:
			fileS.close()
			raise Warning("zone number mismatch!")

def MakeReport(strSum, strAdd, radData):
	lstAdd = MakeSessionReport(open(strAdd, 'w+'), radData)
	lstAddSort = MakeSessionReport(open('sort_' + strAdd, 'w+'), radData, 'sorted')
	if os.path.exists(strSum):
		fileSum = open(strSum, 'r+')
		fileSumSort = open('sort_' + strSum, 'r+')
		lstSum = fileSum.readlines()
		lstSumSort = fileSumSort.readlines()
		if ''.join(lstSum[0].split()[:-1]) == ''.join(lstAdd[0].split()[:-1]):
			SumReport(fileSum, lstSum, radData)
			SumReport(fileSumSort, lstSumSort, radData, 'sorted')
		fileSum.close()
		fileSumSort.close()
	else:
		copy(strAdd, strSum)
		copy('sort_' + strAdd, 'sort_' + strSum)

#move to __repr__ class method
def PrintData(lstdata, lstdir):
	f1 = open('raw_data.txt', 'w')
	for i, d in enumerate(lstdata):
		if i:
			f1.write(lstdir[i-1] + '\n')
		else:
			f1.write('sum\n')
		work = d.__dict__
		f1.write(str(list(work))+'\n')
		for k in work:
			f1.write(12*'-' + '\n')
			f1.write(k + ':\n')
			if isinstance(work[k], int):
				strWork = str(work[k]) + '\n'
			elif isinstance(work[k], dict):
				strWork = ''
				for key in work[k]:
					strWork += key + ':\n'
					for v in work[k][key]:
						strWork += str(v) + '\n'
			else:
				strWork = ''
				for v in work[k]:
					strWork += str(v) + '\n'
			f1.write(strWork)
		f1.write(120*'=' + '\n')
	f1.close()

def MakeDat(strDirM, lstDir, strSesName, lstZones):
	strSumName = 'SumReport'
	strExt = '.dat'
	strOut = strDirM + '\\Report'
	workData = GetData(lstDir, lstZones)
	os.chdir(strOut)
	PrintData(workData, lstDir)
	if os.path.exists(strSumName + strExt):
		copy(strSumName + strExt, strSumName + '_old' + strExt)
		copy('sort_' + strSumName + strExt, 'sort_' + strSumName + '_old' + strExt)
	MakeReport(strSumName + strExt, strSesName + strExt, workData[0])
	plot_data(workData[0])

if __name__ == '__main__':
	strDir = 'TestCub'
	strSes = 'SingleRep'
	#MakeDat([strDir], strSes)