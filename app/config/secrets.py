from dotenv import load_dotenv
from enum import Enum
import os
import json


load_dotenv()

class Environment(Enum):
    LOCAL = "local"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

    @property
    def is_local(self):
        return self in {Environment.LOCAL, Environment.DEVELOPMENT}

    @classmethod
    def from_string(cls, env_str: str):
        try:
            return cls[env_str.upper()]
        except KeyError:
            raise ValueError(f"Unknown environment: {env_str}")



class SecretManager:

    PORT : int = int(os.environ.get("PORT", "8080"))
    ENV : Environment = Environment.from_string(os.environ.get("ENV", "local"))