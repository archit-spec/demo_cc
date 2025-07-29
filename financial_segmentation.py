#!/usr/bin/env python3
"""
Advanced Financial Performance Segmentation Analysis
Segments insurance agencies into performance tiers with comprehensive scorecards
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

def load_and_clean_data():
    """Load and clean the insurance dataset"""
    print("Loading insurance agency data...")
    df = pd.read_csv('finalapi.csv')
    
    # Replace missing value indicators
    df = df.replace(99999, np.nan)
    
    # Convert data types
    numeric_cols = ['WRTN_PREM_AMT', 'LOSS_RATIO', 'RETENTION_RATIO', 'GROWTH_RATE_3YR', 'PRD_ERND_PREM_AMT', 'PRD_INCRD_LOSSES_AMT']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Create derived metrics
    df['PROFIT_MARGIN'] = (df['WRTN_PREM_AMT'] * (1 - df['LOSS_RATIO'] / 100)).fillna(0)
    df['ROI'] = (df['PROFIT_MARGIN'] / df['WRTN_PREM_AMT'] * 100).replace([np.inf, -np.inf], 0)
    df['PREMIUM_EFFICIENCY'] = df['WRTN_PREM_AMT'] / df.groupby('STATE_ABBR')['WRTN_PREM_AMT'].transform('mean')
    
    # Additional business metrics
    df['PREMIUM_GROWTH'] = ((df['WRTN_PREM_AMT'] - df['PREV_WRTN_PREM_AMT']) / df['PREV_WRTN_PREM_AMT'] * 100).replace([np.inf, -np.inf], 0)
    df['AGENCY_TENURE'] = df['STAT_PROFILE_DATE_YEAR'] - df['AGENCY_APPOINTMENT_YEAR']
    
    return df

def create_performance_segments(df):
    """Create sophisticated performance segments based on multiple metrics"""
    print("Creating performance segments...")
    
    # Calculate composite performance score using available metrics
    metrics = ['WRTN_PREM_AMT', 'ROI', 'RETENTION_RATIO', 'PREMIUM_EFFICIENCY']
    valid_df = df.dropna(subset=metrics)
    
    # Normalize metrics (0-100 scale)
    normalized_metrics = {}
    for metric in metrics:
        if valid_df[metric].std() > 0:  # Avoid division by zero
            normalized_metrics[f'{metric}_NORM'] = (
                (valid_df[metric] - valid_df[metric].min()) / 
                (valid_df[metric].max() - valid_df[metric].min()) * 100
            )
        else:
            normalized_metrics[f'{metric}_NORM'] = pd.Series([50] * len(valid_df), index=valid_df.index)
    
    # Create weighted composite score
    weights = {'WRTN_PREM_AMT_NORM': 0.3, 'ROI_NORM': 0.3, 'RETENTION_RATIO_NORM': 0.2, 'PREMIUM_EFFICIENCY_NORM': 0.2}
    
    composite_score = sum(normalized_metrics[metric] * weight for metric, weight in weights.items())
    valid_df = valid_df.copy()
    valid_df['PERFORMANCE_SCORE'] = composite_score
    
    # Create performance tiers
    valid_df['PERFORMANCE_TIER'] = pd.cut(
        valid_df['PERFORMANCE_SCORE'],
        bins=[0, 20, 40, 60, 80, 100],
        labels=['Bottom 20%', 'Low Performers', 'Average', 'High Performers', 'Top 20%']
    )
    
    return valid_df

def generate_agency_scorecards(df):
    """Generate comprehensive agency performance scorecards"""
    print("Generating agency scorecards...")
    
    # Performance tier analysis
    tier_analysis = df.groupby('PERFORMANCE_TIER').agg({
        'AGENCY_ID': 'count',
        'WRTN_PREM_AMT': ['mean', 'median', 'sum'],
        'LOSS_RATIO': 'mean',
        'ROI': 'mean',
        'RETENTION_RATIO': 'mean',
        'PERFORMANCE_SCORE': 'mean'
    }).round(2)
    
    tier_analysis.columns = ['_'.join(col).strip() for col in tier_analysis.columns]
    
    # State-level performance
    state_performance = df.groupby('STATE_ABBR').agg({
        'PERFORMANCE_SCORE': 'mean',
        'WRTN_PREM_AMT': 'sum',
        'AGENCY_ID': 'count',
        'ROI': 'mean'
    }).round(2).sort_values('PERFORMANCE_SCORE', ascending=False)
    
    # Product line analysis
    if 'PROD_LINE' in df.columns:
        product_performance = df.groupby('PROD_LINE').agg({
            'PERFORMANCE_SCORE': 'mean',
            'WRTN_PREM_AMT': 'sum',
            'LOSS_RATIO': 'mean',
            'AGENCY_ID': 'count'
        }).round(2).sort_values('PERFORMANCE_SCORE', ascending=False)
    else:
        product_performance = pd.DataFrame()
    
    return tier_analysis, state_performance, product_performance

def create_performance_visualizations(df, tier_analysis, state_performance):
    """Create advanced performance visualizations"""
    print("Creating performance visualizations...")
    
    # 1. Performance Tier Distribution
    fig1 = px.pie(
        values=tier_analysis['AGENCY_ID_count'].values,
        names=tier_analysis.index,
        title='Agency Distribution by Performance Tier',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    fig1.write_html('agent_comm/charts/performance_tier_distribution.html')
    
    # 2. Performance Metrics Heatmap
    plt.figure(figsize=(12, 8))
    metrics_for_heatmap = df.groupby('PERFORMANCE_TIER')[
        ['WRTN_PREM_AMT', 'LOSS_RATIO', 'ROI', 'RETENTION_RATIO', 'PERFORMANCE_SCORE']
    ].mean()
    
    sns.heatmap(metrics_for_heatmap.T, annot=True, cmap='RdYlGn', center=0, fmt='.1f')
    plt.title('Performance Metrics by Tier Heatmap')
    plt.tight_layout()
    plt.savefig('agent_comm/charts/performance_metrics_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. State Performance Map
    fig3 = px.choropleth(
        state_performance.reset_index(),
        locations='STATE_ABBR',
        color='PERFORMANCE_SCORE',
        locationmode='USA-states',
        title='State-Level Performance Scores',
        color_continuous_scale='RdYlGn',
        scope='usa'
    )
    fig3.write_html('agent_comm/charts/state_performance_map.html')
    
    # 4. ROI vs Premium Volume Scatter
    fig4 = px.scatter(
        df,
        x='WRTN_PREM_AMT',
        y='ROI',
        color='PERFORMANCE_TIER',
        size='RETENTION_RATIO',
        title='ROI vs Premium Volume by Performance Tier',
        labels={'WRTN_PREM_AMT': 'Written Premium Amount', 'ROI': 'Return on Investment (%)'}
    )
    fig4.update_xaxis(type='log')
    fig4.write_html('agent_comm/charts/roi_vs_premium_scatter.html')
    
    # 5. Top vs Bottom Performers Comparison
    top_bottom = df[df['PERFORMANCE_TIER'].isin(['Top 20%', 'Bottom 20%'])]
    
    fig5 = make_subplots(
        rows=2, cols=2,
        subplot_titles=['Premium Distribution', 'Loss Ratio Distribution', 
                       'ROI Distribution', 'Retention Rate Distribution'],
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    for i, metric in enumerate(['WRTN_PREM_AMT', 'LOSS_RATIO', 'ROI', 'RETENTION_RATIO']):
        row = i // 2 + 1
        col = i % 2 + 1
        
        for tier in ['Top 20%', 'Bottom 20%']:
            data = top_bottom[top_bottom['PERFORMANCE_TIER'] == tier][metric].dropna()
            fig5.add_trace(
                go.Histogram(x=data, name=f'{tier} - {metric}', opacity=0.7),
                row=row, col=col
            )
    
    fig5.update_layout(title_text="Top vs Bottom Performers Comparison", showlegend=True)
    fig5.write_html('agent_comm/charts/top_bottom_comparison.html')
    
    print("Performance visualizations created successfully!")

def export_business_intelligence(df, tier_analysis, state_performance, product_performance):
    """Export business intelligence data"""
    print("Exporting business intelligence data...")
    
    # Export performance scorecards
    tier_analysis.to_csv('agent_comm/performance_tier_analysis.csv')
    state_performance.to_csv('agent_comm/state_performance_analysis.csv')
    
    if not product_performance.empty:
        product_performance.to_csv('agent_comm/product_line_analysis.csv')
    
    # Export top and bottom performers for detailed analysis
    top_performers = df[df['PERFORMANCE_TIER'] == 'Top 20%'].copy()
    bottom_performers = df[df['PERFORMANCE_TIER'] == 'Bottom 20%'].copy()
    
    top_performers.to_csv('agent_comm/top_performers.csv', index=False)
    bottom_performers.to_csv('agent_comm/bottom_performers.csv', index=False)
    
    print("Business intelligence data exported successfully!")

def main():
    """Main execution function"""
    print("=== ADVANCED FINANCIAL PERFORMANCE SEGMENTATION ANALYSIS ===")
    
    # Load and prepare data
    df = load_and_clean_data()
    print(f"Dataset loaded: {len(df):,} records")
    
    # Create performance segments
    df_segments = create_performance_segments(df)
    print(f"Performance segments created for {len(df_segments):,} agencies")
    
    # Generate scorecards
    tier_analysis, state_performance, product_performance = generate_agency_scorecards(df_segments)
    
    # Create visualizations
    create_performance_visualizations(df_segments, tier_analysis, state_performance)
    
    # Export data
    export_business_intelligence(df_segments, tier_analysis, state_performance, product_performance)
    
    # Print summary insights
    print("\n=== KEY INSIGHTS ===")
    print(f"Top 20% agencies generate avg ROI: {df_segments[df_segments['PERFORMANCE_TIER'] == 'Top 20%']['ROI'].mean():.1f}%")
    print(f"Bottom 20% agencies generate avg ROI: {df_segments[df_segments['PERFORMANCE_TIER'] == 'Bottom 20%']['ROI'].mean():.1f}%")
    print(f"Best performing state: {state_performance.index[0]} (Score: {state_performance.iloc[0]['PERFORMANCE_SCORE']:.1f})")
    print(f"Total premium volume: ${df_segments['WRTN_PREM_AMT'].sum():,.0f}")
    
    print("\nFinancial segmentation analysis completed!")
    
    return df_segments

if __name__ == "__main__":
    df_result = main()