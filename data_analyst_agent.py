#!/usr/bin/env python3
"""
Data Analyst Agent using Claude Code Python SDK
Leverages Claude Code's capabilities for CSV/SQLite analysis
"""

import asyncio
import os
import logging
import traceback
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent_debug.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Add claude CLI to PATH and set Python path and API key
os.environ['PATH'] = '/home/dumball/.nvm/versions/node/v18.17.0/bin:' + os.environ.get('PATH', '')
os.environ['PYTHON'] = '/home/dumball/training/.venv/bin/python'
os.environ['ANTHROPIC_API_KEY'] = os.getenv('ANTHROPIC_API_KEY')
logger.info(f"Updated PATH: {os.environ['PATH'][:200]}...")
logger.info(f"Set PYTHON to: {os.environ['PYTHON']}")
logger.info("API key configured")

try:
    from claude_code_sdk import query, ClaudeCodeOptions
except ImportError:
    print("Claude Code SDK not installed. Install with: pip install claude-code-sdk")
    exit(1)

class DataAnalystAgent:
    def __init__(self, data_source: str, communication_dir: str = "agent_comm"):
        self.data_source = data_source
        self.communication_dir = Path(communication_dir)
        self.communication_dir.mkdir(exist_ok=True)
        
    async def analyze_csv_structure(self) -> str:
        """Use Claude Code to analyze CSV structure and data quality"""
        
        logger.info("Starting CSV structure analysis...")
        
        prompt = f"""
        You are a specialized data analyst. Analyze the insurance dataset '{self.data_source}' which contains:
        - 213,328 rows of insurance agency data
        - 49 columns including: AGENCY_ID, WRTN_PREM_AMT, LOSS_RATIO, PROD_LINE, STATE_ABBR, etc.
        - Data from 2005-2013 covering premiums, loss ratios, agency performance
        - Contains placeholder value 99999 for missing data
        
        CRITICAL INSTRUCTIONS:
        - DO NOT use Read, Grep, or LS tools to examine files
        - START by writing a complete Python analysis script
        - Execute the script using: /home/dumball/training/.venv/bin/python script_name.py
        - Install packages with: uv pip install pandas matplotlib seaborn
        - Access data ONLY through: df = pd.read_csv('{self.data_source}')
        
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
           - Create '{self.communication_dir}/charts/' directory
           - Save missing data heatmap
           - Distribution plots for key columns
           - Correlation matrix
        
        4. **Save Results**:
           - Export summary statistics to CSV
           - Create markdown report at '{self.communication_dir}/structure_analysis.md'
        
        Write the complete Python script first, then execute it. Include all imports and error handling.
        """
        
        logger.debug(f"Prompt: {prompt[:200]}...")
        
        try:
            options = ClaudeCodeOptions(
                max_turns=15,
                allowed_tools=["Read", "Write", "Bash", "Grep", "Edit", "MultiEdit"]
            )
            logger.info(f"Created options with tools: {options.allowed_tools}")
            
            result = ""
            message_count = 0
            
            logger.info("Starting query iteration...")
            async for message in query(prompt=prompt, options=options):
                message_count += 1
                logger.info(f"\n{'='*60}")
                logger.info(f"MESSAGE #{message_count}: {type(message).__name__}")
                logger.info(f"{'='*60}")
                
                if hasattr(message, 'content'):
                    content = str(message.content)
                    logger.info(f"FULL CONTENT:\n{content}")
                    result += content + "\n"
                    print(f"\n🔍 Message #{message_count} ({type(message).__name__}):")
                    print(content[:200] + "..." if len(content) > 200 else content)
                else:
                    msg_str = str(message)
                    logger.info(f"FULL MESSAGE:\n{msg_str}")
                    result += msg_str + "\n"
                    print(f"\n📝 Message #{message_count} ({type(message).__name__}):")
                    print(msg_str[:200] + "..." if len(msg_str) > 200 else msg_str)
            
            logger.info(f"Query completed with {message_count} messages, result length: {len(result)}")
            return result
            
        except Exception as e:
            logger.error(f"Error in analyze_csv_structure: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
    
    async def analyze_insurance_metrics(self) -> str:
        """Use Claude Code to analyze insurance-specific metrics"""
        
        prompt = f"""
        You are an insurance data specialist. Analyze '{self.data_source}' for insurance metrics.
        
        Dataset info: 213,328 rows of insurance agency data (2005-2013) with columns:
        AGENCY_ID, WRTN_PREM_AMT, LOSS_RATIO, LOSS_RATIO_3YR, PROD_LINE, STATE_ABBR, 
        RETENTION_RATIO, GROWTH_RATE_3YR, ACTIVE_PRODUCERS, etc. (99999 = missing values)
        
        CRITICAL INSTRUCTIONS:
        - DO NOT use Read, Grep, or LS tools to examine files
        - START by writing a complete Python analysis script
        - Execute using: /home/dumball/training/.venv/bin/python script_name.py
        - Install with: uv pip install pandas matplotlib seaborn plotly
        - Access data ONLY through: df = pd.read_csv('{self.data_source}')
        
        WRITE AND EXECUTE a comprehensive Python script for insurance analysis:
        
        1. **Premium Analysis**:
           - Total/average written premiums (WRTN_PREM_AMT)
           - Premium trends by year and state
           - New business vs renewal analysis
        
        2. **Loss Ratio Analysis** (exclude 99999 values):
           - Current loss ratios distribution
           - 3-year trends by product line
           - High-risk agencies identification
        
        3. **Agency Performance**:
           - Top agencies by premium volume
           - Retention rates analysis
           - Producer productivity metrics
        
        4. **Geographic & Product Analysis**:
           - State performance comparison
           - Product line profitability
           - Growth opportunities identification
        
        5. **Advanced Visualizations**:
           - Executive dashboards with charts
           - Save all plots to '{self.communication_dir}/charts/'
           - Interactive business intelligence plots
        
        Write complete Python script first, then execute it. Save analysis to '{self.communication_dir}/insurance_metrics.md'.
        """
        
        options = ClaudeCodeOptions(
            max_turns=15,
            allowed_tools=["Read", "Write", "Bash", "Grep", "Edit", "MultiEdit"]
        )
        
        result = ""
        async for message in query(prompt=prompt, options=options):
            if hasattr(message, 'content'):
                result += str(message.content) + "\n"
            else:
                result += str(message) + "\n"
        
        return result
    
    async def identify_business_insights(self) -> str:
        """Use Claude Code to identify actionable business insights"""
        
        prompt = f"""
        You are a business intelligence analyst. Based on '{self.data_source}', identify:
        
        1. **Growth Opportunities**:
           - Underperforming agencies with high potential
           - Geographic markets for expansion
           - Product lines with growth potential
        
        2. **Risk Assessment**:
           - Agencies/regions with concerning loss ratios
           - Trends indicating increased risk
           - Early warning indicators
        
        3. **Performance Benchmarks**:
           - Top quartile performer characteristics
           - Industry benchmarks and comparisons
           - Best practices from high performers
        
        4. **Strategic Recommendations**:
           - Priority actions for improvement
           - Resource allocation suggestions
           - Market positioning opportunities
        
        Focus on actionable insights that can drive business decisions.
        Save your insights to '{self.communication_dir}/business_insights.md'.
        """
        
        options = ClaudeCodeOptions(
            max_turns=12,
            allowed_tools=["Read", "Write", "Bash", "Grep"]
        )
        
        result = ""
        async for message in query(prompt=prompt, options=options):
            if hasattr(message, 'content'):
                result += str(message.content) + "\n"
            else:
                result += str(message) + "\n"
        
        return result
    
    async def create_data_summary(self) -> str:
        """Create comprehensive summary for sales research agent"""
        
        prompt = f"""
        You are synthesizing data analysis results. Review all analysis files in '{self.communication_dir}/' and create:
        
        1. **Executive Summary**:
           - Key findings across all analyses
           - Most critical insights
           - Priority recommendations
        
        2. **Sales Intelligence Brief**:
           - Target opportunities for sales teams
           - Market positioning insights
           - Competitive advantages to highlight
        
        3. **Data-Driven Talking Points**:
           - Key statistics for sales presentations
           - Success stories and proof points
           - Market trends and opportunities
        
        Create a comprehensive summary at '{self.communication_dir}/data_analysis_summary.md' 
        that the sales research agent can build upon for targeted sales strategies.
        """
        
        options = ClaudeCodeOptions(
            max_turns=8,
            allowed_tools=["Read", "Write", "Glob"]
        )
        
        result = ""
        async for message in query(prompt=prompt, options=options):
            if hasattr(message, 'content'):
                result += str(message.content) + "\n"
            else:
                result += str(message) + "\n"
        
        return result
    
    async def run_complete_analysis(self) -> list:
        """Execute full data analysis pipeline"""
        logger.info("🔍 Starting comprehensive data analysis with Claude Code...")
        print("🔍 Starting comprehensive data analysis with Claude Code...")
        
        results = []
        
        # Step 1: Data structure analysis
        try:
            logger.info("📊 Step 1: Analyzing data structure...")
            print("📊 Step 1: Analyzing data structure...")
            structure_result = await self.analyze_csv_structure()
            results.append(("Structure Analysis", structure_result))
            logger.info(f"Step 1 completed, result length: {len(structure_result)}")
            print("✅ Step 1: Data structure analysis completed!")
        except Exception as e:
            logger.error(f"❌ Step 1 failed: {e}")
            print(f"❌ Step 1 failed: {e}")
            results.append(("Structure Analysis", f"Failed: {e}"))
        
        # Step 2: Insurance metrics analysis
        try:
            logger.info("📈 Step 2: Analyzing insurance metrics...")
            print("📈 Step 2: Analyzing insurance metrics...")
            metrics_result = await self.analyze_insurance_metrics()
            results.append(("Insurance Metrics", metrics_result))
            logger.info(f"Step 2 completed, result length: {len(metrics_result)}")
            print("✅ Step 2: Insurance metrics analysis completed!")
        except Exception as e:
            logger.error(f"❌ Step 2 failed: {e}")
            print(f"❌ Step 2 failed: {e}")
            results.append(("Insurance Metrics", f"Failed: {e}"))
        
        # Step 3: Business insights
        try:
            logger.info("💡 Step 3: Identifying business insights...")
            print("💡 Step 3: Identifying business insights...")
            insights_result = await self.identify_business_insights()
            results.append(("Business Insights", insights_result))
            logger.info(f"Step 3 completed, result length: {len(insights_result)}")
            print("✅ Step 3: Business insights analysis completed!")
        except Exception as e:
            logger.error(f"❌ Step 3 failed: {e}")
            print(f"❌ Step 3 failed: {e}")
            results.append(("Business Insights", f"Failed: {e}"))
        
        # Step 4: Summary
        try:
            logger.info("📋 Step 4: Creating comprehensive summary...")
            print("📋 Step 4: Creating comprehensive summary...")
            summary_result = await self.create_data_summary()
            results.append(("Data Summary", summary_result))
            logger.info(f"Step 4 completed, result length: {len(summary_result)}")
            print("✅ Step 4: Summary creation completed!")
        except Exception as e:
            logger.error(f"❌ Step 4 failed: {e}")
            print(f"❌ Step 4 failed: {e}")
            results.append(("Data Summary", f"Failed: {e}"))
        
        logger.info("✅ Data analysis pipeline completed!")
        print("✅ Data analysis pipeline completed!")
        print(f"📁 Results saved in: {self.communication_dir}/")
        
        return results

async def main():
    """Main execution function"""
    logger.info("Main function starting...")
    
    try:
        agent = DataAnalystAgent("finalapi.csv")
        logger.info(f"Created agent with data source: {agent.data_source}")
        
        results = await agent.run_complete_analysis()
        
        print("\n" + "="*50)
        print("📊 DATA ANALYSIS SUMMARY")
        print("="*50)
        
        for step_name, result in results:
            print(f"\n✅ {step_name}: Completed")
            logger.info(f"{step_name}: Completed with {len(result)} characters")
        
        print(f"\n📁 All analysis files saved to: {agent.communication_dir}/")
        print("🤝 Ready for sales research agent to process!")
        
        logger.info("Main function completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Error in main: {e}")
        logger.error(f"Full main traceback: {traceback.format_exc()}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())