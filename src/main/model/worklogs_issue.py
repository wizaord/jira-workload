"""
This module contains the class WorklogsForIssue that represents the worklogs for an issue.
"""
from dataclasses import dataclass

from src.main.model.worklog import Worklog


@dataclass
class WorklogsForIssue:
    """Class that represents Workloads"""
    issue_id: str
    workloads: list[Worklog]
