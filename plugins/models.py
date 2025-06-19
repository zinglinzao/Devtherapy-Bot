from pydantic import BaseModel
from loguru import logger

class ConfigBaseModel(BaseModel):
    def lazy_load(self, **new_data):
        logger.info(f"---> Loaded Setting: {self.__class__.__name__}")
        merged = {**self.model_dump(), **new_data}
        validated = self.__class__(**merged)
        self.__dict__.update(validated.__dict__)




