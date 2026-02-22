"""
File organization module for competitor intelligence.
Handles report naming and directory management.
Validates: Requirements 6.1, 6.2, 6.3
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class FileOrganizer:
    """Organizes intelligence reports with standardized naming and structure."""
    
    REPORT_FILENAME_PATTERN = '{date}_Intelligence.md'
    
    def __init__(self, reports_dir: str = 'reports'):
        """
        Initialize the file organizer.
        
        Args:
            reports_dir: Base directory for reports
        """
        self.reports_dir = Path(reports_dir)
    
    def generate_filename(self, date: Optional[datetime] = None) -> str:
        """
        Generate a standardized filename for an intelligence report.
        
        Args:
            date: Date for the report (defaults to today)
            
        Returns:
            Generated filename in YYYY-MM-DD_Intelligence.md format
        """
        if date is None:
            date = datetime.now()
        
        return self.REPORT_FILENAME_PATTERN.format(date=date.strftime('%Y-%m-%d'))
    
    def generate_filepath(self, date: Optional[datetime] = None, 
                          competitor_name: Optional[str] = None) -> Path:
        """
        Generate a full file path for an intelligence report.
        
        Args:
            date: Date for the report (defaults to today)
            competitor_name: Optional competitor name for subdirectory
            
        Returns:
            Full path to the report file
        """
        filename = self.generate_filename(date)
        
        if competitor_name:
            # Create competitor-specific subdirectory
            competitor_dir = self.reports_dir / competitor_name.replace(' ', '_')
            return competitor_dir / filename
        else:
            return self.reports_dir / filename
    
    def save_report(self, content: str, date: Optional[datetime] = None,
                    competitor_name: Optional[str] = None) -> Optional[Path]:
        """
        Save a report to the appropriate location.
        
        Args:
            content: Report content to save
            date: Date for the report (defaults to today)
            competitor_name: Optional competitor name for subdirectory
            
        Returns:
            Path to saved file or None if saving failed
        """
        try:
            filepath = self.generate_filepath(date, competitor_name)
            
            # Create directory if it doesn't exist
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # Write report content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return filepath
        except Exception as e:
            print(f"Error saving report: {e}")
            return None
    
    def get_reports_directory(self) -> Path:
        """
        Get the reports directory path.
        
        Returns:
            Path to the reports directory
        """
        return self.reports_dir
    
    def ensure_reports_directory(self) -> bool:
        """
        Ensure the reports directory exists.
        
        Returns:
            True if directory exists or was created, False otherwise
        """
        try:
            self.reports_dir.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"Error creating reports directory: {e}")
            return False
    
    def get_latest_report_path(self) -> Optional[Path]:
        """
        Get the path to the most recent report.
        
        Returns:
            Path to the most recent report or None if no reports exist
        """
        if not self.reports_dir.exists():
            return None
        
        # Find all Intelligence.md files
        reports = list(self.reports_dir.glob('*_Intelligence.md'))
        
        if not reports:
            return None
        
        # Sort by filename (which includes date) and return most recent
        reports.sort(key=lambda x: x.name, reverse=True)
        return reports[0]
    
    def get_competitor_reports(self, competitor_name: str) -> list[Path]:
        """
        Get all reports for a specific competitor.
        
        Args:
            competitor_name: Name of the competitor
            
        Returns:
            List of report paths for the competitor
        """
        competitor_dir = self.reports_dir / competitor_name.replace(' ', '_')
        
        if not competitor_dir.exists():
            return []
        
        return list(competitor_dir.glob('*_Intelligence.md'))


def save_intelligence_report(content: str, reports_dir: str = 'reports',
                             date: Optional[datetime] = None,
                             competitor_name: Optional[str] = None) -> Optional[Path]:
    """
    Convenience function to save an intelligence report.
    
    Args:
        content: Report content to save
        reports_dir: Base directory for reports
        date: Date for the report (defaults to today)
        competitor_name: Optional competitor name for subdirectory
        
    Returns:
        Path to saved file or None if saving failed
    """
    organizer = FileOrganizer(reports_dir)
    return organizer.save_report(content, date, competitor_name)


if __name__ == '__main__':
    # Test the file organizer
    organizer = FileOrganizer('reports')
    
    print("File Organizer Test")
    print("=" * 40)
    
    # Ensure reports directory exists
    organizer.ensure_reports_directory()
    print(f"Reports directory: {organizer.reports_dir}")
    
    # Generate filename
    filename = organizer.generate_filename()
    print(f"\nGenerated filename: {filename}")
    
    # Generate filepath
    filepath = organizer.generate_filepath()
    print(f"Generated filepath: {filepath}")
    
    # Test with competitor name
    filepath_competitor = organizer.generate_filepath(competitor_name='Test Company')
    print(f"Competitor filepath: {filepath_competitor}")
    
    # Test saving a report
    test_content = '# Test Report\n\nThis is a test report.'
    saved_path = organizer.save_report(test_content)
    if saved_path:
        print(f"\nSaved report to: {saved_path}")
        
        # Verify file exists
        if saved_path.exists():
            print("File exists: Yes")
            print(f"File size: {saved_path.stat().st_size} bytes")
    else:
        print("\nFailed to save report")
