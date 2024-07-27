import pandas as pd
import pickle
import logging
import brotli
import gzip
from sklearn.preprocessing import LabelEncoder 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV, KFold

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def data_ingetion(path: str):
    try:
        data = pd.read_csv(path) 
        logger.info(f"Data ingested from {path}")
        return data
    except Exception as e:
        logger.error(f"Error ingesting data: {e}")
        raise

def data_preprocessing(data):
    try:
        label_encoder = LabelEncoder()
        data['sectorName'] = label_encoder.fit_transform(data['sectorName'])
        data['stateDescription']= label_encoder.fit_transform(data['stateDescription'])
        data.drop(['customers','revenue','sales'],axis=1,inplace= True)
        logger.info("Data preprocessed")
        return data
    except Exception as e:
        logger.error(f"Error preprocessing data: {e}")
        raise
    
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

def save_model(model, path):
    try:
        with gzip.open(path, 'wb') as file:
            pickle.dump(model, file)
        logger.info(f"Model saved to {path}")
    except Exception as e:
        logger.error(f"Error saving model: {e}")
        raise

if __name__ == "__main__":
    logger.info("Starting script")
    data= data_ingetion(path="../data/clean_data.csv")
    data= data_preprocessing(data)
    model= hp_model_build(data, test_size=0.2, random_state=123)
    save_model(model, path="../model/model.pkl")
    logger.info("Script completed")