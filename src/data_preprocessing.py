import pandas as pd
from sklearn.preprocessing import LabelEncoder 
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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