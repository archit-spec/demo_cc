import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('uploaded_finalapi.csv')

print("=== MARKET OPPORTUNITIES ANALYSIS ===\n")

# 1. Underperforming Segments Analysis
print("1. UNDERPERFORMING SEGMENTS")
print("=" * 40)

# Define performance metrics
df['premium_per_policy'] = df['WRTN_PREM_AMT'] / (df['POLY_INFORCE_QTY'] + 1)  # +1 to avoid division by zero

# Identify underperforming segments by state and product
segment_performance = df.groupby(['STATE_ABBR', 'PROD_LINE']).agg({
    'WRTN_PREM_AMT': 'sum',
    'LOSS_RATIO': 'mean',
    'RETENTION_RATIO': 'mean',
    'GROWTH_RATE_3YR': 'mean',
    'premium_per_policy': 'mean',
    'POLY_INFORCE_QTY': 'sum'
}).round(2)

# Calculate performance scores (lower loss ratio + higher retention + higher growth = better)
segment_performance['performance_score'] = (
    (1 / (segment_performance['LOSS_RATIO'] + 1)) * 0.4 +
    (segment_performance['RETENTION_RATIO'] / 100000) * 0.3 +
    (segment_performance['GROWTH_RATE_3YR'] / 100000) * 0.3
)

underperforming = segment_performance.sort_values('performance_score').head(10)
print("Top 10 Underperforming Segments (State-Product combinations):")
print(underperforming[['WRTN_PREM_AMT', 'LOSS_RATIO', 'RETENTION_RATIO', 'GROWTH_RATE_3YR']])

# 2. High Growth Potential Areas
print("\n2. HIGH GROWTH POTENTIAL AREAS")
print("=" * 40)

# Identify states with high growth rates but low market penetration
state_growth = df.groupby('STATE_ABBR').agg({
    'GROWTH_RATE_3YR': 'mean',
    'WRTN_PREM_AMT': 'sum',
    'POLY_INFORCE_QTY': 'sum',
    'AGENCY_ID': 'nunique'
}).round(2)

state_growth['premium_per_agency'] = state_growth['WRTN_PREM_AMT'] / state_growth['AGENCY_ID']
state_growth['market_opportunity_score'] = (
    state_growth['GROWTH_RATE_3YR'] / 100000 * 0.5 +
    (1 / (state_growth['premium_per_agency'] / 1000000 + 1)) * 0.5
)

high_opportunity = state_growth.sort_values('market_opportunity_score', ascending=False)
print("States Ranked by Market Opportunity:")
print(high_opportunity)

# 3. Product Line Opportunities
print("\n3. PRODUCT LINE OPPORTUNITIES")
print("=" * 40)

# Analyze product abbreviation performance
product_performance = df.groupby('PROD_ABBR').agg({
    'WRTN_PREM_AMT': ['sum', 'mean'],
    'LOSS_RATIO': 'mean',
    'RETENTION_RATIO': 'mean',
    'GROWTH_RATE_3YR': 'mean',
    'POLY_INFORCE_QTY': 'sum'
}).round(2)

product_performance.columns = ['Total_Premium', 'Avg_Premium', 'Avg_Loss_Ratio', 
                              'Avg_Retention', 'Avg_Growth', 'Total_Policies']

# Calculate profitability score
product_performance['profitability_score'] = (
    (1 / (product_performance['Avg_Loss_Ratio'] / 10000 + 1)) * 0.4 +
    (product_performance['Avg_Retention'] / 100000) * 0.3 +
    (product_performance['Avg_Growth'] / 100000) * 0.3
)

top_products = product_performance.sort_values('profitability_score', ascending=False).head(10)
print("Top 10 Most Profitable Products:")
print(top_products)

# 4. Agency Expansion Opportunities
print("\n4. AGENCY EXPANSION OPPORTUNITIES")
print("=" * 40)

# Identify agencies with high performance but low market share
agency_analysis = df.groupby('AGENCY_ID').agg({
    'WRTN_PREM_AMT': 'sum',
    'LOSS_RATIO': 'mean',
    'RETENTION_RATIO': 'mean',
    'ACTIVE_PRODUCERS': 'mean',
    'STATE_ABBR': lambda x: x.nunique(),  # Number of states
    'PROD_ABBR': lambda x: x.nunique()   # Number of products
}).round(2)

agency_analysis.columns = ['Total_Premium', 'Avg_Loss_Ratio', 'Avg_Retention', 
                          'Avg_Producers', 'States_Count', 'Products_Count']

# Calculate expansion potential
agency_analysis['expansion_score'] = (
    (agency_analysis['Avg_Retention'] / 100000) * 0.3 +
    (1 / (agency_analysis['Avg_Loss_Ratio'] / 10000 + 1)) * 0.3 +
    (agency_analysis['Avg_Producers'] / 100) * 0.2 +
    (agency_analysis['Total_Premium'] / 10000000) * 0.2
)

# Filter agencies with medium to high premium but room for geographic/product expansion
expansion_candidates = agency_analysis[
    (agency_analysis['Total_Premium'] > agency_analysis['Total_Premium'].median()) &
    ((agency_analysis['States_Count'] < 3) | (agency_analysis['Products_Count'] < 10))
].sort_values('expansion_score', ascending=False).head(15)

print("Top 15 Agencies for Expansion (high performance, limited geographic/product reach):")
print(expansion_candidates)

# 5. Market Share Analysis
print("\n5. MARKET SHARE ANALYSIS")
print("=" * 40)

# Calculate market share by various dimensions
total_premium = df['WRTN_PREM_AMT'].sum()

# State market share
state_share = df.groupby('STATE_ABBR')['WRTN_PREM_AMT'].sum().sort_values(ascending=False)
state_share_pct = (state_share / total_premium * 100).round(2)
print("Market Share by State (%):")
print(state_share_pct)

# Product line market share
product_share = df.groupby('PROD_LINE')['WRTN_PREM_AMT'].sum().sort_values(ascending=False)
product_share_pct = (product_share / total_premium * 100).round(2)
print("\nMarket Share by Product Line (%):")
print(product_share_pct)

# 6. Vendor Performance Analysis
print("\n6. VENDOR PERFORMANCE ANALYSIS")
print("=" * 40)

vendor_performance = df.groupby('VENDOR').agg({
    'WRTN_PREM_AMT': 'sum',
    'LOSS_RATIO': 'mean',
    'RETENTION_RATIO': 'mean',
    'AGENCY_ID': 'nunique'
}).round(2)

vendor_performance['premium_per_agency'] = (vendor_performance['WRTN_PREM_AMT'] / 
                                           vendor_performance['AGENCY_ID']).round(2)

print("Vendor Performance Summary:")
print(vendor_performance.sort_values('WRTN_PREM_AMT', ascending=False))

# Generate opportunity visualization
fig, axes = plt.subplots(2, 2, figsize=(20, 16))

# 1. State Growth vs Premium Opportunity Matrix
axes[0,0].scatter(state_growth['GROWTH_RATE_3YR'], state_growth['WRTN_PREM_AMT'], 
                  s=100, alpha=0.7, color='blue')
for i, state in enumerate(state_growth.index):
    axes[0,0].annotate(state, (state_growth.iloc[i]['GROWTH_RATE_3YR'], 
                              state_growth.iloc[i]['WRTN_PREM_AMT']))
axes[0,0].set_title('Growth Rate vs Total Premium by State', fontsize=14, fontweight='bold')
axes[0,0].set_xlabel('3-Year Growth Rate')
axes[0,0].set_ylabel('Total Written Premium ($)')
axes[0,0].grid(True, alpha=0.3)

# 2. Product Profitability Analysis
top_10_products = product_performance.head(10)
axes[0,1].barh(range(len(top_10_products)), top_10_products['profitability_score'], color='green')
axes[0,1].set_yticks(range(len(top_10_products)))
axes[0,1].set_yticklabels(top_10_products.index)
axes[0,1].set_title('Top 10 Products by Profitability Score', fontsize=14, fontweight='bold')
axes[0,1].set_xlabel('Profitability Score')
axes[0,1].grid(True, alpha=0.3)

# 3. Agency Expansion Opportunities
top_expansion = expansion_candidates.head(10)
axes[1,0].scatter(top_expansion['States_Count'], top_expansion['Products_Count'], 
                  s=top_expansion['Total_Premium']/1000000, alpha=0.6, color='red')
axes[1,0].set_title('Agency Expansion Opportunities\n(Size = Premium Volume)', fontsize=14, fontweight='bold')
axes[1,0].set_xlabel('Number of States')
axes[1,0].set_ylabel('Number of Products')
axes[1,0].grid(True, alpha=0.3)

# 4. Vendor Market Share
vendor_share = df.groupby('VENDOR')['WRTN_PREM_AMT'].sum().sort_values(ascending=False)
axes[1,1].pie(vendor_share.values, labels=vendor_share.index, autopct='%1.1f%%', startangle=90)
axes[1,1].set_title('Market Share by Vendor', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('market_opportunities.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n=== MARKET OPPORTUNITIES ANALYSIS COMPLETE ===")
print("Generated visualization: market_opportunities.png")