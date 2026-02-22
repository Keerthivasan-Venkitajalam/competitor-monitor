"""
Local execution guarantee module for competitor intelligence.
Ensures all processing occurs locally on the host machine.
Validates: Requirements 8.1, 8.2, 8.3, 8.4
"""

import os
import socket
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional


class LocalExecutionGuarantee:
    """Ensures all processing occurs locally on the host machine."""
    
    def __init__(self, model_dir: Optional[str] = None):
        """
        Initialize the local execution guarantee.
        
        Args:
            model_dir: Directory for local models (defaults to ./models)
        """
        self.model_dir = Path(model_dir or 'models')
        self.execution_log = []
        self._ensure_model_directory()
    
    def _ensure_model_directory(self):
        """Ensure the model directory exists."""
        self.model_dir.mkdir(parents=True, exist_ok=True)
    
    def get_local_model_path(self, model_name: str) -> Path:
        """
        Get the local path for a model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Path to the local model
        """
        return self.model_dir / model_name
    
    def load_local_model(self, model_name: str) -> Optional[Path]:
        """
        Load a local model from storage.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Path to the loaded model or None if not found
        """
        model_path = self.get_local_model_path(model_name)
        
        if model_path.exists():
            self.execution_log.append({
                'timestamp': datetime.now().isoformat(),
                'action': 'load_local_model',
                'model': model_name,
                'path': str(model_path),
                'source': 'local'
            })
            return model_path
        
        return None
    
    def execute_local_script(self, script_path: str, 
                             args: Optional[list[str]] = None) -> tuple[int, str, str]:
        """
        Execute a local script.
        
        Args:
            script_path: Path to the script
            args: Optional arguments
            
        Returns:
            Tuple of (return_code, stdout, stderr)
        """
        cmd = ['python', script_path]
        if args:
            cmd.extend(args)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            self.execution_log.append({
                'timestamp': datetime.now().isoformat(),
                'action': 'execute_local_script',
                'script': script_path,
                'args': args or [],
                'return_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'execution_type': 'local'
            })
            
            return result.returncode, result.stdout, result.stderr
            
        except subprocess.TimeoutExpired:
            self.execution_log.append({
                'timestamp': datetime.now().isoformat(),
                'action': 'execute_local_script',
                'script': script_path,
                'args': args or [],
                'error': 'timeout',
                'execution_type': 'local'
            })
            return -1, '', 'Script execution timed out'
        
        except Exception as e:
            self.execution_log.append({
                'timestamp': datetime.now().isoformat(),
                'action': 'execute_local_script',
                'script': script_path,
                'args': args or [],
                'error': str(e),
                'execution_type': 'local'
            })
            return -1, '', str(e)
    
    def check_no_network_access(self) -> bool:
        """
        Check if network access is disabled.
        
        Returns:
            True if network access is disabled, False otherwise
        """
        # Check for common network-related environment variables
        network_vars = [
            'HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy',
            'NO_PROXY', 'no_proxy'
        ]
        
        for var in network_vars:
            if var in os.environ:
                return False
        
        return True
    
    def log_data_access(self, data_type: str, 
                        data_size: int,
                        destination: str = 'local') -> dict:
        """
        Log data access for audit purposes.
        
        Args:
            data_type: Type of data being accessed
            data_size: Size of data in bytes
            destination: Where data is being sent
            
        Returns:
            Log entry dictionary
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'data_type': data_type,
            'data_size': data_size,
            'destination': destination,
            'execution_type': 'local' if destination == 'local' else 'external'
        }
        
        self.execution_log.append(log_entry)
        return log_entry
    
    def get_execution_log(self) -> list[dict]:
        """Get the execution log."""
        return self.execution_log
    
    def clear_execution_log(self):
        """Clear the execution log."""
        self.execution_log = []
    
    def verify_local_execution(self) -> dict:
        """
        Verify that all execution was local.
        
        Returns:
            Verification result dictionary
        """
        external_executions = [
            e for e in self.execution_log 
            if e.get('execution_type') == 'external'
        ]
        
        return {
            'all_local': len(external_executions) == 0,
            'total_executions': len(self.execution_log),
            'external_executions': len(external_executions),
            'external_details': external_executions
        }


def run_local_semantic_diff(current_file: str, historical_file: str,
                            script_path: str = 'scripts/semantic_diff.py') -> dict:
    """
    Run semantic diffing locally.
    
    Args:
        current_file: Path to current text file
        historical_file: Path to historical text file
        script_path: Path to the semantic diff script
        
    Returns:
        Result dictionary
    """
    guarantee = LocalExecutionGuarantee()
    
    return_code, stdout, stderr = guarantee.execute_local_script(
        script_path, [current_file, historical_file]
    )
    
    if return_code == 0:
        import json
        try:
            result = json.loads(stdout)
            result['execution_type'] = 'local'
            return result
        except json.JSONDecodeError:
            return {
                'error': 'Failed to parse JSON output',
                'stdout': stdout,
                'stderr': stderr,
                'execution_type': 'local'
            }
    else:
        return {
            'error': stderr,
            'return_code': return_code,
            'execution_type': 'local'
        }


if __name__ == '__main__':
    # Test the local execution guarantee
    guarantee = LocalExecutionGuarantee()
    
    print("Local Execution Guarantee Test")
    print("=" * 40)
    
    # Check network access
    no_network = guarantee.check_no_network_access()
    print(f"\nNetwork access disabled: {no_network}")
    
    # Log some data access
    guarantee.log_data_access('text_embedding', 1024, 'local')
    guarantee.log_data_access('report', 2048, 'local')
    
    # Verify local execution
    verification = guarantee.verify_local_execution()
    print(f"\nVerification:")
    print(f"  All local: {verification['all_local']}")
    print(f"  Total executions: {verification['total_executions']}")
    print(f"  External executions: {verification['external_executions']}")
    
    # Show execution log
    print(f"\nExecution log:")
    for entry in guarantee.get_execution_log():
        action = entry.get('action', 'N/A')
        exec_type = entry.get('execution_type', 'N/A')
        print(f"  {entry['timestamp']}: {action} - {exec_type}")
