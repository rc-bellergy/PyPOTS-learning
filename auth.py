import requests
import json
from typing import Dict, Optional
from config import Config


class AuthManager:
    """JWT Token Authentication Management Class"""
    
    def __init__(self, base_url: str = None):
        """
        Initialize authentication manager
        
        Args:
            base_url: API base URL. If None, uses BASE_URL from config
        """
        if base_url is None:
            base_url = Config.API_BASE_URL
        else:
            # Ensure base URL has /api suffix for authentication endpoints
            if not base_url.endswith('/api'):
                base_url = f"{base_url.rstrip('/')}/api"
                
        self.base_url = base_url.rstrip('/')
        self.token = None
        self.refresh_token = None
    
    def login(self, username: str, password: str) -> Dict[str, str]:
        """
        Login and get JWT Token
        
        Args:
            username: Username
            password: Password
            
        Returns:
            Dict[str, str]: Dictionary containing token and refreshToken
            
        Raises:
            Exception: Raises exception when login fails
        """
        url = f"{self.base_url}/auth/login"
        
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'username': username,
            'password': password
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            
            # Save tokens
            self.token = data.get('token')
            self.refresh_token = data.get('refreshToken')
            
            print("Login successful!")
            return data
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Login request failed: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                error_msg += f" - Status code: {e.response.status_code}"
                try:
                    error_detail = e.response.json()
                    error_msg += f" - Error message: {error_detail}"
                except:
                    error_msg += f" - Response content: {e.response.text}"
            raise Exception(error_msg)
    
    def get_auth_headers(self) -> Dict[str, str]:
        """
        Get request headers with authentication token
        
        Returns:
            Dict[str, str]: Authentication headers
            
        Raises:
            Exception: Raises exception when not logged in
        """
        if not self.token:
            raise Exception("Please login first to get token")
        
        return {
            'Authorization': f'Bearer {self.token}',
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def refresh_token_request(self) -> Dict[str, str]:
        """
        Refresh JWT token using refresh token
        
        Returns:
            Dict[str, str]: Dictionary containing new token and refreshToken
            
        Raises:
            Exception: Raises exception when refresh fails
        """
        if not self.refresh_token:
            raise Exception("No refresh token available")
        
        url = f"{self.base_url}/auth/refresh"
        
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.refresh_token}'
        }
        
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            # Update tokens
            self.token = data.get('token')
            self.refresh_token = data.get('refreshToken')
            
            print("Token refresh successful!")
            return data
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Token refresh failed: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                error_msg += f" - Status code: {e.response.status_code}"
            raise Exception(error_msg)
    
    def logout(self):
        """Logout and clear tokens"""
        self.token = None
        self.refresh_token = None
        print("Logged out")


# Simple usage function
def get_jwt_token(username: str, password: str, base_url: str = None) -> Dict[str, str]:
    """
    Quick function to get JWT Token
    
    Args:
        username: Username
        password: Password
        base_url: API base URL. If None, uses BASE_URL from .env file
        
    Returns:
        Dict[str, str]: Dictionary containing token and refreshToken
    """
    auth_manager = AuthManager(base_url)
    return auth_manager.login(username, password)


# Usage example
# if __name__ == "__main__":
#     # Example usage
#     try:
#         # Method 1: Use simple function
#         result = get_jwt_token(
#             username="user@iot.com",
#             password="1234"
#         )
#         print(f"Token: {result['token']}")
#         print(f"Refresh Token: {result['refreshToken']}")
        
#         # Method 2: Use class
#         auth = AuthManager()
#         auth.login("user@iot.com", "1234")
#         headers = auth.get_auth_headers()
#         print(f"Auth headers: {headers}")
        
#     except Exception as e:
#         print(f"Error: {e}")