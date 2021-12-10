close all; clear; clc;
% Data visalization
%files1 = dir('tests_2-3moves/cr-0.5_mr-0.5/*.csv');
files2 = dir('tests_2-6moves/cr-0.5_mr-0.1/*.csv');
files3 = dir('tests_2-6moves/cr-0.5_mr-0.5/*.csv');
%fullpaths1 = fullfile({files1.folder}, {files1.name});
fullpaths2 = fullfile({files2.folder}, {files2.name});
fullpaths3 = fullfile({files3.folder}, {files3.name});
fullpaths_total = [fullpaths2; fullpaths3];
figure(1)
hold on;
title('Fitness over generations, for each child that solves the scramble')
titles = [{"Fitness of best child over generations","CR = 0.5, MR = 0.1"};{"Fitness of best child over generations","CR = 0.5, MR = 0.5"}
           {"# of moves vs fitness","CR = 0.5, MR = 0.1"};{"# of moves vs fitness","CR = 0.5, MR = 0.5"}];
avg = zeros(2,300);
last_fitness = zeros(2,300);
for j=1:2
    fullpaths = fullpaths_total(j,:);
    
    for i=1:300
        T = readtable(cell2mat(fullpaths(i)));
        T = T(1:end-2,1:2);
        avg(j,1:length(T.maxFitness)) = avg(j,1:length(T.maxFitness)) + T.maxFitness';
        last_fitness(j,i) = T.maxFitness(end);
        if T.maxFitness(end) >= 54
            subplot(2,2,j);
            hold on;
            xlabel('Generation')
            ylabel('Fitness')
            title(titles(j,:))
            plot(T.maxFitness)
            hold off;
            subplot(2,2,j+2);
            hold on;
            xlabel('Fitness')
            ylabel('# Moves')
            title(titles(j+2,:))
            plot(T.maxFitness, strlength(T.bestChild))
            sgtitle('Plots for childs that solves the scrambles')
        end
    end
end
saveFigureAsPDF(gcf,'test')
hold off;
figure(2)
avg = avg/300;
plot(avg')
hold on;
xlabel('Generation')
ylabel('Fitness')
title('Average fitness over population at each generation')
hold off;
figure(3)
hold on;
ylabel('Fitness')
title('Fitness of best child in population at last generation')
ylim([40 55])
boxplot(last_fitness', 'Labels', {'CR = 0.5, MR = 0.1', 'CR = 0.5, MR = 0.5'})

function saveFigureAsPDF(fig, path)
set(fig, 'PaperPosition', [-3.5 0 40 20])
set(fig, 'PaperSize', 1.1*[33 20])
saveas(fig, path, 'pdf')
end
