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

## TradeRoute

In many simulation games, there is an element of trade. Typically, the player visits various producers, which sells a certain set of good for a low price, and then delivers the goods to various consumers, which would purchase the goods for a higher price. A natural in these cases would be to maximize the profit after a successful run. For this analysis, the focus is on Star Citizen, which is a space sim game currently in development. In SC, each outposts on planets/moons, and space stations has a list of goods that they would sell and purchase. For instance, a mining outposts would sell various minerals while buying things like medical supplies. Often, the producing location would sell the goods at a cheaper price. Thus, a trading strategy would be to purchase goods from the producing locations to sell in major hubs like space stations or cities. Thus, the goal would be to determine the optimal producers/consumers to visit, and the amount to purchase/sell. The problem is NP-hard, but it can be formulated as a mixed integer programming problem under the decision theory framework.


