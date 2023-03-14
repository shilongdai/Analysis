# May 2022 Chicago Apartment Analysis

## Key Findings

-   Zip code areas near the lake, as well as area around downtown affects the rent positively, while areas in south Chicago and the northern tip of Chicago are negatively related to rent

-   Increasing number of bedrooms has a diminishing multiplicative marginal effect on the rent. Going from studio to one bedroom leads to approx. 13% increase in rent. However, going from one bedroom to two, or two bedroom to three is associated with approx. 7% increase in rent compared to the previous number of bedrooms.

-   Increasing number of bathrooms has a potentially increasing trend with respect to multiplicative marginal effect. Thus, it is plausible that the number of bathroom is a proxy for factors such as the number of floor in a unit of the apartment.

-   Square footage has a positive multiplicative effect on the rent, with the exception of a few apartments having slightly more than 200 sqft. The marginal effect of square feet is generally decreasing as the square footage gets larger.

## Introduction

In May of 2022, one of my main interest was to find an apartment in Chicago as a got admitted to the UChicago MScA graduate program. However, I did not know much about the apartment market in Chicago. Thus, in order to pick a comfortable apartment without paying an extraordinary price, I decided to take a data driven approach to learn about the Chicago apartments at that time. In order to collect apartment data, I created a Selenium based webscrapper at <https://github.com/shilongdai/Apartment_Scraper> that extracted apartment information from Apartments.com. The data collection process finished at around May 25th, 2022. Then, using the scrapped data, several models were built to estimate the contribution of various factors on rent. Using the models, I was able to select candidate apartments to check out when I eventually visited Chicago. Here, some of the results from the analysis I conducted for apartment searching are compiled.

## Methodology

The following steps were taken to arrive at the final model results of the analysis

1.  Data Collection: The apartment data were fetched from Apartments.com and converted to CSV format

2.  EDA/Data Cleaning: The variables from the webscrape were examined. Some data entry errors were corrected, and some filtering was conducted to arrive at the final target for analysis

3.  Filling missing square feet: One discovery from EDA was that around 3k out of 17k apartments had missing square feet information. Thus, in order to avoid bias, a detour had to be taken that involved using other variables to predict square feet.

4.  Feature Selection/Engineering: There are a few hundred columns in the original scraped CSV file. Some of the features are not appropriate to be used right away, and some are not really proper for the analysis. Thus, some feature engineering had to be done prior to the modeling.

5.  Modeling: A GAM model with transformations is fitted in the end.

6.  Model Assessment: The model was assessed with cross validation. No test set were allocated because the model was not for extrapolation, and it is impossible to find an apartment now from May 2022.

7.  Interpretation: The output of the model was interpreted, and the effect of different attributes of an apartment on rent was assessed.

### Feature Engineering

During the EDA/Data cleaning phase, it was found that in some apartment complexes, there are units with very high prices along with regular priced units. Since the main interests are not exotic units, they are filtered out by eliminating units from a complex with rents greater than 3 mean absolute deviance from the median value. In addition, there are units that are extremely expensive with greater than \$8000 rent per month. Those units are filtered out as well since they are clearly not meant for regular renters. Then, considering the size of the apartment, there are many apartments with almost 0 square feet reported. In the end, 200 square feet was set as the bottom limit for the size of the apartment. Additionally, apartments with more than three bedrooms, and with more full bathroom than bedrooms are removed. The apartments with more than 3 bedrooms are rare with a wide variety of archetypes. Some are almost like town homes, while others are like dorms. Thus, they are outside of the interests for the analysis. The same can be said for apartments with more bathrooms than bedrooms, and in those cases, some can be data entry error as well. Finally, after using geolocation with the shapefiles provided by the City of Chicago, a segment of apartments are actually not located in Chicago proper. Thus, those apartments are removed as well. At the end of the process, there are approx. 16K units remaining in the dataset.

After narrowing down the scope, a separate mini-project was undertaken to fill in the missing square feet. A random forest was used for variable importance. Then, an ensemble of random forest, regression Adaboost, and bagged Adaboost was used on the important variables to interpolate the square feet. The train and test MAE of the model was around 61 and 112 square feet respectively. Then, a final model was fitted on all units with non-missing square feet, and the model was used to fill in the missing square feet for the rest of the units. With the missing square feet filled in, the original analysis was ready to move on to feature engineering.

While picking the feature to use, an important criteria was whether the feature is reliable and understood. Apartments.com had a lot of auxiliary information such as the number of shopping centers, recreational centers, and walk scores etc. However, it is unclear what criteria was used in generating those information. Thus, they are not really reliable or well understood enough. In addition, the site also provides amenities information. However, some of the apartments seem to have used relatively standard tags for amenities. On the other hand, it seems to be possible to have custom defined names for amenities as well. Thus, parsing the amenities of the apartment would have been an NLP undertaking. While possible as a next step, doing NLP analysis to aggregate amenities tags was not on the agenda at the moment, and filtering it by hand would have taken a decent amount of time. Thus, the amenities were not used since it was difficult to clean. Thus, in the end, the following features were picked.

| Feature               | Type        | Description                               |
|-----------------------|-------------|-------------------------------------------|
| Square feet           | Numerical   | The square footage of apartment           |
| Zip                   | Categorical | The zip code for the apartment            |
| Beds                  | Categorical | The number of bedrooms for apartment      |
| Baths                 | Categorical | The number of bathrooms                   |
| Regressed Square Feet | Categorical | Whether the square feet was missing       |
| Covered Parking       | Categorical | Whether the apartment has covered parking |
| Garage                | Categorical | Whether the apartment has garages         |
| Lot                   | Categorical | Whether the apartment has a parking lot   |
| Street                | Categorical | Whether the apartment has street parking  |

: Features Used

### Model Fitting/Assessment

In addition to picking the variables, log transformation was tried with the square feet feature and the rent target variable. Furthermore, since zip, beds, and baths had numerous levels, Fused LASSO was applied to consolidate the levels. Fused LASSO is a generalization of the LASSO, where in addition to the $|\beta|$ penalty, it supports shrinking the coefficients for feature $i, j$ together via the penalty $|\beta_i - \beta_j|$. Thus, by running different levels of the penalty with AIC as the evaluation criteria, a trade-off was made in reducing the degree of freedom due to the categorical variables such as zip, and the performance of the model on the training set. Finally, a GAM model with thin-plate smooth on square feet predicting rent, a GAM model with thin-plate smooth on log square feet predicting log rent, and a log-log linear model were tried and assessed via 10-fold cross validation. The result is shown below.

![CV Result](https://github.com/shilongdai/Analysis/raw/master/Apartments/Images/cvResult.png)

While the CV RMSE is fairly close for the three method, it can be seen that the IQR of the log log GAM model was shifted more towards 0 than the others. Thus, the GAM with logged rent and square feet was picked as the model form in the end.

On the full training set, the GAM was able to achieve an $R^2$ of approx. 79%, and an adjusted $R^2$ of around 78.4%. Thus, after adjusting for the degree of freedom of the model, there was not a great decline in the variance explained. A visual inspection of the normal Q-Q plot shows that the residuals follow the normal distribution within $|2|$ theoretical quantiles. However, a Lilliefors test shows that there are significant deviation from normality likely due to the large sample size. While the normality assumption can be argued based on visual evidence, there are both visual evidence for heteroskedacity and statistically significant evidence based on the Breusch-Pagan test with p-value indistinguishable from 0. The Durbin-Watson test also shows that there are significant correlation among the residuals. Thus, in light of the violation of the assumptions, a more conservative interpretation of the statistical results from the model should be taken. However, it is also worthy to note that almost all coefficients from the model are highly significant with p-value almost indistinguishable from 0. Thus, considering the robustness of the tests and confidence intervals from least square regression, despite the violation of some assumptions, some confidence can be restored in the output of the model.

## Insights from EDA

Prior to exhibiting the model results, some contextual information from the EDA may be helpful to place the model results in the context of the apartments in Chicago.

From the plot below, it can be seen that there seem to be three hot spots for apartment. The two centers in the north are located around downtown, while the bottom less intense center is around the UChicago campus area.

![Apartment Locations](https://github.com/shilongdai/Analysis/raw/master/Apartments/Images/ApartmentDistributed.png)

The distribution of square feets are shown below. The mode and median of the apartments are located at around 900 square feet. However, the distribution is skewed to the right, which means that there are some pretty large apartments at the right tail of the distribution. A log transformation was applied so that the distribution flattens out a bit and became more symmetrical.

![Distribution of Square Feet](https://github.com/shilongdai/Analysis/raw/master/Apartments/Images/SqftEDA.png)

The distribution of rent is shown below. Similar to square feet, it was also skewed to the right. Furthermore, there are potentially multiple modes in the distribution. It seems that there may be a bulk of apartments with rent around 1000 and 2000 followed by a long tail of more expensive apartments.

![Distribution of Rent](https://github.com/shilongdai/Analysis/raw/master/Apartments/Images/RentEDA.png)

Finally, the distribution of beds and baths are shown below. Almost all of the apartments have less than 4 bedrooms and 3 bathrooms. In the model, the apartments are the ones with up to 3 bedrooms and up to 3.5 bathrooms.

![Distribution of Beds and Baths](https://github.com/shilongdai/Analysis/raw/master/Apartments/Images/BedsBathsEDA.png)

## Insights from the Model

The multiplicative effect of square feet is shown below. There are only a few data points with more than 2000 square feet. With only a few points, the spline becomes more unstable with large confidence interval. Thus, the attention was focused on the segment with sufficient data to have tighter confidence intervals and more stable estimates. Now, with the restriction in place, there is a general increasing effect with greater square footage. Furthermore, as the square feet increases, compared to the smaller apartments, the increase in multiplicative effect for the larger apartment is diminishing. For a small group of dorm sized apartments, the small size lead to a reduction in the rent. However, the effect quickly became positive as the square footage approaches 500 sqft. Finally, it is worth noting that the the effect curve is not very smooth. Combined with the fact that there may be omitted effects that lead to bias from the model diagnosis earlier, it may be that the square feet have acted as a proxy variable for some unincluded factors in the model. For instance, as the apartments get larger, they are likely to become more luxurious with more amenities. Then, for the larger apartments, there are several spikes in the estimated effects of square feet. It is possible that the spikes may be actually better explained by factors such as amenities, which are not included. Thus, a potential improvement for the model is to reliably include more factors, which could make it more clear on whether the square footage has an actually complicated structure with respect to effects on rent.

![Effect of Square Feet](https://github.com/shilongdai/Analysis/raw/master/Apartments/Images/sqftEffect.png)

The map of multiplicative effects by zip codes is shown below. The reference level for zip is zip area with the median rent. From the map, it seems that the coastal areas, as well as the areas around and north of downtown correspond to higher apartment rent. Then, the southern area inland as well as the most northern zip codes have a reduced rent compared to the median zip code. While the relatively lower rent associated with the southern area is understandable due to the security issue in south Chicago, it is surprising that the northern tip also has a reduced rent. Some Google search reveals that it may be entering Northern Chicago, which is not the same as Chicago. Consequently, it may be transitioning into lower density areas with land use not as tight as Chicago proper.

![Effect associated with zip](https://github.com/shilongdai/Analysis/raw/master/Apartments/Images/ZipEffect.png)

There are significant multiplicative effects on the rent depending on whether it's a studio, or apartment with various number of bedrooms. The increase in rent from a studio to a single bedroom apartment is slightly lower than 1.15 times. Then, for each subsequent number of bedrooms, the apartments get around 0.05 times more expensive compared to the studio apartments.

![Effects of bedrooms](https://github.com/shilongdai/Analysis/raw/master/Apartments/Images/BedEffect.png)

A different way of looking at the contribution of bedrooms is to consider the increase in rent for an additional bedroom. Then, despite the increase in rent compared to the studio case being almost linear in the previous plot, the marginal increase for each bedroom is diminishing. While going from studio to one bedroom would lead to an approximately 13% increase in rent, going from one bedroom to two would only lead to an approximately 7% increase in rent. There does not seem to be significant difference in the marginal increase from two to three bedroom compared to one to two. Considering that as the bedroom increases, the rent increases, so that a multiplicative increase from the previous number of bedrooms would have a greater increase in raw rent, the decrease in marginal multiplicative effect can control the actual raw increase in rent.

![Marginal effect of bedrooms](https://github.com/shilongdai/Analysis/raw/master/Apartments/Images/marginalBed.png)

The bathroom case seems to be more interesting. As the number of bathroom increases, there seems to be more variety in the rent of the apartments. The addition of a half-bath can be attributed with around 8% increase in the rent from a single bathroom apartment. Then, adding a full-bathroom from a single bathroom can be attributed with around 20% increase from a single bathroom. Interestingly, 2 bathrooms with a half bath is not significantly different from 3 bathrooms, where both can be attributed with around 35-40% increase in rent from single bath. Finally, having 3 full baths with a half bath can be attributed with an increase in rent on the magnitude of 55-100% compared to single bath. The large confidence interval can be attributed to the relatively small number of apartment with these many bathrooms. However, it is clear that despite the large range, apartments with 3 bath and a half bath are fairly luxurious compared to the single bath apartments. In fact, even starting from the 2.5 bathroom apartments, the increase in multiplicative effect is disproportional to the increase seen in the 1.5 and 2 bath apartments. The disproportional change may suggests that the bathrooms are correlated with some form of luxuriousness as the apartments become sort of like a house.

![Effect of Bathrooms](https://github.com/shilongdai/Analysis/raw/master/Apartments/Images/BathEffect.png)

The point marginal effect of bathrooms is increasing with the exception of three bathrooms vs 2.5 bathrooms. However, there are some overlaps in the confidence intervals, so that the difference in marginal effects are not as significant as the bedroom case. Nevertheless, intuitively, it would seem unlikely that for each additional bathroom/half-bath, one has to pay an increasing extra amount of rent just because of the added bathroom. It seems more plausible that the number of bathroom is a proxy for other factors, such as the apartment having two floors for instance, where a half bath would be located on the first floor.

![Marginal effect of bathrooms](https://github.com/shilongdai/Analysis/raw/master/Apartments/Images/maginalBath.png)
