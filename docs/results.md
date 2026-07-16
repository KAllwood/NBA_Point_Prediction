| Model             | RMSE | MAE | R²   | Notes               |
|-------------------|-----:|----:|-----:|---------------------|
| League Mean       | 8.99 | 7.20 | N/A | Constant prediction |
| Player Mean       | 6.53 | 4.99 | N/A | Historical average  |
| OLS               | **5.16** | 3.91 | **0.67** | Best generalization |
| Negative Binomial | 7.29 | 4.84 | 0.34 | Count-data GLM      |
| Random Forest     | 5.21 | **3.49** | 0.66 | Comparable to OLS  |


