#!/usr/bin/env python3
"""
Direct Claude CLI approach - bypass SDK communication issues
"""

import subprocess
import json
import os
import logging
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure verbose logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('direct_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_claude_analysis():
    """Run Claude analysis using direct CLI calls"""
    
    logger.info("🚀 Starting Claude CLI analysis")
    
    # Set up environment
    logger.debug("Setting up environment variables...")
    original_path = os.environ.get('PATH', '')
    os.environ['PATH'] = '/home/dumball/.nvm/versions/node/v18.17.0/bin:' + original_path
    os.environ['ANTHROPIC_API_KEY'] = os.getenv('ANTHROPIC_API_KEY')
    
    logger.info(f"Updated PATH: {os.environ['PATH'][:100]}...")
    logger.info("API key configured successfully")
    
    # Create the prompt
    prompt = """
You are a specialized data analyst. Analyze the insurance dataset 'finalapi.csv' which contains:
- 213,328 rows of insurance agency data
- 49 columns including: AGENCY_ID, WRTN_PREM_AMT, LOSS_RATIO, PROD_LINE, STATE_ABBR, etc.
- Data from 2005-2013 covering premiums, loss ratios, agency performance
- Contains placeholder value 99999 for missing data

CRITICAL INSTRUCTIONS:
- DO NOT use Read, Grep, or LS tools to examine files
- START by writing a complete Python analysis script
- Execute the script using: /home/dumball/training/.venv/bin/python script_name.py
- Install packages with: uv pip install pandas matplotlib seaborn
- Access data ONLY through: df = pd.read_csv('finalapi.csv')

WRITE AND EXECUTE a comprehensive Python script that performs:

1. **Data Structure Analysis**:
   - Load CSV with pandas
   - Print dataset shape, column info, data types
   - Show first 5 rows with df.head()

2. **Data Quality Assessment**:
   - Missing values: df.isnull().sum()
   - Duplicates: df.duplicated().sum()
   - Identify 99999 placeholder values

3. **Generate Visualizations**:
   - Create 'agent_comm/charts/' directory
   - Save missing data heatmap
   - Distribution plots for key columns
   - Correlation matrix

4. **Save Results**:
   - Export summary statistics to CSV
   - Create markdown report at 'agent_comm/structure_analysis.md'

Write the complete Python script first, then execute it. Include all imports and error handling.
"""
    
    # Save prompt to file for Claude CLI
    logger.debug("Saving prompt to file...")
    with open('analysis_prompt.txt', 'w') as f:
        f.write(prompt)
    logger.info("📝 Prompt saved to analysis_prompt.txt")
    
    logger.info("🚀 Running Claude CLI directly...")
    
    try:
        # Run Claude CLI with the prompt (using correct syntax)
        cmd = [
            'claude',
            '--print', 
            '--allowedTools', 'Write Bash Edit MultiEdit',
            '--dangerously-skip-permissions',
            prompt
        ]
        
        logger.info(f"💻 Command: {' '.join(cmd[:4])} [prompt...]")
        logger.debug(f"Full command: {cmd}")
        logger.info(f"Working directory: /home/dumball/ccagent")
        logger.info(f"Timeout: 900 seconds (15 minutes)")
        
        start_time = time.time()
        logger.info("⏱️ Starting subprocess execution...")
        
        # Run the command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=900,  # 15 minute timeout for comprehensive analysis
            cwd='/home/dumball/ccagent'
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        logger.info(f"✅ Claude CLI completed in {execution_time:.2f} seconds")
        logger.info(f"Return code: {result.returncode}")
        logger.info(f"STDOUT length: {len(result.stdout)} characters")
        logger.info(f"STDERR length: {len(result.stderr)} characters")
        
        if result.stdout:
            logger.info("📤 STDOUT (first 500 chars):")
            logger.info(result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout)
            print("📤 FULL STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            logger.warning("⚠️ STDERR:")
            logger.warning(result.stderr)
            print("⚠️ STDERR:")
            print(result.stderr)
        
        return result
        
    except subprocess.TimeoutExpired:
        logger.error("❌ Claude CLI timed out after 15 minutes")
        print("❌ Claude CLI timed out after 15 minutes")
        return None
    except Exception as e:
        logger.error(f"❌ Error running Claude CLI: {e}")
        logger.debug(f"Exception details: {type(e).__name__}: {e}")
        print(f"❌ Error running Claude CLI: {e}")
        return None

def check_generated_files():
    """Check what files were generated"""
    logger.info("📁 Checking generated files...")
    print("\n📁 Checking generated files...")
    
    try:
        # Check for Python scripts
        scripts = list(Path('.').glob('*.py'))
        logger.info(f"Found {len(scripts)} Python scripts: {[s.name for s in scripts]}")
        print(f"Python scripts: {[s.name for s in scripts]}")
        
        # Check agent_comm directory
        agent_comm = Path('agent_comm')
        if agent_comm.exists():
            comm_files = list(agent_comm.iterdir())
            logger.info(f"Agent comm directory has {len(comm_files)} files")
            print(f"Agent comm files: {[f.name for f in comm_files]}")
            
            charts_dir = agent_comm / 'charts'
            if charts_dir.exists():
                chart_files = list(charts_dir.iterdir())
                logger.info(f"Charts directory has {len(chart_files)} files")
                print(f"Chart files: {[f.name for f in chart_files]}")
            else:
                logger.warning("Charts directory does not exist")
        else:
            logger.warning("Agent comm directory does not exist")
        
        # Check for analysis results
        results = list(Path('.').glob('*analysis*'))
        logger.info(f"Found {len(results)} analysis files: {[r.name for r in results]}")
        print(f"Analysis files: {[r.name for r in results]}")
        
    except Exception as e:
        logger.error(f"Error checking files: {e}")
        print(f"Error checking files: {e}")

if __name__ == "__main__":
    logger.info("="*60)
    logger.info("🔍 STARTING DIRECT CLAUDE CLI DATA ANALYSIS")
    logger.info("="*60)
    
    print("🔍 Direct Claude CLI Data Analysis")
    print("="*50)
    
    # Run the analysis
    logger.info("Phase 1: Running Claude CLI analysis...")
    result = run_claude_analysis()
    
    if result:
        logger.info(f"Claude CLI execution completed with return code: {result.returncode}")
    else:
        logger.error("Claude CLI execution failed")
    
    # Check results
    logger.info("Phase 2: Checking generated files...")
    check_generated_files()
    
    logger.info("="*60)
    logger.info("📊 ANALYSIS ATTEMPT COMPLETED")
    logger.info("="*60)
    logger.info("🔍 Check the generated files and logs for detailed results")
    logger.info("📋 Log file saved to: direct_analysis.log")
    
    print("\n" + "="*50)
    print("📊 Analysis attempt completed!")
    print("🔍 Check the generated files for results.")
    print("📋 Detailed logs saved to: direct_analysis.log")