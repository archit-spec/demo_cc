# Deep Research Agent System

A sophisticated multi-agent system built with Claude Code SDK for comprehensive data analysis and sales research on CSV/SQLite datasets.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                Deep Research Orchestrator                   │
│                 (Main Coordination Agent)                   │
└──────────────────┬─────────────────┬────────────────────────┘
                   │                 │
         ┌─────────▼──────────┐  ┌───▼──────────────────┐
         │   Data Analyst     │  │  Sales Research      │
         │     Agent          │  │      Agent           │
         │                    │  │                      │
         │ • CSV Analysis     │  │ • Market Analysis    │
         │ • Insurance        │  │ • Sales Strategies   │
         │   Metrics          │  │ • Prospect Targeting │
         │ • Business         │  │ • Intelligence Brief │
         │   Insights         │  │                      │
         └─────────┬──────────┘  └───┬──────────────────┘
                   │                 │
                   ▼                 ▼
            ┌─────────────────────────────────────┐
            │      Inter-Agent Communication       │
            │         (Markdown Files)            │
            │                                     │
            │ • structure_analysis.md             │
            │ • insurance_metrics.md              │
            │ • business_insights.md              │
            │ • market_opportunities.md           │
            │ • sales_strategies.md               │
            │ • prospect_targeting.md             │
            └─────────────────────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Final Reports     │
                    │                     │
                    │ • FINAL_SALES_      │
                    │   REPORT.md         │
                    │ • EXECUTIVE_        │
                    │   DASHBOARD.md      │
                    └─────────────────────┘
```

## Features

### 🔍 Data Analyst Agent
- **CSV Structure Analysis**: Comprehensive data quality assessment
- **Insurance Metrics**: Premium analysis, loss ratios, agency performance
- **Business Insights**: Growth opportunities, risk assessment, benchmarks

### 🎯 Sales Research Agent
- **Market Opportunities**: Target segments, competitive positioning
- **Sales Strategies**: Account-specific tactics, product strategies
- **Intelligence Brief**: Field team playbook, enablement tools
- **Prospect Targeting**: Scoring criteria, prioritization frameworks

### 🤖 Orchestrator Agent
- **Pipeline Coordination**: Manages agent workflow and communication
- **Report Generation**: Creates comprehensive final sales reports
- **Executive Dashboard**: High-level strategic summaries
- **Validation**: Ensures complete analysis pipeline execution

## Installation

1. Install Claude Code SDK:
```bash
pip install claude-code
```

2. Install additional dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start
```bash
# Run the complete research pipeline
python deep_research_orchestrator.py
```

### Individual Agents
```bash
# Run data analysis only
python data_analyst_agent.py

# Run sales research only
python sales_research_agent.py
```

## Generated Outputs

The system generates comprehensive markdown reports in the `agent_comm/` directory:

### Data Analysis Phase
- `structure_analysis.md` - Data structure and quality assessment
- `insurance_metrics.md` - Insurance-specific performance metrics
- `business_insights.md` - Strategic business recommendations
- `data_analysis_summary.md` - Consolidated data findings

### Sales Research Phase
- `market_opportunities.md` - Market analysis and opportunities
- `sales_strategies.md` - Targeted sales strategies
- `sales_intelligence_brief.md` - Field team actionable intelligence
- `prospect_targeting.md` - Prospect prioritization and scoring

### Final Reports
- `FINAL_SALES_REPORT.md` - Comprehensive executive sales report
- `EXECUTIVE_DASHBOARD.md` - High-level strategic dashboard

## Agent Communication

Agents communicate through structured markdown files that serve as:
- **Data Exchange**: Structured information sharing between agents
- **Context Preservation**: Maintains analysis context across pipeline stages
- **Audit Trail**: Complete record of analysis progression
- **Human Readable**: Easy review and validation of agent work

## Target Dataset

Optimized for insurance agency data with fields like:
- `AGENCY_ID`, `WRTN_PREM_AMT`, `LOSS_RATIO`
- `PROD_LINE`, `STATE_ABBR`, `GROWTH_RATE_3YR`
- `RETENTION_RATIO`, `ACTIVE_PRODUCERS`

## Extensibility

The system is designed for easy extension:
- Add new specialized agents
- Customize analysis prompts
- Extend communication protocols
- Add new output formats

## Built With

- **Claude Code SDK** - AI-powered analysis engine
- **Python AsyncIO** - Concurrent agent execution
- **Markdown** - Inter-agent communication format
- **Modular Architecture** - Easy maintenance and extension