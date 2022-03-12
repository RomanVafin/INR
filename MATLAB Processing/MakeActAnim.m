function MakeActAnim(mActiv,vConst)

z=0.0:0.1:29.9;
dShare=1.0; 				%fracture of O13(5) -> N13(4)
nTimeScale=1;
dSeparate=log(2)/60;
dMax=max(mActiv(:,10));
hfig1=figure('Color','w','Position', [30 10 1400 1050]);
%axis ([0 30.0 0 1.1*dMax]);
sname=sprintf('t=% i',0);
hfig1.Name=sname;
mData=mActiv(1:300,1:11);
%hold on
%for index=1:11
%	plotActiv(index)=stairs(z,mData(:,index),'linewidth', 1.5);
%end
plotActiv=stairs(z,mData(:,11),'linewidth', 1.5);
pause(0.1);
%hold off
for it=1:120*nTimeScale
	sname=sprintf('t=% 4.2f',it/nTimeScale);
	hfig1.Name=sname;
	%mData(:,4)=mData(:,4)*exp(-vConst(4)/nTimeScale)+vConst(4)*dShare*mData(:,5)*(1-exp((vConst(5)-vConst(4))/nTimeScale))/(vConst(4)-vConst(5));
	mData(:,4)=mActiv(1:300,4)*exp(-vConst(4)*it/nTimeScale)+vConst(4)*dShare*mActiv(1:300,5)*(exp(-vConst(5)*it/nTimeScale)-exp(-vConst(4)*it/nTimeScale))/(vConst(4)-vConst(5));
    for index=[1:3,5:9]
		mData(:,index)=mData(:,index)*exp(-vConst(index)/nTimeScale);
	end
	mData(:,10)=sum(mData(:,1:9),2);
	mData(:,11)=sum(mData(:,vConst<dSeparate),2);
    dMax=max([mData(:,10);1e4]);
    %{
    if it<10*nTimeScale
        dMax=max([mData(:,4); vCheck]);
    elseif it<40*nTimeScale
        if mod(it,5*nTimeScale)==0
            dMax=dMax*0.5;
        end
    else
        dMax=1e2;
    end
    %}
	axis ([0 30.0 0 dMax]);
	%for index=1:11
	%	set(plotActiv(index),'Ydata',mData(:,index));
	%end
    set(plotActiv,'Ydata',mData(:,10));
	pause(0.1);
end

