function D=GetDose(Dir,iCase)
%clc; clear variables;
%Dir=dir('Data'); iCase=2;

nDataFiles=length(Dir)-2;
l(1:nDataFiles)=0;
cnt=0;
for i=1:nDataFiles
	filename=Dir(i+2).name;
	itxt=length(filename);
	sExt=[filename(itxt-3),filename(itxt-2),filename(itxt-1),filename(itxt)];
	if strcmp(sExt,'.txt')
		cnt=cnt+1;
		l(cnt)=i;
	end
end

if nDataFiles==0&&cnt==0
	D=0;
	disp('Нет .txt файлов');
else
	nDataFiles=cnt;
	DataFile(1:nDataFiles)=0;
	nLineN=8;
	nLineZ=24;
	nLineD1Init=30;
	nLinesBetweenD=5;
	nZone(1:nDataFiles)=1;
	nStat(1:nDataFiles)=0;
	itxt=1;

	while itxt<=nDataFiles&&l(itxt)~=0
		filename=Dir(l(itxt)+2).name;
		filename=['Data\',filename];
		DataFile(itxt)=fopen(filename,'r');
		%nCurrentLine=0;
		for cnt=1:nLineN
			String=fgetl(DataFile(itxt));                                                                   %Строка с NSTAT
		end
		nCurrentLine=nLineN;
		i=1;
		while String(i)~=':'
			if i<length(String)
				i=i+1;
			else
				break;
			end
		end
		PosN=i+1;
		StringN=String(PosN:length(String));
		nStat(itxt)=str2double(StringN);
		
		for cnt=1:(nLineZ-nCurrentLine)
			String=fgetl(DataFile(itxt));                                                                   %Строка с NZON
		end
		while String(i)~='='
			if i<length(String)
				i=i+1;
			else
				break;
			end
		end
		%nCurrentLine=nLineZ;
		PosN=i+1;
		StringN=String(PosN:length(String));
		nZone(itxt)=str2double(StringN);
		itxt=itxt+1;
	end
	clear StringN PosN filename sExt;
	
	nMaxZone=max(nZone);
	Dose(1:nMaxZone,1:nDataFiles)=0;
	itxt=1;
	while  itxt<=nDataFiles&&l(itxt)~=0
		nCurrentLine=nLineZ;
        switch iCase 
        case 1    
            for cnt=1:(nLineD1Init-nCurrentLine)
    			String=fgetl(DataFile(itxt));                                                               %Строка с дозвым распределением (на самом деле только заголовок)
            end
    		nCurrentLine=nLineD1Init;
    		nCol=23;
            for i=1:nZone(itxt)
    			String=fgetl(DataFile(itxt));
                dWork=str2num(String);
    			Dose(i,itxt)=dWork(3);
            end
    		%nCurrentLine=nCurrentLine+nZone(itxt);
			D=Dose;
		case 2
            for cnt=1:(nLinesBetweenD+nZone(itxt)+nLineD1Init-nCurrentLine)
    			String=fgetl(DataFile(itxt));                                                               %Строка с дозвым распределением (на самом деле только заголовок)
            end
            nCurrentLine=nCurrentLine+nLinesBetweenD;
            for i=1:nZone(itxt)
    			String=fgetl(DataFile(itxt));
        		dWork=str2num(String);
    			Dose(i,itxt)=dWork(3);
            end
    		%nCurrentLine=nCurrentLine+nZone;
			D=Dose;
        end
		fclose(DataFile(itxt));
		itxt=itxt+1;
	end
	clear dWork nCurrentLine String i itxt(l) cnt;
end;
