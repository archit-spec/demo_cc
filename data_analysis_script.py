import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Load the CSV file
print("Loading finalapi.csv...")
df = pd.read_csv('finalapi.csv')

print("=" * 60)
print("DATA STRUCTURE ANALYSIS")
print("=" * 60)

# Basic structure information
print(f"Dataset shape: {df.shape}")
print(f"Total rows: {df.shape[0]:,}")
print(f"Total columns: {df.shape[1]}")

print("\nColumn Information:")
print("-" * 40)
for i, (col, dtype) in enumerate(zip(df.columns, df.dtypes), 1):
    print(f"{i:2d}. {col:<25} | {str(dtype):<15}")

print("\nFirst 5 rows:")
print("-" * 40)
print(df.head())

print("\nData types summary:")
print("-" * 40)
print(df.dtypes.value_counts())

print("\nBasic statistics for numeric columns:")
print("-" * 40)
numeric_cols = df.select_dtypes(include=[np.number]).columns
if len(numeric_cols) > 0:
    print(df[numeric_cols].describe())
else:
    print("No numeric columns found")

# Save structure info to file
with open('agent_comm/data_info.txt', 'w') as f:
    f.write(f"Dataset Shape: {df.shape}\n")
    f.write(f"Total Rows: {df.shape[0]:,}\n")
    f.write(f"Total Columns: {df.shape[1]}\n\n")
    f.write("Column Information:\n")
    for i, (col, dtype) in enumerate(zip(df.columns, df.dtypes), 1):
        f.write(f"{i:2d}. {col:<25} | {str(dtype):<15}\n")

print("\nStructure analysis saved to agent_comm/data_info.txt")