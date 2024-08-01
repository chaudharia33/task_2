import pickle
import gzip
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def save_model(model, path):
    try:
        with gzip.open(path, 'wb') as file:
            pickle.dump(model, file)
        logger.info(f"Model saved to {path}")
    except Exception as e:
        logger.error(f"Error saving model: {e}")
        raise