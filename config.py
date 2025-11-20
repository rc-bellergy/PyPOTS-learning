import os

# Load environment variables from .env file if it exists
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path)
        print(f"✓ Loaded environment variables from {env_path}")
    except ImportError:
        print("⚠ python-dotenv not installed, using system environment variables")
else:
    print("⚠ .env file not found, using system environment variables")

class Config:
    """Configuration class for loading environment variables"""
    
    # API Configuration
    BASE_URL = os.getenv('BASE_URL', 'https://ioter.mpiot.com.hk')
    AUTHORIZATION_TOKEN = os.getenv('AUTHORIZATION_TOKEN')
    USERNAME = os.getenv('USERNAME')
    PASSWORD = os.getenv('PASSWORD')
    
    # API Endpoints
    API_BASE_URL = f"{BASE_URL.rstrip('/')}/api"
    TELEMETRY_BASE_URL = f"{BASE_URL.rstrip('/')}/api/plugins/telemetry"
    
    # Default settings
    DEFAULT_TIMEZONE = "Asia/Hong_Kong"
    DEFAULT_LIMIT = 1000
    
    @classmethod
    def validate_config(cls):
        """Validate that required environment variables are set"""
        if not cls.BASE_URL:
            raise ValueError("BASE_URL environment variable is not set")
        
        if not cls.USERNAME:
            print("Warning: USERNAME environment variable is not set")
        
        if not cls.PASSWORD:
            print("Warning: PASSWORD environment variable is not set")
        
        if not cls.AUTHORIZATION_TOKEN:
            print("Warning: AUTHORIZATION_TOKEN environment variable is not set")
        
        return True

# Validate configuration on import
Config.validate_config()