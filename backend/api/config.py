import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Settings:
    ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "")
    API_PORT = int(os.getenv("API_PORT", "8000"))

settings = Settings()
