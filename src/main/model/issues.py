from dataclasses import dataclass

from src.main.model.issue import Issue


@dataclass
class Issues:
    """Class that represents all issues in Jira"""
    issues: list[Issue]

    def __init__(self, issues: list[Issue]):
        self.issues = issues


    def get_issue_by_id(self, issue_id: str) -> Issue:
        """Return the issue with the given id"""
        for issue in self.issues:
            if issue.id == issue_id:
                return issue
        return None
