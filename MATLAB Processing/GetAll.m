function C=GetAll(Dir)
%clc; clear variables;
%Dir=dir('Data');

nDataFiles=length(Dir)-2;
itxt(1:nDataFiles)=0;
cnt=0;

%Параметры цилиндра (cm,cm,g/cm3)
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

ZonesFile=fopen('Zones\zones.dat', 'r');

if nDataFiles==0&&cnt==0
	C=0;
	disp('Нет .dat файлов');
else
	nParam=7;
	nDataFiles=cnt;
	DataFile(1:nDataFiles)=0;
	data=struct('fileName', '', 'statistic', 1, 'nZone' , 1, 'dose', [], 'petIsotope', []);
	
	itxt=1;
	while itxt<=nDataFiles&&l(itxt)~=0
		filename=Dir(l(itxt)+2).name;
		data(itxt).fileName=filename;
		filename=['Data\',filename];
		DataFile(itxt)=fopen(filename,'r');
		String=fgetl(DataFile(itxt));                                                                   %Строка с NSTAT
		data(itxt).statistic=str2double(String);
		String=fgetl(DataFile(itxt));                                                                   %Строка с NZON
		data(itxt).nZone=str2double(String);
		itxt=itxt+1;
	end
	clear filename sExt;
			
	%mAns(1:nMaxZone,1:nParam)=0;
	%mAns(1,nParam)=sum(nStat);
	%mWork(1:nMaxZone,1:(nParam-1))=0;
	%vWork(1:nMaxZone)=0
	
	nMaxZone=max([data(:).nZone]);
	sZoneParam=fgetl(ZonesFile);
    sZoneParam=fgetl(ZonesFile);
	dWorkZ=str2num(sZoneParam);
	fclose(ZonesFile);
	
	itxt=1;
	while  itxt<=nDataFiles&&l(itxt)~=0																	%Считывание дозы
		data(itxt).dose=zeros(nMaxZone,1);
		data(itxt).petIsotope=zeros(nMaxZone,9);
		nCurrentLine=2;
		String=fgetl(DataFile(itxt));																	%Строка с дозвым распределением (на самом деле только заголовок)
		for i=1:data(itxt).nZone
    		String=fgetl(DataFile(itxt));
			nCurrentLine=nCurrentLine+1;
            dWork=str2num(String);
			data(itxt).dose(i)=dWork(3)/dWorkZ(4)*1.6e-7;												%MeV/g -> mGy
        end	

    	for cnt=1:4
    		String=fgetl(DataFile(itxt));
			nCurrentLine=nCurrentLine+1;
        end
        for i=1:data(itxt).nZone																			
    		String=fgetl(DataFile(itxt));
			nCurrentLine=nCurrentLine+1;
        	dWork=str2num(String);																		%Считывание концентрации ПЭТ изотопов
			for cnt=1:9
				data(itxt).petIsotope(i,cnt)=dWork(2+cnt)/dWorkZ(3);									%1/cm3
			end
		end
		
		fclose(DataFile(itxt));
		itxt=itxt+1;
	end
	
	iSum=itxt;
	itxt=1;
	data(iSum).fileName='Sum';
	data(iSum).statistic=0;
	data(iSum).nZone=nMaxZone;
	data(iSum).dose=zeros(nMaxZone,1);
	data(iSum).petIsotope=zeros(nMaxZone,9);
	while  itxt<=nDataFiles&&l(itxt)~=0
		data(iSum).statistic=data(iSum).statistic+data(itxt).statistic;
		data(iSum).dose=data(iSum).dose+data(itxt).dose;
		data(iSum).petIsotope=data(iSum).petIsotope+data(itxt).petIsotope;
		itxt=itxt+1;
	end
	C=data;
	clear dWork nCurrentLine String i itxt cnt;
end
