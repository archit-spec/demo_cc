#!/usr/bin/env python3
"""
FastAPI Server for Advanced CSV Analysis using Claude CLI
Provides endpoints for running detailed research reports on CSV data
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import markdown
import os
import shutil
import subprocess
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import tempfile
import asyncio
from typing import Optional, Dict, List
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import time

# Load environment variables
load_dotenv()

app = FastAPI(
    title="CSV Analysis API",
    description="Advanced CSV analysis using Claude CLI with detailed research reports",
    version="1.0.0"
)

# Add CORS middleware for web interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for tracking analysis
analysis_status = {}
analysis_results = {}

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.analysis_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, analysis_id: str = None):
        await websocket.accept()
        self.active_connections.append(websocket)
        
        if analysis_id:
            if analysis_id not in self.analysis_connections:
                self.analysis_connections[analysis_id] = []
            self.analysis_connections[analysis_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, analysis_id: str = None):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        
        if analysis_id and analysis_id in self.analysis_connections:
            if websocket in self.analysis_connections[analysis_id]:
                self.analysis_connections[analysis_id].remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except:
            pass
    
    async def broadcast_to_analysis(self, message: str, analysis_id: str):
        if analysis_id in self.analysis_connections:
            dead_connections = []
            for connection in self.analysis_connections[analysis_id]:
                try:
                    await connection.send_text(message)
                except:
                    dead_connections.append(connection)
            
            # Clean up dead connections
            for dead_conn in dead_connections:
                self.disconnect(dead_conn, analysis_id)

manager = ConnectionManager()

# File monitoring class
class AnalysisFileHandler(FileSystemEventHandler):
    def __init__(self, analysis_id: str, target_files: List[str]):
        super().__init__()
        self.analysis_id = analysis_id
        self.target_files = target_files
        self.last_content = {}
        
    def on_modified(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            if filename in self.target_files:
                asyncio.create_task(self.handle_file_change(event.src_path, filename))
    
    def on_created(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            if filename in self.target_files:
                asyncio.create_task(self.handle_file_change(event.src_path, filename))
    
    async def handle_file_change(self, file_path: str, filename: str):
        try:
            # Wait a bit for file to be fully written
            await asyncio.sleep(0.5)
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Only send update if content changed
                if file_path not in self.last_content or self.last_content[file_path] != content:
                    self.last_content[file_path] = content
                    
                    message = {
                        "type": "file_update",
                        "filename": filename,
                        "content": content,
                        "size": len(content),
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    await manager.broadcast_to_analysis(json.dumps(message), self.analysis_id)
        except Exception as e:
            print(f"Error handling file change: {e}")

# Global file observers
file_observers: Dict[str, Observer] = {}

def start_file_monitoring(analysis_id: str, target_files: List[str]):
    """Start monitoring files for an analysis"""
    try:
        if analysis_id in file_observers:
            stop_file_monitoring(analysis_id)
        
        event_handler = AnalysisFileHandler(analysis_id, target_files)
        observer = Observer()
        observer.schedule(event_handler, path='.', recursive=False)
        observer.start()
        
        file_observers[analysis_id] = observer
        print(f"Started file monitoring for analysis {analysis_id}")
        
    except Exception as e:
        print(f"Error starting file monitoring: {e}")

def stop_file_monitoring(analysis_id: str):
    """Stop monitoring files for an analysis"""
    try:
        if analysis_id in file_observers:
            file_observers[analysis_id].stop()
            file_observers[analysis_id].join()
            del file_observers[analysis_id]
            print(f"Stopped file monitoring for analysis {analysis_id}")
    except Exception as e:
        print(f"Error stopping file monitoring: {e}")

# Keep original function for backward compatibility
def run_advanced_analysis(csv_filename: str = "finalapi.csv", output_dir: str = "analysis_output") -> dict:
    return run_advanced_analysis_with_monitoring(csv_filename, output_dir, None)

def run_advanced_analysis_with_monitoring(csv_filename: str = "finalapi.csv", output_dir: str = "analysis_output", analysis_id: str = None) -> dict:
    """
    Run advanced analysis using Claude CLI
    """
    try:
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Set environment variables for Claude
        os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY", "")
        if not os.environ["ANTHROPIC_API_KEY"]:
            return {"error": "ANTHROPIC_API_KEY not found in environment"}
        
        # Check if CSV file exists
        if not os.path.exists(csv_filename):
            return {"error": f"CSV file {csv_filename} not found"}
        
        # Start file monitoring if analysis_id provided
        if analysis_id:
            start_file_monitoring(analysis_id, ["research.md", "analysis.log", "error.log"])
        
        # Build Claude CLI command with deep investigative analysis
        research_prompt = f'''
        Build a detailed INVESTIGATIVE research report for @{csv_filename} and save it as research.md. 
        
        This is insurance agency data with 213,328 rows covering 2005-2013. I need DEEP INVESTIGATIVE ANALYSIS to understand WHY some agencies succeed while others fail.
        
        **QUICK INVESTIGATIVE ANALYSIS (10-15 minute focus):**
        
        1. **TOP & BOTTOM 5 PERFORMERS ONLY**
           - Identify top 5 and bottom 5 agencies by loss ratio and premium volume
           - Focus on AGENCY_ID, WRTN_PREM_AMT, LOSS_RATIO, STATE_ABBR
           - Quick performance scoring using 2-3 key metrics only
           
        2. **KEY SUCCESS/FAILURE PATTERNS (Top 5 focus)**
           - 3 main differences between top 5 vs bottom 5 performers  
           - Geographic clustering patterns (STATE_ABBR analysis for top/bottom 5)
           - Product line specialization effects (PROD_LINE analysis for top/bottom 5)
           - Producer efficiency patterns (ACTIVE_PRODUCERS vs premiums for top/bottom 5)
           - Agency size vs efficiency analysis (small vs large, top/bottom 5 only)
           
        3. **QUICK INSIGHTS & RECOMMENDATIONS**
           - 5 immediate red flags for agency risk
           - 3 key success factors for new agencies
           - Top 3 states for expansion opportunities
           
        
        **EXECUTION APPROACH:**
        - Focus on pandas analysis for quick insights
        - Simple statistical summaries, avoid complex modeling
        - Prioritize actionable findings over comprehensive analysis
        - Keep analysis under 10 minutes
        
        **QUICK DELIVERABLES:**
        - 5-point executive summary
        - Top 5 and Bottom 5 agency list with reasons
        - 3 key geographic insights 
        - 5 immediate action items
        
        Make this a true INVESTIGATIVE ANALYSIS that uncovers hidden patterns and provides specific, actionable intelligence for business decisions.
        '''
        
        # Run Claude CLI command
        cmd = [
            'claude',
            '--dangerously-skip-permissions',
            research_prompt
        ]
        
        print(f"🚀 Running Claude CLI analysis...")
        print(f"📊 CSV file: {csv_filename}")
        print(f"📁 Output directory: {output_dir}")
        
        # Execute the command
        result = subprocess.run(
            cmd,
            cwd=os.getcwd(),
            capture_output=True,
            text=True,
            timeout=1800  # 30 minute timeout
        )
        
        response_data = {
            "timestamp": datetime.now().isoformat(),
            "csv_file": csv_filename,
            "output_directory": output_dir,
            "command_return_code": result.returncode,
            "command_output": result.stdout if result.stdout else "No output",
            "command_errors": result.stderr if result.stderr else "No errors"
        }
        
        # Check if research.md was created
        research_file = "research.md"
        if os.path.exists(research_file):
            with open(research_file, "r", encoding="utf-8") as f:
                research_content = f.read()
            
            response_data.update({
                "success": True,
                "research_report": research_content,
                "research_file_size": len(research_content),
                "message": "Research report generated successfully"
            })
            
            # Move research.md to output directory
            shutil.move(research_file, os.path.join(output_dir, research_file))
            response_data["research_file_path"] = os.path.join(output_dir, research_file)
            
        else:
            response_data.update({
                "success": False,
                "research_report": None,
                "message": "Research report not generated - check command output for details"
            })
        
        return response_data
        
    except subprocess.TimeoutExpired:
        error_result = {
            "error": "Analysis timed out after 30 minutes",
            "timestamp": datetime.now().isoformat()
        }
        if analysis_id:
            stop_file_monitoring(analysis_id)
        return error_result
    except Exception as e:
        error_result = {
            "error": f"Analysis failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }
        if analysis_id:
            stop_file_monitoring(analysis_id)
        return error_result

@app.get("/", response_class=HTMLResponse)
async def root():
    """Main page with custom HTML interface"""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Insurance Agency Intelligence - Deep Investigative Analysis</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 700;
        }

        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        .main-content {
            padding: 40px;
        }

        .upload-section {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 30px;
            margin-bottom: 30px;
            border: 2px dashed #dee2e6;
            transition: all 0.3s ease;
        }

        .upload-section:hover {
            border-color: #667eea;
            background: #f0f2ff;
        }

        .upload-section.dragover {
            border-color: #667eea;
            background: #e8ecff;
            transform: scale(1.02);
        }

        .upload-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 15px;
            color: #2c3e50;
        }

        .file-input-wrapper {
            position: relative;
            display: inline-block;
            cursor: pointer;
            width: 100%;
        }

        .file-input {
            position: absolute;
            opacity: 0;
            width: 100%;
            height: 100%;
            cursor: pointer;
        }

        .file-input-button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .file-input-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .file-list {
            margin-top: 20px;
        }

        .file-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 15px;
            background: white;
            border-radius: 8px;
            margin-bottom: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .file-info {
            flex: 1;
        }

        .file-name {
            font-weight: 600;
            color: #2c3e50;
        }

        .file-size {
            font-size: 0.9rem;
            color: #6c757d;
        }

        .remove-file {
            background: #e74c3c;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 5px 10px;
            cursor: pointer;
            font-size: 0.9rem;
        }

        .analyze-button {
            width: 100%;
            padding: 20px;
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1.2rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-bottom: 30px;
        }

        .analyze-button:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(39, 174, 96, 0.4);
        }

        .analyze-button:disabled {
            background: #95a5a6;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }

        .quick-analyze {
            text-align: center;
            margin-top: 20px;
            padding: 20px;
            background: #e8f5e8;
            border-radius: 8px;
        }

        .quick-analyze-button {
            display: inline-block;
            padding: 15px 30px;
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .quick-analyze-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(39, 174, 96, 0.4);
        }

        .error-message {
            background: #ff7675;
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
        }

        @media (max-width: 768px) {
            .main-content {
                padding: 20px;
            }

            .header h1 {
                font-size: 2rem;
            }

            .upload-section {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🕵️ Insurance Agency Intelligence</h1>
            <p>Deep investigative analysis to uncover why agencies succeed or fail</p>
        </div>

        <div class="main-content">
            <div class="upload-section" id="uploadSection">
                <h2 class="upload-title">📊 Upload Your Data</h2>
                <p style="margin-bottom: 20px; color: #6c757d;">
                    Upload CSV files for autonomous analysis. Maximum file size: 100MB
                </p>

                <div class="file-input-wrapper">
                    <input type="file" id="fileInput" class="file-input" multiple accept=".csv" />
                    <button class="file-input-button">
                        📁 Choose CSV Files or Drag & Drop
                    </button>
                </div>

                <div class="file-list" id="fileList"></div>
            </div>

            <button id="analyzeButton" class="analyze-button" disabled>
                🚀 Start Analysis
            </button>

            <div class="quick-analyze">
                <h3 style="margin-bottom: 15px; color: #2c3e50;">🕵️ Investigative Analysis</h3>
                <p style="margin-bottom: 15px; color: #6c757d;">
                    Deep analysis of 213K insurance agency records - discover top/bottom performers and why
                </p>
                <a href="/analyze-now" class="quick-analyze-button" style="margin-right: 10px;">
                    ⚡ Complete Investigation
                </a>
                <a href="/realtime" class="quick-analyze-button" style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);">
                    🔴 Live Investigation
                </a>
            </div>

            <div id="errorMessage" class="error-message" style="display: none;"></div>
        </div>
    </div>

    <script>
        let selectedFiles = [];
        
        const fileInput = document.getElementById('fileInput');
        const fileList = document.getElementById('fileList');
        const uploadSection = document.getElementById('uploadSection');
        const analyzeButton = document.getElementById('analyzeButton');
        const errorMessage = document.getElementById('errorMessage');

        // File input handling
        fileInput.addEventListener('change', handleFileSelect);

        // Drag and drop handling
        uploadSection.addEventListener('dragover', handleDragOver);
        uploadSection.addEventListener('dragleave', handleDragLeave);
        uploadSection.addEventListener('drop', handleFileDrop);

        // Analyze button
        analyzeButton.addEventListener('click', startAnalysis);

        function handleFileSelect(event) {
            const files = Array.from(event.target.files);
            addFiles(files);
        }

        function handleDragOver(event) {
            event.preventDefault();
            uploadSection.classList.add('dragover');
        }

        function handleDragLeave(event) {
            event.preventDefault();
            uploadSection.classList.remove('dragover');
        }

        function handleFileDrop(event) {
            event.preventDefault();
            uploadSection.classList.remove('dragover');
            const files = Array.from(event.dataTransfer.files);
            addFiles(files);
        }

        function addFiles(files) {
            const validFiles = files.filter(file => {
                const extension = file.name.toLowerCase().split('.').pop();
                return extension === 'csv';
            });

            if (validFiles.length !== files.length) {
                showError('Some files were skipped. Only CSV files are supported.');
            }

            selectedFiles = [...selectedFiles, ...validFiles];
            updateFileList();
            updateAnalyzeButton();
        }

        function updateFileList() {
            fileList.innerHTML = '';

            selectedFiles.forEach((file, index) => {
                const fileItem = document.createElement('div');
                fileItem.className = 'file-item';

                const fileSize = (file.size / (1024 * 1024)).toFixed(2);

                fileItem.innerHTML = `
                    <div class="file-info">
                        <div class="file-name">${file.name}</div>
                        <div class="file-size">${fileSize} MB</div>
                    </div>
                    <button class="remove-file" onclick="removeFile(${index})">Remove</button>
                `;

                fileList.appendChild(fileItem);
            });
        }

        function removeFile(index) {
            selectedFiles.splice(index, 1);
            updateFileList();
            updateAnalyzeButton();
        }

        function updateAnalyzeButton() {
            analyzeButton.disabled = selectedFiles.length === 0;
        }

        function showError(message) {
            errorMessage.textContent = message;
            errorMessage.style.display = 'block';
            setTimeout(() => {
                errorMessage.style.display = 'none';
            }, 5000);
        }

        async function startAnalysis() {
            if (selectedFiles.length === 0) return;

            const formData = new FormData();
            selectedFiles.forEach(file => {
                formData.append('files', file);
            });

            try {
                analyzeButton.disabled = true;
                analyzeButton.textContent = '🔄 Uploading and Starting Analysis...';

                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();

                if (!response.ok) {
                    throw new Error(result.detail || 'Upload failed');
                }

                // Redirect to analysis page for uploaded file
                const filename = result.filename;
                window.location.href = `/analyze/${filename}`;

            } catch (error) {
                showError(`Error starting analysis: ${error.message}`);
                analyzeButton.disabled = false;
                analyzeButton.textContent = '🚀 Start Analysis';
            }
        }

        // Initialize
        updateAnalyzeButton();
    </script>
</body>
</html>"""

@app.get("/analyze-now", response_class=HTMLResponse)
async def analyze_now():
    """Run immediate analysis and return rendered markdown"""
    try:
        # Run analysis synchronously for immediate results
        result = run_advanced_analysis("finalapi.csv", "immediate_analysis")
        
        if result.get("success") and result.get("research_report"):
            markdown_content = result["research_report"]
            html_content = markdown.markdown(
                markdown_content, 
                extensions=['tables', 'fenced_code', 'toc']
            )
            
            html_template = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>CSV Analysis Report</title>
                <meta charset="utf-8">
                <style>
                    body {{ 
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                        max-width: 1200px; 
                        margin: 0 auto; 
                        padding: 20px; 
                        line-height: 1.6; 
                    }}
                    h1, h2, h3 {{ color: #333; }}
                    table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                    code {{ background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; }}
                    pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
                    .header {{ 
                        background-color: #2c3e50; 
                        color: white; 
                        padding: 20px; 
                        margin: -20px -20px 20px -20px; 
                    }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>📊 CSV Analysis Report</h1>
                    <p>Generated: {result.get('timestamp', 'Unknown')}</p>
                    <p>File: {result.get('csv_file', 'Unknown')}</p>
                    <div style="margin-top: 15px;">
                        <a href="/download-markdown" style="background: #27ae60; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: 600;">
                            📄 Download Markdown Report
                        </a>
                    </div>
                </div>
                {html_content}
            </body>
            </html>
            """
            return html_template
        else:
            error_html = f"""
            <!DOCTYPE html>
            <html>
            <head><title>Analysis Error</title></head>
            <body>
                <h1>❌ Analysis Failed</h1>
                <p>Error: {result.get('message', 'Unknown error')}</p>
                <pre>{result.get('command_errors', 'No error details')}</pre>
            </body>
            </html>
            """
            return error_html
            
    except Exception as e:
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Analysis Error</title></head>
        <body>
            <h1>❌ Analysis Failed</h1>
            <p>Exception: {str(e)}</p>
        </body>
        </html>
        """
        return error_html

@app.get("/realtime", response_class=HTMLResponse)
async def realtime_analysis():
    """Real-time analysis page with WebSocket updates"""
    try:
        with open("realtime_analysis.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Real-time analysis page not found</h1>"
    except Exception as e:
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Analysis Error</title></head>
        <body>
            <h1>❌ Analysis Failed</h1>
            <p>Exception: {str(e)}</p>
        </body>
        </html>
        """
        return error_html

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "claude_cli_available": shutil.which("claude") is not None,
        "anthropic_api_key_set": bool(os.getenv("ANTHROPIC_API_KEY"))
    }

@app.post("/analyze")
async def analyze_default_csv(background_tasks: BackgroundTasks):
    """Run analysis on the default finalapi.csv file"""
    
    analysis_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Initialize status tracking
    analysis_status[analysis_id] = {
        "status": "starting",
        "timestamp": datetime.now().isoformat(),
        "csv_file": "finalapi.csv"
    }
    
    # Run analysis in background
    background_tasks.add_task(run_background_analysis, analysis_id, "finalapi.csv")
    
    return {
        "analysis_id": analysis_id,
        "status": "started",
        "message": "Analysis started in background",
        "check_status_url": f"/status/{analysis_id}"
    }

@app.post("/analyze/{filename}")
async def analyze_csv_file_post(filename: str, background_tasks: BackgroundTasks):
    """Run analysis on a specific CSV file (POST)"""
    
    if not filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV file")
    
    if not os.path.exists(filename):
        raise HTTPException(status_code=404, detail=f"CSV file {filename} not found")
    
    analysis_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Initialize status tracking
    analysis_status[analysis_id] = {
        "status": "starting",
        "timestamp": datetime.now().isoformat(),
        "csv_file": filename
    }
    
    # Run analysis in background
    background_tasks.add_task(run_background_analysis, analysis_id, filename)
    
    return {
        "analysis_id": analysis_id,
        "status": "started",
        "message": f"Analysis started for {filename}",
        "check_status_url": f"/status/{analysis_id}"
    }

@app.get("/analyze/{filename}", response_class=HTMLResponse)
async def analyze_csv_file_get(filename: str):
    """Run analysis on a specific CSV file and return HTML (GET)"""
    
    if not filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV file")
    
    if not os.path.exists(filename):
        raise HTTPException(status_code=404, detail=f"CSV file {filename} not found")
    
    try:
        # Run analysis immediately for GET requests
        result = run_advanced_analysis(filename, f"analysis_output_{filename}")
        
        if result.get("success") and result.get("research_report"):
            markdown_content = result["research_report"]
            html_content = markdown.markdown(
                markdown_content, 
                extensions=['tables', 'fenced_code', 'toc']
            )
            
            html_template = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>CSV Analysis Report - {filename}</title>
                <meta charset="utf-8">
                <style>
                    body {{ 
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                        max-width: 1200px; 
                        margin: 0 auto; 
                        padding: 20px; 
                        line-height: 1.6; 
                    }}
                    h1, h2, h3 {{ color: #333; }}
                    table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                    code {{ background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; }}
                    pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
                    .header {{ 
                        background-color: #2c3e50; 
                        color: white; 
                        padding: 20px; 
                        margin: -20px -20px 20px -20px; 
                    }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>📊 CSV Analysis Report</h1>
                    <p>Generated: {result.get('timestamp', 'Unknown')}</p>
                    <p>File: {filename}</p>
                    <div style="margin-top: 15px;">
                        <a href="/download-markdown" style="background: #27ae60; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: 600;">
                            📄 Download Markdown Report
                        </a>
                        <a href="/" style="background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: 600; margin-left: 10px;">
                            🏠 Back to Home
                        </a>
                    </div>
                </div>
                {html_content}
            </body>
            </html>
            """
            return html_template
        else:
            error_html = f"""
            <!DOCTYPE html>
            <html>
            <head><title>Analysis Error</title></head>
            <body>
                <h1>❌ Analysis Failed</h1>
                <p>Error: {result.get('message', 'Unknown error')}</p>
                <p>File: {filename}</p>
                <pre>{result.get('command_errors', 'No error details')}</pre>
                <a href="/" style="background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                    🏠 Back to Home
                </a>
            </body>
            </html>
            """
            return error_html
            
    except Exception as e:
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Analysis Error</title></head>
        <body>
            <h1>❌ Analysis Failed</h1>
            <p>Exception: {str(e)}</p>
            <p>File: {filename}</p>
            <a href="/" style="background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                🏠 Back to Home
            </a>
        </body>
        </html>
        """
        return error_html

@app.post("/upload")
async def upload_csv_file(files: list[UploadFile] = File(...)):
    """Upload CSV files for analysis"""
    
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    # Take the first file for now
    file = files[0]
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    try:
        # Save uploaded file
        file_path = f"uploaded_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            "message": f"File {file.filename} uploaded successfully",
            "filename": file_path,
            "size": os.path.getsize(file_path),
            "analyze_url": f"/analyze/{file_path}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/status/{analysis_id}")
async def get_analysis_status(analysis_id: str):
    """Get the status of a running analysis"""
    
    if analysis_id not in analysis_status:
        raise HTTPException(status_code=404, detail="Analysis ID not found")
    
    status_info = analysis_status[analysis_id]
    
    # Check if analysis is completed
    if analysis_id in analysis_results:
        status_info.update({
            "status": "completed",
            "results_available": True,
            "download_url": f"/download/research_{analysis_id}.md"
        })
    
    return status_info

@app.get("/results/{analysis_id}")
async def get_analysis_results(analysis_id: str):
    """Get the results of a completed analysis"""
    
    if analysis_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Analysis results not found")
    
    return analysis_results[analysis_id]

@app.get("/results/{analysis_id}/markdown", response_class=HTMLResponse)
async def get_analysis_results_rendered(analysis_id: str):
    """Get the results of a completed analysis rendered as HTML from markdown"""
    
    if analysis_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Analysis results not found")
    
    result_data = analysis_results[analysis_id]
    
    if not result_data.get("success") or not result_data.get("research_report"):
        raise HTTPException(status_code=404, detail="Research report not available")
    
    # Convert markdown to HTML
    markdown_content = result_data["research_report"]
    html_content = markdown.markdown(
        markdown_content, 
        extensions=['tables', 'fenced_code', 'toc']
    )
    
    # Wrap in a nice HTML template
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>CSV Analysis Report</title>
        <meta charset="utf-8">
        <style>
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                max-width: 1200px; 
                margin: 0 auto; 
                padding: 20px; 
                line-height: 1.6; 
            }}
            h1, h2, h3 {{ color: #333; }}
            table {{ 
                border-collapse: collapse; 
                width: 100%; 
                margin: 10px 0; 
            }}
            th, td {{ 
                border: 1px solid #ddd; 
                padding: 8px; 
                text-align: left; 
            }}
            th {{ background-color: #f2f2f2; }}
            code {{ 
                background-color: #f4f4f4; 
                padding: 2px 4px; 
                border-radius: 3px; 
            }}
            pre {{ 
                background-color: #f4f4f4; 
                padding: 10px; 
                border-radius: 5px; 
                overflow-x: auto; 
            }}
            .header {{ 
                background-color: #2c3e50; 
                color: white; 
                padding: 20px; 
                margin: -20px -20px 20px -20px; 
                border-radius: 5px 5px 0 0; 
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📊 CSV Analysis Report</h1>
            <p>Generated: {result_data.get('timestamp', 'Unknown')}</p>
            <p>File: {result_data.get('csv_file', 'Unknown')}</p>
        </div>
        {html_content}
    </body>
    </html>
    """
    
    return html_template

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download generated files"""
    
    # Check in current directory
    if os.path.exists(filename):
        return FileResponse(filename, media_type='text/markdown', filename=filename)
    
    # Check in analysis_output directory
    output_path = os.path.join("analysis_output", filename)
    if os.path.exists(output_path):
        return FileResponse(output_path, media_type='text/markdown', filename=filename)
    
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/download-markdown")
async def download_research_markdown():
    """Download the latest research.md file"""
    
    research_file = "research.md"
    if os.path.exists(research_file):
        return FileResponse(
            research_file, 
            media_type='text/markdown',
            filename="insurance_research_report.md"
        )
    
    raise HTTPException(status_code=404, detail="Research report not found")

async def run_background_analysis(analysis_id: str, csv_filename: str):
    """Run analysis in background task with real-time monitoring"""
    
    try:
        # Update status
        analysis_status[analysis_id]["status"] = "running"
        analysis_status[analysis_id]["started_at"] = datetime.now().isoformat()
        
        # Notify connected clients
        status_message = {
            "type": "status_update",
            "status": "running",
            "message": "Analysis started",
            "timestamp": datetime.now().isoformat()
        }
        await manager.broadcast_to_analysis(json.dumps(status_message), analysis_id)
        
        # Run the analysis with monitoring
        result = run_advanced_analysis_with_monitoring(csv_filename, f"analysis_output_{analysis_id}", analysis_id)
        
        # Store results
        analysis_results[analysis_id] = result
        
        # Update status
        final_status = "completed" if result.get("success") else "failed"
        analysis_status[analysis_id].update({
            "status": final_status,
            "completed_at": datetime.now().isoformat(),
            "success": result.get("success", False)
        })
        
        # Notify completion
        completion_message = {
            "type": "analysis_complete",
            "status": final_status,
            "success": result.get("success", False),
            "message": "Analysis completed" if result.get("success") else f"Analysis failed: {result.get('error', 'Unknown error')}",
            "timestamp": datetime.now().isoformat()
        }
        await manager.broadcast_to_analysis(json.dumps(completion_message), analysis_id)
        
        # Stop file monitoring
        stop_file_monitoring(analysis_id)
        
    except Exception as e:
        analysis_status[analysis_id].update({
            "status": "error",
            "error": str(e),
            "completed_at": datetime.now().isoformat()
        })
        
        # Notify error
        error_message = {
            "type": "analysis_error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
        await manager.broadcast_to_analysis(json.dumps(error_message), analysis_id)
        
        # Stop file monitoring
        stop_file_monitoring(analysis_id)

@app.websocket("/ws/{analysis_id}")
async def websocket_endpoint(websocket: WebSocket, analysis_id: str):
    """WebSocket endpoint for real-time analysis updates"""
    await manager.connect(websocket, analysis_id)
    
    try:
        # Send initial status
        if analysis_id in analysis_status:
            status_data = analysis_status[analysis_id]
            await manager.send_personal_message(json.dumps({
                "type": "status_update",
                "status": status_data.get("status", "unknown"),
                "message": f"Connected to analysis {analysis_id}",
                "timestamp": datetime.now().isoformat()
            }), websocket)
        
        # Keep connection alive
        while True:
            try:
                # Wait for messages (heartbeat)
                await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
            except asyncio.TimeoutError:
                # Send heartbeat
                await manager.send_personal_message(json.dumps({
                    "type": "heartbeat",
                    "timestamp": datetime.now().isoformat()
                }), websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, analysis_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, analysis_id)

@app.get("/list-files")
async def list_csv_files():
    """List available CSV files"""
    
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    
    file_info = []
    for filename in csv_files:
        try:
            stat = os.stat(filename)
            file_info.append({
                "filename": filename,
                "size": stat.st_size,
                "size_mb": round(stat.st_size / 1024 / 1024, 2),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
        except:
            pass
    
    return {
        "csv_files": file_info,
        "count": len(file_info)
    }

if __name__ == "__main__":
    import uvicorn
    
    # Check if required dependencies are available
    if not shutil.which("claude"):
        print("❌ Warning: Claude CLI not found in PATH")
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Warning: ANTHROPIC_API_KEY not set")
    
    print("🚀 Starting CSV Analysis API Server...")
    print("📊 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("🎯 Direct Analysis: http://localhost:8000/analyze-now")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)