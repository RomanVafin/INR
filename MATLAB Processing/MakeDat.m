function MakeDat(vDose,mConData,mActData)

%Check isotopes
%mGy | 1/cm3 | mCi/cm3/proj
vC10Con=mConData(:,1);
vC11Con=mConData(:,2);
vN13Con=mConData(:,3);
vO14Con=mConData(:,4);
vO15Con=mConData(:,5);
vPET=mConData(:,6);
vC10Act=mActData(:,1);
vC11Act=mActData(:,2);
vN13Act=mActData(:,4);
vO14Act=mActData(:,6);
vO15Act=mActData(:,7);
vTotAct=mActData(:,10);
vLongAct=mActData(:,11);
vTimeAct=mActData(:,12);
fOutFile=fopen('Out\Dose.dat','wt+');
fprintf(fOutFile, ' z\t\t  Dose\t\t (O14)Con.\t(C10)Con.\t(N13)Con.\t(C11)Con.\t(O15)Con.\ttot.con.\t(C10)Act\t(C11)Act\t(N13)Act\t(O14)Act\t(O15)Act\ttot.act.\tlong.act.\ttot.act.(2min)\n');
fprintf(fOutFile, '(cm)\t   (mGy)\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t (1/cm3)\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tmCi/proj\t\n');
if length(vDose)==length(vO15Con)
	for cnt=1:length(vDose)
		fprintf(fOutFile,'% 4.1f\t% 4.3e\t% 9.2f\t% 9.2f\t% 9.2f\t% 9.2f\t% 9.2f\t% 8.2f\t% 6.4e\t% 6.4e\t% 6.4e\t% 6.4e\t% 6.4e\t% 6.4e\t% 6.4e\t% 6.4e\n',...
				cnt*0.1,vDose(cnt),vO14Con(cnt),vC10Con(cnt),vN13Con(cnt),vC11Con(cnt),vO15Con(cnt),vPET(cnt),...		%check cnt*0.1=z(cm)!
				vC10Act(cnt), vC11Act(cnt), vN13Act(cnt), vO14Act(cnt), vO15Act(cnt),vTotAct(cnt),vLongAct(cnt),vTimeAct(cnt));
	end
else
	disp('Ты дурак');
end
fclose(fOutFile);