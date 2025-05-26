"""
Test cases for the Issues class
"""
import unittest
from datetime import datetime

from src.main.domain.model.issues import Issues, Issue
from src.main.domain.model.worklog import Worklog
from src.main.domain.model.worklogs_issue import WorklogsForIssue


class TestIssues(unittest.TestCase):
    """Test cases for the WorklogsForComponent class"""

    def test_counts_issues_correctly(self):
        """Test that the count_issues method returns the correct number of issues"""
        issues = Issues([
            Issue("1", "key", "title", "A faire", WorklogsForIssue("1", [])),
            Issue("2", "key", "title", "En cours", WorklogsForIssue("2", [])),
        ])
        self.assertEqual(issues.count_issues(), 2)

    def test_get_all_distinct_worklogs_user_emails_return_empty_if_no_worklogs(self):
        """Test that the get_all_distinct_user_emails method returns the correct emails"""
        issues = Issues([
            Issue("1", "key", "title", "A faire", WorklogsForIssue("1", [])),
            Issue("2", "key", "title", "En cours", WorklogsForIssue("2", [])),
        ])
        self.assertEqual(len(issues.get_all_distinct_worklogs_user_emails()), 0)

    def test_get_all_distinct_worklogs_user_emails_return_all_users(self):
        """Test that the get_all_distinct_user_emails method returns the correct emails"""
        issues = Issues([
            Issue("1", "key", "title", "Terminé", WorklogsForIssue("1", [
                Worklog("w11", "email1", datetime.now(), 10, "1"),
                Worklog("w21", "email2", datetime.now(), 10, "2"),
            ])),
            Issue("2", "key", "title", "En cours", WorklogsForIssue("2", [
                Worklog("w21", "email1", datetime.now(), 10, "1"),
                Worklog("w22", "email3", datetime.now(), 10, "2"),
            ])),
        ])
        self.assertSetEqual(issues.get_all_distinct_worklogs_user_emails(),
                            {"email1", "email2", "email3"})

    def test_filter_for_user_returns_only_issues_for_user(self):
        """Test that the filter_for_user method returns the correct issues"""
        issues = Issues([
            Issue("1", "key", "title", "A faire", WorklogsForIssue("1", [
                Worklog("w11", "email1", datetime.now(), 10, "1"),
                Worklog("w21", "email2", datetime.now(), 10, "2"),
            ])),
            Issue("2", "key", "title", "En cours", WorklogsForIssue("2", [
                Worklog("w21", "email1", datetime.now(), 10, "1"),
                Worklog("w22", "email3", datetime.now(), 10, "2"),
            ])),
        ])
        filtered_issues = issues.filter_for_user("email1")
        self.assertEqual(len(filtered_issues.issues), 2)

        self.assertEqual(filtered_issues.issues[0].id, "1")
        self.assertEqual(len(filtered_issues.issues[0].worklogs_for_issue.workloads), 1)
        self.assertEqual(filtered_issues.issues[0].worklogs_for_issue.workloads[0].id, "w11")

        self.assertEqual(filtered_issues.issues[1].id, "2")
        self.assertEqual(len(filtered_issues.issues[1].worklogs_for_issue.workloads), 1)
        self.assertEqual(filtered_issues.issues[1].worklogs_for_issue.workloads[0].id, "w21")
