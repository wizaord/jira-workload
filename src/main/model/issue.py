"""
This module contains the Issue class, which represents a Jira issue.
"""
from dataclasses import dataclass


@dataclass
class Issue:
    """Class that represents a Jira issue"""
    id: str
    key: str
    title: str
