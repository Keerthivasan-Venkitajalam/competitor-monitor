# Competitor Monitor Skill

**Autonomous competitive intelligence that saves 150+ hours per year.**

## Overview

This Accomplish skill automatically monitors competitor websites, detects strategic shifts using AI semantic analysis, and generates executive intelligence reports. Built for indie hackers and solo founders who need to stay informed without spending hours manually checking competitor sites.

## Quick Start

### 1. Configure Your Competitors

Copy the example config and add your competitors:

```bash
cp .github/skills/competitor-monitor/competitors.json.example competitors.json
```

Edit `competitors.json`:

```json
{
  "competitors": [
    {
      "name": "Lovable",
      "url": "https://lovable.dev",
      "crunchbase": "https://www.crunchbase.com/organization/lovable",
      "twitter": "@lovable_dev",
      "description": "Build apps & websites with AI, fast."
    }
  ]
}
```

### 2. Install Dependencies

```bash
pip install sentence-transformers playwright
playwright install
```

### 3. Run the Monitor

```bash
python .github/skills/competitor-monitor/scripts/integration.py
```

### 4. View Your Intelligence Report

```bash
cat reports/$(date +%Y-%m-%d)_Intelligence.md
```

## What It Does

### Before (Manual Process)
- ⏰ 45 minutes daily checking competitor websites
- 📋 Copy-pasting content into docs
- 🤔 Trying to remember what changed
- ❌ Missing important strategic shifts
- 📊 No historical tracking

### After (Automated)
- ⚡ 2 minutes to run and review
- 🤖 Automatic website browsing
- 🧠 AI-powered change detection
- ✅ Strategic shift alerts
- 📈 Complete historical archive

**Time saved: 95.6% (150+ hours per year)**

## Key Features

### 🧠 Semantic Diffing (Not Just Text Comparison)

Traditional tools flag every typo. This skill uses AI embeddings to detect REAL strategic changes:

- ✅ Pricing model changes
- ✅ Feature launches
- ✅ Positioning pivots
- ✅ Target market shifts
- ❌ Typo fixes (ignored)
- ❌ Date updates (ignored)

**How it works:**
1. Extracts text from competitor websites
2. Generates embeddings using sentence-transformers
3. Calculates cosine similarity vs. historical baseline
4. Flags changes < 80% similarity as "Strategic Shift"

### 📊 Beautiful Intelligence Reports

Generated reports include:
- Executive summary with key findings
- Per-competitor analysis with similarity scores
- Strategic shift highlighting with recommendations
- Historical comparison data
- Error handling and status

### 🔒 Privacy-First Design

- All processing runs locally on your machine
- No data sent to external servers
- Optional local LLM integration (Ollama/LM Studio)
- Full control over your competitive intelligence

### 📈 Historical Tracking

- Automatic report archiving with timestamps
- Trend analysis over time
- Compare current vs. any historical baseline
- Track competitor evolution

## Architecture

```
competitors.json → Browser Automation → DOM Extraction
                                            ↓
                                    Semantic Diffing
                                    (AI Embeddings)
                                            ↓
                                    Strategic Shift Detection
                                            ↓
                                    Intelligence Report Generation
                                            ↓
                                    reports/YYYY-MM-DD_Intelligence.md
```

## Components

- **integration.py** - Main orchestration script
- **browser.py** - Playwright-based web automation
- **dom_extractor.py** - Text extraction from HTML
- **historical_retriever.py** - Report history management
- **semantic_diff.py** - AI-powered semantic comparison
- **report_generator.py** - Markdown report generation
- **file_organizer.py** - Report naming and organization
- **error_handler.py** - Graceful error handling
- **approval_handler.py** - User-in-the-loop approvals

## Configuration

### competitors.json

```json
{
  "competitors": [
    {
      "name": "Competitor Name",
      "url": "https://competitor.com",
      "crunchbase": "https://crunchbase.com/org/competitor",
      "twitter": "@competitor",
      "description": "What they do"
    }
  ]
}
```

### Customization

**Adjust similarity threshold** (in `semantic_diff.py`):
```python
STRATEGIC_SHIFT_THRESHOLD = 0.80  # Default: 80%
```

**Change embedding model** (in `semantic_diff.py`):
```python
model = SentenceTransformer('all-MiniLM-L6-v2')  # Fast
# or
model = SentenceTransformer('all-mpnet-base-v2')  # Better quality
```

## Scheduling

### Daily Monitoring (Linux/Mac)

```bash
# Add to crontab (crontab -e)
0 9 * * * cd /path/to/workspace && python .github/skills/competitor-monitor/scripts/integration.py
```

### Daily Monitoring (Windows)

```cmd
schtasks /create /tn "CompetitorMonitor" /tr "python C:\path\to\workspace\.github\skills\competitor-monitor\scripts\integration.py" /sc daily /st 09:00
```

### GitHub Actions

```yaml
name: Daily Competitor Monitor
on:
  schedule:
    - cron: '0 9 * * *'
jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install sentence-transformers playwright
          playwright install
      - name: Run monitor
        run: python .github/skills/competitor-monitor/scripts/integration.py
      - name: Commit report
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add reports/
          git commit -m "Add daily intelligence report"
          git push
```

## Real-World Example

### Scenario: Lovable Changes Pricing

**Day 1 (Baseline):**
```
Lovable pricing: Individual ($29), Pro ($79)
Similarity: 100% (baseline established)
```

**Day 7 (Strategic Shift Detected):**
```
Lovable pricing: Individual ($29), Pro ($79), Team Pro ($99)
Similarity: 52.3% → Strategic Shift flagged!

Alert: "Lovable has introduced a new Team Pro tier, 
suggesting a move upmarket to development teams."
```

**Your Action:**
- Review the intelligence report (2 minutes)
- Investigate Lovable's new positioning
- Adjust your own strategy to capture solo developers
- Total time: 10 minutes vs. 45 minutes manual checking

## Troubleshooting

### "competitors.json not found"
```bash
cp .github/skills/competitor-monitor/competitors.json.example competitors.json
```

### "Failed to extract text from URL"
```bash
# Check URL accessibility
curl -I https://competitor-url.com

# Reinstall browser
playwright install
```

### "Embedding model not found"
```bash
pip install sentence-transformers
# Model downloads automatically on first run
```

### "Report not generated"
```bash
mkdir -p reports
chmod 755 reports
```

## Performance

| Competitors | Time (seconds) | Memory (MB) |
|-------------|----------------|-------------|
| 3           | ~15-20         | ~500        |
| 5           | ~25-30         | ~600        |
| 10          | ~45-60         | ~800        |

**Note:** First run takes longer due to model download (~100MB).

## Use Cases

### For Indie Hackers
- Monitor well-funded competitors
- Detect pricing changes instantly
- Track feature launches
- Stay informed without the time sink

### For Solo Founders
- Competitive intelligence on autopilot
- Data-driven strategic decisions
- Level the playing field
- Focus on building, not monitoring

### For Product Managers
- Track competitor product evolution
- Identify market trends
- Validate feature priorities
- Inform roadmap decisions

## Integration Ideas

### Slack Notifications
```python
if result.get('is_strategic_shift'):
    send_slack_message(
        f"🚨 Strategic shift: {result['competitor_name']}"
    )
```

### Discord Webhooks
```python
if result.get('is_strategic_shift'):
    send_discord_webhook(
        f"Strategic shift detected for {result['competitor_name']}"
    )
```

### Email Alerts
```python
if result.get('is_strategic_shift'):
    send_email(
        subject=f"Strategic Shift: {result['competitor_name']}",
        body=result['findings']
    )
```

## Contributing

Contributions welcome! Areas for improvement:
- [ ] Crunchbase funding monitoring
- [ ] Twitter sentiment analysis
- [ ] Web dashboard for trends
- [ ] Multi-language support
- [ ] Enhanced error recovery
- [ ] Performance optimizations

## License

Apache License 2.0 (see LICENSE file)

## Credits

Built by Keerthivasan S V for the "Automate Me If You Can" hackathon.

**Tech Stack:**
- Accomplish AI Custom Skills
- Playwright (browser automation)
- sentence-transformers (semantic analysis)
- Python 3.10+ (async/await)

## Support

- **GitHub Issues**: [Report bugs](https://github.com/Keerthivasan-Venkitajalam/Recall/issues)
- **Email**: keerthivasansv2006@gmail.com
- **Documentation**: See SKILL.md for detailed workflow

---

**From 45 minutes of manual work to 2 minutes of automated intelligence.** 🚀

*Built with Accomplish AI*
