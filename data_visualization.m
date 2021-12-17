close all; clear; clc;
% Data visalization
%files1 = dir('tests_2-3moves/cr-0.5_mr-0.5/*.csv');
files1 = dir('tests_2-6moves/cr-0.0_mr-0.0/*.csv');
files2 = dir('tests_2-6moves/cr-0.0_mr-0.5/*.csv');
files3 = dir('tests_2-6moves/cr-0.5_mr-0.1/*.csv');
files4 = dir('tests_2-6moves/cr-0.5_mr-0.5/*.csv');
%fullpaths1 = fullfile({files1.folder}, {files1.name});
fullpaths1 = fullfile({files1.folder}, {files1.name});
fullpaths2 = fullfile({files2.folder}, {files2.name});
fullpaths3 = fullfile({files3.folder}, {files3.name});
fullpaths4 = fullfile({files4.folder}, {files4.name});
fullpaths_total = [fullpaths1; fullpaths2; fullpaths3; fullpaths4];
number_of_test = min(size(fullpaths_total));
figure(1)
hold on;
title('Fitness over generations, for each child that solves the scramble')
titles = [{"Fitness of best child over generations","CR = 0.0, MR = 0.0"};{"Fitness of best child over generations","CR = 0.0, MR = 0.5"};{"Fitness of best child over generations","CR = 0.5, MR = 0.1"};{"Fitness of best child over generations","CR = 0.5, MR = 0.5"}
           {"# of moves vs fitness","CR = 0.0, MR = 0.0"};{"# of moves vs fitness","CR = 0.0, MR = 0.5"};{"# of moves vs fitness","CR = 0.5, MR = 0.1"};{"# of moves vs fitness","CR = 0.5, MR = 0.5"}];
avg = zeros(number_of_test,300);
last_fitness = zeros(number_of_test,300);
for j=1:number_of_test
    fullpaths = fullpaths_total(j,:);
    
    for i=1:300
        T = readtable(cell2mat(fullpaths(i)));
        T = T(1:end-2,1:2);
        avg(j,1:length(T.maxFitness)) = avg(j,1:length(T.maxFitness)) + T.maxFitness';
        last_fitness(j,i) = T.maxFitness(end);
        if T.maxFitness(end) >= 54
            subplot(2,number_of_test,j);
            hold on;
            xlabel('Generation')
            ylabel('Fitness')
            title(titles(j,:))
            plot(T.maxFitness)
            hold off;
            subplot(2,number_of_test,j+number_of_test);
            hold on;
            xlabel('Fitness')
            ylabel('# Moves')
            title(titles(j+number_of_test,:))
            plot(T.maxFitness, strlength(T.bestChild))
            sgtitle('Plots for childs that solves the scrambles')
        end
    end
end
saveFigureAsPDF(gcf,'individual_fitness')
hold off;
CR_MR_str = {'CR = 0.0, MR = 0.0','CR = 0.0, MR = 0.5','CR = 0.5, MR = 0.1', 'CR = 0.5, MR = 0.5'};
figure(2)
avg = avg/300;
plot(avg')
hold on;
xlabel('Generation')
ylabel('Fitness')
title('Average fitness over population at each generation')
legend(CR_MR_str,'Location','southeast');
hold off;
saveFigureAsPDF(gcf,'average_fitness')
figure(3)
hold on;
ylabel('Fitness')
title('Fitness of best child in population at last generation')
ylim([40 55])
boxplot(last_fitness', 'Labels', CR_MR_str)
saveFigureAsPDF(gcf,'best_fitness_boxplot')

function saveFigureAsPDF(fig, path)
set(fig, 'PaperPosition', [-3.5 0 40 20])
set(fig, 'PaperSize', [33 20])
saveas(fig, path, 'pdf')
end
