"""
LM Studio API client for chat communication.
"""
import requests
import json
import os
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LMStudioClient:
    """Client for communicating with LM Studio API."""
    
    def __init__(self, 
                 host: str = None, 
                 port: int = None, 
                 timeout: int = 30):
        """
        Initialize LM Studio client.
        
        Args:
            host: LM Studio server host (default from env or 192.168.1.123)
            port: LM Studio server port (default from env or 1234)  
            timeout: Request timeout in seconds
        """
        self.host = host or os.getenv('LM_STUDIO_HOST', '192.168.1.123')
        self.port = port or int(os.getenv('LM_STUDIO_PORT', '1234'))
        self.timeout = timeout
        self.base_url = f"http://{self.host}:{self.port}"
        
    def test_connection(self) -> Dict[str, Any]:
        """
        Test connection to LM Studio server.
        
        Returns:
            Dict with connection status and info
        """
        try:
            response = requests.get(
                f"{self.base_url}/v1/models",
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "message": "Connected to LM Studio",
                    "models": response.json()
                }
            else:
                return {
                    "status": "error", 
                    "message": f"HTTP {response.status_code}: {response.text}"
                }
                
        except requests.exceptions.ConnectionError:
            return {
                "status": "error",
                "message": f"Cannot connect to LM Studio at {self.base_url}"
            }
        except requests.exceptions.Timeout:
            return {
                "status": "error",
                "message": f"Connection timeout after {self.timeout}s"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            }
    
    def get_models(self) -> List[Dict[str, Any]]:
        """
        Get available models from LM Studio.
        
        Returns:
            List of available models
        """
        try:
            response = requests.get(
                f"{self.base_url}/v1/models",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json().get('data', [])
            
        except Exception as e:
            print(f"Error getting models: {e}")
            return []
    
    def send_message(self, 
                    messages: List[Dict[str, str]], 
                    model: str = None,
                    temperature: float = 0.7,
                    max_tokens: int = 150) -> Dict[str, Any]:
        """
        Send chat message to LM Studio.
        
        Args:
            messages: List of message objects with 'role' and 'content'
            model: Model name (optional, uses first available if not specified)
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in response
            
        Returns:
            Response from LM Studio API
        """
        try:
            # If no model specified, try to get first available
            if not model:
                models = self.get_models()
                if models:
                    model = models[0].get('id', 'local-model')
                else:
                    model = 'local-model'  # fallback
            
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload,
                timeout=self.timeout,
                headers={"Content-Type": "application/json"}
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.ConnectionError:
            return {
                "error": f"Cannot connect to LM Studio at {self.base_url}"
            }
        except requests.exceptions.Timeout:
            return {
                "error": f"Request timeout after {self.timeout}s"
            }
        except requests.exceptions.HTTPError as e:
            return {
                "error": f"HTTP error: {response.status_code} - {response.text}"
            }
        except Exception as e:
            return {
                "error": f"Unexpected error: {str(e)}"
            }
    
    def extract_message_content(self, response: Dict[str, Any]) -> str:
        """
        Extract message content from LM Studio API response.
        
        Args:
            response: API response from send_message
            
        Returns:
            Message content string
        """
        if "error" in response:
            return f"Error: {response['error']}"
        
        try:
            return response['choices'][0]['message']['content']
        except (KeyError, IndexError):
            return "Error: Invalid response format from LM Studio"


# Convenience function for testing
def test_lm_studio_connection():
    """Test function for checking LM Studio connection."""
    client = LMStudioClient()
    result = client.test_connection()
    print(f"Connection test: {result['status']}")
    print(f"Message: {result['message']}")
    
    if result['status'] == 'success' and 'models' in result:
        models = result['models'].get('data', [])
        print(f"Available models: {len(models)}")
        for model in models:
            print(f"  - {model.get('id', 'Unknown')}")


if __name__ == "__main__":
    test_lm_studio_connection()