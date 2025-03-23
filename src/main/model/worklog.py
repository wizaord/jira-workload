from dataclasses import dataclass
from datetime import datetime


@dataclass
class Worklog:
    """Class that represents a Worklog in Jira"""
    id: str
    user_email: str
    date_started: datetime
    time_spent_minutes: int
    issue_id: str
