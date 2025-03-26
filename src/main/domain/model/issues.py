"""
This module contains the class that represents all issues in Jira.
"""
from dataclasses import dataclass
from typing import Optional

from src.main.domain.model.worklog import Worklog


@dataclass
class Issue:
    """Class that represents a Jira issue"""
    id: str
    key: str
    title: str
    worklogs: list[Worklog]
    parent_key: str = None
    parent: 'Issue' = None
    sub_issues: 'Issues' = None

    def get_worklogs_for_issue_and_sub_issues(self):
        """Return the worklogs for the issue and its sub-issues"""
        worklogs = self.worklogs
        if self.sub_issues:
            for sub_issue in self.sub_issues.issues:
                worklogs.extend(sub_issue.worklogs)
        return worklogs

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

    def get_all_worklogs(self):
        """Return the worklogs for all issues"""
        worklogs = []
        for issue in self.issues:
            worklogs.extend(issue.get_worklogs_for_issue_and_sub_issues())
        return worklogs
