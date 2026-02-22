"""
User approval loop handler for competitor intelligence.
Handles user-in-the-loop approval for autonomous actions.
Validates: Requirements 7.1, 7.2, 7.3, 7.4, 7.5
"""

import json
from datetime import datetime
from enum import Enum
from typing import Optional


class ApprovalStatus(Enum):
    """Status of an approval request."""
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    EXPIRED = 'expired'


class ApprovalRequest:
    """Represents an approval request."""
    
    def __init__(self, action_type: str, description: str, 
                 action_data: dict, timeout_seconds: int = 300):
        """
        Initialize an approval request.
        
        Args:
            action_type: Type of action (terminal, file, url)
            description: Human-readable description of the action
            action_data: Data about the action being requested
            timeout_seconds: Timeout in seconds (default 5 minutes)
        """
        self.action_type = action_type
        self.description = description
        self.action_data = action_data
        self.timeout_seconds = timeout_seconds
        self.status = ApprovalStatus.PENDING
        self.requested_at = datetime.now()
        self.approved_at: Optional[datetime] = None
        self.rejected_at: Optional[datetime] = None
        self.approver: Optional[str] = None
    
    def approve(self, approver: str = 'user') -> bool:
        """Approve the request."""
        if self.status != ApprovalStatus.PENDING:
            return False
        
        self.status = ApprovalStatus.APPROVED
        self.approved_at = datetime.now()
        self.approver = approver
        return True
    
    def reject(self, approver: str = 'user') -> bool:
        """Reject the request."""
        if self.status != ApprovalStatus.PENDING:
            return False
        
        self.status = ApprovalStatus.REJECTED
        self.rejected_at = datetime.now()
        self.approver = approver
        return True
    
    def is_expired(self) -> bool:
        """Check if the request has expired."""
        if self.status != ApprovalStatus.PENDING:
            return False
        
        elapsed = (datetime.now() - self.requested_at).total_seconds()
        return elapsed > self.timeout_seconds
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'action_type': self.action_type,
            'description': self.description,
            'action_data': self.action_data,
            'status': self.status.value,
            'requested_at': self.requested_at.isoformat(),
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'rejected_at': self.rejected_at.isoformat() if self.rejected_at else None,
            'approver': self.approver,
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class ApprovalHandler:
    """Handles user approval requests for autonomous actions."""
    
    def __init__(self):
        """Initialize the approval handler."""
        self.pending_requests: list[ApprovalRequest] = []
        self.approved_requests: list[ApprovalRequest] = []
        self.rejected_requests: list[ApprovalRequest] = []
    
    def request_terminal_approval(self, command: str) -> ApprovalRequest:
        """
        Request approval for a terminal command.
        
        Args:
            command: The terminal command to execute
            
        Returns:
            ApprovalRequest object
        """
        request = ApprovalRequest(
            action_type='terminal',
            description=f'Execute terminal command: {command[:50]}...',
            action_data={'command': command}
        )
        self.pending_requests.append(request)
        return request
    
    def request_file_approval(self, file_path: str, 
                              action: str = 'write') -> ApprovalRequest:
        """
        Request approval for a file operation.
        
        Args:
            file_path: Path to the file
            action: Action being performed (write, delete, modify)
            
        Returns:
            ApprovalRequest object
        """
        request = ApprovalRequest(
            action_type='file',
            description=f'{action} file: {file_path}',
            action_data={'file_path': file_path, 'action': action}
        )
        self.pending_requests.append(request)
        return request
    
    def request_url_approval(self, url: str) -> ApprovalRequest:
        """
        Request approval for URL browsing.
        
        Args:
            url: The URL to browse
            
        Returns:
            ApprovalRequest object
        """
        request = ApprovalRequest(
            action_type='url',
            description=f'Browse URL: {url}',
            action_data={'url': url}
        )
        self.pending_requests.append(request)
        return request
    
    def get_pending_request(self) -> Optional[ApprovalRequest]:
        """Get the oldest pending request."""
        if not self.pending_requests:
            return None
        
        # Check for expired requests
        for request in self.pending_requests:
            if request.is_expired():
                request.status = ApprovalStatus.EXPIRED
                self.rejected_requests.append(request)
        
        # Remove expired requests from pending
        self.pending_requests = [
            r for r in self.pending_requests 
            if r.status == ApprovalStatus.PENDING
        ]
        
        if not self.pending_requests:
            return None
        
        return self.pending_requests[0]
    
    def approve_request(self, request: ApprovalRequest, 
                        approver: str = 'user') -> bool:
        """
        Approve a pending request.
        
        Args:
            request: The request to approve
            approver: Name of the approver
            
        Returns:
            True if approved, False otherwise
        """
        if request not in self.pending_requests:
            return False
        
        if request.approve(approver):
            self.pending_requests.remove(request)
            self.approved_requests.append(request)
            return True
        return False
    
    def reject_request(self, request: ApprovalRequest,
                       approver: str = 'user') -> bool:
        """
        Reject a pending request.
        
        Args:
            request: The request to reject
            approver: Name of the approver
            
        Returns:
            True if rejected, False otherwise
        """
        if request not in self.pending_requests:
            return False
        
        if request.reject(approver):
            self.pending_requests.remove(request)
            self.rejected_requests.append(request)
            return True
        return False
    
    def get_approval_status(self, request: ApprovalRequest) -> ApprovalStatus:
        """Get the status of a request."""
        if request in self.pending_requests:
            return request.status
        
        if request in self.approved_requests:
            return request.status
        
        if request in self.rejected_requests:
            return request.status
        
        return ApprovalStatus.EXPIRED
    
    def get_all_requests(self) -> list[dict]:
        """Get all requests as dictionaries."""
        all_requests = []
        
        for request in self.pending_requests:
            all_requests.append(request.to_dict())
        
        for request in self.approved_requests:
            all_requests.append(request.to_dict())
        
        for request in self.rejected_requests:
            all_requests.append(request.to_dict())
        
        return all_requests
    
    def get_approved_count(self) -> int:
        """Get count of approved requests."""
        return len(self.approved_requests)
    
    def get_rejected_count(self) -> int:
        """Get count of rejected requests."""
        return len(self.rejected_requests)
    
    def clear_requests(self):
        """Clear all requests."""
        self.pending_requests.clear()
        self.approved_requests.clear()
        self.rejected_requests.clear()


# Global approval handler instance
approval_handler = ApprovalHandler()


def request_approval(action_type: str, description: str, 
                     action_data: dict) -> ApprovalRequest:
    """
    Convenience function to request approval.
    
    Args:
        action_type: Type of action
        description: Description of the action
        action_data: Action data
        
    Returns:
        ApprovalRequest object
    """
    return approval_handler.request_terminal_approval(description)


if __name__ == '__main__':
    # Test the approval handler
    handler = ApprovalHandler()
    
    print("Approval Handler Test")
    print("=" * 40)
    
    # Request approvals for different actions
    terminal_request = handler.request_terminal_approval('python semantic_diff.py')
    file_request = handler.request_file_approval('reports/2026-02-19_Intelligence.md')
    url_request = handler.request_url_approval('https://example.com')
    
    print(f"\nPending requests: {len(handler.pending_requests)}")
    
    # Get pending request
    pending = handler.get_pending_request()
    if pending:
        print(f"\nFirst pending request:")
        print(f"  Type: {pending.action_type}")
        print(f"  Description: {pending.description}")
        print(f"  Status: {pending.status.value}")
    
    # Approve a request
    if handler.approve_request(terminal_request, 'user'):
        print(f"\nApproved: {terminal_request.action_type}")
    
    # Reject a request
    if handler.reject_request(file_request, 'user'):
        print(f"Rejected: {file_request.action_type}")
    
    # Get all requests
    all_requests = handler.get_all_requests()
    print(f"\nTotal requests: {len(all_requests)}")
    print(f"  Approved: {handler.get_approved_count()}")
    print(f"  Rejected: {handler.get_rejected_count()}")
    
    # Show request details
    print(f"\nRequest details:")
    for request in all_requests:
        print(f"  {request['action_type']}: {request['status']}")
