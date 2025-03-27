"""
This module contains the class WorklogsForIssue that represents the worklogs for an issue.
"""
from dataclasses import dataclass
from typing import Optional

from src.main.domain.model.worklog import Worklog


@dataclass
class WorklogsForIssue:
    """Class that represents Workloads"""
    issue_id: str
    workloads: list[Worklog]

    def extend(self, worklogs: list[Worklog]) -> 'WorklogsForIssue':
        """Extend the worklogs"""
        self.workloads.extend(worklogs)
        return self

    def filter_for_user(self, user_email: str) -> Optional['WorklogsForIssue']:
        """Filter the worklogs for a specific user"""
        workloads_filtered = [worklog for worklog in self.workloads if worklog.user_email == user_email]
        if len(workloads_filtered) > 0:
            return WorklogsForIssue(self.issue_id, workloads_filtered)
        return None

    def get_spent_time_group_by_day(self):
        """Return the time spent grouped by day"""
        time_spent_group_by_day = {}
        for workload in self.workloads:
            workload_date = workload.date_started.date()
            if workload_date not in time_spent_group_by_day:
                time_spent_group_by_day[workload_date] = 0
            time_spent_group_by_day[workload_date] += workload.time_spent_minutes
        return time_spent_group_by_day
