#!/usr/bin/env python3
"""
Advanced Insurance Analytics - Deep Business Intelligence Analysis
"""

import subprocess
import os
import logging
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def run_advanced_analysis():
    """Run advanced insurance business analytics"""
    
    # Set up environment
    os.environ['PATH'] = '/home/dumball/.nvm/versions/node/v18.17.0/bin:' + os.environ.get('PATH', '')
    os.environ['ANTHROPIC_API_KEY'] = os.getenv('ANTHROPIC_API_KEY')
    
    prompt = """
You are a senior insurance data scientist and business analyst. Perform ADVANCED analytics on 'finalapi.csv' containing 213,328 insurance agency records (2005-2013).

CRITICAL: DO NOT do basic data exploration. I need SOPHISTICATED BUSINESS INTELLIGENCE ANALYSIS.

Dataset context:
- Insurance agencies with premiums, loss ratios, retention rates, growth metrics
- AGENCY_ID, WRTN_PREM_AMT (written premiums), LOSS_RATIO, PROD_LINE, STATE_ABBR
- Time series data from 2005-2013 with 99999 as missing value indicator

CRITICAL INSTRUCTIONS:
- Execute Python scripts using: /home/dumball/training/.venv/bin/python script_name.py
- Install packages by first activating venv: source /home/dumball/training/.venv/bin/activate && uv pip install pandas scikit-learn plotly seaborn matplotlib
- Or use direct pip: /home/dumball/training/.venv/bin/pip install pandas scikit-learn plotly seaborn matplotlib
- DO NOT use Read/Grep/LS tools - only Python pandas for data access

REQUIRED ADVANCED ANALYSES - Write and execute Python scripts:

1. **FINANCIAL PERFORMANCE SEGMENTATION**:
   - Segment agencies into performance tiers (top 10%, middle 80%, bottom 10%)
   - Calculate ROI, profit margins, premium efficiency ratios
   - Identify high-value, high-growth agencies vs declining performers
   - Generate agency performance scorecards

2. **PREDICTIVE LOSS MODELING**:
   - Build models to predict loss ratios based on agency characteristics
   - Identify leading indicators of agency failure/success
   - Calculate risk-adjusted premium pricing recommendations
   - Generate early warning system for high-risk agencies

3. **MARKET OPPORTUNITY ANALYSIS**:
   - Geographic market penetration analysis by state
   - Product line profitability and cross-selling opportunities  
   - Competitive positioning and white space identification
   - Growth trajectory forecasting by market segment

4. **CUSTOMER LIFETIME VALUE ANALYTICS**:
   - Calculate CLV for different agency segments
   - Retention curve analysis and churn prediction
   - Revenue optimization strategies by agency type
   - Investment allocation recommendations

5. **ADVANCED VISUALIZATIONS**:
   - Executive dashboard with KPI scorecards
   - Geographic heat maps of performance metrics
   - Time series trend analysis with forecasting
   - Interactive business intelligence charts

DELIVERABLES:
- Execute comprehensive Python analysis (use pandas, scikit-learn, plotly)
- Save 10+ professional charts to 'agent_comm/charts/'
- Generate executive summary with actionable insights
- Create detailed markdown report at 'agent_comm/advanced_insurance_analysis.md'
- Export business intelligence data to CSV files

Focus on BUSINESS VALUE and ACTIONABLE RECOMMENDATIONS for insurance executives.
Use statistical modeling, machine learning, and advanced visualization techniques.
"""
    
    print("🚀 Running Advanced Insurance Analytics with Claude CLI...")
    
    try:
        cmd = [
            'claude',
            '--print', 
            '--allowedTools', 'Write Bash Edit MultiEdit',
            '--dangerously-skip-permissions',
            prompt
        ]
        
        print("💻 Executing advanced analytics...")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,  # 10 minute timeout for complex analysis
            cwd='/home/dumball/ccagent'
        )
        
        print(f"✅ Analysis completed with return code: {result.returncode}")
        
        if result.stdout:
            print("📊 ANALYSIS OUTPUT:")
            print(result.stdout)
        
        if result.stderr:
            print("⚠️ ERRORS:")
            print(result.stderr)
        
        return result
        
    except subprocess.TimeoutExpired:
        print("❌ Analysis timed out after 10 minutes")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def check_advanced_results():
    """Check generated advanced analysis files"""
    print("\n📈 Advanced Analysis Results:")
    
    # Check for analysis files
    agent_comm = Path('agent_comm')
    if agent_comm.exists():
        analysis_files = list(agent_comm.glob('*analysis*.md'))
        print(f"📋 Analysis Reports: {[f.name for f in analysis_files]}")
        
        charts_dir = agent_comm / 'charts'
        if charts_dir.exists():
            charts = list(charts_dir.glob('*.png'))
            print(f"📊 Generated Charts: {len(charts)} files")
            for chart in charts:
                print(f"  📈 {chart.name}")
        
        csv_files = list(agent_comm.glob('*.csv'))
        print(f"📊 Data Exports: {[f.name for f in csv_files]}")
    
    # Check for Python analysis scripts
    analysis_scripts = list(Path('.').glob('*analysis*.py'))
    print(f"🐍 Analysis Scripts: {[s.name for s in analysis_scripts if 'advanced' not in s.name]}")

if __name__ == "__main__":
    print("🏢 ADVANCED INSURANCE BUSINESS INTELLIGENCE ANALYTICS")
    print("="*60)
    
    result = run_advanced_analysis()
    check_advanced_results()
    
    print("\n" + "="*60)
    print("📊 Advanced analytics completed!")
    print("🔍 Check agent_comm/ for comprehensive business intelligence reports.")