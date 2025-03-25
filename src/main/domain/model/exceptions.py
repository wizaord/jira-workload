"""
File contains custom exceptions for the domain layer.
"""

class JiraGetIssueException(Exception):
    """Exception raised when unable to extract issues from Jira"""

class JiraGetWorkloadFromIssue(Exception):
    """Exception raised when unable to extract workload from Jira"""
