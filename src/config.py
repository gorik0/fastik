from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings (BaseSettings):
    DATABASE_URL:str 
    JWT_SECRET:str 
    JWT_ALGORITHM:str 
    REDIS_HOST:str="localhost"
    REDIS_PORT:int=6379
    model_config = SettingsConfigDict(env_file = ".env",extra="ignore")
    MAIL_USERNAME:str="gorik"
    MAIL_PASSWORD:str=""
    MAIL_FROM:str="delavarus"
    MAIL_SERVER:str="smt.gmail.com"
    MAIL_FROM_NAME:str="Goriko"


Config = Settings()