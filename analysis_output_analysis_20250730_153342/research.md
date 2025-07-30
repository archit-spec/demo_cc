# Insurance Portfolio Analysis - Comprehensive Research Report

**Date:** July 30, 2025  
**Analysis Period:** 2005-2015  
**Dataset:** finalapi.csv (213,328 records, 49 variables)

---

## Executive Summary

This comprehensive analysis of the insurance portfolio data reveals significant insights across $4.19 billion in written premiums spanning 11 years (2005-2015). The dataset encompasses 1,623 agencies across 28 product lines in 6 states, with detailed performance metrics including loss ratios, retention rates, and digital channel performance.

### Key Findings:
- **Market Concentration**: Ohio dominates with 58.5% market share, followed by Pennsylvania (13.3%) and Kentucky (11.7%)
- **Product Performance**: Anniversary products lead with $1.35B in premiums, while some specialty lines show concerning loss ratios exceeding 2.0
- **Risk Profile**: Overall loss ratio averaging 3,529.7 indicates data quality issues requiring investigation
- **Agency Distribution**: 415 agencies in the "Very Large" category ($1M-$5M premium) represent the core business
- **Growth Opportunities**: Michigan shows strong growth potential across multiple product lines

---

## 1. Data Overview

### Dataset Structure
- **Records**: 213,328 observations
- **Time Period**: 2005-2015 (11 years)
- **Geographic Coverage**: 6 states (OH, PA, KY, IN, WV, MI)
- **Product Lines**: 28 distinct products across Commercial Lines (CL) and Personal Lines (PL)
- **Agencies**: 1,623 unique agencies with 588 primary agencies

### Data Quality Assessment
- **Missing Values**: No explicit null values found
- **Data Issues**: Extensive use of 99999 as placeholder values requiring cleaning
- **Completeness**: All key financial metrics present with varying data quality
- **Consistency**: Standardized state abbreviations and product codes maintained

---

## 2. Statistical Analysis

### Financial Metrics Summary
- **Total Written Premium**: $4,188,201,163.52
- **Total Earned Premium**: $4,151,089,590.60
- **Total Incurred Losses**: $2,362,171,641.95
- **Average Agency Premium**: $2,580,693

### Distribution Analysis
- **Premium Distribution**: Highly right-skewed with top 10% of agencies generating majority of volume
- **Loss Ratio Spread**: Wide variance from 0.0 to >5.0, indicating diverse risk profiles
- **Geographic Concentration**: Uneven distribution with Ohio representing majority market share

---

## 3. Business Intelligence

### Premium Performance by Product Line

| Product | Written Premium | Market Share | Avg Loss Ratio |
|---------|----------------|--------------|----------------|
| ANNIV | $1,351,740,000 | 32.3% | 0.710 |
| COMMAUTO | $469,057,000 | 11.2% | 0.629 |
| HOMEOWNERS | $894,963,000 | 21.4% | 0.810 |
| GENERALIAB | $339,867,000 | 8.1% | 0.767 |
| FIREALLIED | $304,491,000 | 7.3% | 0.803 |

### Yearly Trends (2005-2015)
- **Peak Performance**: 2014 with $436.5M in written premium
- **Growth Period**: 2005-2008 showing consistent expansion
- **Market Maturity**: 2009-2014 relatively stable performance
- **Decline**: 2015 showing significant reduction to $184.5M (partial year data)

### Agency Performance Tiers
- **Enterprise (>$5M)**: 282 agencies, high-value relationships
- **Very Large ($1M-$5M)**: 415 agencies, core business segment
- **Large ($500K-$1M)**: 141 agencies, growth potential
- **Medium/Small**: 492 agencies, relationship development opportunities

---

## 4. Geographic Analysis

### Market Share by State
- **Ohio**: 58.5% ($2.45B) - Dominant market position
- **Pennsylvania**: 13.3% ($555M) - Strong secondary market
- **Kentucky**: 11.7% ($492M) - Established presence
- **Indiana**: 10.9% ($455M) - Stable market
- **West Virginia**: 4.6% ($191M) - Emerging market
- **Michigan**: 1.1% ($46M) - Growth opportunity

### Regional Performance Insights
- **Ohio Advantage**: Likely headquarters state with mature agency network
- **Pennsylvania Potential**: Strong performance suggesting expansion opportunities
- **Michigan Growth**: Despite low market share, showing strong growth rates
- **West Virginia**: Smallest market but stable retention rates

---

## 5. Risk Assessment

### Loss Ratio Analysis by Risk Level

**High-Risk Products (Loss Ratio >2.0):**
- SNOWMOBI12: 5.154
- PERSINLMAR: 2.967
- CYCLES 12: 2.737
- PERSUMBREL: 2.610
- YACHT: 2.551
- MOTORHOM12: 2.521

**Well-Performing Products (Loss Ratio <1.0):**
- COMMAUTO: 0.629
- ANNIV: 0.710
- GENERALIAB: 0.767
- FIREALLIED: 0.803
- HOMEOWNERS: 0.810

### Risk Factors Identified
1. **Specialty Vehicles**: Recreational vehicles showing poor loss experience
2. **Personal Lines Marine**: Significant underwriting concerns
3. **Seasonal Products**: Winter sports equipment showing volatility
4. **Commercial Lines**: Generally better controlled risk profiles

### Outlier Detection
- **High Loss Ratios**: 14,221 records with loss ratios >1.0 require investigation
- **Zero Premiums**: Significant number of records with $0 premium but positive losses
- **Data Anomalies**: Loss ratios exceeding 10.0 suggest data quality issues

---

## 6. Market Opportunities

### High Growth Segments
Based on 3-year growth analysis, top opportunities include:

1. **Michigan Expansion**:
   - GARAGE: 24.2% growth rate
   - COMMUMBREL: 17.1% growth rate
   - WORKCOMP: 14.1% growth rate

2. **Product Line Growth**:
   - ANNIV 12 in KY: 12.2% growth, $19M premium
   - ANNIV 12 in PA: 11.1% growth, $10M premium

3. **West Virginia Development**:
   - Multiple product lines showing positive growth
   - Lower market penetration suggests expansion potential

### Digital Channel Performance
- **Quote-to-Bind Conversion**: ~22% across most product lines
- **Digital Adoption**: Strong utilization of eQT and ELINKS platforms
- **Opportunity**: Improve conversion rates through enhanced digital experience

### Underserved Markets
- **Michigan**: Only 1.1% market share despite growth potential
- **Specialty Products**: Limited penetration in recreational vehicle insurance
- **Commercial Umbrella**: Strong growth trajectory in select markets

---

## 7. Recommendations

### Strategic Initiatives

**1. Geographic Expansion**
- **Michigan Focus**: Invest in agency development and marketing in Michigan market
- **Pennsylvania Growth**: Leverage strong performance to expand market share
- **West Virginia Development**: Build on stable foundation for growth

**2. Product Portfolio Optimization**
- **High-Risk Review**: Conduct thorough underwriting review of specialty vehicle lines
- **Commercial Focus**: Leverage strong commercial lines performance
- **Personal Lines Enhancement**: Improve homeowners and auto profitability

**3. Agency Management**
- **Enterprise Tier**: Strengthen relationships with top 282 agencies
- **Growth Tier**: Develop programs for agencies in $500K-$5M range
- **Small Agency**: Create development pathways for smaller partners

**4. Digital Transformation**
- **Conversion Optimization**: Improve 22% quote-to-bind rate through UX enhancements
- **Platform Integration**: Streamline quote processes across all channels
- **Analytics Enhancement**: Implement real-time monitoring of digital performance

### Risk Management Actions

**1. Immediate (0-6 months)**
- Conduct data quality audit on loss ratio calculations
- Review underwriting guidelines for high-risk specialty products
- Implement enhanced monitoring for loss ratios >2.0

**2. Medium-term (6-12 months)**
- Develop risk-based pricing models for specialty products
- Enhance agency training on high-risk product lines
- Implement predictive analytics for loss forecasting

**3. Long-term (12+ months)**
- Market expansion strategy for Michigan and Pennsylvania
- Product line consolidation for unprofitable segments
- Advanced analytics platform for real-time risk monitoring

---

## 8. Visualizations

The analysis includes eight key visualizations supporting these findings:

1. **Premium by State** - Shows Ohio market dominance
2. **Loss Ratio Distribution** - Reveals risk concentration patterns
3. **Premium Trends** - Illustrates 11-year performance trajectory
4. **Product Line Performance** - Compares premium volume by product
5. **Correlation Heatmap** - Shows relationships between key metrics
6. **Agency Size Distribution** - Depicts agency tier structure
7. **Market Concentration** - Visualizes geographic distribution
8. **Growth vs Premium Scatter** - Identifies growth opportunities

---

## 9. Appendix

### Technical Methodology
- **Analysis Tools**: Python, Pandas, Matplotlib, Seaborn
- **Data Processing**: 99999 placeholder values converted to NaN for accurate analysis
- **Statistical Methods**: Descriptive statistics, correlation analysis, outlier detection
- **Visualization Standards**: Professional charts with consistent formatting

### Data Quality Notes
- Loss ratio calculations appear to have data quality issues with some extreme values
- Retention ratio calculations show realistic ranges (0.0-1.0)
- Premium figures validated against business logic expectations
- Geographic and product code consistency maintained throughout dataset

### Limitations
- Analysis limited to available variables in dataset
- Time series analysis constrained by 11-year period
- Some calculations impacted by data quality issues requiring further investigation
- External market factors not incorporated in analysis

---

**Report Prepared by:** Advanced Analytics Team  
**Classification:** Business Intelligence - Internal Use  
**Next Review:** Quarterly basis with updated data