from pydantic import Field, computed_field
from pymilvus import MilvusClient
from pydantic_settings import BaseSettings
from functools import cached_property


class Settings(BaseSettings):
    MILVUS_HOST:str = Field(alias="MILVUS_HOST", default="localhost")
    MILVUS_PORT:int = Field(alias="MILVUS_PORT", default=19530)
    MILVUS_DB:str = Field(alias="MILVUS_DB", default="default") 

    CHAT_COLLECTION:str = Field(alias="CHAT_COLLECTION", default="pdf_documents")
    


    @computed_field
    @cached_property
    def MILVUS_CLIENT(self) -> MilvusClient:
        uri = f"http://{self.MILVUS_HOST}:{self.MILVUS_PORT}"
        return MilvusClient(uri=uri, db_name=self.MILVUS_DB)
    
settings = Settings()