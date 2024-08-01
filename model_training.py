from src.data_ingetion import data_ingetion
from src.data_preprocessing import data_preprocessing
from src.hp_model_build import hp_model_build
from src.save_model import save_model
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting script")
    data= data_ingetion(path="data/clean_data.csv")
    data= data_preprocessing(data)
    model= hp_model_build(data, test_size=0.2, random_state=123)
    save_model(model, path="model/model.pkl")
    logger.info("Script completed")