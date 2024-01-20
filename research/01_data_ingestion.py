# create entity
from dataclasses import dataclass
from pathlib import Path


# create entity
@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path


# importing dependencies
from cnnClassifier.constants import *
from cnnClassifier.utils.common import read_yaml, create_directories


# Update the Configuration Manager
class ConfigurationManager:
    def __init__(
        self, config_filepath=CONFIG_FILE_PATH, param_filepath=PARAMS_FILE_PATH
    ):
        self.config = read_yaml(config_filepath)
        self.param = read_yaml(param_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir,
        )

        return data_ingestion_config


# update the components: contains all the classes and methods that are gonig to be used in pipeline
import urllib.request as request
import zipfile
import os
from cnnClassifier import logger
from cnnClassifier.utils.common import get_size


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


# create data ingestion pipeline
try:
    config = ConfigurationManager()
    data_ingestion_config = config.get_data_ingestion_config()
    data_ingestion = DataIngestion(config=data_ingestion_config)
    data_ingestion.download_file()
    data_ingestion.extract_zip_file()
except Exception as e:
    raise e
