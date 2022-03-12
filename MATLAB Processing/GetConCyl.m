function C=GetCon(Dir,sCase)
%clc; clear variables;
%Dir=dir('Data'); sCase='Dose';

nDataFiles=length(Dir)-2;
itxt(1:nDataFiles)=0;
cnt=0;

%Параметры цилиндра
dCylR=10.0;
dStep=0.1;
dDensity=1;

for i=1:nDataFiles
	filename=Dir(i+2).name;
	itxt=length(filename);
	sExt=[filename(itxt-3),filename(itxt-2),filename(itxt-1),filename(itxt)];
	if strcmp(sExt,'.dat')
		cnt=cnt+1;
		l(cnt)=i;
	end
end

if nDataFiles==0&&cnt==0
	C=0;
	disp('Нет .dat файлов');
else
	nDataFiles=cnt;
	DataFile(1:nDataFiles)=0;
	%nLineN=1;
	%nLineZ=2;
	%nLinesBetweenD=2;
	nZone(1:nDataFiles)=1;
	nStat(1:nDataFiles)=0;
	itxt=1;
	
	while itxt<=nDataFiles&&l(itxt)~=0
		filename=Dir(l(itxt)+2).name;
		filename=['Data\',filename];
		DataFile(itxt)=fopen(filename,'r');
		String=fgetl(DataFile(itxt));                                                                   %Строка с NSTAT
		nStat(itxt)=str2double(String);
		String=fgetl(DataFile(itxt));                                                                   %Строка с NZON
		nZone(itxt)=str2double(String);
		itxt=itxt+1;
	end
	clear filename sExt;

	nMaxZone=max(nZone);
	Work(1:nMaxZone,1:nDataFiles)=0;
	vWork(1:nMaxZone)=0;
	itxt=1;
	while  itxt<=nDataFiles&&l(itxt)~=0
		nCurrentLine=2;
        switch sCase 
        case 'Dose'    
    		String=fgetl(DataFile(itxt));                                                               %Строка с дозвым распределением (на самом деле только заголовок)
    		for i=1:nZone(itxt)
    			String=fgetl(DataFile(itxt));
                dWork=str2num(String);
    			Work(i,itxt)=dWork(3)/dDensity/pi/dCylR/dCylR/dStep*1.6e-10;
            end
            for cnt=1:nDataFiles
				vWork(:)=vWork(:)+Work(:,cnt);
			end;
			C=vWork;
    		%nCurrentLine=nCurrentLine+nZone(itxt)+1;
		case 'Concentration'
    		for cnt=1:(nZone(itxt)+4)
    			String=fgetl(DataFile(itxt));                                                               %Строка с дозвым распределением (на самом деле только заголовок)
            end
			%nCurrentLine=nCurrentLine+nZone+4;
            for i=1:nZone(itxt)
    			String=fgetl(DataFile(itxt));
        		dWork=str2num(String);
    			Work(i,itxt)=dWork(8)/dDensity/pi/dCylR/dCylR/dStep;
            end
			for cnt=1:nDataFiles
				vWork(:)=vWork(:)+Work(:,cnt);
			end;
    		C=vWork;
			%nCurrentLine=nCurrentLine+nZone;
        end
		fclose(DataFile(itxt));
		itxt=itxt+1;
	end
	clear dWork nCurrentLine String i itxt cnt;
end
