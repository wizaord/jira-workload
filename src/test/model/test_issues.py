"""
Test cases for the Issues class.
"""
import unittest

from src.main.model.issue import Issue
from src.main.model.issues import Issues


class TestIssues(unittest.TestCase):
    """Test cases for the Issues class"""

    def test_issues_can_be_initialized(self):
        """Test that the Issues class can be initialized"""
        issue1 = Issue(id="1", title="Issue 1", key="KEY-1")
        issue2 = Issue(id="2", title="Issue 2", key="KEY-2")
        issues = Issues([issue1, issue2])
        self.assertEqual(len(issues.issues), 2)

    def test_get_issue_by_id_returns_correct_issue(self):
        """Test that the get_issue_by_id method returns the correct issue"""
        issue1 = Issue(id="1", title="Issue 1", key="KEY-1")
        issue2 = Issue(id="2", title="Issue 2", key="KEY-2")
        issues = Issues([issue1, issue2])
        self.assertEqual(issues.get_issue_by_id("1"), issue1)

    def test_get_issue_by_id_returns_none_for_nonexistent_id(self):
        """Test that the get_issue_by_id method returns None for a nonexistent id"""
        issue1 = Issue(id="1", title="Issue 1", key="KEY-1")
        issue2 = Issue(id="2", title="Issue 2", key="KEY-2")
        issues = Issues([issue1, issue2])
        self.assertIsNone(issues.get_issue_by_id("3"))

    def test_get_issue_by_id_returns_none_for_empty_list(self):
        """Test that the get_issue_by_id method returns None for an empty list"""
        issues = Issues([])
        self.assertIsNone(issues.get_issue_by_id("1"))

if __name__ == "__main__":
    unittest.main()
