from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from Model import x_train, y_train

gbm = GradientBoostingRegressor()

param_grid = {
    "n_estimators": [100, 200, 500],
    "learning_rate": [0.01, 0.05, 0.1],
    "max_depth": [3, 5, 7],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 3, 5],
    "subsample": [0.8, 1.0]
}

gridSearch = GridSearchCV(gbm, param_grid, cv=5, scoring="neg_mean_absolute_error", n_jobs=-1, verbose=2)
gridSearch.fit(x_train, y_train)

print("Best parameters:", gridSearch.best_params_)
print("Best MAE:", -gridSearch.best_score_)
