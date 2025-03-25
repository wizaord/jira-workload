"""
This module contains the class that represents the workloads for a component.
"""
from dataclasses import dataclass

from src.main.domain.model.worklog import Worklog
from src.main.domain.model.worklogs_issue import WorklogsForIssue
from src.main.domain.model.worklogs_user import WorklogsForUser


@dataclass
class WorklogsForComponent:
    """Class that represents Workloads"""
    jira_component_name: str
    workloads: list[Worklog]

    def __init__(self, jira_component_name: str, workloads: list[Worklog]):
        """Initialize the WorkloadsForComponent"""
        self.jira_component_name = jira_component_name
        self.workloads = workloads

    def extend(self, workloads: list[Worklog]):
        """Append worklogs to the existing workloads"""
        self.workloads.extend(workloads)

    def get_usernames(self) -> set[str]:
        """Return the users that have workloads"""
        return set([workload.user_email for workload in self.workloads])

    def get_worklogs_for_issue(self, issue_id: str) -> WorklogsForIssue:
        """Return the workloads for the given issue"""
        return WorklogsForIssue(issue_id, [workload for workload in self.workloads if workload.issue_id == issue_id])

    def get_worklogs_for_user(self, username: str)-> WorklogsForUser:
        """Return the workloads for the given user"""
        return WorklogsForUser(username,
                               [workload for workload in self.workloads if workload.user_email == username])

    def get_component_issues(self):
        """Return the issues that have workloads"""
        return set([workload.issue_id for workload in self.workloads])
