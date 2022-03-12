%function C=GetCon(Dir,sCase)
clc; clear variables;
Dir=dir('Data'); sCase='Dose';

nDataFiles=length(Dir)-2;
itxt(1:nDataFiles)=0;
cnt=0;

%{
Параметры цилиндра
dCylR=10.0;
dStep=0.1;
dDensity=1;
%}
for i=1:nDataFiles
	filename=Dir(i+2).name;
	itxt=length(filename);
	sExt=[filename(itxt-3),filename(itxt-2),filename(itxt-1),filename(itxt)];
	if strcmp(sExt,'.dat')
		cnt=cnt+1;
		l(cnt)=i;
	end
end

ZonesDir=dir('Zones');
if cnt==length(ZonesDir)-2;
	ZonesFile(1:cnt)=-1;
	for i=1:cnt
		filename=Dir(l(i)+2).name;
		nLFileName=length(filename);
		filename=filename(1:nLFileName-3);
		filename=['Zones\',filename,'geo'];
		ZonesFile(i)=fopen(filename, 'r');
		if ZonesFile(i)==-1
			sWarn=['нет соответствующего для', filename, 'geo файла! (имена geo и dat файлов должны совпадать)'];
			%error(sWarn);
			disp(sWarn);
		end
	end
else
	disp('Не совпадает число .dat файлов');
end

if nDataFiles==0&&cnt==0
	C=0;
	disp('Нет .dat файлов');
	fclose('all');
else
	nDataFiles=cnt;
	DataFile(1:nDataFiles)=0;
	%nLineN=1;
	%nLineZ=2;
	%nLinesBetweenD=2;
	nZone(1:nDataFiles)=-1;
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
	sZoneParam=fgetl(ZonesFile(1));
	nBlocks=str2num(sZoneParam);
	mSort=zeros([nBlocks(1), nBlocks(2)]);
    sZoneParam=fgetl(ZonesFile(1));
	dTarget=str2num(sZoneParam);
	sZoneParam=fgetl(ZonesFile(1));
	vx=str2num(sZoneParam);
	sZoneParam=fgetl(ZonesFile(1));
	vz=str2num(sZoneParam);
	for cnt=1:nBlocks(1)
		
	end
	itxt=1;
	while  itxt<=nDataFiles&&l(itxt)~=0
		nCurrentLine=2;
        switch sCase 
        case 'Dose'    
    		String=fgetl(DataFile(itxt));			%Строка с дозовым распределением (на самом деле только заголовок)
    		sZoneParam=fgetl(ZonesFile(itxt));
			for i=1:nZone(itxt)
    			String=fgetl(DataFile(itxt));
				sZoneParam=fgetl(ZonesFile(itxt));
                dWork=str2num(String);
				dWorkZ=str2num(sZoneParam);
				Work(i,itxt)=dWork(3)/dWorkZ(3);
            end
            for cnt=1:nDataFiles
				vWork(:)=vWork(:)+Work(:,cnt);
			end;
			frewind(ZonesFile(1));
			sZoneParam=fgetl(ZonesFile(1));
			sZoneParam=fgetl(ZonesFile(1));
			sZoneParam=fgetl(ZonesFile(1));
			sZoneParam=fgetl(ZonesFile(1));
			sZoneParam=fgetl(ZonesFile(1));
			if length(vWork)==nBlocks(1)*nBlocks(2)+1
				for cnt=1:length(vWork)-1
					sZoneParam=fgetl(ZonesFile(1));
					dWorkZ=str2num(sZoneParam);
					%i=uint8(1+fix((dWorkZ(4)+dSize(1)*0.5)/dWorkZ(7)));
					%j=uint8(1+fix((dWorkZ(6)+dSize(2)*0.5)/dWorkZ(9)));
					mSort(dWorkZ(10),dWorkZ(11))=vWork(cnt);
                    surf(vz,vx,mSort);
                    C=mSort;
				end
			else
				disp('Не могу отсортировать');
				C=vWork;
			end
    		%nCurrentLine=nCurrentLine+nZone(itxt)+1;
		case 'Concentration'
    		for cnt=1:(nZone(itxt)+4)
    			String=fgetl(DataFile(itxt));                                                               %Строка с дозвым распределением (на самом деле только заголовок)
            end
			%nCurrentLine=nCurrentLine+nZone+4;
			sZoneParam=fgetl(ZonesFile(itxt));
            for i=1:nZone(itxt)
    			String=fgetl(DataFile(itxt));
				sZoneParam=fgetl(ZonesFile(itxt));
        		dWork=str2num(String);
				dWorkZ=str2num(sZoneParam);
    			Work(i,itxt)=dWork(8)/dWorkZ(2);
            end
			for cnt=1:nDataFiles
				vWork(:)=vWork(:)+Work(:,cnt);
			end;
    		C=vWork;
			%nCurrentLine=nCurrentLine+nZone;
        end
		fclose(DataFile(itxt));
		fclose(ZonesFile(itxt));
		itxt=itxt+1;
	end
	clear dWork nCurrentLine String i itxt cnt;
end
