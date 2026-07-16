# Overview 

This project predicts the number of points an NBA player will score in their next game using only information that would be available prior to tip-off. Classical statistical and machine learning models are compared while adhering to proper time-series validation. Several predictive features are engineered to improve model generalization.

# Motivation 

My initial motivation was reading [this research paper ](https://arxiv.org/html/2405.10453v1)  and I initially wanted to reproduce the paper but make my own changes such as using Python instead of R, or using Python instead of R and exploring different statistical methodologies. but I figured that I could get a lot done starting small and going my own direction.

Another reason is that NBA data is abundant and `nba_api` is a free API with very rich documentation so collecting data from it would likely be a lot more facile than other sources. Not to mention, their is no shortage of people discussing the NBA and related topics (especially with the last championship that just passed at the time of writing this. **Go Knicks!**) so getting ideas on how to approach modeling data from it and filling in gaps in domain knowledge is quite easy.

I also see that many from a more machine learning background tend to stick with just using methods from it and those from classical statistical backgrounds also like to stay within that paradigm. I wanted to include both frameworks in my modelling and I'm open to borrowing methods from other spheres in future iterations where it would be appropriate.

# Dataset

As implied before, I used the `nba_api ` library to query data for this project. I used the game logs for every player who played during the 2023-2024 season via the  `LeagueGameLog` endpoint. This gave me 26,401 observation of 572 players and 1,230 games.

# Feature Engineering

The dataset itself did not come with many features that could support my predictive goals.  This data is sequenced and there is a temporal constraint in that I can't use information that is derived from games that already happened. Doing so would cause data leakage and would lead to spurious predictions informed by data that does not yet exist. For that reason, many of the original features were not used in the models. To prevent temporal leakage, each player's games were sorted chronologically, with the first 80% used for training and the remaining 20% reserved for testing.

However, there was enough information to engineer features that are defensible and most importantly would be available prior to a given upcoming game. The engineered features were:

| Feature                | Why it might help predict points                          |
| ---------------------- | --------------------------------------------------------- |
| Previous game points   | Captures immediate form                                   |
| Rolling 5-game average | Smooths out random game-to-game noise                     |
| Days of rest           | Fatigue and recovery can affect performance               |
| Home/Away              | Home-court advantage may influence performance            |
| Opponent               | Different defenses present different levels of difficulty |

# Models

I wanted to have something largely uninformed by the features to have baselines to compare the models that I fit to. I figured that if you could simply use the averages for that season or just the average points of that player to predict and do better than ML or statistical models, then I know that the models aren't performing well at all. It is arguable that you would not know the overall mean points for the season or the mean number of points scored by a given player for the season before the start of a game in the season in the first place. This is true and a better baseline could probably be made but I argue that if my models could even beat a naïve guess from someone who somehow had data from the future, then they are at least worth considering.

I used linear regression because it is very simple, ubiquitous, interpretable out of the box, and is a high-bias but low-variance model that is quite robust against overfitting. A Random Forest is a non-linear, tree-based ensemble model that may be prone to overfitting but offers potentially high predictive power due to it being low-bias, high-variance.

At first, I wanted to used Poisson regression as another model since the data the number of points $\in \mathbf{N_0}$ that is, nonnegative integer-valued counts. This mirrors the support for the ${Poisson}(\lambda)$ distribution so I thought that would be a good model to try. However, I investigated further and saw that the points column was **overdispersed** meaning that its variance of the number points (81.32 points^2 )  is very high relative to its mean (10.91 points). This is a direct violation of assuming a Poisson distribution for the count of points made by a player because the distribution assumes that $Mean = \lambda = Variance$ which means it doesn't have enough parameters to be flexible. 

I needed a more flexible and overdispersed substitute for Poisson regression and decided on negative binomial regression. The Negative Binomial distribution may be viewed as a Gamma-Poisson mixture, allowing it to naturally model overdispersed count data. and  does not have the "equi-dispersed" assumption like before because the parameter $\lambda$ is now itself treated as a random value drawn from the Gamma distribution and the mean and variance are no longer forced to be equal.


# Conclusion/Results

Here is a table of the performance metrics for each model. I used RMSE because it is always in the unit of the response variable and is more immediately interpretable due to this. However, RMSE is more sensitive to outliers given that there is squaring involved. MAE is more robust to outliers as it treats all errors linearly as opposed to quadratically. Also given that the points data is overdispersed and has heavier tails, using MAE may help to offset this.

| Model             | RMSE     | MAE      | R²       | Notes               |
| ----------------- | -------- | -------- | -------- | ------------------- |
| League Mean       | 8.99     | 7.20     | N/A      | Constant prediction |
| Player Mean       | 6.53     | 4.99     | N/A      | Historical average  |
| OLS               | **5.16** | 3.91     | **0.67** | Best generalization |
| Negative Binomial | 7.29     | 4.84     | 0.34     | Count-data GLM      |
| Random Forest     | 5.21     | **3.49** | 0.66     | Comparable to OLS   |

OLS achieved the best overall predictive performance. The Random Forest achieved comparable predictive performance but it wasn't much different from the OLS model which is a simpler model. Feature importance analysis showed that the rolling 5-game average accounted for approximately 96% of the Random Forest's predictive importance. For the other two models, the rolling 5-game average was the highest coefficient showing that it was overall the feature that yielded the most amount of signal compared to the others. Despite being statistically justified, the negative binomial regression model did not outperform the other two models but all of the models outperformed the baselines.

Overall, the results suggest that feature engineering contributed more to predictive performance than model complexity. The relatively simple OLS model generalized slightly better than the more flexible Random Forest, while all fitted models substantially outperformed the naïve baselines.

# Future Ideas

There were quiet a lot ideas I forewent out for brevity's sake and wanting to have something complete. Here are some ideas that I may implement later for this project:

- **Engineer richer contextual features** – The results suggest that additional predictive performance is more likely to come from improved feature engineering than from increasingly complex models. Potential additions include opponent defensive statistics, player usage rate, expected minutes, team pace, betting lines, injury reports, and other game-level context obtained by joining additional datasets.
- **Improve the representation of recent player form** – Replace the simple 5-game rolling average with an exponentially weighted moving average (EWMA) or a Kalman filter. Both approaches adapt more naturally to changes in player performance by assigning greater weight to recent observations while retaining historical information.
- **Evaluate additional machine learning models** – Compare the current models with more advanced tree-based and sequential learning methods such as **XGBoost**, **LightGBM**, and, if additional data are available, **LSTMs** for modeling temporal dependencies.
- **Investigate additional statistical models** – Explore count-data models including the **Beta-Negative Binomial**, and hierarchical (mixed-effects) models to better account for overdispersion, and player-specific effects.
- **Improve project engineering** – Develop an automated data ingestion pipeline, improve project modularity, and build an interactive dashboard (e.g., Tableau) for model exploration and visualization.

# Repository Structure

NBA_Point_Prediction/
│
├── data/
├── notebooks/
├── README.md
├── requirements.txt


# Installation

git clone ...

pip install -r requirements.txt
