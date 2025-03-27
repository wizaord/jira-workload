import unittest
from datetime import datetime

from src.main.domain.model.worklog import Worklog
from src.main.domain.model.worklogs_issue import WorklogsForIssue


class TestsWorklogsIssue(unittest.TestCase):
    """Test cases for the WorklogsForComponent class"""

    def test_get_spent_time_group_by_day(self):
        """Test that the get_spent_time_group_by_day method returns the correct time spent"""
        # given
        datetime_1 = datetime.strptime("2021-10-10", "%Y-%m-%d")
        datetime_2 = datetime.strptime("2021-10-11", "%Y-%m-%d")
        workloads = WorklogsForIssue("issue1", [
            Worklog("id1", "user1", datetime_1, 60, "issue1"),
            Worklog("id2", "user1", datetime_1, 60, "issue1"),
            Worklog("id3", "user1", datetime_2, 60, "issue1"),
            Worklog("id4", "user1", datetime_2, 20, "issue1"),
        ])
        # when
        time_spent_group_by_day = workloads.get_spent_time_group_by_day()

        # then
        self.assertEqual(len(time_spent_group_by_day), 2)
        self.assertEqual(time_spent_group_by_day[datetime_1.date()], 120)
        self.assertEqual(time_spent_group_by_day[datetime_2.date()], 80)