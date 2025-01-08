from dataclasses import dataclass


@dataclass
class Workload:
    """Class that represents a Workload in Jira"""
    id: str
    username: str
    date_started: str
    time_spent_seconds: int
    issue_id: str
