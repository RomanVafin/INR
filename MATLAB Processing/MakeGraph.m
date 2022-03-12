function MakeGraph(Con);

z=0.0:0.1:30.0;
dMaxCon=max(Con(:,6));

hfig1=figure('Color','w','Position', [30 10 1400 1050]);
yData=fliplr(Con);
stairs(z,yData,'linewidth', 1.5);
axesHandle1=hfig1.CurrentAxes;
set(axesHandle1, 'FontSize', 14);
title('Распределения коцентрации ПЭТ изотопов по глубине','fontsize', 20);
xlabel('z (cm)','fontsize',14);
ylabel('Concentration (cm^-^3)','fontsize',14);
legend({'Total','O^1^5','O^1^4','N^1^3','C^1^1','C^1^0'},'FontSize',14,'Location','northwest');
legend('boxoff');

hfig2=figure('Color', 'w');
set(hfig2, 'Position', [30 10 1400 1050]);
z=[z; z];
z=z(2:end);
yData=zeros(length(z),4);
dWork=transpose([Con(:,5)/dMaxCon Con(:,5)/dMaxCon]);
yData(:,1)=dWork(1:end-1);
dWork=transpose([Con(:,3)/dMaxCon Con(:,3)/dMaxCon]);
yData(:,2)=dWork(1:end-1);
dWork=transpose([Con(:,2)/dMaxCon Con(:,2)/dMaxCon]);
yData(:,3)=dWork(1:end-1);
dWork=transpose([(Con(:,6)-transpose(sum(transpose(Con(:,[2 3 5])))))/dMaxCon (Con(:,6)-transpose(sum(transpose(Con(:,[2 3 5])))))/dMaxCon]);
yData(:,4)=dWork(1:end-1);
area(z,yData);
axesHandle=gca;
set(axesHandle, 'FontSize', 14);
title('Доли концентраций ПЭТ изотопов','FontSize',20);
xlabel('z (cm)','FontSize',14);
legend({'O^1^5','O^1^5 + N^1^3','O^1^5 + N^1^3 + C^1^1','Total'},'FontSize',14,'Location','northwest');
legend('boxoff');

clear z dWork;