#!/usr/bin/env python3
"""
Comprehensive CSV Data Analysis Script
Analyzes finalapi.csv and generates visualizations and reports
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path

# Set up directories
charts_dir = Path("agent_comm/charts")
charts_dir.mkdir(parents=True, exist_ok=True)

def load_and_examine_data():
    """Load CSV and perform initial examination"""
    print("Loading CSV file...")
    df = pd.read_csv('finalapi.csv')
    
    print(f"Data loaded successfully!")
    print(f"Shape: {df.shape}")
    print(f"Columns: {len(df.columns)}")
    print(f"Rows: {len(df)}")
    
    return df

def data_structure_analysis(df):
    """Analyze data structure and types"""
    print("\n=== DATA STRUCTURE ANALYSIS ===")
    
    # Basic info
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    
    # Column analysis
    print("\nColumn Names and Data Types:")
    for i, col in enumerate(df.columns, 1):
        dtype = df[col].dtype
        non_null = df[col].count()
        print(f"{i:2d}. {col:30s} | {str(dtype):10s} | Non-null: {non_null:,}")
    
    # Sample data
    print("\nFirst 5 rows:")
    print(df.head())
    
    return {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'column_info': [(col, str(df[col].dtype), df[col].count()) for col in df.columns]
    }

def data_quality_assessment(df):
    """Assess data quality - missing values, duplicates, anomalies"""
    print("\n=== DATA QUALITY ASSESSMENT ===")
    
    # Missing values
    missing_data = df.isnull().sum()
    missing_percent = (missing_data / len(df)) * 100
    
    print("Missing Values per Column:")
    missing_summary = pd.DataFrame({
        'Column': missing_data.index,
        'Missing_Count': missing_data.values,
        'Missing_Percent': missing_percent.values
    }).sort_values('Missing_Count', ascending=False)
    
    print(missing_summary[missing_summary['Missing_Count'] > 0])
    
    # Duplicate rows
    duplicates = df.duplicated().sum()
    print(f"\nDuplicate rows: {duplicates}")
    
    # Data ranges and potential anomalies
    print("\nNumerical columns statistics:")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print(df[numeric_cols].describe())
    
    # Check for unusual values (like 99999 which seems to be a placeholder)
    placeholder_analysis = {}
    for col in numeric_cols:
        if (df[col] == 99999).any():
            count_99999 = (df[col] == 99999).sum()
            placeholder_analysis[col] = count_99999
    
    if placeholder_analysis:
        print("\nColumns with placeholder value 99999:")
        for col, count in placeholder_analysis.items():
            print(f"{col}: {count} occurrences ({count/len(df)*100:.1f}%)")
    
    return {
        'missing_summary': missing_summary,
        'duplicates': duplicates,
        'placeholder_analysis': placeholder_analysis
    }

def generate_visualizations(df):
    """Generate and save visualizations"""
    print("\n=== GENERATING VISUALIZATIONS ===")
    
    # Set style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # 1. Missing data heatmap
    plt.figure(figsize=(15, 8))
    missing_data = df.isnull()
    sns.heatmap(missing_data, cbar=True, xticklabels=True, yticklabels=False)
    plt.title('Missing Data Heatmap')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('agent_comm/charts/missing_data_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Missing data heatmap saved")
    
    # 2. Data type distribution
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Column types
    type_counts = df.dtypes.value_counts()
    ax1.pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%')
    ax1.set_title('Distribution of Data Types')
    
    # Missing data by column
    missing_counts = df.isnull().sum()
    top_missing = missing_counts[missing_counts > 0].head(10)
    if len(top_missing) > 0:
        ax2.bar(range(len(top_missing)), top_missing.values)
        ax2.set_xticks(range(len(top_missing)))
        ax2.set_xticklabels(top_missing.index, rotation=45, ha='right')
        ax2.set_title('Top 10 Columns with Missing Values')
        ax2.set_ylabel('Missing Count')
    else:
        ax2.text(0.5, 0.5, 'No Missing Values', ha='center', va='center')
        ax2.set_title('Missing Values')
    
    plt.tight_layout()
    plt.savefig('agent_comm/charts/data_overview.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Data overview charts saved")
    
    # 3. Numerical distributions
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        # Select key numerical columns (exclude obvious placeholders)
        key_numeric = [col for col in numeric_cols if not (df[col] == 99999).all()][:8]
        
        if key_numeric:
            fig, axes = plt.subplots(2, 4, figsize=(20, 10))
            axes = axes.flatten()
            
            for i, col in enumerate(key_numeric):
                if i < len(axes):
                    # Filter out obvious placeholder values for better visualization
                    data_clean = df[col][df[col] != 99999]
                    if not data_clean.empty:
                        axes[i].hist(data_clean, bins=30, alpha=0.7)
                        axes[i].set_title(f'Distribution of {col}')
                        axes[i].set_xlabel(col)
                        axes[i].set_ylabel('Frequency')
            
            # Hide unused subplots
            for i in range(len(key_numeric), len(axes)):
                axes[i].set_visible(False)
            
            plt.tight_layout()
            plt.savefig('agent_comm/charts/numerical_distributions.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("✓ Numerical distributions saved")
    
    # 4. Correlation matrix (for numeric columns)
    if len(numeric_cols) > 1:
        # Select a subset of numeric columns and remove placeholder values
        corr_cols = [col for col in numeric_cols if not (df[col] == 99999).all()][:10]
        if len(corr_cols) > 1:
            corr_data = df[corr_cols].replace(99999, np.nan)
            correlation_matrix = corr_data.corr()
            
            plt.figure(figsize=(12, 10))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                       square=True, fmt='.2f')
            plt.title('Correlation Matrix of Key Numerical Variables')
            plt.tight_layout()
            plt.savefig('agent_comm/charts/correlation_matrix.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("✓ Correlation matrix saved")
    
    print("All visualizations saved to agent_comm/charts/")

def initial_observations(df, quality_results):
    """Generate initial observations and recommendations"""
    observations = []
    recommendations = []
    
    # Data size observation
    observations.append(f"Dataset contains {len(df):,} rows and {len(df.columns)} columns")
    
    # Missing data patterns
    missing_cols = quality_results['missing_summary']
    missing_cols_with_data = missing_cols[missing_cols['Missing_Count'] > 0]
    if len(missing_cols_with_data) > 0:
        observations.append(f"{len(missing_cols_with_data)} columns have missing values")
        recommendations.append("Investigate patterns in missing data - are they systematic or random?")
    
    # Placeholder values
    if quality_results['placeholder_analysis']:
        placeholder_count = len(quality_results['placeholder_analysis'])
        observations.append(f"{placeholder_count} columns contain placeholder value 99999")
        recommendations.append("Replace 99999 placeholder values with appropriate NaN or actual values")
    
    # Duplicates
    if quality_results['duplicates'] > 0:
        observations.append(f"{quality_results['duplicates']} duplicate rows found")
        recommendations.append("Review and remove duplicate rows if they are truly duplicates")
    
    # Data types
    numeric_cols = len(df.select_dtypes(include=[np.number]).columns)
    text_cols = len(df.select_dtypes(include=[object]).columns)
    observations.append(f"Data contains {numeric_cols} numerical and {text_cols} text columns")
    
    return observations, recommendations

def main():
    """Main analysis function"""
    print("Starting comprehensive CSV analysis...")
    
    # Load data
    df = load_and_examine_data()
    
    # Analyze structure
    structure_info = data_structure_analysis(df)
    
    # Assess quality
    quality_results = data_quality_assessment(df)
    
    # Generate visualizations
    generate_visualizations(df)
    
    # Generate observations
    observations, recommendations = initial_observations(df, quality_results)
    
    print("\n=== INITIAL OBSERVATIONS ===")
    for obs in observations:
        print(f"• {obs}")
    
    print("\n=== RECOMMENDATIONS ===")
    for rec in recommendations:
        print(f"• {rec}")
    
    # Return results for report generation
    return {
        'structure_info': structure_info,
        'quality_results': quality_results,
        'observations': observations,
        'recommendations': recommendations,
        'dataframe': df
    }

if __name__ == "__main__":
    results = main()
    print("\nAnalysis complete!")