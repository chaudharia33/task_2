from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV, KFold
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def hp_model_build(data, test_size=0.2,random_state=123):
    try:
        X = data.drop(['price'],axis=1)
        y=data['price']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        param_grid = {
                'n_estimators': [50]
                #'n_estimators': [50, 100, 150, 200, 250]  # Adjust this range as needed
                }
        rf = RandomForestRegressor(random_state=42)
        cv = KFold(n_splits=5, shuffle=True, random_state=42)  # 5-fold cross-validation
        grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=cv, scoring='neg_mean_squared_error', n_jobs=-1)
        grid_search.fit(X_train, y_train)
        best_n_estimators = grid_search.best_params_['n_estimators']
        best_rf = RandomForestRegressor(n_estimators=best_n_estimators, random_state=42)
        best_rf.fit(X_train, y_train)
        y_pred = best_rf.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        logger.info(f"Best number of estimators: {best_n_estimators}")
        logger.info(f"Mean Squared Error (MSE): {mse}")
        return best_rf
    except Exception as e:
        logger.error(f"Error building model: {e}")
        raise