import math

NZones=300
RCyl=10.0
LCyl=30.0
NZonesCyl=NZones
Step=LCyl/NZonesCyl
output1=open('Out\\for017t', 'w+')
output2=open('Out\pasint.dat','w+')
CurrentString='    0    0             Cylinder H2O, DxL{: 5.1f}x{:4.1f}cm, step {: 3.2f}cm,{:4d} zones\n'
CurrentString=CurrentString.format(2*RCyl, LCyl, Step, NZones)
output1.write(CurrentString)
output2.write(CurrentString)

#Определение тел
#Простой цилиндр
x=.0
for cnt in range(NZonesCyl):
	CurrentString='  RCC{:5d}     0.000     0.000{: 10.3f}     0.000     0.000{: 10.3f}\n'
	CurrentString=CurrentString.format(cnt+1, x, Step)
	output1.write(CurrentString)
	CurrentString='            {: 8.3f}\n';
	CurrentString=CurrentString.format(RCyl)
	output1.write(CurrentString)
	CurrentString='  RCC{:5d}       0.0       0.0{: 10.1f}       0.0       0.0{: 10.1f}\n'
	CurrentString=CurrentString.format(cnt+1, x, Step)
	output2.write(CurrentString)
	CurrentString='            {: 8.1f}\n'
	CurrentString=CurrentString.format(RCyl)
	output2.write(CurrentString)
	x=x+Step
CurrentString='  RCC{:5d}     0.000     0.000     0.000     0.000     0.000{: 10.3f}\n'
CurrentString=CurrentString.format(NZonesCyl+1, LCyl)
output1.write(CurrentString)
CurrentString='            {: 8.3f}\n'
CurrentString=CurrentString.format(RCyl)
output1.write(CurrentString)
CurrentString='  RCC{:5d}       0.0       0.0       0.0       0.0       0.0{: 10.1f}\n'
CurrentString=CurrentString.format(NZonesCyl+1, LCyl)
output2.write(CurrentString)
CurrentString='            {: 8.1f}\n'
CurrentString=CurrentString.format(RCyl)
output2.write(CurrentString)

#Окружаещее пространство
CurrentString='  RCC{:5d}     0.000     0.000   -10.000     0.000     0.000    60.000\n'
output1.write(CurrentString.format(NZonesCyl+2))
output1.write('              20.000\n')
output1.write('  END')
output1.close()
CurrentString='  RCC{:5d}       0.0       0.0     -10.0       0.0       0.0      60.0\n'
CurrentString.format(NZonesCyl+2)
output2.write(CurrentString)
output2.write('                20.0\n')
output2.write('  END\n')

#Определяем зоны
#Простой цилиндр
print(NZonesCyl)
for cnt in range(NZonesCyl):
	CurrentString='  {0:03d}{0:+12d}\n';
	output2.write(CurrentString.format(cnt+1))
	print(cnt)
CurrentString='  OUT{:+12d}{:+7d}\n'
CurrentString=CurrentString.format(NZonesCyl+2, -NZonesCyl-1)
output2.write(CurrentString)
output2.write('  END\n')

#Задание сред
#Простой цилиндр
nCol=14
for cnt in range(NZonesCyl):
	if (cnt+1)%nCol>0:
		output2.write('{:5d}'.format(cnt+1))
	else:
		output2.write('{:5d}\n'.format(cnt+1))
output2.write('{:5d}\n'.format(NZonesCyl+2))
for cnt in range(NZonesCyl):
	if (cnt+1)%nCol>0:
		output2.write('{:5d}'.format(1))
	else:
		output2.write('{:5d}\n'.format(1))
output2.write('{:5d}\n'.format(0))
output2.close()

output3=open('Out\zones.dat','w+')
output3.write('ZONE\tMED\tVOL(cm3)\tMASS(g)\n')
Volume=math.pi*Step*RCyl**2								#предполагается dens=1.0 для воды и Mass=Volume
for cnt in range(NZonesCyl)
	CurrentString='{0:d}\t{1:d}\t{2:7.4f}\t{2:7.4f}\n'
	CurrentString=CurrentString.format(cnt, 1, Volume)
	output3.write(CurrentString)

output3.close()