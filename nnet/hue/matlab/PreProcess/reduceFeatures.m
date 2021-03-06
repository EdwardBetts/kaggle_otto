function reduceFeatures
% Remove outlier from data using PCA and Mahal distance
% For each class:
% - remove outliers 
% - save to file, 1 file per class 

    pathIn = '..\..\Data\RemoveOutliers\';
%     pathIn = '..\..\Data\Classes\';
    pathOut = '..\..\Data\ReducedFeatures\';
    numClasses = 9;
    percentageFeatures = 0.90;
    
    outlierOpt = 155;     
%     < 1: exlude n% samples that have highest Mahalanobis Distance
%     example value: 0.95
%     outlierOpt = threshold;     
%     threshold > 1: exclude samples that have Mahalanobis
%     Distance > threshold, example value: 150 or 200, 
%     keyword: Chi square table
%     http://sites.stat.psu.edu/~mga/401/tables/Chi-square-table.pdf
    
    for i =1:numClasses
        data = csvread(strcat(pathIn, sprintf('%d.csv',i)));
        N = size(data, 1);
        fprintf('Class %d:\t%6.0f\t', i, N);        
        X_i = zscore(data(:, 1:end-1));
%         X_i = (data(:, 1:end-1));
        
        % find the number of components which count 95% of the features
%         [~, ~, ~, ~, explained] = pca(X_i);        
%         cumSum = cumsum(explained);
%         numComponents = find(cumSum < percentageFeatures*cumSum(end), 1, 'last');
%         fprintf('%d\n', numComponents);
%         % visuallization
%         plot(cumSum(1:numComponents));

        numComponents = 72;
        
        [coeff, score, latent, tsquared, explained] = pca(X_i, 'NumComponents', numComponents);
%         residuals = sum((X_i - score*coeff').^2, 2);
%         %         % equipvalent to these:
%         %         residuals = pcares(X_i, numComponents);
%         %         residuals = sum(residuals .^2, 2);
% 
%         
%         % calculate Mahalanobis Distances to exclude outliers 
%         MD = mahal(score, score);
%         MD_res = mahal(residuals, residuals);
       
% %         % visuallization
%         f= figure(222);
%         scatter([1:size(MD,1)],MD);
%         title(sprintf('Mahalanobis Distances - class %d', i));
%         saveas(f, strcat(pathOut, sprintf('%d.jpg',i)));
% 
%         f= figure(222);
%         scatter([1:size(MD_res,1)],MD_res);
%         title(sprintf('Mahalanobis Distances Res - class %d', i));
%         saveas(f, strcat(pathOut, sprintf('res%d.jpg',i)));

%         if outlierOpt<1            
%             % Option 1: take n percentage of samples
%             [~,Index] = sort(MD, 'ascend');
%             numSamples = floor(outlierOpt * N);
%             idxNormals = Index(1:numSamples);
%             idxOutliers = Index(numSamples+1:end);
%             
%             [~,idxRes] = sort(MD_res, 'descend');
%             idxResidualOutliers = idxRes(1:(N - numSamples));            
%         else
%             % Option 2: take samples with Mahalanobis Distance < threshold            
%             idxNormals = find(MD<outlierOpt);
%             idxOutliers = find(MD>=outlierOpt);
%             
%             idxResidualOutliers = find(MD_res>=outlierOpt);
%         end

%         idxNormals(ismember(idxNormals, idxResidualOutliers)) = [];  % remove these from the normal set of the 90% components
%         idxOutliers = unique([idxOutliers; idxResidualOutliers]);
        
%         fprintf('%6.0f\t%6.0f\n', size(idxNormals,1), size(idxOutliers,1));
%         csvwrite(strcat(pathOut, sprintf('%d.csv', i)), [score(idxNormals, :), data(idxNormals, end)]);
%         csvwrite(strcat(pathOut, sprintf('o%d.csv', i)), [score(idxOutliers, :), data(idxOutliers,end)]);        

        csvwrite(strcat(pathOut, sprintf('%d.csv', i)), [score, data(:, end)]);
    end   
end