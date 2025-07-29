#!/usr/bin/env python3
"""
Data Structure Analysis Script for finalapi.csv
Analyzes CSV file structure, data types, and basic statistics
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def analyze_csv_structure(file_path):
    """Analyze the structure and basic properties of a CSV file"""
    print("="*60)
    print("DATA STRUCTURE ANALYSIS")
    print("="*60)
    
    # Load the CSV file
    try:
        df = pd.read_csv(file_path)
        print(f"✓ Successfully loaded CSV file: {file_path}")
    except Exception as e:
        print(f"✗ Error loading CSV file: {e}")
        return None
    
    # Basic structure information
    print(f"\n📊 BASIC STRUCTURE:")
    print(f"   Total rows: {len(df):,}")
    print(f"   Total columns: {len(df.columns)}")
    print(f"   Memory usage: {df.memory_usage().sum() / 1024**2:.2f} MB")
    
    # Column information
    print(f"\n📋 COLUMN INFORMATION:")
    print("-" * 50)
    for i, col in enumerate(df.columns, 1):
        dtype = df[col].dtype
        non_null = df[col].count()
        null_count = df[col].isnull().sum()
        unique_vals = df[col].nunique()
        
        print(f"{i:2d}. {col:<25} | {str(dtype):<12} | {non_null:>6} non-null | {null_count:>5} null | {unique_vals:>6} unique")
    
    # Sample data
    print(f"\n📝 SAMPLE DATA (First 5 rows):")
    print("-" * 80)
    print(df.head().to_string())
    
    # Data types summary
    print(f"\n📈 DATA TYPES SUMMARY:")
    dtype_counts = df.dtypes.value_counts()
    for dtype, count in dtype_counts.items():
        print(f"   {str(dtype):<12}: {count} columns")
    
    return df

def assess_data_quality(df):
    """Assess data quality issues"""
    print("\n" + "="*60)
    print("DATA QUALITY ASSESSMENT")
    print("="*60)
    
    # Missing values analysis
    print(f"\n🔍 MISSING VALUES ANALYSIS:")
    missing_data = df.isnull().sum()
    missing_percent = (missing_data / len(df)) * 100
    
    missing_summary = pd.DataFrame({
        'Column': missing_data.index,
        'Missing_Count': missing_data.values,
        'Missing_Percentage': missing_percent.values
    }).sort_values('Missing_Count', ascending=False)
    
    print(missing_summary[missing_summary['Missing_Count'] > 0].to_string(index=False))
    
    # Duplicate rows
    duplicate_count = df.duplicated().sum()
    print(f"\n🔄 DUPLICATE ROWS: {duplicate_count:,} ({duplicate_count/len(df)*100:.2f}%)")
    
    # Data consistency checks
    print(f"\n🎯 DATA CONSISTENCY CHECKS:")
    
    # Check for columns with very few unique values (potential categorical)
    low_cardinality = []
    high_cardinality = []
    
    for col in df.columns:
        unique_ratio = df[col].nunique() / len(df)
        if unique_ratio < 0.01 and df[col].dtype == 'object':
            low_cardinality.append((col, df[col].nunique()))
        elif unique_ratio > 0.9 and df[col].dtype == 'object':
            high_cardinality.append((col, df[col].nunique()))
    
    if low_cardinality:
        print(f"   Low cardinality columns (potential categorical): {low_cardinality}")
    if high_cardinality:
        print(f"   High cardinality columns (potential identifiers): {high_cardinality}")
    
    return missing_summary, duplicate_count

def generate_initial_observations(df):
    """Generate initial observations about the data"""
    print("\n" + "="*60)
    print("INITIAL OBSERVATIONS")
    print("n="*60)
    
    observations = []
    
    # Numeric columns analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        print(f"\n📊 NUMERIC COLUMNS SUMMARY ({len(numeric_cols)} columns):")
        numeric_summary = df[numeric_cols].describe()
        print(numeric_summary.round(2).to_string())
        
        # Check for potential outliers
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)][col].count()
            if outliers > 0:
                observations.append(f"Column '{col}' has {outliers} potential outliers ({outliers/len(df)*100:.1f}%)")
    
    # Categorical columns analysis  
    categorical_cols = df.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        print(f"\n📝 CATEGORICAL COLUMNS ANALYSIS ({len(categorical_cols)} columns):")
        for col in categorical_cols[:5]:  # Show first 5 categorical columns
            top_values = df[col].value_counts().head()
            print(f"\n   {col}:")
            print(f"   {top_values.to_string()}")
    
    # Key patterns and recommendations
    print(f"\n🔑 KEY PATTERNS IDENTIFIED:")
    for i, obs in enumerate(observations, 1):
        print(f"   {i}. {obs}")
    
    return observations

if __name__ == "__main__":
    # Analyze the CSV file
    csv_file = "finalapi.csv"
    df = analyze_csv_structure(csv_file)
    
    if df is not None:
        missing_summary, duplicate_count = assess_data_quality(df)
        observations = generate_initial_observations(df)
        
        # Save summary statistics
        print(f"\n💾 Saving analysis results...")
        df.info(buf=open('agent_comm/data_info.txt', 'w'))
        df.describe().to_csv('agent_comm/summary_statistics.csv')
        missing_summary.to_csv('agent_comm/missing_values_summary.csv', index=False)
        
        print(f"✓ Analysis complete! Check agent_comm/ for detailed results.")