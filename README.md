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
