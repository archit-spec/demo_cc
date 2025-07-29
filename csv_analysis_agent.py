#!/usr/bin/env python3
"""
CSV Analysis Agent - Autonomous CSV data analysis using pandas
Works with finalapi.csv for comprehensive data analysis
"""

import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AutonomousCSVAnalysisAgent:
    def __init__(self, csv_path='finalapi.csv'):
        self.csv_path = csv_path
        self.df = None
        self.analysis_results = {}
        
        # Ensure output directory exists
        self.output_dir = Path('agent_comm')
        self.output_dir.mkdir(exist_ok=True)
        
        # Ensure charts directory exists
        self.charts_dir = self.output_dir / 'charts'
        self.charts_dir.mkdir(exist_ok=True)
    
    def load_data(self):
        """Load CSV data with error handling"""
        try:
            print(f"📊 Loading data from {self.csv_path}")
            self.df = pd.read_csv(self.csv_path)
            print(f"✅ Successfully loaded {len(self.df)} rows and {len(self.df.columns)} columns")
            return True
        except FileNotFoundError:
            print(f"❌ Error: {self.csv_path} not found")
            return False
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def get_data_overview(self):
        """Get basic data overview and structure"""
        if self.df is None:
            return None
            
        overview = {
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'dtypes': self.df.dtypes.to_dict(),
            'memory_usage': self.df.memory_usage(deep=True).sum(),
            'missing_values': self.df.isnull().sum().to_dict(),
            'duplicate_rows': self.df.duplicated().sum()
        }
        
        # Get first few rows
        overview['sample_data'] = self.df.head().to_dict('records')
        
        return overview
    
    def analyze_data_quality(self):
        """Analyze data quality issues"""
        if self.df is None:
            return None
            
        quality_report = {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'missing_data': {},
            'data_types': {},
            'unique_values': {},
            'potential_issues': []
        }
        
        # Check for missing values
        missing_counts = self.df.isnull().sum()
        quality_report['missing_data'] = {
            col: int(count) for col, count in missing_counts.items() if count > 0
        }
        
        # Check for 99999 placeholder values (specific to finalapi.csv)
        placeholder_counts = (self.df == 99999).sum()
        quality_report['placeholder_99999'] = {
            col: int(count) for col, count in placeholder_counts.items() if count > 0
        }
        
        # Data types analysis
        quality_report['data_types'] = self.df.dtypes.astype(str).to_dict()
        
        # Unique values for categorical columns
        for col in self.df.columns:
            unique_count = self.df[col].nunique()
            if unique_count < 50:  # Likely categorical
                quality_report['unique_values'][col] = {
                    'count': int(unique_count),
                    'values': self.df[col].value_counts().head(10).to_dict()
                }
        
        return quality_report
    
    def analyze_numeric_columns(self):
        """Analyze numeric columns for statistical insights"""
        if self.df is None:
            return None
            
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        numeric_analysis = {}
        
        for col in numeric_cols:
            # Replace 99999 with NaN for analysis
            clean_data = self.df[col].replace(99999, np.nan)
            
            numeric_analysis[col] = {
                'count': int(clean_data.count()),
                'mean': float(clean_data.mean()) if not clean_data.empty else None,
                'median': float(clean_data.median()) if not clean_data.empty else None,
                'std': float(clean_data.std()) if not clean_data.empty else None,
                'min': float(clean_data.min()) if not clean_data.empty else None,
                'max': float(clean_data.max()) if not clean_data.empty else None,
                'percentiles': {
                    '25%': float(clean_data.quantile(0.25)) if not clean_data.empty else None,
                    '75%': float(clean_data.quantile(0.75)) if not clean_data.empty else None
                }
            }
        
        return numeric_analysis
    
    def generate_business_insights(self):
        """Generate business-specific insights for insurance data"""
        if self.df is None:
            return None
            
        insights = {
            'agency_performance': {},
            'geographic_analysis': {},
            'product_line_analysis': {},
            'financial_metrics': {}
        }
        
        # Check for key insurance columns
        key_columns = {
            'agency_id': ['AGENCY_ID', 'agency_id', 'AgencyID'],
            'premium': ['WRTN_PREM_AMT', 'premium', 'written_premium'],
            'loss_ratio': ['LOSS_RATIO', 'loss_ratio'],
            'state': ['STATE_ABBR', 'state', 'State'],
            'product_line': ['PROD_LINE', 'product_line', 'ProductLine']
        }
        
        # Find matching columns
        available_columns = {}
        for key, possible_names in key_columns.items():
            for name in possible_names:
                if name in self.df.columns:
                    available_columns[key] = name
                    break
        
        # Agency performance analysis
        if 'agency_id' in available_columns:
            agency_col = available_columns['agency_id']
            insights['agency_performance']['total_agencies'] = int(self.df[agency_col].nunique())
            
            if 'premium' in available_columns:
                premium_col = available_columns['premium']
                # Replace 99999 with NaN for calculations
                clean_premiums = self.df[premium_col].replace(99999, np.nan)
                
                insights['financial_metrics']['total_premium'] = float(clean_premiums.sum())
                insights['financial_metrics']['avg_premium'] = float(clean_premiums.mean())
                
                # Top agencies by premium
                top_agencies = self.df.groupby(agency_col)[premium_col].sum().sort_values(ascending=False).head(10)
                insights['agency_performance']['top_agencies_by_premium'] = top_agencies.to_dict()
        
        # Geographic analysis
        if 'state' in available_columns:
            state_col = available_columns['state']
            state_counts = self.df[state_col].value_counts()
            insights['geographic_analysis']['agencies_by_state'] = state_counts.head(10).to_dict()
            insights['geographic_analysis']['total_states'] = int(self.df[state_col].nunique())
        
        # Product line analysis
        if 'product_line' in available_columns:
            product_col = available_columns['product_line']
            product_counts = self.df[product_col].value_counts()
            insights['product_line_analysis']['distribution'] = product_counts.to_dict()
        
        return insights
    
    def run_comprehensive_analysis(self):
        """Run complete analysis pipeline"""
        print("🤖 AUTONOMOUS CSV ANALYSIS AGENT STARTING...")
        print("=" * 60)
        
        # Load data
        if not self.load_data():
            return None
        
        # Run all analyses
        print("\n📊 PHASE 1: DATA OVERVIEW")
        overview = self.get_data_overview()
        
        print("\n🔍 PHASE 2: DATA QUALITY ANALYSIS")
        quality = self.analyze_data_quality()
        
        print("\n📈 PHASE 3: NUMERIC ANALYSIS")
        numeric = self.analyze_numeric_columns()
        
        print("\n💼 PHASE 4: BUSINESS INSIGHTS")
        insights = self.generate_business_insights()
        
        # Compile results
        self.analysis_results = {
            'overview': overview,
            'quality': quality,
            'numeric_analysis': numeric,
            'business_insights': insights,
            'timestamp': datetime.now().isoformat(),
            'csv_file': self.csv_path
        }
        
        # Save results
        self.save_results()
        
        print("\n✅ ANALYSIS COMPLETED")
        print(f"📁 Results saved to: {self.output_dir}/")
        
        return self.analysis_results
    
    def save_results(self):
        """Save analysis results to files"""
        if not self.analysis_results:
            return
        
        # Save JSON results
        json_file = self.output_dir / 'csv_analysis_results.json'
        with open(json_file, 'w') as f:
            json.dump(self.analysis_results, f, indent=2, default=str)
        
        # Save summary statistics to CSV
        if self.df is not None:
            numeric_df = self.df.select_dtypes(include=[np.number])
            if not numeric_df.empty:
                summary = numeric_df.describe()
                summary.to_csv(self.output_dir / 'summary_statistics.csv')
        
        # Create markdown report
        self.create_markdown_report()
        
        print(f"📄 JSON results: {json_file}")
        print(f"📊 Summary stats: {self.output_dir / 'summary_statistics.csv'}")
        print(f"📝 Report: {self.output_dir / 'csv_analysis_report.md'}")
    
    def create_markdown_report(self):
        """Create a comprehensive markdown report"""
        if not self.analysis_results:
            return
        
        report_lines = [
            "# CSV Data Analysis Report",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**File:** {self.csv_path}",
            "",
            "## Data Overview",
            f"- **Rows:** {self.analysis_results['overview']['shape'][0]:,}",
            f"- **Columns:** {self.analysis_results['overview']['shape'][1]:,}",
            f"- **Memory Usage:** {self.analysis_results['overview']['memory_usage']:,} bytes",
            f"- **Duplicate Rows:** {self.analysis_results['overview']['duplicate_rows']:,}",
            "",
            "## Data Quality Summary"
        ]
        
        # Missing data summary
        missing_data = self.analysis_results['quality']['missing_data']
        if missing_data:
            report_lines.extend([
                "### Missing Values",
                "| Column | Missing Count |",
                "|--------|---------------|"
            ])
            for col, count in missing_data.items():
                report_lines.append(f"| {col} | {count:,} |")
        
        # Placeholder values (99999)
        placeholder_data = self.analysis_results['quality'].get('placeholder_99999', {})
        if placeholder_data:
            report_lines.extend([
                "",
                "### Placeholder Values (99999)",
                "| Column | Count |",
                "|--------|-------|"
            ])
            for col, count in placeholder_data.items():
                report_lines.append(f"| {col} | {count:,} |")
        
        # Business insights
        business_insights = self.analysis_results.get('business_insights', {})
        if business_insights:
            report_lines.extend([
                "",
                "## Business Insights"
            ])
            
            # Financial metrics
            financial = business_insights.get('financial_metrics', {})
            if financial:
                report_lines.extend([
                    "### Financial Overview",
                    f"- **Total Premium:** ${financial.get('total_premium', 0):,.2f}",
                    f"- **Average Premium:** ${financial.get('avg_premium', 0):,.2f}"
                ])
            
            # Geographic analysis
            geographic = business_insights.get('geographic_analysis', {})
            if geographic:
                report_lines.extend([
                    "",
                    "### Geographic Distribution",
                    f"- **Total States:** {geographic.get('total_states', 0)}"
                ])
        
        # Save report
        report_file = self.output_dir / 'csv_analysis_report.md'
        with open(report_file, 'w') as f:
            f.write('\n'.join(report_lines))

def main():
    """Main execution function"""
    # Check if CSV file exists
    csv_file = 'finalapi.csv'
    if not os.path.exists(csv_file):
        print(f"❌ Error: {csv_file} not found in current directory")
        print("Available files:")
        for f in os.listdir('.'):
            if f.endswith('.csv'):
                print(f"  📄 {f}")
        return
    
    # Run analysis
    agent = AutonomousCSVAnalysisAgent(csv_file)
    results = agent.run_comprehensive_analysis()
    
    if results:
        print("\n" + "="*60)
        print("📊 ANALYSIS SUMMARY")
        print("="*60)
        print(f"✅ Analyzed {results['overview']['shape'][0]:,} rows")
        print(f"✅ Processed {results['overview']['shape'][1]:,} columns")
        print(f"📁 Results saved to: agent_comm/")
    else:
        print("❌ Analysis failed")

if __name__ == "__main__":
    main()