import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set up matplotlib for better plots
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)

# Load the data
df = pd.read_csv('uploaded_finalapi.csv')

print("=== COMPREHENSIVE DATA ANALYSIS ===\n")

# Data Quality Assessment
print("1. DATA QUALITY ASSESSMENT")
print("=" * 40)
print(f"Total records: {len(df):,}")
print(f"Total columns: {len(df.columns)}")
print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
print(f"Missing values: {df.isnull().sum().sum()}")
print(f"Duplicate records: {df.duplicated().sum()}")

# Check unique values for categorical columns
categorical_cols = ['PROD_ABBR', 'PROD_LINE', 'STATE_ABBR', 'VENDOR_IND', 'VENDOR']
print("\nCategorical variables summary:")
for col in categorical_cols:
    print(f"{col}: {df[col].nunique()} unique values")
    print(f"  Top 5: {df[col].value_counts().head().to_dict()}")

# Business metrics overview
print("\n2. BUSINESS METRICS OVERVIEW")
print("=" * 40)
print(f"Date range: {df['STAT_PROFILE_DATE_YEAR'].min()} - {df['STAT_PROFILE_DATE_YEAR'].max()}")
print(f"Total agencies: {df['AGENCY_ID'].nunique():,}")
print(f"States covered: {df['STATE_ABBR'].nunique()}")
print(f"Product lines: {df['PROD_LINE'].nunique()}")

# Financial metrics
total_written_premium = df['WRTN_PREM_AMT'].sum()
total_earned_premium = df['PRD_ERND_PREM_AMT'].sum()
total_losses = df['PRD_INCRD_LOSSES_AMT'].sum()
total_policies = df['POLY_INFORCE_QTY'].sum()

print(f"\nFinancial Summary:")
print(f"Total Written Premium: ${total_written_premium:,.2f}")
print(f"Total Earned Premium: ${total_earned_premium:,.2f}")
print(f"Total Incurred Losses: ${total_losses:,.2f}")
print(f"Total Policies In-Force: {total_policies:,}")
print(f"Average Loss Ratio: {df['LOSS_RATIO'].mean():.3f}")
print(f"Average Retention Ratio: {df['RETENTION_RATIO'].mean():.3f}")

# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(20, 16))

# 1. Loss Ratio Distribution
axes[0,0].hist(df['LOSS_RATIO'], bins=50, alpha=0.7, color='skyblue', edgecolor='black')
axes[0,0].axvline(df['LOSS_RATIO'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["LOSS_RATIO"].mean():.3f}')
axes[0,0].set_title('Distribution of Loss Ratios', fontsize=14, fontweight='bold')
axes[0,0].set_xlabel('Loss Ratio')
axes[0,0].set_ylabel('Frequency')
axes[0,0].legend()
axes[0,0].grid(True, alpha=0.3)

# 2. Premium by State (Top 15)
state_premium = df.groupby('STATE_ABBR')['WRTN_PREM_AMT'].sum().sort_values(ascending=False).head(15)
axes[0,1].bar(state_premium.index, state_premium.values, color='lightcoral')
axes[0,1].set_title('Top 15 States by Written Premium', fontsize=14, fontweight='bold')
axes[0,1].set_xlabel('State')
axes[0,1].set_ylabel('Written Premium ($)')
axes[0,1].tick_params(axis='x', rotation=45)
axes[0,1].grid(True, alpha=0.3)

# 3. Premium Trend by Year
yearly_premium = df.groupby('STAT_PROFILE_DATE_YEAR')['WRTN_PREM_AMT'].sum()
axes[1,0].plot(yearly_premium.index, yearly_premium.values, marker='o', linewidth=2, markersize=8, color='green')
axes[1,0].set_title('Written Premium Trend by Year', fontsize=14, fontweight='bold')
axes[1,0].set_xlabel('Year')
axes[1,0].set_ylabel('Written Premium ($)')
axes[1,0].grid(True, alpha=0.3)

# 4. Product Line Performance
prod_performance = df.groupby('PROD_LINE').agg({
    'WRTN_PREM_AMT': 'sum',
    'LOSS_RATIO': 'mean',
    'RETENTION_RATIO': 'mean'
}).sort_values('WRTN_PREM_AMT', ascending=True)

y_pos = np.arange(len(prod_performance))
axes[1,1].barh(y_pos, prod_performance['WRTN_PREM_AMT'], color='orange')
axes[1,1].set_yticks(y_pos)
axes[1,1].set_yticklabels(prod_performance.index)
axes[1,1].set_title('Written Premium by Product Line', fontsize=14, fontweight='bold')
axes[1,1].set_xlabel('Written Premium ($)')
axes[1,1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('comprehensive_analysis_overview.png', dpi=300, bbox_inches='tight')
plt.close()

# Advanced Analysis
print("\n3. ADVANCED STATISTICAL ANALYSIS")
print("=" * 40)

# Correlation analysis for key metrics
key_metrics = ['WRTN_PREM_AMT', 'PRD_ERND_PREM_AMT', 'PRD_INCRD_LOSSES_AMT', 
               'LOSS_RATIO', 'RETENTION_RATIO', 'GROWTH_RATE_3YR', 'ACTIVE_PRODUCERS']
correlation_matrix = df[key_metrics].corr()

plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
            square=True, fmt='.3f', cbar_kws={'shrink': 0.8})
plt.title('Correlation Matrix of Key Business Metrics', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
plt.close()

# Risk Analysis
print("\n4. RISK ANALYSIS")
print("=" * 40)

# Identify high-risk segments
high_risk_threshold = df['LOSS_RATIO'].quantile(0.90)
high_risk_records = df[df['LOSS_RATIO'] > high_risk_threshold]
print(f"High-risk threshold (90th percentile): {high_risk_threshold:.3f}")
print(f"High-risk records: {len(high_risk_records):,} ({len(high_risk_records)/len(df)*100:.1f}%)")

# Risk by state
state_risk = df.groupby('STATE_ABBR').agg({
    'LOSS_RATIO': ['mean', 'std', 'count'],
    'WRTN_PREM_AMT': 'sum'
}).round(3)

state_risk.columns = ['Avg_Loss_Ratio', 'Loss_Ratio_Std', 'Record_Count', 'Total_Premium']
state_risk = state_risk.sort_values('Avg_Loss_Ratio', ascending=False)

print("\nTop 10 Highest Risk States by Loss Ratio:")
print(state_risk.head(10))

# Geographic Analysis
print("\n5. GEOGRAPHIC PERFORMANCE")
print("=" * 40)

fig, axes = plt.subplots(2, 2, figsize=(20, 16))

# Top states by premium
top_states = df.groupby('STATE_ABBR')['WRTN_PREM_AMT'].sum().sort_values(ascending=False).head(20)
axes[0,0].bar(top_states.index, top_states.values, color='steelblue')
axes[0,0].set_title('Top 20 States by Written Premium', fontsize=14, fontweight='bold')
axes[0,0].set_xlabel('State')
axes[0,0].set_ylabel('Written Premium ($)')
axes[0,0].tick_params(axis='x', rotation=45)
axes[0,0].grid(True, alpha=0.3)

# States by loss ratio
state_loss_ratio = df.groupby('STATE_ABBR')['LOSS_RATIO'].mean().sort_values(ascending=False).head(20)
axes[0,1].bar(state_loss_ratio.index, state_loss_ratio.values, color='red', alpha=0.7)
axes[0,1].set_title('Top 20 States by Average Loss Ratio', fontsize=14, fontweight='bold')
axes[0,1].set_xlabel('State')
axes[0,1].set_ylabel('Average Loss Ratio')
axes[0,1].tick_params(axis='x', rotation=45)
axes[0,1].grid(True, alpha=0.3)

# State efficiency (Premium vs Loss Ratio)
state_efficiency = df.groupby('STATE_ABBR').agg({
    'WRTN_PREM_AMT': 'sum',
    'LOSS_RATIO': 'mean'
}).reset_index()

axes[1,0].scatter(state_efficiency['WRTN_PREM_AMT'], state_efficiency['LOSS_RATIO'], 
                  alpha=0.6, s=60, color='purple')
axes[1,0].set_title('State Performance: Premium vs Risk', fontsize=14, fontweight='bold')
axes[1,0].set_xlabel('Total Written Premium ($)')
axes[1,0].set_ylabel('Average Loss Ratio')
axes[1,0].grid(True, alpha=0.3)

# Growth analysis
growth_by_state = df.groupby('STATE_ABBR')['GROWTH_RATE_3YR'].mean().sort_values(ascending=False).head(20)
axes[1,1].bar(growth_by_state.index, growth_by_state.values, color='green', alpha=0.7)
axes[1,1].set_title('Top 20 States by 3-Year Growth Rate', fontsize=14, fontweight='bold')
axes[1,1].set_xlabel('State')
axes[1,1].set_ylabel('Average 3-Year Growth Rate')
axes[1,1].tick_params(axis='x', rotation=45)
axes[1,1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('geographic_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# Agency Performance Analysis
print("\n6. AGENCY PERFORMANCE ANALYSIS")
print("=" * 40)

agency_performance = df.groupby('AGENCY_ID').agg({
    'WRTN_PREM_AMT': 'sum',
    'LOSS_RATIO': 'mean',
    'RETENTION_RATIO': 'mean',
    'GROWTH_RATE_3YR': 'mean',
    'ACTIVE_PRODUCERS': 'mean',
    'POLY_INFORCE_QTY': 'sum'
}).round(3)

# Top performing agencies
top_agencies_premium = agency_performance.sort_values('WRTN_PREM_AMT', ascending=False).head(10)
print("Top 10 Agencies by Written Premium:")
print(top_agencies_premium)

# Product Line Analysis
print("\n7. PRODUCT LINE ANALYSIS")
print("=" * 40)

product_analysis = df.groupby('PROD_LINE').agg({
    'WRTN_PREM_AMT': ['sum', 'mean'],
    'LOSS_RATIO': ['mean', 'std'],
    'RETENTION_RATIO': 'mean',
    'GROWTH_RATE_3YR': 'mean',
    'POLY_INFORCE_QTY': 'sum'
}).round(3)

product_analysis.columns = ['Total_Premium', 'Avg_Premium', 'Avg_Loss_Ratio', 
                           'Loss_Ratio_Std', 'Avg_Retention', 'Avg_Growth', 'Total_Policies']
product_analysis = product_analysis.sort_values('Total_Premium', ascending=False)

print("Product Line Performance Summary:")
print(product_analysis)

# Time series analysis
print("\n8. TEMPORAL ANALYSIS")
print("=" * 40)

temporal_metrics = df.groupby('STAT_PROFILE_DATE_YEAR').agg({
    'WRTN_PREM_AMT': 'sum',
    'PRD_INCRD_LOSSES_AMT': 'sum',
    'LOSS_RATIO': 'mean',
    'RETENTION_RATIO': 'mean',
    'POLY_INFORCE_QTY': 'sum',
    'ACTIVE_PRODUCERS': 'sum'
}).round(3)

print("Year-over-Year Performance:")
print(temporal_metrics)

# Calculate year-over-year changes
temporal_metrics['Premium_YoY_Change'] = temporal_metrics['WRTN_PREM_AMT'].pct_change() * 100
temporal_metrics['Loss_Ratio_Change'] = temporal_metrics['LOSS_RATIO'].diff()

plt.figure(figsize=(15, 10))

# Create subplots for temporal analysis
fig, axes = plt.subplots(2, 2, figsize=(20, 12))

# Premium trend
axes[0,0].plot(temporal_metrics.index, temporal_metrics['WRTN_PREM_AMT'], marker='o', linewidth=2, color='blue')
axes[0,0].set_title('Written Premium Trend Over Time', fontsize=14, fontweight='bold')
axes[0,0].set_xlabel('Year')
axes[0,0].set_ylabel('Written Premium ($)')
axes[0,0].grid(True, alpha=0.3)

# Loss ratio trend
axes[0,1].plot(temporal_metrics.index, temporal_metrics['LOSS_RATIO'], marker='s', linewidth=2, color='red')
axes[0,1].set_title('Average Loss Ratio Trend Over Time', fontsize=14, fontweight='bold')
axes[0,1].set_xlabel('Year')
axes[0,1].set_ylabel('Average Loss Ratio')
axes[0,1].grid(True, alpha=0.3)

# Policies in force
axes[1,0].plot(temporal_metrics.index, temporal_metrics['POLY_INFORCE_QTY'], marker='^', linewidth=2, color='green')
axes[1,0].set_title('Policies In-Force Trend Over Time', fontsize=14, fontweight='bold')
axes[1,0].set_xlabel('Year')
axes[1,0].set_ylabel('Policies In-Force')
axes[1,0].grid(True, alpha=0.3)

# Active producers
axes[1,1].plot(temporal_metrics.index, temporal_metrics['ACTIVE_PRODUCERS'], marker='d', linewidth=2, color='orange')
axes[1,1].set_title('Active Producers Trend Over Time', fontsize=14, fontweight='bold')
axes[1,1].set_xlabel('Year')
axes[1,1].set_ylabel('Active Producers')
axes[1,1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('temporal_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n=== ANALYSIS COMPLETE ===")
print("Generated visualizations:")
print("- comprehensive_analysis_overview.png")
print("- correlation_matrix.png") 
print("- geographic_analysis.png")
print("- temporal_analysis.png")