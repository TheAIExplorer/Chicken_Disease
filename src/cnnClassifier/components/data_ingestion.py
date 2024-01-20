# update the components: contains all the classes and methods that are gonig to be used in pipeline
import urllib.request as request
import zipfile
import os
from cnnClassifier import logger
from cnnClassifier.utils.common import get_size
from cnnClassifier.entity.config_entity import DataIngestionConfig


# Data_Ingestion <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url=self.config.source_URL, filename=self.config.local_data_file
            )
            logger.info(f"File {filename} downloaded with following info:  \n{headers}")
        else:
            logger.info(
                f"file {filename} already exists of size: {get_size(Path(self.config.local_data_file))}"
            )

    def extract_zip_file(self):
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, "r") as zip_ref:
            zip_ref.extractall(unzip_path)


# Data_ingestion >>>>>>>>>>>>>>>>>>>>
