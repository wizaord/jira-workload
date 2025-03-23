from dataclasses import dataclass

from src.main.model.worklogs_issue import WorklogsForIssue
from src.main.model.worklogs_user import WorklogsForUser
from src.main.model.worklog import Worklog



@dataclass
class WorklogsForComponent:
    """Class that represents Workloads"""
    jira_component_name: str
    workloads: list[Worklog]

    def __init__(self, jira_component_name: str, workloads: list[Worklog]):
        self.jira_component_name = jira_component_name
        self.workloads = workloads

    def extend(self, workloads: list[Worklog]):
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
