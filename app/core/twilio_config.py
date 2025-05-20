from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class TwilioSettings(BaseSettings):
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str

    class Config:
        env_file = "dev.env"
        env_file_encoding = 'utf-8'
        extra = 'ignore'

@lru_cache()
def get_twilio_settings():
    return TwilioSettings() 