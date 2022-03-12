clc;
clear variables;

DataDir=dir('Data');

Work=GetAll(DataDir);
n=length(Work);
nCheckZones=length(Work(n).dose);
dLam=log(2)./[19.290, 20.334*60, 0.011, 9.965*60, 0.00858, 70.598, 122.24, 64.49, 109.771*60];		% ln2/T(1/sec) for C10 C11 N12 N13 O13 O14 O15 F17 F18
dLamSep=log(2)/60;
dTSep=log(2)/0.037;
mAct=zeros(nCheckZones, 12);

DoseSum=Work(n).dose;
Con(:,1)=Work(n).petIsotope(:,1);												%C10Con
Con(:,2)=Work(n).petIsotope(:,2);												%C11Con
Con(:,3)=Work(n).petIsotope(:,4);												%N13Con
Con(:,4)=Work(n).petIsotope(:,6);												%O14Con
Con(:,5)=Work(n).petIsotope(:,7);												%O15Con
Con(:,6)=sum(Work(n).petIsotope,2);                                     		%TotCon
checkCon=Work(n).petIsotope(:,dLam<dLamSep(1)*4);
for i=1:9
	mAct(:,i)=(2.7027*1e-8)*Work(n).petIsotope(:,i)*dLam(i)/Work(n).statistic  ;                    % 1 [mCi/proj/cm3] || 2,7027*1e-8 [1/sec/cm3/proj]
end
dCNShare=0.89;
mAct(:,10)=sum(mAct(:,[1,2,4:9]),2);
mAct(:,11)=sum(mAct(:,dLam<dLamSep),2);
mAct(:,12)=mAct(:,4)*exp(-dLam(4)*120)+...
		   dLam(4)*dCNShare*mAct(:,5)*...
		   (exp(-dLam(5)*120)-exp(-dLam(4)*120))/(dLam(4)-dLam(5)); 								%O13->N13 decay
for i=[1:3,5:9]
   mAct(:,12)=mAct(:,12)+mAct(:,i)*exp(-dLam(i)*120);
end
%MakeDat(DoseSum,Con(:,1),Con(:,2),Con(:,3),Con(:,4),Con(:,5),Con(:,6));
MakeDat(DoseSum,Con,mAct);														% mGy | 1/cm3 | mCi/cm3/proj
%MakeGraph(Con(1:301,:));
%animation for activity
%MakeActAnim(mAct,dLam);

nZones=length(DoseSum);
DoseSum(:)=0.0;
vCon=zeros(nZones,1);
vTot=zeros(nZones,1);
vOAct=zeros(nZones,1);
vAct=zeros(nZones,n);
vTimeAct=zeros(nZones,n-1);
nStat=0;
for i=1:n-1
	DoseSum=DoseSum+Work(i).dose;
	vTot=vTot+sum(Work(i).petIsotope,2);
	vCon=vCon+Work(i).petIsotope(:,7);
	nStat=nStat+Work(i).statistic;
	vOAct=vOAct+(2.7027*1e-8)*Work(i).petIsotope(:,7)*dLam(7)/Work(i).statistic/(n-1);
	vWork=sum(Work(i).petIsotope(:,1:9)*dLam',2);
	vWork2=sum(Work(i).petIsotope(:,[1:3,5:9])*(dLam([1:3,5:9]).*exp(-dLam([1:3,5:9])*120))',2);
	vWork2=vWork2+Work(i).petIsotope(:,4)*dLam(4)*exp(-dLam(4)*120)+...
		   dLam(4)*dLam(5)*dCNShare*Work(i).petIsotope(:,5)*...
           (exp(-dLam(5)*120)-exp(-dLam(4)*120))/(dLam(4)-dLam(5));
	vAct(:,i)=(2.7027*1e-8)*vWork/Work(i).statistic;												%mCi/cm3/proj
	vTimeAct(:,i)=(2.7027*1e-8)*vWork2/Work(i).statistic;											%mCi/cm3/proj
	vAct(:,n)=vAct(:,n)+vAct(:,i)/(n-1);
	[dMD, iMD]=max(DoseSum);
	[dMT, iMT]=max(vTot);
	[dMO, iMO]=max(vCon);
	[dMOA, iMOA]=max(vOAct);
	[dMTA, iMTA]=max(vAct(:,n));
	[dMLA, iMLA]=max(sum(vTimeAct,2));
	if (mod(i,3)==1)||(i==n-1)
		MakeSum(dMD,dMT,dMTA,dMO,dMOA,dMLA,iMD,iMT,iMTA,iMO,iMOA,iMLA,nStat);
    end
end
