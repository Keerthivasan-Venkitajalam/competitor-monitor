"""
Error handling module for competitor intelligence.
Handles logging and recovery for various error scenarios.
Validates: Requirements 9.1, 9.2, 9.3, 9.4
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional


class ErrorHandler:
    """Handles errors and maintains error logs for the intelligence workflow."""
    
    def __init__(self, log_dir: str = 'logs'):
        """
        Initialize the error handler.
        
        Args:
            log_dir: Directory for error logs
        """
        self.log_dir = Path(log_dir)
        self.errors = []
        self._setup_logging()
    
    def _setup_logging(self):
        """Set up logging configuration."""
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = self.log_dir / f'error_{datetime.now().strftime("%Y%m%d")}.log'
        
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def log_error(self, error_type: str, message: str, 
                  competitor_name: Optional[str] = None,
                  context: Optional[dict] = None) -> dict:
        """
        Log an error and add it to the error list.
        
        Args:
            error_type: Type of error (configuration, network, script, report)
            message: Error message
            competitor_name: Name of the affected competitor (if applicable)
            context: Additional context information
            
        Returns:
            Error record dictionary
        """
        error_record = {
            'timestamp': datetime.now().isoformat(),
            'error_type': error_type,
            'message': message,
            'competitor_name': competitor_name,
            'context': context or {}
        }
        
        self.errors.append(error_record)
        
        # Log to file
        self.logger.error(
            f"[{error_type}] {message} "
            f"(competitor: {competitor_name or 'N/A'})"
        )
        
        return error_record
    
    def log_configuration_error(self, message: str) -> dict:
        """Log a configuration error."""
        return self.log_error('configuration', message)
    
    def log_network_error(self, message: str, 
                          competitor_name: Optional[str] = None) -> dict:
        """Log a network error."""
        return self.log_error('network', message, competitor_name)
    
    def log_script_error(self, message: str,
                         competitor_name: Optional[str] = None) -> dict:
        """Log a script execution error."""
        return self.log_error('script', message, competitor_name)
    
    def log_report_error(self, message: str,
                         competitor_name: Optional[str] = None) -> dict:
        """Log a report generation error."""
        return self.log_error('report', message, competitor_name)
    
    def get_errors(self) -> list[dict]:
        """Get all logged errors."""
        return self.errors
    
    def get_errors_by_type(self, error_type: str) -> list[dict]:
        """Get errors filtered by type."""
        return [e for e in self.errors if e['error_type'] == error_type]
    
    def get_errors_by_competitor(self, competitor_name: str) -> list[dict]:
        """Get errors filtered by competitor."""
        return [e for e in self.errors if e['competitor_name'] == competitor_name]
    
    def has_errors(self) -> bool:
        """Check if any errors have been logged."""
        return len(self.errors) > 0
    
    def get_error_summary(self) -> dict:
        """Get a summary of all errors."""
        summary = {
            'total_errors': len(self.errors),
            'errors_by_type': {},
            'errors_by_competitor': {},
            'timestamp': datetime.now().isoformat()
        }
        
        for error in self.errors:
            # Count by type
            error_type = error['error_type']
            summary['errors_by_type'][error_type] = \
                summary['errors_by_type'].get(error_type, 0) + 1
            
            # Count by competitor
            competitor = error['competitor_name'] or 'N/A'
            summary['errors_by_competitor'][competitor] = \
                summary['errors_by_competitor'].get(competitor, 0) + 1
        
        return summary
    
    def clear_errors(self):
        """Clear all logged errors."""
        self.errors = []
    
    def save_error_summary(self, output_path: Optional[str] = None) -> Optional[str]:
        """
        Save error summary to a file.
        
        Args:
            output_path: Output file path (defaults to logs/error_summary.json)
            
        Returns:
            Path to saved file or None if saving failed
        """
        if output_path is None:
            output_path = self.log_dir / 'error_summary.json'
        
        try:
            summary = self.get_error_summary()
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2)
            
            return str(output_path)
        except Exception as e:
            self.logger.error(f"Failed to save error summary: {e}")
            return None


def handle_error(error_handler: ErrorHandler, error_type: str, 
                 message: str, competitor_name: Optional[str] = None) -> dict:
    """
    Convenience function to handle an error.
    
    Args:
        error_handler: ErrorHandler instance
        error_type: Type of error
        message: Error message
        competitor_name: Name of the affected competitor
        
    Returns:
        Error record dictionary
    """
    return error_handler.log_error(error_type, message, competitor_name)


if __name__ == '__main__':
    # Test the error handler
    handler = ErrorHandler()
    
    print("Error Handler Test")
    print("=" * 40)
    
    # Log some errors
    handler.log_configuration_error("Invalid competitors.json format")
    handler.log_network_error("Connection timeout", "Acme Corp")
    handler.log_script_error("Python script failed", "TechStart Inc")
    handler.log_report_error("Markdown generation failed", "Innovate Labs")
    
    # Get error summary
    summary = handler.get_error_summary()
    print(f"\nError Summary:")
    print(f"  Total errors: {summary['total_errors']}")
    print(f"  By type: {summary['errors_by_type']}")
    print(f"  By competitor: {summary['errors_by_competitor']}")
    
    # Save error summary
    saved_path = handler.save_error_summary()
    if saved_path:
        print(f"\nError summary saved to: {saved_path}")
    
    # Get errors by type
    network_errors = handler.get_errors_by_type('network')
    print(f"\nNetwork errors: {len(network_errors)}")
    
    # Get errors by competitor
    acme_errors = handler.get_errors_by_competitor('Acme Corp')
    print(f"Acme Corp errors: {len(acme_errors)}")
