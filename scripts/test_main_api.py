import sys
import os
from fastapi.testclient import TestClient

sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))
from app.main import app

client = TestClient(app)

def run_test():
    print("Testing /health endpoint...")
    response = client.get("/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    
    print("\nTesting CORS headers...")
    response = client.options("/health", headers={
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "GET"
    })
    print(f"CORS Headers: {response.headers}")
    assert "access-control-allow-origin" in response.headers
    
    print("\nAll main API configuration tests passed!")

if __name__ == "__main__":
    run_test()
