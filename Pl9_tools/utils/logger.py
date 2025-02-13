# src/shopify_search/config.py
import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        
       
       
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        self.MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
        self.TIMEOUT_SECONDS = int(os.getenv('TIMEOUT_SECONDS', 10))
        
        self.validate_config()
    
    def validate_config(self):
        required_vars = ['STORE_URL', 'STOREFRONT_TOKEN']
        missing_vars = [var for var in required_vars if not getattr(self, var)]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
