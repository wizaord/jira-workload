import unittest
from src.main.model.issues import Issues
from src.main.model.issue import Issue

class TestIssues(unittest.TestCase):

    def test_issues_can_be_initialized(self):
        issue1 = Issue(id="1", title="Issue 1", key="KEY-1")
        issue2 = Issue(id="2", title="Issue 2", key="KEY-2")
        issues = Issues([issue1, issue2])
        self.assertEqual(len(issues.issues), 2)

    def test_get_issue_by_id_returns_correct_issue(self):
        issue1 = Issue(id="1", title="Issue 1", key="KEY-1")
        issue2 = Issue(id="2", title="Issue 2", key="KEY-2")
        issues = Issues([issue1, issue2])
        self.assertEqual(issues.get_issue_by_id("1"), issue1)

    def test_get_issue_by_id_returns_none_for_nonexistent_id(self):
        issue1 = Issue(id="1", title="Issue 1", key="KEY-1")
        issue2 = Issue(id="2", title="Issue 2", key="KEY-2")
        issues = Issues([issue1, issue2])
        self.assertIsNone(issues.get_issue_by_id("3"))

    def test_get_issue_by_id_returns_none_for_empty_list(self):
        issues = Issues([])
        self.assertIsNone(issues.get_issue_by_id("1"))

if __name__ == "__main__":
    unittest.main()