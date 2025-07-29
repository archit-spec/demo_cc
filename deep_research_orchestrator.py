#!/usr/bin/env python3
"""
Deep Research Orchestrator - Main coordination agent
Orchestrates data analyst and sales research agents using Claude Code SDK
"""

import asyncio
import os
from datetime import datetime
from pathlib import Path

# Add claude CLI to PATH
os.environ['PATH'] = '/home/dumball/.nvm/versions/node/v18.17.0/bin:' + os.environ.get('PATH', '')

from data_analyst_agent import DataAnalystAgent
from sales_research_agent import SalesResearchAgent

try:
    from claude_code_sdk import query, ClaudeCodeOptions
except ImportError:
    print("Claude Code SDK not installed. Install with: pip install claude-code-sdk")
    exit(1)

class DeepResearchOrchestrator:
    def __init__(self, data_source: str, communication_dir: str = "agent_comm"):
        self.data_source = data_source
        self.communication_dir = Path(communication_dir)
        self.communication_dir.mkdir(exist_ok=True)
        
        # Initialize sub-agents
        self.data_analyst = DataAnalystAgent(data_source, str(self.communication_dir))
        self.sales_researcher = SalesResearchAgent(str(self.communication_dir))
        
    async def generate_final_sales_report(self) -> str:
        """Generate comprehensive final sales report using Claude Code"""
        
        prompt = f"""
        You are the chief strategist creating a comprehensive sales report. 
        
        Review ALL analysis files in '{self.communication_dir}/' and create a masterpiece sales report:
        
        1. **EXECUTIVE SUMMARY** (1-2 pages):
           - Key findings and strategic insights
           - Top revenue opportunities identified
           - Critical success factors
           - Investment recommendations
        
        2. **MARKET ANALYSIS** (2-3 pages):
           - Current market position assessment
           - Competitive landscape analysis
           - Growth opportunity mapping
           - Risk factor evaluation
        
        3. **STRATEGIC RECOMMENDATIONS** (2-3 pages):
           - Priority action items with timelines
           - Resource allocation guidance
           - Expected ROI projections
           - Implementation roadmap
        
        4. **TACTICAL EXECUTION PLAN** (3-4 pages):
           - Specific account targeting strategies
           - Sales process optimizations
           - Team deployment recommendations
           - Performance measurement framework
        
        5. **APPENDICES**:
           - Detailed data analysis summaries
           - Prospect lists and scoring criteria
           - Sales tools and templates
           - Monitoring and review protocols
        
        Create a professional, actionable report at '{self.communication_dir}/FINAL_SALES_REPORT.md'.
        Make it comprehensive yet readable, with clear action items and measurable outcomes.
        """
        
        options = ClaudeCodeOptions(
            max_turns=10,
            allowed_tools=["Read", "Write", "Glob", "Grep"],
        )
        
        result = ""
        async for message in query(prompt=prompt, options=options):
            if hasattr(message, 'content'):
                result += str(message.content) + "\n"
            else:
                result += str(message) + "\n"
        
        return result
    
    async def create_executive_dashboard(self) -> str:
        """Create executive dashboard summary using Claude Code"""
        
        prompt = f"""
        You are creating an executive dashboard. Based on all research in '{self.communication_dir}/', create:
        
        1. **KEY METRICS DASHBOARD**:
           - Top 10 KPIs with current status
           - Performance trending indicators
           - Alert/warning indicators
           - Success probability scores
        
        2. **OPPORTUNITY PIPELINE**:
           - Revenue opportunity sizes
           - Probability-weighted projections
           - Timeline expectations
           - Resource requirements
        
        3. **STRATEGIC PRIORITIES**:
           - Immediate actions (next 30 days)
           - Short-term initiatives (90 days)
           - Long-term strategies (1 year)
           - Success metrics for each
        
        4. **RISK ASSESSMENT MATRIX**:
           - High-risk accounts requiring attention
           - Market risks and mitigation strategies
           - Operational risks and contingencies
           - Financial impact assessments
        
        Create a concise executive summary at '{self.communication_dir}/EXECUTIVE_DASHBOARD.md'.
        """
        
        options = ClaudeCodeOptions(
            max_turns=5,
            allowed_tools=["Read", "Write", "Glob"],
        )
        
        result = ""
        async for message in query(prompt=prompt, options=options):
            if hasattr(message, 'content'):
                result += str(message.content) + "\n"
            else:
                result += str(message) + "\n"
        
        return result
    
    async def run_complete_research_pipeline(self) -> dict:
        """Execute the complete deep research pipeline"""
        print("🚀 Starting Deep Research Pipeline with Claude Code SDK...")
        print(f"📊 Data Source: {self.data_source}")
        print(f"📁 Communication Directory: {self.communication_dir}")
        print("="*60)
        
        results = {}
        
        try:
            # Phase 1: Data Analysis
            print("\n🔬 PHASE 1: DATA ANALYSIS")
            print("-" * 30)
            data_results = await self.data_analyst.run_complete_analysis()
            results['data_analysis'] = data_results
            print("✅ Data analysis phase completed successfully!")
            
            # Phase 2: Sales Research
            print("\n🎯 PHASE 2: SALES RESEARCH")
            print("-" * 30)
            sales_results = await self.sales_researcher.run_complete_sales_research()
            results['sales_research'] = sales_results
            print("✅ Sales research phase completed successfully!")
            
            # Phase 3: Final Report Generation
            print("\n📄 PHASE 3: FINAL REPORT GENERATION")
            print("-" * 40)
            print("📊 Generating comprehensive sales report...")
            final_report = await self.generate_final_sales_report()
            results['final_report'] = final_report
            
            print("📈 Creating executive dashboard...")
            dashboard = await self.create_executive_dashboard()
            results['executive_dashboard'] = dashboard
            
            print("✅ Final report generation completed successfully!")
            
            # Summary
            print("\n" + "="*60)
            print("🎉 DEEP RESEARCH PIPELINE COMPLETED!")
            print("="*60)
            print(f"📁 All results saved to: {self.communication_dir}/")
            print(f"📊 Final Sales Report: {self.communication_dir}/FINAL_SALES_REPORT.md")
            print(f"📈 Executive Dashboard: {self.communication_dir}/EXECUTIVE_DASHBOARD.md")
            print(f"📋 Total files generated: {len(list(self.communication_dir.glob('*.md')))}")
            
            return results
            
        except Exception as e:
            print(f"❌ Pipeline failed: {e}")
            raise
    
    def list_generated_files(self) -> list:
        """List all generated analysis files"""
        return sorted(list(self.communication_dir.glob('*.md')))
    
    async def validate_results(self) -> bool:
        """Validate that all expected files were generated"""
        expected_files = [
            'structure_analysis.md',
            'insurance_metrics.md', 
            'business_insights.md',
            'data_analysis_summary.md',
            'market_opportunities.md',
            'sales_strategies.md',
            'sales_intelligence_brief.md',
            'prospect_targeting.md',
            'FINAL_SALES_REPORT.md',
            'EXECUTIVE_DASHBOARD.md'
        ]
        
        generated_files = [f.name for f in self.list_generated_files()]
        missing_files = [f for f in expected_files if f not in generated_files]
        
        if missing_files:
            print(f"⚠️  Missing files: {missing_files}")
            return False
        
        print("✅ All expected files generated successfully!")
        return True

async def main():
    """Main execution function"""
    print("🤖 Deep Research Agent System")
    print("Powered by Claude Code SDK")
    print("="*50)
    
    # Initialize orchestrator
    orchestrator = DeepResearchOrchestrator("finalapi.csv")
    
    try:
        # Run complete pipeline
        results = await orchestrator.run_complete_research_pipeline()
        
        # Validate results
        await orchestrator.validate_results()
        
        # Show generated files
        files = orchestrator.list_generated_files()
        print(f"\n📋 Generated Files ({len(files)}):")
        for file in files:
            print(f"  📄 {file.name}")
        
        print("\n🎉 Deep research system ready!")
        print("🔍 Review the generated files for comprehensive insights.")
        
    except Exception as e:
        print(f"❌ System error: {e}")

if __name__ == "__main__":
    asyncio.run(main())