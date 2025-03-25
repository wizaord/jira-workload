"""
Test cases for the Issues class
"""
import unittest

from src.main.model.issue import Issue
from src.main.model.issues import Issues


class TestIssues(unittest.TestCase):
    """Test cases for the WorklogsForComponent class"""

    def test_counts_issues_correctly(self):
        """Test that the count_issues method returns the correct number of issues"""
        issues = Issues([
            Issue("1", "key", "title"),
            Issue("2", "key", "title"),
        ])
        self.assertEqual(issues.count_issues(), 2)

