# Intelligence Report: {{date}}

## Executive Summary

This report contains competitive intelligence gathered on {{competitor_count}} competitors. The analysis includes web content extraction, semantic diffing against historical baselines, and identification of strategic shifts.

---

## Competitor: {{competitor_name}}

### Overview
- **URL**: {{competitor_url}}
- **Analysis Date**: {{analysis_date}}
- **Similarity Score**: {{similarity_percentage}}%
- **Classification**: {{classification}}

### Findings

{{findings}}

### Historical Comparison

The current content was compared against the baseline from {{baseline_date}}. The cosine similarity between embeddings is {{similarity_percentage}}%, indicating a {{classification}}.

### Detailed Changes

{{detailed_changes}}

---

{{#if has_strategic_shift}}
> **⚠️ STRATEGIC SHIFT DETECTED**
> 
> This competitor has made a significant change in their messaging that may indicate a change in business strategy, pricing model, or target demographic. Further analysis is recommended.
{{/if}}

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

The current content was compared against the baseline from {{baseline_date}}. The cosine similarity between embeddings is {{similarity_percentage}}%, indicating a {{classification}}.

### Detailed Changes

{{detailed_changes}}

{{#if has_strategic_shift}}
> **⚠️ STRATEGIC SHIFT DETECTED**
> 
> This competitor has made a significant change in their messaging that may indicate a change in business strategy, pricing model, or target demographic. Further analysis is recommended.
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
1. **Review Strategic Shifts**: The following competitors have detected strategic shifts that may require immediate attention:
   {{#each strategic_shifts}}
   - {{name}}: {{shift_details}}
   {{/each}}
{{else}}
1. No immediate strategic shifts detected. Continue regular monitoring.
{{/if}}

2. **Monitor Crunchbase**: Check Crunchbase profiles for recent funding rounds or team changes
3. **Track Social Media**: Monitor Twitter/X for brand sentiment and customer feedback
