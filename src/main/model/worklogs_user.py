"""
This module contains the class WorklogsForUser that represents the workloads for a user.
"""
from dataclasses import dataclass
from datetime import date

from src.main.model.worklog import Worklog


@dataclass
class WorklogsForUser:
    """Class that represents Workloads"""
    username: str
    workloads: list[Worklog]

    def get_worklogs_for_day(self, day: date) -> 'WorklogsForUser':
        """Return the workloads for the given day"""
        return WorklogsForUser(self.username,
                               [workload for workload in self.workloads if workload.date_started.date() == day])

    def get_time_spent_group_by_day(self) -> dict[date, int]:
        """Return the time spent grouped by day"""
        time_spent_group_by_day = {}
        for workload in self.workloads:
            workload_date = workload.date_started.date()
            if workload_date not in time_spent_group_by_day:
                time_spent_group_by_day[workload_date] = 0
            time_spent_group_by_day[workload_date] += workload.time_spent_minutes
        return time_spent_group_by_day

    def get_issues(self) -> set[str]:
        """Return the issues that have workloads"""
        return set([workload.issue_id for workload in self.workloads])

    def get_total_time_spent(self) -> int:
        """Return the total time spent in minutes"""
        return sum([workload.time_spent_minutes for workload in self.workloads])

    def append_worklogs(self, worklogs: list[Worklog]):
        """Append worklogs to the existing workloads"""
        self.workloads.extend(worklogs)
