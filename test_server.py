#!/usr/bin/env python3
"""
Test script for the FastAPI CSV Analysis Server
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_server():
    """Test the FastAPI server endpoints"""
    
    print("🧪 Testing CSV Analysis API Server")
    print("=" * 50)
    
    try:
        # Test health endpoint
        print("1. Testing health check...")
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test list files
        print("\n2. Testing file listing...")
        response = requests.get(f"{BASE_URL}/list-files")
        print(f"   Status: {response.status_code}")
        files_data = response.json()
        print(f"   Found {files_data['count']} CSV files")
        
        # Test analysis endpoint
        print("\n3. Testing analysis endpoint...")
        response = requests.post(f"{BASE_URL}/analyze")
        print(f"   Status: {response.status_code}")
        analysis_data = response.json()
        print(f"   Analysis ID: {analysis_data.get('analysis_id')}")
        
        # Check status
        if 'analysis_id' in analysis_data:
            analysis_id = analysis_data['analysis_id']
            print(f"\n4. Checking analysis status...")
            
            for i in range(5):  # Check status 5 times
                time.sleep(2)
                response = requests.get(f"{BASE_URL}/status/{analysis_id}")
                status_data = response.json()
                print(f"   Check {i+1}: {status_data.get('status')}")
                
                if status_data.get('status') == 'completed':
                    print("   ✅ Analysis completed!")
                    break
                elif status_data.get('status') == 'failed':
                    print("   ❌ Analysis failed!")
                    break
        
        print("\n✅ Server tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    test_server()