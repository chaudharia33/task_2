import pandas as pd 
import logging

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