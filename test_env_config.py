#!/usr/bin/env python3
"""
Test script to verify environment configuration loading
"""

from config import Config
from getTelemetry import get_telemetry_data
from auth import AuthManager

def test_config_loading():
    """Test that configuration is loaded correctly from .env file"""
    print("=== Testing Configuration Loading ===")
    print(f"BASE_URL: {Config.BASE_URL}")
    print(f"AUTHORIZATION_TOKEN: {'***' + Config.AUTHORIZATION_TOKEN[-10:] if Config.AUTHORIZATION_TOKEN else 'None'}")
    print(f"API_BASE_URL: {Config.API_BASE_URL}")
    print(f"TELEMETRY_BASE_URL: {Config.TELEMETRY_BASE_URL}")
    print(f"DEFAULT_TIMEZONE: {Config.DEFAULT_TIMEZONE}")
    print(f"DEFAULT_LIMIT: {Config.DEFAULT_LIMIT}")
    print()

def test_auth_manager():
    """Test AuthManager with environment configuration"""
    print("=== Testing AuthManager ===")
    try:
        # Test with default configuration (from .env)
        auth = AuthManager()
        print(f"AuthManager base_url: {auth.base_url}")
        print("✓ AuthManager initialized successfully with .env configuration")
    except Exception as e:
        print(f"✗ AuthManager initialization failed: {e}")
    print()

def test_telemetry_function():
    """Test telemetry function with environment configuration"""
    print("=== Testing Telemetry Function ===")
    try:
        # Test with minimal parameters (should use .env configuration)
        data = get_telemetry_data(limit=1)  # Just get 1 record for testing
        if data:
            print("✓ Telemetry function working with .env configuration")
            print(f"  Retrieved {len(data)} telemetry keys")
            for key in data.keys():
                print(f"  - {key}: {len(data[key])} data points")
        else:
            print("✗ Telemetry function returned no data")
    except Exception as e:
        print(f"✗ Telemetry function failed: {e}")
    print()

def test_direct_api_call():
    """Test direct API call using environment configuration"""
    print("=== Testing Direct API Call ===")
    import requests
    
    if not Config.AUTHORIZATION_TOKEN:
        print("✗ No authorization token available for direct API test")
        return
    
    try:
        # Test a simple API endpoint
        headers = {
            "accept": "application/json",
            "X-Authorization": f"Bearer {Config.AUTHORIZATION_TOKEN}"
        }
        
        # Test the base URL connectivity
        response = requests.get(f"{Config.BASE_URL}/api/auth/user", headers=headers)
        if response.status_code == 200:
            print("✓ Direct API call successful")
            user_info = response.json()
            print(f"  User: {user_info.get('email', 'Unknown')}")
        else:
            print(f"✗ API call failed with status: {response.status_code}")
            print(f"  Response: {response.text}")
            
    except Exception as e:
        print(f"✗ Direct API call failed: {e}")
    print()

if __name__ == "__main__":
    print("Environment Configuration Test Suite")
    print("=" * 50)
    
    test_config_loading()
    test_auth_manager()
    test_telemetry_function()
    test_direct_api_call()
    
    print("Test suite completed!")