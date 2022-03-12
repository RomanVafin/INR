"""
Initial constant declaration

"""

import numpy as np

#Geometry
#Target
bIsCuboid = True
zTargetLength = 30.0
xTargetWidth = 10.0
zTargetInit = 10.0
zBegin = [x * zTargetLength for x in [0.5, 0.9]]
#Main Blocks
nXBlocks = 80
nZBlocks = 40
nBlocks = nXBlocks * nZBlocks
nZTargetSmallBlocks = np.ceil(zTargetLength * nZBlocks / (zBegin[1] - zBegin[0])) * nXBlocks
#Front, Rear and Side Blocks
nFrontBlocks = 1
nBackBlocks = 1 			#1 or 0
#Filter
bWithFilter = True
zScatererThickness = 0.02
xBeamSize = 6.0
nRepeat = 12
fOneWidth = xBeamSize / nRepeat
lstStepsWidth = [0.35, 0.16, 0.1, 0.082, 0.07, 0.07, 0.05, 0.04, 0.04, 0.02]
lstStepsLength = [0.0, 0.47, 0.95, 1.43, 1.92, 2.39, 2.87, 3.35, 3.83, 4.31]
nSteps = len(lstStepsLength) - 1
alphaDeg = 0.                                  #Rotation angle in degrees
#Environment
fTotalLength = 60.0
fTotalRadius = 40.0

#Media description
lstMediaType = [2, 4, 1, 2]						#Media types for Water, Air, Copper, PMMA
lstMediaDensity = [1.0, 0.001205, 8.92, 1.19]	#Water, Air, Copper, PMMA
lstIcruId = [276, 104, 29, 223]
lstNuclId = [[ 1, 8], [ 7, 8], 29, [ 1, 6, 8]]
lstAtomicWeight = [[ 1.00797, 15.99940], [ 14.00670, 15.99940], 63.540, [ 1, 6, 8]]
lstNumComponents = [[ 2, 1], [0.755, 0.245], 1, [ 8, 5, 2]]
lstAng = [[ 20.8, 103.7], [ 80.0, 103.2], 0, [ 19.2, 81.0, 106.0]]
nMedia = 4

#For023
fMaxEnergy = 200.0
fDeltaEnergy = 0.0
fSigmaX = 5.0
fSigmaY = 5.0
nStatistics = int(1e6)
nStepofSaving = int(5e5)

strAnswers = ['no\n', 'ICRU\n', 'yes\n']

#Processing
lstHalfLife = np.array([19.290, 20.334*60, 0.011, 9.965*60, 0.00858, 70.598, 122.24, 64.49, 109.771*60])            #T(1/2)[sec] for C10 C11 N12 N13 O13 O14 O15 F17 F18
lstIsotopes = ['C10', 'C11', 'N12', 'N13', 'O13', 'O14', 'O15', 'F17', 'F18', 'sum']
#numIso = len(lstHalfLife)
numIso = len(lstIsotopes)
