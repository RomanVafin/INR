function MakeOutput(dMaxd,dMaxt,dMaxta,dMaxoc,dMaxoa,dMaxla,iPosd,iPost,iPosta,iPoso,iPosoa,iMaxla,nStat)
fOutFile=fopen('Out\Sum.dat','a+');
fprintf(fOutFile,'% 4.3e\t% 8.2f\t% 6.4e\t% 8.2f\t% 6.4e\t% 6.4e\t% 8u\t% 8u\t% 8u\t% 8u\t% 8u\t% 8u\t% 6.2e\n',...
					dMaxd,dMaxt,dMaxta,dMaxoc,dMaxoa,dMaxla,iPosd,iPosd-iPost,iPosta,iPosd-iPoso,iPosoa,iMaxla,nStat);
fclose(fOutFile);
