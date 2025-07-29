import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Load the CSV file
df = pd.read_csv('finalapi.csv')

print("=" * 60)
print("DATA QUALITY ASSESSMENT")
print("=" * 60)

# Missing values analysis
print("Missing Values Analysis:")
print("-" * 40)
missing_values = df.isnull().sum()
missing_percentage = (missing_values / len(df)) * 100

missing_df = pd.DataFrame({
    'Column': df.columns,
    'Missing_Count': missing_values.values,
    'Missing_Percentage': missing_percentage.values
}).sort_values('Missing_Count', ascending=False)

print(missing_df[missing_df['Missing_Count'] > 0])

# Save missing values summary
missing_df.to_csv('agent_comm/missing_values_summary.csv', index=False)

# Duplicate rows analysis
print(f"\nDuplicate Rows Analysis:")
print("-" * 40)
total_duplicates = df.duplicated().sum()
print(f"Total duplicate rows: {total_duplicates:,}")
print(f"Percentage of duplicates: {(total_duplicates/len(df)*100):.2f}%")

# Check for completely identical rows
if total_duplicates > 0:
    print("\nFirst few duplicate rows:")
    duplicated_rows = df[df.duplicated(keep=False)].sort_values(list(df.columns))
    print(duplicated_rows.head())
else:
    print("No duplicate rows found")

# Anomaly detection for numeric columns
print(f"\nAnomalies and Data Consistency:")
print("-" * 40)

numeric_cols = df.select_dtypes(include=[np.number]).columns

for col in numeric_cols[:10]:  # Check first 10 numeric columns
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    outlier_count = len(outliers)
    outlier_percentage = (outlier_count / len(df)) * 100
    
    if outlier_count > 0:
        print(f"{col}: {outlier_count:,} outliers ({outlier_percentage:.2f}%)")

# Check categorical data consistency
print(f"\nCategorical Data Analysis:")
print("-" * 40)

categorical_cols = df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    unique_count = df[col].nunique()
    print(f"{col}: {unique_count} unique values")
    if unique_count <= 20:  # Show unique values for columns with few categories
        print(f"  Values: {sorted(df[col].dropna().unique())}")
    print()

# Summary statistics for all numeric columns
numeric_summary = df.describe()
numeric_summary.to_csv('agent_comm/summary_statistics.csv')

print("Data quality analysis complete!")
print("Files saved:")
print("- agent_comm/missing_values_summary.csv")
print("- agent_comm/summary_statistics.csv")