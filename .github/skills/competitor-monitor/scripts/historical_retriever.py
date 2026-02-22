"""
Historical report retrieval module for competitor intelligence.
Searches for previous intelligence reports and extracts baseline text content.
Validates: Requirements 3.1, 3.2, 3.3, 3.4
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional


class HistoricalRetriever:
    """Retrieves historical intelligence reports for comparison."""
    
    REPORT_PATTERN = re.compile(r'^(\d{4}-\d{2}-\d{2})_Intelligence\.md$')
    
    def __init__(self, reports_dir: str = 'reports'):
        """
        Initialize the historical retriever.
        
        Args:
            reports_dir: Directory containing intelligence reports
        """
        self.reports_dir = Path(reports_dir)
    
    def find_latest_report(self, before_date: Optional[datetime] = None) -> Optional[Path]:
        """
        Find the most recent report before a given date.
        
        Args:
            before_date: Date to find report before (defaults to today)
            
        Returns:
            Path to the most recent report or None if no report found
        """
        if before_date is None:
            before_date = datetime.now()
        
        if not self.reports_dir.exists():
            return None
        
        latest_report = None
        latest_date = None
        
        for file_path in self.reports_dir.glob('*.md'):
            match = self.REPORT_PATTERN.match(file_path.name)
            if match:
                try:
                    report_date = datetime.strptime(match.group(1), '%Y-%m-%d')
                    
                    # Check if report is before the target date
                    if report_date < before_date:
                        if latest_date is None or report_date > latest_date:
                            latest_date = report_date
                            latest_report = file_path
                except ValueError:
                    # Skip files with invalid date format
                    continue
        
        return latest_report
    
    def find_report_for_date(self, target_date: datetime) -> Optional[Path]:
        """
        Find the report closest to but before a specific date.
        
        Args:
            target_date: Target date to find report for
            
        Returns:
            Path to the closest report or None if no report found
        """
        if not self.reports_dir.exists():
            return None
        
        closest_report = None
        closest_diff = None
        
        for file_path in self.reports_dir.glob('*.md'):
            match = self.REPORT_PATTERN.match(file_path.name)
            if match:
                try:
                    report_date = datetime.strptime(match.group(1), '%Y-%m-%d')
                    
                    # Only consider reports before the target date
                    if report_date < target_date:
                        diff = (target_date - report_date).days
                        if closest_diff is None or diff < closest_diff:
                            closest_diff = diff
                            closest_report = file_path
                except ValueError:
                    continue
        
        return closest_report
    
    def get_all_reports(self) -> list[Path]:
        """
        Get all intelligence reports in the directory.
        
        Returns:
            List of report file paths sorted by date
        """
        if not self.reports_dir.exists():
            return []
        
        reports = []
        
        for file_path in self.reports_dir.glob('*.md'):
            if self.REPORT_PATTERN.match(file_path.name):
                reports.append(file_path)
        
        # Sort by date (newest first)
        reports.sort(key=lambda x: x.name, reverse=True)
        
        return reports
    
    def get_report_date(self, file_path: Path) -> Optional[datetime]:
        """
        Extract the date from a report filename.
        
        Args:
            file_path: Path to the report file
            
        Returns:
            Date extracted from filename or None if invalid
        """
        match = self.REPORT_PATTERN.match(file_path.name)
        if match:
            try:
                return datetime.strptime(match.group(1), '%Y-%m-%d')
            except ValueError:
                return None
        return None
    
    def get_report_content(self, file_path: Path) -> Optional[str]:
        """
        Extract the text content from a report.
        
        Args:
            file_path: Path to the report file
            
        Returns:
            Text content of the report or None if reading fails
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return None
    
    def is_new_competitor(self, competitor_name: str) -> bool:
        """
        Check if a competitor has no previous reports.
        
        Args:
            competitor_name: Name of the competitor
            
        Returns:
            True if no previous reports exist, False otherwise
        """
        reports = self.get_all_reports()
        return len(reports) == 0
    
    def get_baseline_text(self, file_path: Path) -> Optional[str]:
        """
        Extract baseline text content from a report for comparison.
        
        Args:
            file_path: Path to the report file
            
        Returns:
            Baseline text content or None if extraction fails
        """
        content = self.get_report_content(file_path)
        if content:
            # Extract the main content section (between headers)
            # This is a simplified extraction - in production, you'd want
            # a more robust Markdown parser
            lines = content.split('\n')
            
            # Find the main content section
            content_lines = []
            in_content = False
            
            for line in lines:
                # Skip YAML frontmatter
                if line.strip() == '---':
                    continue
                
                # Skip headers
                if line.startswith('#'):
                    if in_content:
                        break
                    continue
                
                # Skip empty lines at the start
                if not in_content and not line.strip():
                    continue
                
                in_content = True
                content_lines.append(line)
            
            return '\n'.join(content_lines).strip()
        
        return None


def find_latest_report(reports_dir: str = 'reports', before_date: Optional[datetime] = None) -> Optional[Path]:
    """
    Convenience function to find the latest report.
    
    Args:
        reports_dir: Directory containing intelligence reports
        before_date: Date to find report before
        
    Returns:
        Path to the most recent report or None if no report found
    """
    retriever = HistoricalRetriever(reports_dir)
    return retriever.find_latest_report(before_date)


def get_report_content(file_path: Path) -> Optional[str]:
    """
    Convenience function to get report content.
    
    Args:
        file_path: Path to the report file
        
    Returns:
        Text content of the report or None if reading fails
    """
    retriever = HistoricalRetriever()
    return retriever.get_report_content(file_path)


if __name__ == '__main__':
    # Test the historical retriever
    retriever = HistoricalRetriever('reports')
    
    print("Historical Retriever Test")
    print("=" * 40)
    
    # Create test reports directory if it doesn't exist
    if not retriever.reports_dir.exists():
        retriever.reports_dir.mkdir(parents=True)
        print(f"Created reports directory: {retriever.reports_dir}")
    
    # Find latest report
    latest = retriever.find_latest_report()
    if latest:
        print(f"\nLatest report: {latest.name}")
        print(f"Date: {retriever.get_report_date(latest)}")
    else:
        print("\nNo reports found")
    
    # Get all reports
    all_reports = retriever.get_all_reports()
    print(f"\nTotal reports: {len(all_reports)}")
    for report in all_reports:
        print(f"  - {report.name}")
