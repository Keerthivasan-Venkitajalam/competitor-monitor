"""
Report generation module for competitor intelligence.
Generates structured Markdown intelligence reports with strategic shift highlighting.
Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class ReportGenerator:
    """Generates structured Markdown intelligence reports."""
    
    def __init__(self, template_path: Optional[str] = None):
        """
        Initialize the report generator.
        
        Args:
            template_path: Path to the report template file
        """
        self.template_path = template_path
        self.default_template = '''# Intelligence Report: {{date}}

## Executive Summary

This report contains competitive intelligence gathered on {{competitor_count}} competitors. 
The analysis includes web content extraction, semantic diffing against historical baselines, 
and identification of strategic shifts.

---

{{#each competitors}}
## Competitor: {{name}}

### Overview
- **URL**: {{url}}
- **Analysis Date**: {{analysis_date}}
- **Similarity Score**: {{similarity_percentage}}%
- **Classification**: {{classification}}

### Findings

{{findings}}

### Historical Comparison

The current content was compared against the baseline from {{baseline_date}}. 
The cosine similarity between embeddings is {{similarity_percentage}}%, 
indicating a {{classification}}.

### Detailed Changes

{{detailed_changes}}

{{#if has_strategic_shift}}
> **⚠️ STRATEGIC SHIFT DETECTED**
> 
> This competitor has made a significant change in their messaging that may indicate 
> a change in business strategy, pricing model, or target demographic. 
> Further analysis is recommended.
{{/if}}

{{/each}}

## Error Summary

{{#if errors}}
The following errors occurred during processing:

{{#each errors}}
- **{{competitor_name}}**: {{error_message}}
{{/each}}
{{else}}
All competitors were processed successfully with no errors.
{{/if}}

## Recommendations

Based on the analysis, consider the following actions:

{{#if strategic_shifts}}
1. **Review Strategic Shifts**: The following competitors have detected strategic shifts 
   that may require immediate attention:
   {{#each strategic_shifts}}
   - {{name}}: {{shift_details}}
   {{/each}}
{{else}}
1. No immediate strategic shifts detected. Continue regular monitoring.
{{/if}}

2. **Monitor Crunchbase**: Check Crunchbase profiles for recent funding rounds or team changes
3. **Track Social Media**: Monitor Twitter/X for brand sentiment and customer feedback
'''
    
    def generate_report(self, competitor_results: list[dict], errors: Optional[list[dict]] = None) -> str:
        """
        Generate an intelligence report from competitor results.
        
        Args:
            competitor_results: List of competitor analysis results
            errors: List of error records
            
        Returns:
            Generated Markdown report
        """
        # Get current date
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Count strategic shifts
        strategic_shifts = [r for r in competitor_results if r.get('is_strategic_shift', False)]
        
        # Build competitor sections
        competitor_sections = []
        for result in competitor_results:
            section = self._generate_competitor_section(result)
            competitor_sections.append(section)
        
        # Build error section
        error_section = self._generate_error_section(errors or [])
        
        # Build recommendations section
        recommendations_section = self._generate_recommendations_section(strategic_shifts)
        
        # Combine all sections
        report = f'''# Intelligence Report: {current_date}

## Executive Summary

This report contains competitive intelligence gathered on {len(competitor_results)} competitors. 
The analysis includes web content extraction, semantic diffing against historical baselines, 
and identification of strategic shifts.

---

{''.join(competitor_sections)}

{error_section}

{recommendations_section}
'''
        
        return report
    
    def _generate_competitor_section(self, result: dict) -> str:
        """Generate a section for a single competitor."""
        name = result.get('competitor_name', 'Unknown')
        url = result.get('url', 'N/A')
        analysis_date = result.get('analysis_date', 'N/A')
        similarity_percentage = result.get('similarity_percentage', 0)
        classification = result.get('shift_classification', 'Unknown')
        findings = result.get('findings', 'No significant findings.')
        baseline_date = result.get('baseline_date', 'N/A')
        detailed_changes = result.get('detailed_changes', 'No detailed changes available.')
        has_strategic_shift = result.get('is_strategic_shift', False)
        
        section = f'''## Competitor: {name}

### Overview
- **URL**: {url}
- **Analysis Date**: {analysis_date}
- **Similarity Score**: {similarity_percentage}%
- **Classification**: {classification}

### Findings

{findings}

### Historical Comparison

The current content was compared against the baseline from {baseline_date}. 
The cosine similarity between embeddings is {similarity_percentage}%, 
indicating a {classification}.

### Detailed Changes

{detailed_changes}
'''
        
        if has_strategic_shift:
            section += '''
> **⚠️ STRATEGIC SHIFT DETECTED**
> 
> This competitor has made a significant change in their messaging that may indicate 
> a change in business strategy, pricing model, or target demographic. 
> Further analysis is recommended.
'''
        
        return section + '\n'
    
    def _generate_error_section(self, errors: list[dict]) -> str:
        """Generate the error summary section."""
        if not errors:
            return '''## Error Summary

All competitors were processed successfully with no errors.
'''
        
        error_lines = ['## Error Summary\n\nThe following errors occurred during processing:\n']
        for error in errors:
            competitor_name = error.get('competitor_name', 'Unknown')
            error_message = error.get('error_message', 'Unknown error')
            error_lines.append(f'- **{competitor_name}**: {error_message}')
        
        return '\n'.join(error_lines) + '\n'
    
    def _generate_recommendations_section(self, strategic_shifts: list[dict]) -> str:
        """Generate the recommendations section."""
        if strategic_shifts:
            shift_lines = ['## Recommendations\n\nBased on the analysis, consider the following actions:\n\n1. **Review Strategic Shifts**: The following competitors have detected strategic shifts that may require immediate attention:\n']
            for shift in strategic_shifts:
                name = shift.get('competitor_name', 'Unknown')
                shift_details = shift.get('shift_details', 'No details available')
                shift_lines.append(f'   - {name}: {shift_details}')
            
            return '\n'.join(shift_lines) + '''
2. **Monitor Crunchbase**: Check Crunchbase profiles for recent funding rounds or team changes
3. **Track Social Media**: Monitor Twitter/X for brand sentiment and customer feedback
'''
        
        return '''## Recommendations

Based on the analysis, consider the following actions:

1. No immediate strategic shifts detected. Continue regular monitoring.

2. **Monitor Crunchbase**: Check Crunchbase profiles for recent funding rounds or team changes
3. **Track Social Media**: Monitor Twitter/X for brand sentiment and customer feedback
'''
    
    def save_report(self, report: str, output_path: str) -> bool:
        """
        Save a report to a file.
        
        Args:
            report: The report content to save
            output_path: Path to save the report
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create output directory if it doesn't exist
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            
            return True
        except Exception as e:
            print(f"Error saving report: {e}")
            return False


def generate_intelligence_report(competitor_results: list[dict], errors: Optional[list[dict]] = None) -> str:
    """
    Convenience function to generate an intelligence report.
    
    Args:
        competitor_results: List of competitor analysis results
        errors: List of error records
        
    Returns:
        Generated Markdown report
    """
    generator = ReportGenerator()
    return generator.generate_report(competitor_results, errors)


if __name__ == '__main__':
    # Test the report generator
    test_results = [
        {
            'competitor_name': 'Acme Corp',
            'url': 'https://acmecorp.com',
            'analysis_date': '2026-02-18',
            'similarity_percentage': 97.45,
            'shift_classification': 'minor_update',
            'findings': 'No significant changes detected.',
            'baseline_date': '2026-02-11',
            'detailed_changes': 'Minor text updates on pricing page.',
            'is_strategic_shift': False,
        },
        {
            'competitor_name': 'TechStart Inc',
            'url': 'https://techstart.io',
            'analysis_date': '2026-02-18',
            'similarity_percentage': 65.23,
            'shift_classification': 'Strategic_Shift',
            'findings': 'Significant changes to value proposition detected.',
            'baseline_date': '2026-02-11',
            'detailed_changes': 'Changed from "for small businesses" to "for enterprise".',
            'is_strategic_shift': True,
            'shift_details': 'Pricing model changed from SMB-focused to enterprise-focused',
        },
    ]
    
    generator = ReportGenerator()
    report = generator.generate_report(test_results)
    
    print("Generated Report:")
    print("=" * 40)
    print(report)
