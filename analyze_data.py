import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Load the dataset
df = pd.read_csv('finalapi.csv')

print("Dataset loaded successfully!")
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# Basic info about the dataset
print("\n=== DATASET OVERVIEW ===")
print(df.info())
print("\n=== FIRST FEW ROWS ===")
print(df.head())

# Data quality assessment
print("\n=== DATA QUALITY ASSESSMENT ===")
print("Missing values per column:")
missing_values = df.isnull().sum()
print(missing_values[missing_values > 0])

print("\nUnique values per column:")
for col in df.columns:
    unique_count = df[col].nunique()
    print(f"{col}: {unique_count}")

# Replace 99999 values with NaN for better analysis
df_clean = df.replace(99999, np.nan)

# Statistical analysis
print("\n=== STATISTICAL ANALYSIS ===")
numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
print("Descriptive statistics for numeric columns:")
print(df_clean[numeric_cols].describe())

# Business Intelligence Analysis
print("\n=== BUSINESS INTELLIGENCE ANALYSIS ===")

# Key business metrics
total_written_premium = df_clean['WRTN_PREM_AMT'].sum()
total_earned_premium = df_clean['PRD_ERND_PREM_AMT'].sum()
total_losses = df_clean['PRD_INCRD_LOSSES_AMT'].sum()

print(f"Total Written Premium: ${total_written_premium:,.2f}")
print(f"Total Earned Premium: ${total_earned_premium:,.2f}")
print(f"Total Incurred Losses: ${total_losses:,.2f}")

# Loss ratio analysis
valid_loss_ratios = df_clean['LOSS_RATIO'][df_clean['LOSS_RATIO'].notna() & (df_clean['LOSS_RATIO'] != 0)]
if len(valid_loss_ratios) > 0:
    avg_loss_ratio = valid_loss_ratios.mean()
    print(f"Average Loss Ratio: {avg_loss_ratio:.3f}")

# Geographic analysis
print("\n=== GEOGRAPHIC ANALYSIS ===")
state_analysis = df_clean.groupby('STATE_ABBR').agg({
    'WRTN_PREM_AMT': ['sum', 'mean', 'count'],
    'PRD_INCRD_LOSSES_AMT': 'sum',
    'LOSS_RATIO': 'mean'
}).round(2)

print("Top 10 states by written premium:")
state_premiums = df_clean.groupby('STATE_ABBR')['WRTN_PREM_AMT'].sum().sort_values(ascending=False)
print(state_premiums.head(10))

# Product line analysis
print("\n=== PRODUCT LINE ANALYSIS ===")
product_analysis = df_clean.groupby('PROD_ABBR').agg({
    'WRTN_PREM_AMT': ['sum', 'mean', 'count'],
    'PRD_INCRD_LOSSES_AMT': 'sum',
    'LOSS_RATIO': 'mean'
}).round(2)

print("Product line performance:")
print(product_analysis)

# Time series analysis
print("\n=== TIME SERIES ANALYSIS ===")
yearly_trends = df_clean.groupby('STAT_PROFILE_DATE_YEAR').agg({
    'WRTN_PREM_AMT': 'sum',
    'PRD_INCRD_LOSSES_AMT': 'sum',
    'LOSS_RATIO': 'mean',
    'AGENCY_ID': 'nunique'
}).round(2)

print("Yearly trends:")
print(yearly_trends)

# Risk assessment
print("\n=== RISK ASSESSMENT ===")
# Identify high-risk segments
high_loss_ratio_threshold = 1.0
high_risk_data = df_clean[df_clean['LOSS_RATIO'] > high_loss_ratio_threshold]
print(f"Records with Loss Ratio > {high_loss_ratio_threshold}: {len(high_risk_data)}")

# Agency performance analysis
print("\n=== AGENCY PERFORMANCE ANALYSIS ===")
agency_performance = df_clean.groupby('AGENCY_ID').agg({
    'WRTN_PREM_AMT': 'sum',
    'PRD_INCRD_LOSSES_AMT': 'sum',
    'LOSS_RATIO': 'mean',
    'RETENTION_RATIO': 'mean'
}).round(3)

top_agencies = agency_performance.nlargest(10, 'WRTN_PREM_AMT')
print("Top 10 agencies by written premium:")
print(top_agencies)

# Create visualizations
print("\n=== CREATING VISUALIZATIONS ===")

# 1. Written Premium by State (Top 15)
plt.figure(figsize=(12, 8))
top_states = state_premiums.head(15)
plt.bar(range(len(top_states)), top_states.values)
plt.xlabel('State')
plt.ylabel('Written Premium ($)')
plt.title('Written Premium by State (Top 15)')
plt.xticks(range(len(top_states)), top_states.index, rotation=45)
plt.ticklabel_format(style='plain', axis='y')
plt.tight_layout()
plt.savefig('premium_by_state.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Loss Ratio Distribution
plt.figure(figsize=(10, 6))
valid_loss_ratios_plot = df_clean['LOSS_RATIO'][(df_clean['LOSS_RATIO'] >= 0) & (df_clean['LOSS_RATIO'] <= 5)]
plt.hist(valid_loss_ratios_plot, bins=50, alpha=0.7, edgecolor='black')
plt.xlabel('Loss Ratio')
plt.ylabel('Frequency')
plt.title('Distribution of Loss Ratios')
plt.axvline(x=1.0, color='red', linestyle='--', label='Break-even (1.0)')
plt.legend()
plt.tight_layout()
plt.savefig('loss_ratio_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Premium Trends by Year
plt.figure(figsize=(12, 6))
yearly_premium = df_clean.groupby('STAT_PROFILE_DATE_YEAR')['WRTN_PREM_AMT'].sum()
plt.plot(yearly_premium.index, yearly_premium.values, marker='o', linewidth=2, markersize=6)
plt.xlabel('Year')
plt.ylabel('Total Written Premium ($)')
plt.title('Premium Trends Over Time')
plt.grid(True, alpha=0.3)
plt.ticklabel_format(style='plain', axis='y')
plt.tight_layout()
plt.savefig('premium_trends.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Product Line Performance
plt.figure(figsize=(12, 8))
product_premiums = df_clean.groupby('PROD_ABBR')['WRTN_PREM_AMT'].sum().sort_values(ascending=True)
plt.barh(range(len(product_premiums)), product_premiums.values)
plt.xlabel('Written Premium ($)')
plt.ylabel('Product Line')
plt.title('Written Premium by Product Line')
plt.yticks(range(len(product_premiums)), product_premiums.index)
plt.ticklabel_format(style='plain', axis='x')
plt.tight_layout()
plt.savefig('product_line_performance.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. Correlation heatmap
plt.figure(figsize=(14, 10))
correlation_cols = ['WRTN_PREM_AMT', 'PRD_ERND_PREM_AMT', 'PRD_INCRD_LOSSES_AMT', 
                   'LOSS_RATIO', 'RETENTION_RATIO', 'GROWTH_RATE_3YR', 'ACTIVE_PRODUCERS']
corr_matrix = df_clean[correlation_cols].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
            square=True, linewidths=0.5, cbar_kws={"shrink": .8})
plt.title('Correlation Matrix of Key Business Metrics')
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

print("Analysis complete! Visualizations saved.")
print("Ready to generate the research report...")