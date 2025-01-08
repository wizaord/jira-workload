from dataclasses import dataclass

from src.main.model.workload import Workload



@dataclass
class Workloads:
    """Class that represents Workloads"""
    jira_component_name: str
    workloads: list[Workload]

    def __init__(self, jira_component_name: str, workloads: list[Workload]):
        self.jira_component_name = jira_component_name
        self.workloads = workloads

    def extend(self, workloads: list[Workload]):
        self.workloads.extend(workloads)

    def get_usernames(self) -> set[str]:
        """Return the users that have workloads"""
        return set([workload.username for workload in self.workloads])

    def get_issues(self) -> set[str]:
        """Return the issues that have workloads"""
        return set([workload.issue_id for workload in self.workloads])

    def get_workloads_for_issue(self, issue_id: str):
        """Return the workloads for the given issue"""
        return Workloads(self.jira_component_name, [workload for workload in self.workloads if workload.issue_id == issue_id])

    def get_workloads_for_user(self, username: str):
        """Return the workloads for the given user"""
        return Workloads(self.jira_component_name, [workload for workload in self.workloads if workload.username == username])

    def get_total_time_spent(self) -> int:
        """Return the total time spent in seconds"""
        return sum([workload.time_spent_seconds for workload in self.workloads])