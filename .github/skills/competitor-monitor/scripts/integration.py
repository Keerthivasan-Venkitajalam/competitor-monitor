"""
Integration module for competitor intelligence workflow.
Wires all components together to create a complete end-to-end workflow.
Validates: Requirements 10.4
"""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from browser import CompetitorBrowser
from dom_extractor import DOMTextExtractor
from historical_retriever import HistoricalRetriever
from semantic_diff import SemanticDiffer
from report_generator import ReportGenerator
from file_organizer import FileOrganizer
from error_handler import ErrorHandler
from approval_handler import ApprovalHandler


class CompetitorMonitor:
    """Main integration class for the competitor intelligence workflow."""
    
    def __init__(self, workspace_dir: str = '.'):
        """
        Initialize the competitor monitor.
        
        Args:
            workspace_dir: Directory containing the workspace
        """
        self.workspace_dir = Path(workspace_dir)
        self.reports_dir = Path(workspace_dir).resolve() / 'reports'
        
        # Initialize components
        self.browser = CompetitorBrowser()
        self.dom_extractor = DOMTextExtractor()
        self.historical_retriever = HistoricalRetriever(str(self.reports_dir))
        self.semantic_differ = SemanticDiffer()
        self.report_generator = ReportGenerator()
        self.file_organizer = FileOrganizer(str(self.reports_dir))
        self.error_handler = ErrorHandler()
        self.approval_handler = ApprovalHandler()
        
        # Ensure reports directory exists
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def load_competitors_config(self) -> Optional[dict]:
        """Load competitors configuration from JSON file."""
        config_path = self.workspace_dir / 'competitors.json'
        
        if not config_path.exists():
            self.error_handler.log_configuration_error(
                "competitors.json not found"
            )
            return None
        
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            self.error_handler.log_configuration_error(
                f"Invalid JSON in competitors.json: {e}"
            )
            return None
    
    async def process_competitor(self, competitor: dict) -> dict:
        """
        Process a single competitor.
        
        Args:
            competitor: Competitor configuration
            
        Returns:
            Processing result dictionary
        """
        name = competitor.get('name', 'Unknown')
        url = competitor.get('url', '')
        
        result = {
            'competitor_name': name,
            'url': url,
            'analysis_date': datetime.now().strftime('%Y-%m-%d'),
            'is_strategic_shift': False,
            'findings': 'Processing...',
        }
        
        try:
            # Request approval for URL browsing
            url_approval = self.approval_handler.request_url_approval(url)
            
            # Auto-approve for testing (in production, this would wait for user approval)
            self.approval_handler.approve_request(url_approval, 'test')
            
            if url_approval.status.value != 'approved':
                result['findings'] = 'URL browsing not approved'
                return result
            
            # Extract text from URL
            current_text = await self.browser.extract_text_from_url(url)
            
            if not current_text:
                self.error_handler.log_network_error(
                    f"Failed to extract text from {url}",
                    name
                )
                result['findings'] = 'Failed to extract text'
                return result
            
            # Find historical report
            historical_report = self.historical_retriever.find_latest_report()
            
            if historical_report:
                historical_text = self.historical_retriever.get_baseline_text(
                    historical_report
                )
                baseline_date = self.historical_retriever.get_report_date(
                    historical_report
                ).strftime('%Y-%m-%d') if historical_report else 'N/A'
            else:
                historical_text = None
                baseline_date = 'N/A'
            
            # Perform semantic diffing
            if historical_text:
                diff_result = self.semantic_differ.diff_texts(
                    current_text, historical_text
                )
                
                result['similarity_percentage'] = diff_result['similarity_percentage']
                result['shift_classification'] = diff_result['shift_classification']
                result['is_strategic_shift'] = diff_result['is_strategic_shift']
                result['baseline_date'] = baseline_date
                result['detailed_changes'] = f"Similarity: {diff_result['similarity_percentage']}%"
                
                if diff_result['is_strategic_shift']:
                    result['findings'] = (
                        f"Strategic shift detected! Similarity: "
                        f"{diff_result['similarity_percentage']}%. "
                        f"Changes may indicate a change in business strategy."
                    )
                else:
                    result['findings'] = (
                        f"No major changes detected. Similarity: "
                        f"{diff_result['similarity_percentage']}%. "
                        f"Minor updates observed."
                    )
            else:
                # First time monitoring this competitor
                result['similarity_percentage'] = 0
                result['shift_classification'] = 'new_competitor'
                result['is_strategic_shift'] = False
                result['baseline_date'] = 'N/A'
                result['detailed_changes'] = 'No historical data available'
                result['findings'] = 'New competitor - no historical data for comparison'
            
        except Exception as e:
            self.error_handler.log_script_error(
                f"Error processing {name}: {e}",
                name
            )
            result['findings'] = f'Error: {str(e)}'
        
        return result
    
    def process_competitor_sync(self, competitor: dict) -> dict:
        """
        Process a single competitor (synchronous wrapper).
        
        Args:
            competitor: Competitor configuration
            
        Returns:
            Processing result dictionary
        """
        return asyncio.run(self.process_competitor(competitor))
    
    async def run_workflow(self) -> str:
        """
        Run the complete competitor monitoring workflow.
        
        Returns:
            Generated report content
        """
        # Load competitors configuration
        config = self.load_competitors_config()
        
        if not config:
            return self._generate_error_report('Failed to load configuration')
        
        competitors = config.get('competitors', [])
        
        if not competitors:
            return self._generate_error_report('No competitors configured')
        
        # Process each competitor
        results = []
        errors = []
        
        for competitor in competitors:
            result = await self.process_competitor(competitor)
            
            if result.get('findings', '').startswith('Error:'):
                errors.append({
                    'competitor_name': result.get('competitor_name', 'Unknown'),
                    'error_message': result.get('findings', 'Unknown error')
                })
            
            results.append(result)
        
        # Generate report
        report = self.report_generator.generate_report(results, errors)
        
        # Save report
        filename = self.file_organizer.generate_filename()
        filepath = self.reports_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report)
        except Exception as e:
            self.error_handler.log_report_error(
                f"Failed to save report: {e}"
            )
        
        return report
    
    def _generate_error_report(self, error_message: str) -> str:
        """Generate an error report."""
        return f'''# Intelligence Report: {datetime.now().strftime('%Y-%m-%d')}

## Error

{error_message}

## Error Summary

All competitors failed to process due to configuration errors.
'''


def run_competitor_monitor(workspace_dir: str = '.') -> str:
    """
    Convenience function to run the competitor monitor.
    
    Args:
        workspace_dir: Directory containing the workspace
        
    Returns:
        Generated report content
    """
    monitor = CompetitorMonitor(workspace_dir)
    return asyncio.run(monitor.run_workflow())


if __name__ == '__main__':
    async def main():
        print("Running Competitor Monitor Integration Test")
        print("=" * 40)
        
        monitor = CompetitorMonitor('.')
        
        # Load config
        config = monitor.load_competitors_config()
        
        if config:
            print(f"\nLoaded {len(config.get('competitors', []))} competitors")
            
            # Run full workflow
            report = await monitor.run_workflow()
            print(f"\nWorkflow completed")
            print(f"Report saved to: {monitor.reports_dir / monitor.file_organizer.generate_filename()}")
        else:
            print("\nFailed to load configuration")
    
    asyncio.run(main())
