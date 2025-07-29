#!/usr/bin/env python3
"""
Simple server startup script
"""
import uvicorn
from fastapi_analysis_server import app

if __name__ == "__main__":
    print("🚀 Starting CSV Analysis FastAPI Server...")
    print("📊 Access your analysis at: http://localhost:8000/analyze-now")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("\n" + "="*60)
    
    # Start the server
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info"
    )