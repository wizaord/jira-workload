"""
This module contains the class that represents all issues in Jira.
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class Issue:
    """Class that represents a Jira issue"""
    id: str
    key: str
    title: str
    parent_key: str = None
    parent: 'Issue' = None
    sub_issues: 'Issues' = None

@dataclass
class Issues:
    """Class that represents a group of issues in Jira"""
    issues: list[Issue]

    def __init__(self, issues: list[Issue]):
        self.issues = issues

    def count_issues(self) -> int:
        """Return the number of issues"""
        return len(self.issues)

    def get_issue_by_id(self, issue_id: str) -> Optional[Issue]:
        """Return the issue with the given id"""
        for issue in self.issues:
            if issue.id == issue_id:
                return issue
        return None
