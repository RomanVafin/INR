'''
simple drawing module

'''

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib import cm
#from mpl_toolkits.mplot3d import axes3d
import numpy as np

import InitShield as insh

def DrawGeom(lstBody, mRotation):
	fig1 = plt.figure()
	ax = fig1.add_subplot()
	xradTotal = lstBody[-1].geompos[6]
	zlenTotal = lstBody[-1].geompos[5]
	ax.set_xlim(-xradTotal*1.2, xradTotal*1.2)
	ax.set_ylim(-10, zlenTotal*1.1)

	envir = mpatches.Rectangle((-xradTotal, -10), 
							   2*xradTotal, zlenTotal, 
							   facecolor = 'lightgray')
	if insh.bIsCuboid:
		target = mpatches.Rectangle((-insh.xTargetWidth*0.5, insh.zTargetInit), 
									 insh.xTargetWidth, insh.zTargetLength, 
									 facecolor = 'deepskyblue')
	else:
		target = mpatches.Rectangle((-insh.xTargetWidth, insh.zTargetInit), 
									 insh.xTargetWidth*2, insh.zTargetLength, 
									 facecolor = 'deepskyblue')

	ax.add_patch(envir)
	ax.add_patch(target)

	if insh.bWithFilter:
		iBeg = [b.name[0:6] for b in lstBody].index('Step 1')
		#iEnd = [b.name[0:6] for b in lstBody].index('Step {}'.format(insh.nSteps))
		filterRotatedShift = np.array([insh.fOneWidth, 0.0, 0.0])
		if insh.alphaDeg:
			filterRotatedShift = filterRotatedShift @ mRotation
		for i in range(iBeg, iBeg + insh.nSteps):
			for k in range(lstBody[i].ncopy):
				piv = (lstBody[i].geompos[0][0] + filterRotatedShift[0]*k, lstBody[i].geompos[0][2] + filterRotatedShift[2]*k)
				if insh.alphaDeg:
					patchWidth = np.linalg.norm(lstBody[i].geompos[1])
					patchLength = np.linalg.norm(lstBody[i].geompos[3])
				else:
					patchWidth = lstBody[i].geompos[1][0]
					patchLength = lstBody[i].geompos[3][2]
				workPatch = mpatches.Rectangle(piv, 
											   patchWidth, patchLength, 
											   angle = -insh.alphaDeg, facecolor = 'wheat',
											   ec = 'k', alpha = 0.3)
				ax.add_patch(workPatch)

		i = [b.name[0:5] for b in lstBody].index('Coppe')
		piv = (lstBody[i].geompos[0, 0], lstBody[i].geompos[0, 2])
		if insh.alphaDeg:
			patchWidth = np.linalg.norm(lstBody[i].geompos[1])
			patchLength = np.linalg.norm(lstBody[i].geompos[3])
		else:
			patchWidth = lstBody[i].geompos[1][0]
			patchLength = lstBody[i].geompos[3][2]
		workPatch = mpatches.Rectangle(piv, 
									   patchWidth, patchLength, 
									   angle = -insh.alphaDeg, facecolor = 'sienna')
		ax.add_patch(workPatch)

	plt.show()
	
def plot_data(data):
	fig = []
	ax = []
	if insh.nXBlocks > 1:
		ax.append(plt.figure().add_subplot(projection='3d'))
		x, y = np.meshgrid(data.x, data.z)
		max_z = np.max(data.dose_targ)
		lvls = max_z * np.linspace(0., 1., num=5)
		max_y = insh.zTargetLength + insh.zTargetInit
		ax[0].plot_surface(x, 
						   y, 
						   data.dose_targ, 
						   cmap=cm.jet, 
						   rstride=5,
						   cstride=5, 
						   alpha=0.8)
		
		cset = ax[0].contourf(x, y, data.dose_targ, zdir='z', offset=-0.3*max_z, cmap=cm.coolwarm)
		cset = ax[0].contourf(x, y, data.dose_targ, zdir='x', offset=-insh.xTargetWidth, cmap=cm.coolwarm)
		cset = ax[0].contourf(x, y, data.dose_targ, zdir='y', offset=max_y, cmap=cm.coolwarm)
		
		ax[0].set_xlim(-insh.xTargetWidth, insh.xTargetWidth)
		ax[0].set_ylim(insh.zTargetInit, max_y)
		#ax[0].set_zlim(-0.3*max_z, max_z)
		ax[0].set(title='dose distribition')
		
		ax.append(plt.figure().add_subplot(projection='3d'))
		max_z = np.max(data.pet_targ['sum'])
		ax[1].plot_surface(x, 
						   y, 
						   data.pet_targ['sum'], 
						   cmap=cm.gist_earth, 
						   rstride=5,
						   cstride=5, 
						   alpha=0.8)
		
		cset = ax[1].contourf(x, y, data.pet_targ['sum'], zdir='z', offset=-0.3*max_z, cmap=cm.coolwarm)
		cset = ax[1].contourf(x, y, data.pet_targ['sum'], zdir='x', offset=-insh.xTargetWidth, cmap=cm.coolwarm)
		cset = ax[1].contourf(x, y, data.pet_targ['sum'], zdir='y', offset=max_y, cmap=cm.coolwarm)
		ax[1].set(title='PET distribition')
		
		ax[1].set_xlim(-insh.xTargetWidth, insh.xTargetWidth)
		ax[1].set_ylim(insh.zTargetInit, max_y)
		ax[1].set_zlim(-0.3*max_z, max_z)
		
		ax.append(plt.figure().add_subplot(projection='3d'))
		max_z = np.max(data.activity_targ['sum'])
		ax[2].plot_surface(x, 
						   y, 
						   data.activity_targ['sum'], 
						   cmap=cm.gist_earth, 
						   rstride=1,
						   cstride=1, 
						   alpha=0.8)
		
		cset = ax[2].contourf(x, y, data.activity_targ['sum'], zdir='z', offset=-0.3*max_z, cmap=cm.coolwarm)
		cset = ax[2].contourf(x, y, data.activity_targ['sum'], zdir='x', offset=-insh.xTargetWidth, cmap=cm.coolwarm)
		cset = ax[2].contourf(x, y, data.activity_targ['sum'], zdir='y', offset=max_y, cmap=cm.coolwarm)
		ax[2].set(title='activity distribition')
		
		ax[2].set_xlim(-insh.xTargetWidth, insh.xTargetWidth)
		ax[2].set_ylim(insh.zTargetInit, max_y)
		ax[2].set_zlim(-0.3*max_z, max_z)
		
		ax.append(plt.figure().add_subplot())
		ax[-1].contourf(x,
						y, 
						data.pet_targ['sum'], 
						cmap=cm.gist_earth
						)
		ax[-1].contour(x,
					   y, 
					   data.dose_targ,
					   5,
					   cmap=cm.jet
					   )
	else:
		fig[0], ax[0] = plt.subplots()
		ax[0].plot(data.z, data.dose[:len(data.z)])
	plt.show()
