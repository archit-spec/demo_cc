import sqlite3
from openai import OpenAI
import json
from datetime import datetime

# Configure OpenAI client
#client = OpenAI(api_key="your-openai-api-key")  # Replace with your OpenAI API key

class AutonomousSQLDeepResearchAgent:
    def __init__(self, db_path='database.sqlite'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def _get_database_schema(self):
        """Get minimal database schema information to avoid context explosion"""
        schema_info = {}

        # Get all tables
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in self.cursor.fetchall()]

        for table in tables:
            print(f"  📋 Analyzing table: {table}")

            # Get table structure
            self.cursor.execute(f"PRAGMA table_info({table})")
            columns = self.cursor.fetchall()

            # Get row count only
            try:
                self.cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                row_count = self.cursor.fetchone()[0]
            except:
                row_count = 0

            # Only get column names and types - NO SAMPLE DATA to avoid context explosion
            schema_info[table] = {
                'columns': [f"{col[1]} ({col[2]})" for col in columns[:10]],  # Limit to first 10 columns
                'row_count': int(row_count)
            }

        return schema_info

    def autonomous_research(self, research_objective=None):
        """
        Main autonomous research process using OpenAI Deep Research API
        """
        print("🤖 AUTONOMOUS SQL DEEP RESEARCH AGENT STARTING...")
        print("=" * 60)

        # Get database schema information
        print("\n📊 PHASE 1: DATABASE DISCOVERY")
        schema_info = self._get_database_schema()

        # Minimal system message to avoid token explosion
        system_message = """
        Health insurance marketplace analyst. Database: 'database.sqlite' (historical ACA data 2015-2016).
        Use code interpreter for SQL analysis. Use web search for current context.
        Provide quantitative insights with specific numbers.
        """

        # Concise research objective
        if not research_objective:
            research_objective = """
            Analyze health insurance database:
            1. Market structure by metal tier/issuer
            2. Premium pricing patterns
            3. Network types and sizes
            4. Geographic variations
            5. Strategic insights for current market

            Be concise but quantitative.
            """

        # Execute deep research
        print("\n🧠 PHASE 2: INITIATING DEEP RESEARCH ANALYSIS...")
        print("This may take several minutes as the model plans and executes comprehensive analysis...")

        try:
            response = client.responses.create(
                model="o4-mini-deep-research",  # Use the more efficient model
                input=[
                    {
                        "role": "developer",
                        "content": [{"type": "input_text", "text": system_message}]
                    },
                    {
                        "role": "user",
                        "content": [{"type": "input_text", "text": f"Database schema: {json.dumps(schema_info)}\n\nTask: {research_objective}"}]
                    }
                ],
                reasoning={"summary": "auto"},
                tools=[
                    {"type": "web_search_preview"},
                    {"type": "code_interpreter", "container": {"type": "auto", "file_ids": []}}
                ]
            )

            # Extract the final report
            final_report = None
            reasoning_summary = None

            if response.output:
                # Get the final content (last item in output)
                final_report = response.output[-1].content[0].text

                # Get reasoning summary if available - fix the attribute access
                if hasattr(response, 'reasoning') and response.reasoning:
                    reasoning_summary = getattr(response.reasoning, 'summary', None)

            return {
                'research_objective': research_objective,
                'database_schema': schema_info,
                'final_report': final_report,
                'reasoning_summary': reasoning_summary,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            return {
                'error': f"Deep Research API Error: {str(e)}",
                'research_objective': research_objective,
                'database_schema': schema_info,
                'timestamp': datetime.now().isoformat()
            }

    def execute_custom_research(self, custom_objective):
        """Execute research with a custom objective"""
        return self.autonomous_research(custom_objective)

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("\n✅ Database connection closed.")

# Health Insurance Specific Analysis Functions

def analyze_plan_competitiveness(db_path):
    """Analyze plan competitiveness and market positioning"""
    agent = AutonomousSQLDeepResearchAgent(db_path)
    objective = """
    Analyze health insurance plan competitiveness in this historical marketplace data:

    1. Premium benchmarking across metal tiers and plan types
    2. Market share analysis by issuer and service area
    3. Plan availability and choice diversity by geography
    4. Cost-sharing comparison (deductibles, copays, coinsurance)
    5. Out-of-pocket maximum analysis and member financial exposure
    6. Actuarial value distribution and benefit generosity
    7. Competitive positioning patterns that may still be relevant today

    Use web search to understand how competitive dynamics have evolved since this historical data period.
    Provide both historical analysis and current market context.
    """
    results = agent.execute_custom_research(objective)
    agent.close()
    return results

def analyze_market_evolution(db_path):
    """Analyze how the market has evolved since this historical data"""
    agent = AutonomousSQLDeepResearchAgent(db_path)
    objective = """
    Compare this historical health insurance marketplace data to current market conditions:

    1. Analyze historical market structure and issuer participation
    2. Research current marketplace participation and plan offerings via web search
    3. Compare premium inflation trends from historical data to current rates
    4. Assess how benefit designs have evolved over time
    5. Examine changes in market concentration and competition
    6. Identify regulatory changes that have impacted the marketplace
    7. Forecast future market trends based on historical patterns and current developments

    Focus on actionable insights for current marketplace strategy despite the age of this data.
    """
    results = agent.execute_custom_research(objective)
    agent.close()
    return results

def create_historical_baseline_report(db_path):
    """Create comprehensive historical baseline analysis"""
    agent = AutonomousSQLDeepResearchAgent(db_path)
    objective = """
    Create a comprehensive historical baseline report of the ACA marketplace using this data:

    1. Establish baseline metrics for market structure, pricing, and participation
    2. Document early marketplace challenges and patterns
    3. Analyze initial consumer choice patterns and plan selection
    4. Assess early network adequacy and access patterns
    5. Document premium and cost-sharing trends from the early marketplace
    6. Research how these baseline conditions compare to current marketplace maturity
    7. Identify lessons learned that remain relevant for today's marketplace strategy

    This analysis will serve as a historical reference point for understanding marketplace evolution.
    Focus on creating a definitive baseline that current plans can learn from.
    """
    results = agent.execute_custom_research(objective)
    agent.close()
    return results

# Main execution
if __name__ == "__main__":
    # General autonomous research
    agent = AutonomousSQLDeepResearchAgent(db_path='database.sqlite')
    results = agent.autonomous_research()

    print("\n\n" + "="*80)
    print("📊 AUTONOMOUS DEEP RESEARCH RESULTS")
    print("="*80)

    if 'error' in results:
        print(f"❌ Error: {results['error']}")
    else:
        print(results.get('final_report', 'No report generated'))

        if results.get('reasoning_summary'):
            print("\n" + "="*60)
            print("🧠 REASONING SUMMARY")
            print("="*60)
            print(results['reasoning_summary'])

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f'health_insurance_deep_research_{timestamp}.json'

    # Clean results for JSON serialization
    clean_results = {
        'research_objective': results.get('research_objective'),
        'database_schema': results.get('database_schema'),
        'final_report': results.get('final_report'),
        'reasoning_summary': results.get('reasoning_summary'),
        'timestamp': results.get('timestamp'),
        'error': results.get('error')
    }

    with open(output_filename, 'w') as f:
        json.dump(clean_results, f, indent=2, default=str)

    print(f"\n📄 Results saved to: {output_filename}")
    agent.close()

    # Example specialized analyses
    print("\n" + "="*60)
    print("🏥 SPECIALIZED HEALTH INSURANCE ANALYSES AVAILABLE")
    print("="*60)
    print("Uncomment to run specific analyses:")
    print("# competitiveness_results = analyze_plan_competitiveness('database.sqlite')")
    print("# evolution_results = analyze_market_evolution('database.sqlite')")
    print("# baseline_results = create_historical_baseline_report('database.sqlite')")
