# Analysis
Repository for various statistics analysis/projects

## Apartments

The data is a set of apartment model information crawled from apartment.com on May 25th.
It contains about 17K apartment listings. Each entry is a specific type of apartment listed.
An overview of the variable is as follow:

* location informations:
    * address
    * state
    * zip
    * city
    * neighborhood
* room information:
    * beds
    * baths
    * sqft: the median sqft of the specific type of unit
    * rent: the median rent of the specific type of unit
* pet information:
    * pet.allowed: whether pets are allowed
    * pet.deposit
    * pet.fee
    * pet.rent
* parking information:
    * has.garage
    * garage.fee
    * has.lot
    * lot.fee
    * has.street
    * street.fee
    * has.convered
    * covered.fee
* counts of various types of schools listed on website, with variable *.School, and college.count
* counts of place of interests in the vicinity listed on the website
    * rec.num: number of parks or other recreational facility
    * transit.num: number of public transit stations
    * shopping.num: number of shopping centers
    * air.num: number of airports
    * rail.num: number of rail stations
    * base.num: number of military bases
* assessment of environment
    * transit.score: public transit score
    * sound.score
    * walk.score
    * bike.score
    * traffic.level
    * air.level
    * busi.level: the level of bussiness operations

The full data also has boolean variables indicating whether the given type of 
unit has a certain feature, i.e. microwave. It also has variables indicating the 
exact name of the school under the counts of the schools. However, for the initial 
analysis, they are not considered. The eventual goal is to be able to create a pricing 
model for the rent of generic apartment units based on the other information. Thus, 
it's a regression task with the goal of predicting the rent from the other variables.


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
