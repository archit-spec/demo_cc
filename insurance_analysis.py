#!/usr/bin/env python3
"""
Comprehensive Insurance Dataset Analysis Script
Analyzes finalapi.csv with 213,328 rows and 49 columns of insurance agency data (2005-2013)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def create_output_directories():
    """Create necessary output directories"""
    Path('agent_comm/charts').mkdir(parents=True, exist_ok=True)
    print("✓ Created output directories")

def load_and_basic_info(filepath):
    """Load dataset and display basic information"""
    print("="*60)
    print("1. DATA STRUCTURE ANALYSIS")
    print("="*60)
    
    try:
        df = pd.read_csv(filepath)
        print(f"Dataset loaded successfully from: {filepath}")
        print(f"Dataset shape: {df.shape}")
        print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        print("\nColumn Information:")
        print("-" * 40)
        df.info()
        
        print("\nData Types Summary:")
        print("-" * 40)
        print(df.dtypes.value_counts())
        
        print("\nFirst 5 rows:")
        print("-" * 40)
        print(df.head())
        
        return df
        
    except FileNotFoundError:
        print(f"ERROR: File {filepath} not found!")
        return None
    except Exception as e:
        print(f"ERROR loading data: {e}")
        return None

def data_quality_assessment(df):
    """Perform comprehensive data quality assessment"""
    print("\n" + "="*60)
    print("2. DATA QUALITY ASSESSMENT")
    print("="*60)
    
    # Missing values analysis
    print("Missing Values Analysis:")
    print("-" * 40)
    missing_stats = df.isnull().sum()
    missing_pct = (missing_stats / len(df)) * 100
    missing_df = pd.DataFrame({
        'Missing_Count': missing_stats,
        'Missing_Percentage': missing_pct
    }).sort_values('Missing_Count', ascending=False)
    
    print(f"Total missing values: {missing_stats.sum()}")
    print(f"Columns with missing data: {(missing_stats > 0).sum()}")
    print("\nTop 10 columns with missing data:")
    print(missing_df.head(10))
    
    # Duplicates analysis
    print(f"\nDuplicate Analysis:")
    print("-" * 40)
    duplicates = df.duplicated().sum()
    print(f"Total duplicate rows: {duplicates}")
    print(f"Duplicate percentage: {(duplicates/len(df))*100:.2f}%")
    
    # Placeholder values (99999) analysis
    print(f"\nPlaceholder Values (99999) Analysis:")
    print("-" * 40)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    placeholder_stats = {}
    
    for col in numeric_cols:
        count_99999 = (df[col] == 99999).sum()
        if count_99999 > 0:
            placeholder_stats[col] = {
                'count': count_99999,
                'percentage': (count_99999/len(df))*100
            }
    
    if placeholder_stats:
        print("Columns with 99999 placeholder values:")
        for col, stats in sorted(placeholder_stats.items(), key=lambda x: x[1]['count'], reverse=True):
            print(f"  {col}: {stats['count']} ({stats['percentage']:.2f}%)")
    else:
        print("No 99999 placeholder values found")
    
    return missing_df, placeholder_stats

def generate_visualizations(df):
    """Generate comprehensive visualizations"""
    print("\n" + "="*60)
    print("3. GENERATING VISUALIZATIONS")
    print("="*60)
    
    # Set style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # 1. Missing data heatmap
    print("Creating missing data heatmap...")
    plt.figure(figsize=(15, 8))
    missing_data = df.isnull()
    if missing_data.any().any():
        sns.heatmap(missing_data, cbar=True, yticklabels=False, cmap='viridis')
        plt.title('Missing Data Heatmap', fontsize=16, fontweight='bold')
        plt.xlabel('Columns')
        plt.tight_layout()
        plt.savefig('agent_comm/charts/missing_data_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Missing data heatmap saved")
    else:
        print("✓ No missing data to visualize")
    
    # 2. Key column distributions
    print("Creating distribution plots for key columns...")
    key_columns = ['WRTN_PREM_AMT', 'LOSS_RATIO', 'PROD_LINE', 'STATE_ABBR']
    available_key_cols = [col for col in key_columns if col in df.columns]
    
    if available_key_cols:
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        axes = axes.ravel()
        
        for i, col in enumerate(available_key_cols[:4]):
            if i >= 4:
                break
                
            if df[col].dtype in ['object', 'category']:
                # Categorical data
                top_values = df[col].value_counts().head(10)
                top_values.plot(kind='bar', ax=axes[i])
                axes[i].set_title(f'Top 10 {col} Distribution')
                axes[i].tick_params(axis='x', rotation=45)
            else:
                # Numerical data - filter out placeholder values
                clean_data = df[col][(df[col] != 99999) & df[col].notna()]
                if len(clean_data) > 0:
                    clean_data.hist(bins=50, ax=axes[i], alpha=0.7)
                    axes[i].set_title(f'{col} Distribution (excluding 99999)')
                    axes[i].set_xlabel(col)
                    axes[i].set_ylabel('Frequency')
        
        plt.tight_layout()
        plt.savefig('agent_comm/charts/key_distributions.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Distribution plots saved")
    
    # 3. Correlation matrix for numeric columns
    print("Creating correlation matrix...")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 1:
        # Filter out placeholder values for correlation
        df_numeric = df[numeric_cols].replace(99999, np.nan)
        correlation_matrix = df_numeric.corr()
        
        plt.figure(figsize=(12, 10))
        mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
        sns.heatmap(correlation_matrix, mask=mask, annot=False, cmap='coolwarm', 
                   center=0, square=True, linewidths=0.5)
        plt.title('Correlation Matrix (excluding placeholder values)', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('agent_comm/charts/correlation_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Correlation matrix saved")

def save_results(df, missing_df, placeholder_stats):
    """Save summary statistics and create markdown report"""
    print("\n" + "="*60)
    print("4. SAVING RESULTS")
    print("="*60)
    
    # Save summary statistics to CSV
    print("Saving summary statistics...")
    summary_stats = df.describe()
    summary_stats.to_csv('agent_comm/summary_statistics.csv')
    print("✓ Summary statistics saved to agent_comm/summary_statistics.csv")
    
    # Save missing data analysis
    missing_df.to_csv('agent_comm/missing_data_analysis.csv')
    print("✓ Missing data analysis saved to agent_comm/missing_data_analysis.csv")
    
    # Create comprehensive markdown report
    print("Creating markdown report...")
    report_content = f"""# Insurance Dataset Structure Analysis Report

## Dataset Overview
- **File**: finalapi.csv
- **Shape**: {df.shape[0]:,} rows × {df.shape[1]} columns
- **Time Period**: 2005-2013
- **Memory Usage**: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB

## Column Information
Total columns: {len(df.columns)}

### Data Types Distribution
"""
    
    dtype_counts = df.dtypes.value_counts()
    for dtype, count in dtype_counts.items():
        report_content += f"- **{dtype}**: {count} columns\n"
    
    report_content += f"""
## Data Quality Assessment

### Missing Data
- **Total missing values**: {df.isnull().sum().sum():,}
- **Columns with missing data**: {(df.isnull().sum() > 0).sum()}
- **Complete rows**: {df.dropna().shape[0]:,} ({(df.dropna().shape[0]/len(df))*100:.1f}%)

### Duplicate Data
- **Duplicate rows**: {df.duplicated().sum():,}
- **Duplicate percentage**: {(df.duplicated().sum()/len(df))*100:.2f}%

### Placeholder Values (99999)
"""
    
    if placeholder_stats:
        report_content += f"Found placeholder values in {len(placeholder_stats)} columns:\n\n"
        for col, stats in sorted(placeholder_stats.items(), key=lambda x: x[1]['count'], reverse=True)[:10]:
            report_content += f"- **{col}**: {stats['count']:,} values ({stats['percentage']:.2f}%)\n"
    else:
        report_content += "No 99999 placeholder values detected.\n"
    
    report_content += f"""
## Key Columns Analysis

### Available Key Columns
"""
    key_columns = ['AGENCY_ID', 'WRTN_PREM_AMT', 'LOSS_RATIO', 'PROD_LINE', 'STATE_ABBR']
    for col in key_columns:
        if col in df.columns:
            if df[col].dtype in ['object', 'category']:
                unique_count = df[col].nunique()
                report_content += f"- **{col}**: {unique_count:,} unique values\n"
            else:
                clean_data = df[col][(df[col] != 99999) & df[col].notna()]
                if len(clean_data) > 0:
                    report_content += f"- **{col}**: Range {clean_data.min():.2f} to {clean_data.max():.2f}, Mean: {clean_data.mean():.2f}\n"
                else:
                    report_content += f"- **{col}**: No valid data (all missing or placeholder)\n"
    
    report_content += f"""
## Generated Files
- `agent_comm/charts/missing_data_heatmap.png` - Visualization of missing data patterns
- `agent_comm/charts/key_distributions.png` - Distribution plots for key variables
- `agent_comm/charts/correlation_matrix.png` - Correlation matrix of numeric variables
- `agent_comm/summary_statistics.csv` - Descriptive statistics for all numeric columns
- `agent_comm/missing_data_analysis.csv` - Detailed missing data analysis

## Recommendations
1. **Handle Missing Data**: Consider imputation strategies for columns with high missing rates
2. **Address Placeholders**: Replace 99999 values with appropriate missing value indicators
3. **Data Validation**: Investigate duplicate records and unusual value patterns
4. **Further Analysis**: Focus on temporal trends (2005-2013) and state-level patterns

---
*Report generated on {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    with open('agent_comm/structure_analysis.md', 'w') as f:
        f.write(report_content)
    
    print("✓ Comprehensive report saved to agent_comm/structure_analysis.md")

def main():
    """Main execution function"""
    print("Insurance Dataset Analysis - Starting...")
    print("="*60)
    
    # Create output directories
    create_output_directories()
    
    # Load and analyze data
    df = load_and_basic_info('finalapi.csv')
    if df is None:
        return
    
    # Data quality assessment
    missing_df, placeholder_stats = data_quality_assessment(df)
    
    # Generate visualizations
    generate_visualizations(df)
    
    # Save results
    save_results(df, missing_df, placeholder_stats)
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE!")
    print("="*60)
    print("Check the 'agent_comm/' directory for all generated files:")
    print("- structure_analysis.md (comprehensive report)")
    print("- charts/ (visualizations)")
    print("- summary_statistics.csv")
    print("- missing_data_analysis.csv")

if __name__ == "__main__":
    main()