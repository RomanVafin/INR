import subprocess
import os
import datetime
from shutil import copy
from multiprocessing import Process
import numpy as np

import InitShield as insh
from ShieldInputWrite import PrepareInput
from ShieldProcessing import MakeDat


def runShield(srs):
	os.chdir(srs)
	#print('Session in ' + srs.split('\\')[-1] + ' is starting...')
	for f in ['for{:03d}'.format(i) for i in range(24,34)]:
		if os.path.exists(f):
			os.remove(f)
	if insh.bIsCuboid:
		res = subprocess.run('ShieldSq.exe',
							 stdin=open('ShieldInput.txt'),
							 stdout=subprocess.DEVNULL)
	else:
		res = subprocess.run('ShieldHIT_19.exe',
							 stdin=open('ShieldInput.txt'),
							 stdout=subprocess.DEVNULL)
	#print(srs[-5:])
	print('Session in ' + srs.split('\\')[-1] + ' has been completed!')
	return res

def runInParallel(func, lstdir):
	proc = []
	for s in lstdir:
		p = Process(target=func, args=(s,))
		p.start()
		proc.append(p)
	for p in proc:
		p.join()

def main():
	ses = 4
	dtSession = datetime.date.today()
	strSessionName = dtSession.strftime('%y%m%d')
	dirMaster = os.getcwd()
	os.chdir('.\Shield')
	orig = os.getcwd()
	srsFiles = [orig + '\\' + s for s in os.listdir() if os.path.isfile(s)]
	os.chdir('..')
	dirName = [dirMaster + '\\' + strSessionName + '_{}'.format(i+1) for i in range(ses)]
	
	for s in dirName:
		if not os.path.exists(s):
			os.mkdir(s)
			for f in srsFiles:
				copy(f,s)
	
	lstZones = PrepareInput(dirMaster + "\Out\\", dirName)
	print(dirName)
	#runShield(dirName[0])
	#runInParallel(runShield, dirName)
	
	os.chdir(dirMaster)
	MakeDat(dirMaster, dirName, strSessionName, lstZones)

if __name__ == '__main__':
	main()