import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV, KFold

def data_ingetion(path: str):
    data = pd.read_csv(path) 
    return data

def data_preprocessing(data):
    label_encoder = LabelEncoder()
    data['sectorName'] = label_encoder.fit_transform(data['sectorName'])
    data['stateDescription']= label_encoder.fit_transform(data['stateDescription'])
    data.drop(['customers','revenue','sales'],axis=1,inplace= True)
    return data
    
def hp_model_build(data, test_size=0.2,random_state=123):
    X = data.drop(['price'],axis=1)
    y=data['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    param_grid = {
            'n_estimators': [50, 100, 150, 200, 250]  # Adjust this range as needed
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
    print("Best number of estimators:", best_n_estimators)
    print("Mean Squared Error (MSE):", mse)
    return best_rf

def save_model(model, path):
    with open(path, 'wb') as file:
        pickle.dump(model, file)

if __name__ == "__main__":
    data= data_ingetion(path="../data/clean_data.csv")
    data_preprocessing(data)
    model= hp_model_build(data, test_size=0.2,random_state=123)
    save_model(model, path="../model/model.pkl")