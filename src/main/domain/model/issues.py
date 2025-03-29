"""
This module contains the class that represents all issues in Jira.
"""
import copy
from dataclasses import dataclass
from typing import Optional

from src.main.domain.model.worklog import Worklog
from src.main.domain.model.worklogs_issue import WorklogsForIssue


@dataclass
class Issue:
    """Class that represents a Jira issue"""
    id: str
    key: str
    title: str
    worklogs_for_issue: WorklogsForIssue
    parent_key: str = None
    parent: 'Issue' = None
    sub_issues: 'Issues' = None

    def get_worklogs_from_issue_and_sub_issues(self) -> WorklogsForIssue:
        """Return the worklogs for the issue and its sub-issues"""
        new_worklogs_for_issue = copy.deepcopy(self.worklogs_for_issue)
        if self.sub_issues:
            for sub_issue in self.sub_issues.issues:
                new_worklogs_for_issue.extend(sub_issue.worklogs_for_issue.workloads)
        return new_worklogs_for_issue

    def filter_for_user(self, user_email: str) -> Optional['Issue']:
        """Return this issue if user is present in worklogs or sub issues worklogs"""
        sub_issues_filtered = None
        if self.sub_issues:
            sub_issues_filtered = self.sub_issues.filter_for_user(user_email)
        worklogs_filtered = self.worklogs_for_issue.filter_for_user(user_email)
        if sub_issues_filtered is None and worklogs_filtered is None:
            return None
        return Issue(self.id, self.key, self.title, worklogs_filtered, self.parent_key, self.parent, sub_issues_filtered)



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

    def get_worklogs_from_all_issues_and_sub_issues(self) -> list[Worklog]:
        """Return the worklogs for all issues"""
        worklogs = []
        for issue in self.issues:
            worklogs.extend(issue.get_worklogs_from_issue_and_sub_issues().workloads)
        return worklogs

    def get_all_distinct_worklogs_user_emails(self) -> set[str]:
        """Return all distinct user emails from worklogs"""
        return set(worklog.user_email for worklog in self.get_worklogs_from_all_issues_and_sub_issues())

    def filter_for_user(self, user_email: str) -> Optional['Issues']:
        """Filter the issues for a specific user"""
        issues = []
        for issue in self.issues:
            issue_filtered = issue.filter_for_user(user_email)
            if issue_filtered is not None:
                issues.append(issue_filtered)
        if len(issues) > 0:
            return Issues(issues)
        return None

    def get_issue_by_key(self, parent_key: str)-> Optional[Issue]:
        """Return the issue with the given key"""
        for issue in self.issues:
            if issue.key == parent_key:
                return issue
        return None

    def append(self, issues: 'Issues') -> 'Issues':
        """Append the issues to the current issues"""
        self.issues.extend(issues.issues)
        return self
