# Analysis
Repository for various statistics analysis/projects

## Apartments

In May of 2022, one of my main interest was to find an apartment in Chicago as a got admitted to the UChicago MScA graduate program. However, I did not know much about the apartment market in Chicago. Thus, in order to pick a comfortable apartment without paying an extraordinary price, I decided to take a data driven approach to learn about the Chicago apartments at that time. In order to collect apartment data, I created a Selenium based webscrapper at https://github.com/shilongdai/Apartment_Scraper that extracted apartment information from Apartments.com. The data collection process finished at around May 25th, 2022. Then, using the scrapped data, several models were built to estimate the contribution of various factors on rent. Using the models, I was able to select candidate apartments to check out when I eventually visited Chicago. Here, some of the results from the analysis I conducted for apartment searching are compiled.


## Wheat

Three types of wheat were examined with respect to the geometric properties of
their kernels. The source of the wheat data was the paper https://www.researchgate.net/publication/226738117_Complete_Gradient_Clustering_Algorithm_for_Features_Analysis_of_X-Ray_Images, 
which applies X-ray techniques to extract the information of the kernel automatically.

There are 7 numerical variables recorded:

- area: the area of the kernel
- parameter: the perimeter of the wheat kernel
- compactness: the geometric compactness of the shape of the kernel
- kernel length: the length of the kernel
- kernel width: the width of the kernel
- asymmetry: the asymmetry of the shape of the kernel
- grove_length: the length of the grove
- type: the type of wheat, which are Kama, Rosa, and Canadian

Exploratory data analysis were conducted to inspect the distribution of the variables.
Then, PCA was applied to reduce the dimension of the data. The result of PCA was
used to do KMeans clustering using 3 clusters. It was found that the clusters closely 
resembles the type of wheat. Finally, QDA and SVM were applied to predict the type 
of wheat from the data, with KNN as a baseline. Both achieved similar performance 
on cross validation, with an accuracy of 96.7% and 96.8%. QDA outperformed SVM by 
one error on the test set, with an accuracy of 96.23% as opposed to 94.34%.

## ApplicationOpt

The goal is to optimize the decision of applying to something like universities, positions, jobs etc. In these situations, there are multiple options, but in the end only one can be chosen. Thus, in the end, regardless of which universities, positions, or jobs that someone had applied to, the only one that matters is the one which the person chooses to accept. Hence, it is a different class of problem than the ones commonly considered, such as stock selection.

## NNMnist

A quick project to get started with CNN and Pytorch via the MNIST dataset. As a baseline, gradient boosting is applied 
to achieve an accuracy of 98%. Then, a CNN inspired by the VGG architecture is used to achieve an accuracy of 99% on 
the test set.

## YelpSentiment

This is a project that finetunes the distilled BERT model on the Yelp ratings dataset to perform sentiment classification. 
To convert the ratings data into sentiment label, the reviews with rating <= 2 are considered to be negative, while 
rating >= 4 are considered positives. The medium rating of 3 is discarded. Next, since the ratings are unbalanced with a 
large number of 4-5 star reviews, a balanced version of the training set is also created by down sampling. 
Various tuning methods were attempted for max of 4 epochs each, and the performances on a test set of around 120K 
entries are summarized below.

| Method               | Data       | Train N | F1   | Kappa |
|----------------------|------------|---------|------|-------|
| Classifier Only      | Balanced   | 217928  | 0.92 | 0.82  |
| Classifier Only      | Unbalanced | 554372  | 0.94 | 0.86  |
| Full Tuning          | Balanced   | 217928  | 0.93 | 0.84  |
| LORA                 | Balanced   | 217928  | 0.96 | 0.91  |
| LORA + Weighted Loss | Unbalanced | 554372  | 0.97 | 0.94  |

Thus, it would seem that the data size had some effect on the performance, as well as the difficulty of the optimization 
problem (full fine-tuning vs LORA).

