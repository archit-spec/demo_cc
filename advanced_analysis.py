import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('finalapi.csv')
df_clean = df.replace(99999, np.nan)

print("=== ADVANCED MARKET OPPORTUNITY ANALYSIS ===")

# Growth rate analysis
print("\n1. GROWTH OPPORTUNITIES BY SEGMENT")
growth_analysis = df_clean[df_clean['GROWTH_RATE_3YR'].notna() & 
                          (df_clean['GROWTH_RATE_3YR'] != 0)].groupby(['PROD_ABBR', 'STATE_ABBR']).agg({
    'GROWTH_RATE_3YR': 'mean',
    'WRTN_PREM_AMT': 'sum'
}).round(3)

print("Top growth segments (by 3-year growth rate):")
top_growth = growth_analysis[growth_analysis['WRTN_PREM_AMT'] > 1000000]  # Minimum $1M premium
top_growth = top_growth.sort_values('GROWTH_RATE_3YR', ascending=False).head(15)
print(top_growth)

# Retention analysis
print("\n2. RETENTION ANALYSIS")
retention_analysis = df_clean[df_clean['RETENTION_RATIO'].notna() & 
                             (df_clean['RETENTION_RATIO'] != 0)].groupby('PROD_ABBR').agg({
    'RETENTION_RATIO': ['mean', 'std', 'count'],
    'WRTN_PREM_AMT': 'sum'
}).round(3)

print("Product retention rates:")
print(retention_analysis)

# Underperforming segments
print("\n3. UNDERPERFORMING SEGMENTS")
# Calculate average loss ratio by product and identify high-risk products
loss_ratio_by_product = df_clean[df_clean['LOSS_RATIO'].notna() & 
                                (df_clean['LOSS_RATIO'] > 0) & 
                                (df_clean['LOSS_RATIO'] <= 10)].groupby('PROD_ABBR').agg({
    'LOSS_RATIO': ['mean', 'median', 'count'],
    'WRTN_PREM_AMT': 'sum',
    'PRD_INCRD_LOSSES_AMT': 'sum'
}).round(3)

print("Loss ratios by product line:")
print(loss_ratio_by_product)

# Market concentration analysis
print("\n4. MARKET CONCENTRATION ANALYSIS")
state_concentration = df_clean.groupby('STATE_ABBR')['WRTN_PREM_AMT'].sum().sort_values(ascending=False)
total_premium = state_concentration.sum()
state_concentration_pct = (state_concentration / total_premium * 100).round(2)

print("Market share by state:")
print(state_concentration_pct)

# Agency size distribution
print("\n5. AGENCY SIZE DISTRIBUTION")
agency_sizes = df_clean.groupby('AGENCY_ID')['WRTN_PREM_AMT'].sum()
size_buckets = pd.cut(agency_sizes, bins=[0, 100000, 500000, 1000000, 5000000, float('inf')], 
                     labels=['Small (<$100K)', 'Medium ($100K-$500K)', 
                            'Large ($500K-$1M)', 'Very Large ($1M-$5M)', 'Enterprise (>$5M)'])
size_distribution = size_buckets.value_counts()
print("Agency size distribution:")
print(size_distribution)

# Digital channel analysis
print("\n6. DIGITAL CHANNEL ANALYSIS")
digital_metrics = df_clean.groupby('PROD_ABBR').agg({
    'PL_BOUND_CT_ELINKS': 'sum',
    'PL_QUO_CT_ELINKS': 'sum',
    'PL_BOUND_CT_eQTte': 'sum',
    'PL_QUO_CT_eQTte': 'sum',
    'WRTN_PREM_AMT': 'sum'
}).round(0)

# Calculate conversion rates
digital_metrics['ELINKS_conversion'] = np.where(digital_metrics['PL_QUO_CT_ELINKS'] > 0,
                                               digital_metrics['PL_BOUND_CT_ELINKS'] / digital_metrics['PL_QUO_CT_ELINKS'],
                                               0)
digital_metrics['eQTte_conversion'] = np.where(digital_metrics['PL_QUO_CT_eQTte'] > 0,
                                              digital_metrics['PL_BOUND_CT_eQTte'] / digital_metrics['PL_QUO_CT_eQTte'],
                                              0)

print("Digital channel performance by product:")
print(digital_metrics[digital_metrics['PL_QUO_CT_ELINKS'] > 0].head(10))

# Create additional visualizations
print("\n=== CREATING ADDITIONAL VISUALIZATIONS ===")

# 6. Agency size distribution
plt.figure(figsize=(10, 6))
size_distribution.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Distribution of Agencies by Premium Size')
plt.xlabel('Agency Size Category')
plt.ylabel('Number of Agencies')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('agency_size_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 7. Market concentration by state
plt.figure(figsize=(10, 6))
state_concentration_pct.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Market Share by State')
plt.ylabel('')
plt.tight_layout()
plt.savefig('market_concentration.png', dpi=300, bbox_inches='tight')
plt.close()

# 8. Growth vs. Premium scatter plot
plt.figure(figsize=(12, 8))
growth_data = df_clean[(df_clean['GROWTH_RATE_3YR'].notna()) & 
                      (df_clean['GROWTH_RATE_3YR'] != 0) &
                      (df_clean['GROWTH_RATE_3YR'] > -1) &
                      (df_clean['GROWTH_RATE_3YR'] < 1)]

plt.scatter(growth_data['GROWTH_RATE_3YR'], growth_data['WRTN_PREM_AMT'], 
           alpha=0.6, c=pd.Categorical(growth_data['PROD_LINE']).codes, cmap='viridis')
plt.xlabel('3-Year Growth Rate')
plt.ylabel('Written Premium ($)')
plt.title('Growth Rate vs. Premium Volume')
plt.colorbar(label='Product Line')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('growth_vs_premium.png', dpi=300, bbox_inches='tight')
plt.close()

print("Advanced analysis complete!")