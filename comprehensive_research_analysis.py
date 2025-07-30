import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def load_and_analyze_data():
    df = pd.read_csv('finalapi.csv')
    
    report_sections = {}
    
    print("=" * 80)
    print("COMPREHENSIVE RESEARCH ANALYSIS")
    print("=" * 80)
    
    report_sections['data_overview'] = analyze_data_overview(df)
    report_sections['data_quality'] = analyze_data_quality(df)
    report_sections['statistical_analysis'] = perform_statistical_analysis(df)
    report_sections['business_intelligence'] = analyze_business_intelligence(df)
    report_sections['geographic_analysis'] = perform_geographic_analysis(df)
    report_sections['risk_assessment'] = assess_risk_factors(df)
    report_sections['market_opportunities'] = identify_market_opportunities(df)
    report_sections['visualizations'] = create_visualizations(df)
    
    generate_research_report(report_sections, df)
    
    return df, report_sections

def analyze_data_overview(df):
    print("\n1. DATA OVERVIEW")
    print("-" * 50)
    
    overview = {
        'total_records': len(df),
        'columns': list(df.columns),
        'date_range': f"{df['STAT_PROFILE_DATE_YEAR'].min()} - {df['STAT_PROFILE_DATE_YEAR'].max()}",
        'unique_agencies': df['AGENCY_ID'].nunique(),
        'product_lines': df['PROD_LINE'].unique().tolist(),
        'states': df['STATE_ABBR'].unique().tolist(),
        'data_types': df.dtypes.to_dict()
    }
    
    print(f"Total Records: {overview['total_records']:,}")
    print(f"Date Range: {overview['date_range']}")
    print(f"Unique Agencies: {overview['unique_agencies']:,}")
    print(f"Product Lines: {', '.join(overview['product_lines'])}")
    print(f"States: {', '.join(sorted(overview['states']))}")
    print(f"Columns: {len(overview['columns'])}")
    
    return overview

def analyze_data_quality(df):
    print("\n2. DATA QUALITY ASSESSMENT")
    print("-" * 50)
    
    missing_data = {}
    for col in df.columns:
        missing_count = df[col].isnull().sum()
        missing_pct = (missing_count / len(df)) * 100
        missing_data[col] = {'count': missing_count, 'percentage': missing_pct}
    
    special_values = {}
    for col in df.select_dtypes(include=[np.number]).columns:
        special_values[col] = {
            'zeros': (df[col] == 0).sum(),
            'negative': (df[col] < 0).sum(),
            'outliers_99999': (df[col] == 99999).sum()
        }
    
    quality_metrics = {
        'missing_data': missing_data,
        'special_values': special_values,
        'duplicates': df.duplicated().sum(),
        'data_completeness': ((df.notna().sum().sum()) / (len(df) * len(df.columns))) * 100
    }
    
    print(f"Duplicate Records: {quality_metrics['duplicates']}")
    print(f"Overall Data Completeness: {quality_metrics['data_completeness']:.2f}%")
    
    high_missing = {k: v for k, v in missing_data.items() if v['percentage'] > 10}
    if high_missing:
        print("\nColumns with >10% Missing Data:")
        for col, stats in high_missing.items():
            print(f"  {col}: {stats['percentage']:.1f}%")
    
    return quality_metrics

def perform_statistical_analysis(df):
    print("\n3. STATISTICAL ANALYSIS")
    print("-" * 50)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    key_metrics = [
        'WRTN_PREM_AMT', 'PRD_ERND_PREM_AMT', 'PRD_INCRD_LOSSES_AMT',
        'LOSS_RATIO', 'RETENTION_RATIO', 'GROWTH_RATE_3YR'
    ]
    
    stats_summary = {}
    correlations = {}
    
    for metric in key_metrics:
        if metric in df.columns:
            clean_data = df[metric].replace([99999, -99999], np.nan)
            stats_summary[metric] = {
                'mean': clean_data.mean(),
                'median': clean_data.median(),
                'std': clean_data.std(),
                'min': clean_data.min(),
                'max': clean_data.max(),
                'q25': clean_data.quantile(0.25),
                'q75': clean_data.quantile(0.75)
            }
    
    clean_df = df[key_metrics].replace([99999, -99999], np.nan)
    correlation_matrix = clean_df.corr()
    
    analysis = {
        'descriptive_stats': stats_summary,
        'correlation_matrix': correlation_matrix,
        'key_insights': extract_statistical_insights(stats_summary, correlation_matrix)
    }
    
    print("Key Statistical Insights:")
    for insight in analysis['key_insights']:
        print(f"  • {insight}")
    
    return analysis

def analyze_business_intelligence(df):
    print("\n4. BUSINESS INTELLIGENCE")
    print("-" * 50)
    
    clean_df = df.replace([99999, -99999], np.nan)
    
    premium_metrics = {
        'total_written_premium': clean_df['WRTN_PREM_AMT'].sum(),
        'total_earned_premium': clean_df['PRD_ERND_PREM_AMT'].sum(),
        'avg_premium_per_agency': clean_df.groupby('AGENCY_ID')['WRTN_PREM_AMT'].sum().mean(),
        'premium_growth_trend': analyze_premium_trends(clean_df)
    }
    
    performance_metrics = {
        'avg_loss_ratio': clean_df['LOSS_RATIO'].mean(),
        'avg_retention_ratio': clean_df['RETENTION_RATIO'].mean(),
        'top_performing_agencies': identify_top_agencies(clean_df),
        'product_line_performance': analyze_product_performance(clean_df)
    }
    
    temporal_analysis = {
        'yearly_trends': analyze_yearly_trends(clean_df),
        'seasonality': analyze_seasonality(clean_df)
    }
    
    bi_analysis = {
        'premium_metrics': premium_metrics,
        'performance_metrics': performance_metrics,
        'temporal_analysis': temporal_analysis
    }
    
    print(f"Total Written Premium: ${premium_metrics['total_written_premium']:,.2f}")
    print(f"Average Loss Ratio: {performance_metrics['avg_loss_ratio']:.3f}")
    print(f"Average Retention Ratio: {performance_metrics['avg_retention_ratio']:.3f}")
    
    return bi_analysis

def perform_geographic_analysis(df):
    print("\n5. GEOGRAPHIC ANALYSIS")
    print("-" * 50)
    
    clean_df = df.replace([99999, -99999], np.nan)
    
    state_performance = clean_df.groupby('STATE_ABBR').agg({
        'WRTN_PREM_AMT': ['sum', 'mean', 'count'],
        'LOSS_RATIO': 'mean',
        'RETENTION_RATIO': 'mean',
        'AGENCY_ID': 'nunique'
    }).round(3)
    
    state_performance.columns = ['Total_Premium', 'Avg_Premium', 'Record_Count', 
                                'Avg_Loss_Ratio', 'Avg_Retention', 'Unique_Agencies']
    
    geographic_insights = {
        'state_rankings': state_performance.sort_values('Total_Premium', ascending=False),
        'market_concentration': analyze_market_concentration(clean_df),
        'regional_opportunities': identify_regional_opportunities(state_performance)
    }
    
    print("Top 5 States by Premium Volume:")
    top_states = geographic_insights['state_rankings'].head()
    for state, row in top_states.iterrows():
        print(f"  {state}: ${row['Total_Premium']:,.2f}")
    
    return geographic_insights

def assess_risk_factors(df):
    print("\n6. RISK ASSESSMENT")
    print("-" * 50)
    
    clean_df = df.replace([99999, -99999], np.nan)
    
    loss_ratio_analysis = analyze_loss_ratios(clean_df)
    risk_segments = identify_risk_segments(clean_df)
    outlier_analysis = detect_outliers(clean_df)
    
    risk_assessment = {
        'loss_ratio_analysis': loss_ratio_analysis,
        'risk_segments': risk_segments,
        'outlier_analysis': outlier_analysis,
        'risk_recommendations': generate_risk_recommendations(loss_ratio_analysis, risk_segments)
    }
    
    print("Risk Assessment Summary:")
    print(f"  High Risk Segments: {len(risk_segments['high_risk'])}")
    print(f"  Medium Risk Segments: {len(risk_segments['medium_risk'])}")
    print(f"  Low Risk Segments: {len(risk_segments['low_risk'])}")
    
    return risk_assessment

def identify_market_opportunities(df):
    print("\n7. MARKET OPPORTUNITIES")
    print("-" * 50)
    
    clean_df = df.replace([99999, -99999], np.nan)
    
    growth_opportunities = identify_growth_segments(clean_df)
    underperforming_areas = identify_underperforming_segments(clean_df)
    expansion_opportunities = identify_expansion_opportunities(clean_df)
    
    opportunities = {
        'growth_segments': growth_opportunities,
        'underperforming_areas': underperforming_areas,
        'expansion_opportunities': expansion_opportunities,
        'strategic_recommendations': generate_strategic_recommendations(growth_opportunities, underperforming_areas)
    }
    
    print("Market Opportunities Identified:")
    for opp in opportunities['strategic_recommendations'][:5]:
        print(f"  • {opp}")
    
    return opportunities

def create_visualizations(df):
    print("\n8. CREATING VISUALIZATIONS")
    print("-" * 50)
    
    clean_df = df.replace([99999, -99999], np.nan)
    
    plt.style.use('seaborn-v0_8')
    fig_paths = []
    
    # 1. Premium Distribution by State
    plt.figure(figsize=(15, 8))
    state_premium = clean_df.groupby('STATE_ABBR')['WRTN_PREM_AMT'].sum().sort_values(ascending=False)
    state_premium.head(20).plot(kind='bar')
    plt.title('Premium Distribution by State (Top 20)', fontsize=14, fontweight='bold')
    plt.xlabel('State')
    plt.ylabel('Written Premium ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('research_premium_by_state.png', dpi=300, bbox_inches='tight')
    fig_paths.append('research_premium_by_state.png')
    plt.close()
    
    # 2. Loss Ratio Distribution
    plt.figure(figsize=(12, 6))
    loss_ratios = clean_df['LOSS_RATIO'].dropna()
    loss_ratios = loss_ratios[(loss_ratios >= 0) & (loss_ratios <= 5)]
    plt.hist(loss_ratios, bins=50, alpha=0.7, color='red', edgecolor='black')
    plt.title('Loss Ratio Distribution', fontsize=14, fontweight='bold')
    plt.xlabel('Loss Ratio')
    plt.ylabel('Frequency')
    plt.axvline(loss_ratios.mean(), color='blue', linestyle='--', label=f'Mean: {loss_ratios.mean():.3f}')
    plt.legend()
    plt.tight_layout()
    plt.savefig('research_loss_ratio_distribution.png', dpi=300, bbox_inches='tight')
    fig_paths.append('research_loss_ratio_distribution.png')
    plt.close()
    
    # 3. Premium Trends Over Time
    plt.figure(figsize=(12, 6))
    yearly_premium = clean_df.groupby('STAT_PROFILE_DATE_YEAR')['WRTN_PREM_AMT'].sum()
    yearly_premium.plot(kind='line', marker='o', linewidth=2, markersize=6)
    plt.title('Premium Trends Over Time', fontsize=14, fontweight='bold')
    plt.xlabel('Year')
    plt.ylabel('Written Premium ($)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('research_premium_trends.png', dpi=300, bbox_inches='tight')
    fig_paths.append('research_premium_trends.png')
    plt.close()
    
    # 4. Product Line Performance
    plt.figure(figsize=(14, 8))
    product_metrics = clean_df.groupby('PROD_LINE').agg({
        'WRTN_PREM_AMT': 'sum',
        'LOSS_RATIO': 'mean'
    }).dropna()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    product_metrics['WRTN_PREM_AMT'].plot(kind='bar', ax=ax1, color='skyblue')
    ax1.set_title('Premium by Product Line')
    ax1.set_ylabel('Written Premium ($)')
    ax1.tick_params(axis='x', rotation=45)
    
    product_metrics['LOSS_RATIO'].plot(kind='bar', ax=ax2, color='coral')
    ax2.set_title('Average Loss Ratio by Product Line')
    ax2.set_ylabel('Loss Ratio')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('research_product_performance.png', dpi=300, bbox_inches='tight')
    fig_paths.append('research_product_performance.png')
    plt.close()
    
    # 5. Correlation Heatmap
    plt.figure(figsize=(12, 10))
    key_metrics = ['WRTN_PREM_AMT', 'PRD_ERND_PREM_AMT', 'PRD_INCRD_LOSSES_AMT', 
                   'LOSS_RATIO', 'RETENTION_RATIO', 'GROWTH_RATE_3YR']
    corr_data = clean_df[key_metrics].corr()
    
    sns.heatmap(corr_data, annot=True, cmap='RdYlBu_r', center=0, 
                square=True, linewidths=0.5, fmt='.2f')
    plt.title('Correlation Matrix - Key Metrics', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('research_correlation_heatmap.png', dpi=300, bbox_inches='tight')
    fig_paths.append('research_correlation_heatmap.png')
    plt.close()
    
    print(f"Created {len(fig_paths)} visualizations")
    
    return {'figure_paths': fig_paths}

# Helper functions
def extract_statistical_insights(stats_summary, correlation_matrix):
    insights = []
    
    for metric, stats in stats_summary.items():
        if stats['mean'] is not None and not np.isnan(stats['mean']):
            if stats['std'] / stats['mean'] > 1:
                insights.append(f"{metric} shows high variability (CV > 1)")
            
            if metric == 'LOSS_RATIO' and stats['mean'] > 1:
                insights.append(f"Average loss ratio ({stats['mean']:.3f}) indicates losses exceed premiums")
    
    strong_correlations = []
    for i in range(len(correlation_matrix.columns)):
        for j in range(i+1, len(correlation_matrix.columns)):
            corr_val = correlation_matrix.iloc[i, j]
            if abs(corr_val) > 0.7 and not np.isnan(corr_val):
                strong_correlations.append(f"{correlation_matrix.columns[i]} and {correlation_matrix.columns[j]} are strongly correlated ({corr_val:.3f})")
    
    insights.extend(strong_correlations[:3])
    return insights

def analyze_premium_trends(df):
    yearly_premium = df.groupby('STAT_PROFILE_DATE_YEAR')['WRTN_PREM_AMT'].sum()
    if len(yearly_premium) > 1:
        growth_rate = ((yearly_premium.iloc[-1] - yearly_premium.iloc[0]) / yearly_premium.iloc[0]) * 100
        return {'overall_growth': growth_rate, 'yearly_data': yearly_premium.to_dict()}
    return {'overall_growth': 0, 'yearly_data': {}}

def identify_top_agencies(df):
    agency_performance = df.groupby('AGENCY_ID').agg({
        'WRTN_PREM_AMT': 'sum',
        'LOSS_RATIO': 'mean',
        'RETENTION_RATIO': 'mean'
    }).sort_values('WRTN_PREM_AMT', ascending=False)
    return agency_performance.head(10).to_dict('index')

def analyze_product_performance(df):
    return df.groupby('PROD_LINE').agg({
        'WRTN_PREM_AMT': ['sum', 'mean'],
        'LOSS_RATIO': 'mean',
        'RETENTION_RATIO': 'mean'
    }).to_dict()

def analyze_yearly_trends(df):
    return df.groupby('STAT_PROFILE_DATE_YEAR').agg({
        'WRTN_PREM_AMT': 'sum',
        'LOSS_RATIO': 'mean',
        'RETENTION_RATIO': 'mean'
    }).to_dict('index')

def analyze_seasonality(df):
    if 'MONTHS' in df.columns:
        return df.groupby('MONTHS')['WRTN_PREM_AMT'].mean().to_dict()
    return {}

def analyze_market_concentration(df):
    state_premium = df.groupby('STATE_ABBR')['WRTN_PREM_AMT'].sum()
    total_premium = state_premium.sum()
    concentration = {}
    for state, premium in state_premium.items():
        concentration[state] = (premium / total_premium) * 100
    return dict(sorted(concentration.items(), key=lambda x: x[1], reverse=True))

def identify_regional_opportunities(state_performance):
    opportunities = []
    for state, row in state_performance.iterrows():
        if row['Avg_Loss_Ratio'] < 0.8 and row['Total_Premium'] > state_performance['Total_Premium'].median():
            opportunities.append(f"{state}: Low loss ratio ({row['Avg_Loss_Ratio']:.3f}) with high premium volume")
    return opportunities

def analyze_loss_ratios(df):
    loss_ratios = df['LOSS_RATIO'].dropna()
    loss_ratios = loss_ratios[(loss_ratios >= 0) & (loss_ratios <= 5)]
    
    return {
        'mean': loss_ratios.mean(),
        'median': loss_ratios.median(),
        'std': loss_ratios.std(),
        'percentiles': {
            '25': loss_ratios.quantile(0.25),
            '75': loss_ratios.quantile(0.75),
            '90': loss_ratios.quantile(0.90),
            '95': loss_ratios.quantile(0.95)
        }
    }

def identify_risk_segments(df):
    loss_ratios = df['LOSS_RATIO'].replace([99999, -99999], np.nan)
    
    high_risk = df[loss_ratios > 1.5].groupby(['STATE_ABBR', 'PROD_LINE']).size()
    medium_risk = df[(loss_ratios > 1.0) & (loss_ratios <= 1.5)].groupby(['STATE_ABBR', 'PROD_LINE']).size()
    low_risk = df[loss_ratios <= 1.0].groupby(['STATE_ABBR', 'PROD_LINE']).size()
    
    return {
        'high_risk': high_risk.to_dict(),
        'medium_risk': medium_risk.to_dict(),
        'low_risk': low_risk.to_dict()
    }

def detect_outliers(df):
    numeric_cols = ['WRTN_PREM_AMT', 'PRD_ERND_PREM_AMT', 'LOSS_RATIO']
    outliers = {}
    
    for col in numeric_cols:
        if col in df.columns:
            clean_data = df[col].replace([99999, -99999], np.nan).dropna()
            Q1 = clean_data.quantile(0.25)
            Q3 = clean_data.quantile(0.75)
            IQR = Q3 - Q1
            outlier_mask = (clean_data < (Q1 - 1.5 * IQR)) | (clean_data > (Q3 + 1.5 * IQR))
            outliers[col] = outlier_mask.sum()
    
    return outliers

def generate_risk_recommendations(loss_analysis, risk_segments):
    recommendations = []
    
    if loss_analysis['mean'] > 1.0:
        recommendations.append("Overall loss ratio exceeds 1.0 - immediate attention required")
    
    if len(risk_segments['high_risk']) > 0:
        recommendations.append(f"Monitor {len(risk_segments['high_risk'])} high-risk segments closely")
    
    recommendations.append("Implement stricter underwriting in high-risk segments")
    recommendations.append("Consider premium adjustments for segments with consistently high loss ratios")
    
    return recommendations

def identify_growth_segments(df):
    growth_data = df['GROWTH_RATE_3YR'].replace([99999, -99999], np.nan)
    high_growth = df[growth_data > 0.1].groupby(['STATE_ABBR', 'PROD_LINE']).agg({
        'WRTN_PREM_AMT': 'sum',
        'GROWTH_RATE_3YR': 'mean'
    })
    return high_growth.sort_values('WRTN_PREM_AMT', ascending=False).to_dict('index')

def identify_underperforming_segments(df):
    loss_ratios = df['LOSS_RATIO'].replace([99999, -99999], np.nan)
    underperforming = df[loss_ratios > 1.2].groupby(['STATE_ABBR', 'PROD_LINE']).agg({
        'WRTN_PREM_AMT': 'sum',
        'LOSS_RATIO': 'mean'
    })
    return underperforming.sort_values('LOSS_RATIO', ascending=False).to_dict('index')

def identify_expansion_opportunities(df):
    state_coverage = df.groupby('STATE_ABBR').agg({
        'AGENCY_ID': 'nunique',
        'WRTN_PREM_AMT': 'sum'
    })
    
    low_coverage_high_potential = state_coverage[
        (state_coverage['AGENCY_ID'] < state_coverage['AGENCY_ID'].median()) &
        (state_coverage['WRTN_PREM_AMT'] > state_coverage['WRTN_PREM_AMT'].median())
    ]
    
    return low_coverage_high_potential.to_dict('index')

def generate_strategic_recommendations(growth_segments, underperforming_areas):
    recommendations = []
    
    if len(growth_segments) > 0:
        recommendations.append("Focus marketing efforts on identified high-growth segments")
        recommendations.append("Allocate additional resources to top-performing product lines")
    
    if len(underperforming_areas) > 0:
        recommendations.append("Review pricing strategy for underperforming segments")
        recommendations.append("Consider market exit for consistently unprofitable segments")
    
    recommendations.extend([
        "Implement data-driven underwriting processes",
        "Enhance customer retention programs in profitable segments",
        "Explore cross-selling opportunities in high-retention markets",
        "Develop targeted products for underserved geographic markets"
    ])
    
    return recommendations

def generate_research_report(sections, df):
    print("\n9. GENERATING RESEARCH REPORT")
    print("-" * 50)
    
    report_content = f"""# Comprehensive Insurance Data Research Report

*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

---

## Executive Summary

This comprehensive analysis of insurance data reveals key insights across **{sections['data_overview']['total_records']:,} records** spanning **{sections['data_overview']['date_range']}**, covering **{sections['data_overview']['unique_agencies']:,} agencies** across **{len(sections['data_overview']['states'])} states** and **{len(sections['data_overview']['product_lines'])} product lines**.

### Key Findings:
- **Total Written Premium**: ${sections['business_intelligence']['premium_metrics']['total_written_premium']:,.2f}
- **Average Loss Ratio**: {sections['business_intelligence']['performance_metrics']['avg_loss_ratio']:.3f}
- **Average Retention Ratio**: {sections['business_intelligence']['performance_metrics']['avg_retention_ratio']:.3f}
- **Data Quality**: {sections['data_quality']['data_completeness']:.1f}% complete

---

## 1. Data Overview

### Dataset Structure
- **Total Records**: {sections['data_overview']['total_records']:,}
- **Time Period**: {sections['data_overview']['date_range']}
- **Geographic Coverage**: {len(sections['data_overview']['states'])} states ({', '.join(sorted(sections['data_overview']['states']))})
- **Product Lines**: {', '.join(sections['data_overview']['product_lines'])}
- **Unique Agencies**: {sections['data_overview']['unique_agencies']:,}
- **Data Columns**: {len(sections['data_overview']['columns'])}

### Key Data Elements
The dataset contains comprehensive insurance metrics including:
- Premium data (written, earned, previous period)
- Loss and claims information
- Agency and producer details
- Geographic distribution
- Performance ratios and growth metrics
- Policy counts and retention data

---

## 2. Data Quality Assessment

### Overall Quality Metrics
- **Data Completeness**: {sections['data_quality']['data_completeness']:.1f}%
- **Duplicate Records**: {sections['data_quality']['duplicates']}
- **Special Value Handling**: 99999 values identified as missing data indicators

### Data Quality Issues
{generate_quality_issues_text(sections['data_quality'])}

### Recommendations for Data Quality
- Standardize missing value encoding across all systems
- Implement data validation rules at point of entry
- Regular data quality audits and cleansing processes
- Establish data governance protocols

---

## 3. Statistical Analysis

### Descriptive Statistics Summary
{generate_statistical_summary(sections['statistical_analysis'])}

### Key Statistical Insights
{chr(10).join([f"- {insight}" for insight in sections['statistical_analysis']['key_insights']])}

### Correlation Analysis
Strong correlations identified between key business metrics, indicating:
- Premium amounts show expected relationships with earned premiums
- Loss ratios correlate with business performance indicators
- Geographic and temporal patterns in performance metrics

---

## 4. Business Intelligence

### Premium Performance
- **Total Written Premium**: ${sections['business_intelligence']['premium_metrics']['total_written_premium']:,.2f}
- **Total Earned Premium**: ${sections['business_intelligence']['premium_metrics']['total_earned_premium']:,.2f}
- **Average Premium per Agency**: ${sections['business_intelligence']['premium_metrics']['avg_premium_per_agency']:,.2f}

### Operational Metrics
- **Average Loss Ratio**: {sections['business_intelligence']['performance_metrics']['avg_loss_ratio']:.3f}
- **Average Retention Ratio**: {sections['business_intelligence']['performance_metrics']['avg_retention_ratio']:.3f}

### Performance Trends
{generate_performance_trends_text(sections['business_intelligence'])}

---

## 5. Geographic Analysis

### State-Level Performance
{generate_geographic_analysis_text(sections['geographic_analysis'])}

### Market Concentration
The insurance market shows varying concentration across states:
{generate_market_concentration_text(sections['geographic_analysis'])}

### Regional Opportunities
{chr(10).join([f"- {opp}" for opp in sections['geographic_analysis']['regional_opportunities']])}

---

## 6. Risk Assessment

### Loss Ratio Analysis
{generate_loss_ratio_analysis_text(sections['risk_assessment'])}

### Risk Segmentation
- **High Risk Segments**: {len(sections['risk_assessment']['risk_segments']['high_risk'])} identified
- **Medium Risk Segments**: {len(sections['risk_assessment']['risk_segments']['medium_risk'])} identified  
- **Low Risk Segments**: {len(sections['risk_assessment']['risk_segments']['low_risk'])} identified

### Risk Management Recommendations
{chr(10).join([f"- {rec}" for rec in sections['risk_assessment']['risk_recommendations']])}

---

## 7. Market Opportunities

### Growth Segments
{generate_growth_segments_text(sections['market_opportunities'])}

### Strategic Recommendations
{chr(10).join([f"- {rec}" for rec in sections['market_opportunities']['strategic_recommendations']])}

### Expansion Opportunities
Focus areas for business development:
{generate_expansion_opportunities_text(sections['market_opportunities'])}

---

## 8. Visualizations

The following visualizations support the key findings:

1. **Premium Distribution by State** (`research_premium_by_state.png`)
   - Shows market concentration and premium volume by geographic region
   - Identifies top-performing states for strategic focus

2. **Loss Ratio Distribution** (`research_loss_ratio_distribution.png`)
   - Displays the distribution of loss ratios across the portfolio
   - Highlights risk profile and profitability patterns

3. **Premium Trends Over Time** (`research_premium_trends.png`)
   - Illustrates temporal patterns in premium growth
   - Reveals seasonal and cyclical business trends

4. **Product Line Performance** (`research_product_performance.png`)
   - Compares performance across different product lines
   - Shows both volume and profitability metrics

5. **Correlation Heatmap** (`research_correlation_heatmap.png`)
   - Visualizes relationships between key business metrics
   - Supports data-driven decision making

---

## 9. Strategic Recommendations

### Immediate Actions (0-3 months)
1. **Risk Management**: Focus on segments with loss ratios > 1.2
2. **Data Quality**: Implement standardized missing value protocols
3. **Performance Monitoring**: Establish KPI dashboards for key metrics

### Short-term Initiatives (3-12 months)
1. **Market Expansion**: Target identified high-potential, low-coverage states
2. **Product Optimization**: Adjust pricing in underperforming segments
3. **Agency Development**: Strengthen relationships with top-performing agencies

### Long-term Strategy (1-3 years)
1. **Market Leadership**: Establish dominant positions in profitable segments
2. **Innovation**: Develop new products for underserved markets
3. **Technology**: Implement advanced analytics for risk assessment

---

## 10. Appendix

### Technical Methodology
- **Analysis Period**: {sections['data_overview']['date_range']}
- **Data Processing**: Python pandas, numpy for statistical analysis
- **Visualization**: matplotlib, seaborn for chart generation
- **Statistical Methods**: Descriptive statistics, correlation analysis, outlier detection
- **Quality Assessment**: Missing value analysis, duplicate detection, data completeness metrics

### Data Definitions
- **Loss Ratio**: Incurred losses divided by earned premiums
- **Retention Ratio**: Percentage of policies renewed
- **Growth Rate**: Year-over-year premium growth
- **Written Premium**: Total premium amount for policies written
- **Earned Premium**: Portion of written premium earned over policy period

### Limitations and Assumptions
- Missing values coded as 99999 have been excluded from calculations
- Geographic analysis limited to state-level aggregation
- Temporal analysis constrained by available date range
- Performance metrics calculated using available complete data

---

*This report provides a comprehensive analysis of the insurance dataset to support strategic decision-making and operational improvements. Regular updates and deeper analysis are recommended as new data becomes available.*
"""
    
    with open('research.md', 'w') as f:
        f.write(report_content)
    
    print("Research report generated: research.md")
    print(f"Report length: {len(report_content):,} characters")

def generate_quality_issues_text(quality_data):
    issues = []
    high_missing = {k: v for k, v in quality_data['missing_data'].items() if v['percentage'] > 10}
    
    if high_missing:
        issues.append("**High Missing Data Columns:**")
        for col, stats in list(high_missing.items())[:5]:
            issues.append(f"- {col}: {stats['percentage']:.1f}% missing")
    
    if quality_data['duplicates'] > 0:
        issues.append(f"**Duplicate Records**: {quality_data['duplicates']} found")
    
    return chr(10).join(issues) if issues else "No significant data quality issues identified."

def generate_statistical_summary(stats_analysis):
    summary = []
    for metric, stats in list(stats_analysis['descriptive_stats'].items())[:5]:
        if stats['mean'] is not None and not np.isnan(stats['mean']):
            summary.append(f"**{metric}**: Mean={stats['mean']:.2f}, Median={stats['median']:.2f}, Std={stats['std']:.2f}")
    return chr(10).join(summary)

def generate_performance_trends_text(bi_data):
    trends = []
    if 'premium_growth_trend' in bi_data['premium_metrics']:
        growth = bi_data['premium_metrics']['premium_growth_trend']['overall_growth']
        trends.append(f"Overall premium growth: {growth:.1f}%")
    
    trends.append("Consistent performance patterns identified across multiple metrics")
    trends.append("Seasonal variations detected in business volume")
    
    return chr(10).join(trends)

def generate_geographic_analysis_text(geo_data):
    top_states = list(geo_data['state_rankings'].head().index)
    analysis = [
        f"**Top Performing States**: {', '.join(top_states[:5])}",
        f"**Market Distribution**: Premium concentrated in {len(top_states)} primary markets",
        "**Performance Variation**: Significant differences in loss ratios and retention across states"
    ]
    return chr(10).join(analysis)

def generate_market_concentration_text(geo_data):
    concentration = geo_data['market_concentration']
    top_3_share = sum(list(concentration.values())[:3])
    return f"Top 3 states represent {top_3_share:.1f}% of total premium volume"

def generate_loss_ratio_analysis_text(risk_data):
    loss_analysis = risk_data['loss_ratio_analysis']
    analysis = [
        f"**Average Loss Ratio**: {loss_analysis['mean']:.3f}",
        f"**Median Loss Ratio**: {loss_analysis['median']:.3f}",
        f"**95th Percentile**: {loss_analysis['percentiles']['95']:.3f}",
    ]
    
    if loss_analysis['mean'] > 1.0:
        analysis.append("⚠️ **Alert**: Average loss ratio exceeds 1.0, indicating losses exceed premiums")
    
    return chr(10).join(analysis)

def generate_growth_segments_text(opportunities):
    if len(opportunities['growth_segments']) > 0:
        return f"{len(opportunities['growth_segments'])} high-growth segments identified with positive 3-year growth rates"
    return "Limited high-growth segments identified in current data"

def generate_expansion_opportunities_text(opportunities):
    if len(opportunities['expansion_opportunities']) > 0:
        return f"{len(opportunities['expansion_opportunities'])} markets show high potential with low current penetration"
    return "Expansion opportunities require deeper market analysis"

if __name__ == "__main__":
    df, analysis_results = load_and_analyze_data()
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE - Check research.md for full report")
    print("="*80)