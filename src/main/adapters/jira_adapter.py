"""
Adapter to access to Jira
"""
import logging
from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth

from src.main.model.exceptions import (JiraGetIssueException,
                                       JiraGetWorkloadFromIssue)
from src.main.model.issue import Issue
from src.main.model.issues import Issues
from src.main.model.worklog import Worklog
from src.main.model.worklogs_issue import WorklogsForIssue
from src.main.model.worklogs_user import WorklogsForUser

logger = logging.getLogger(__name__)

class JiraAdapter:
    """Class to access to Jira"""
    __jira_url = "https://seiitra.atlassian.net"

    def __init__(self, username: str, api_token: str):
        self.__jira_url = "https://seiitra.atlassian.net"
        self.__auth = HTTPBasicAuth(username, api_token)
        self.__request_default_headers = {"Accept": "application/json"}

    def get_issues_where_user_has_worked_on_it(self, user_email: str) -> Issues:
        """Function to get issues associated to a user"""
        logger.info("Get issues ids from user %s", user_email)
        jql = f"worklogAuthor = '{user_email}'"
        url = f"{self.__jira_url}/rest/api/3/search"
        params = {
            "jql": jql,
            "fields": "key, summary, worklog"
        }

        response = requests.get(url,
                                headers=self.__request_default_headers,
                                auth=self.__auth,
                                params=params,
                                timeout=1000)

        if response.status_code == 200:
            issues = []
            for issue in response.json().get("issues", []):
                issues.append(Issue(issue["id"], issue["key"], issue["fields"]["summary"]))
            return Issues(issues)

        raise JiraGetIssueException()

    def get_issues_for_component(self, component_name: str) -> Issues:
        """Function to get issues associated to a component"""
        logger.info("Get issues ids from component %s", component_name)
        jql = f"component = '{component_name}'"
        url = f"{self.__jira_url}/rest/api/3/search"
        params = {
            "jql": jql,
            "fields": "key"
        }

        response = requests.get(url,
                                headers=self.__request_default_headers,
                                auth=self.__auth,
                                params=params,
                                timeout=1000)

        logger.debug("ISSUE => %s", response.json())
        if response.status_code == 200:
            return self.__map_issues_to_model(response.json())
        raise JiraGetIssueException()

    def get_users_for_component(self, component_name: str) -> set[str]:
        """
        Get all users who logged time on issues in a specific component
        Returns a set of unique usernames
        """
        # Get all issues for the component
        issues = self.get_issues_for_component(component_name)

        # Initialize empty set for users
        users = set(str)

        for issue in issues.issues:
            worklogs = self.get_worklogs_for_issue(issue.id)
            users.update(worklog.user_email for worklog in worklogs.workloads)

        return users


    def get_issue_details(self, issue_id: str) -> Issue:
        """Function to get issue details"""
        url = f"{self.__jira_url}/rest/api/3/issue/{issue_id}"
        response = requests.get(url,
                                headers=self.__request_default_headers,
                                auth=self.__auth,
                                timeout=1000)
        logger.debug("ISSUE DETAILS => %s", response.json())
        if response.status_code == 200:
            issue_dict = response.json()
            return Issue(issue_id, issue_dict["key"], issue_dict["fields"]["summary"])
        raise JiraGetIssueException()

    def get_worklogs_for_issue(self, issue_key: str) -> WorklogsForIssue:
        """Function to get worklogs for an issue"""
        url = f"{self.__jira_url}/rest/api/3/issue/{issue_key}/worklog"
        response = requests.get(url,
                                headers=self.__request_default_headers,
                                auth=self.__auth,
                                timeout=1000)
        logger.debug("WORKLOGS => %s", response.json())
        if response.status_code == 200:
            return WorklogsForIssue(issue_key, self.__map_workloads_to_model(response.json()))
        raise JiraGetWorkloadFromIssue()


    def get_user_worklogs_for_issue(self, issue_key: str, username: str) -> WorklogsForUser:
        """Function to get worklogs for an issue for a specific user"""
        issue_worklogs = self.get_worklogs_for_issue(issue_key)
        logger.debug("worklogs for issue %s => %s", issue_key, issue_worklogs)
        return WorklogsForUser(
            username,
            [worklog for worklog in issue_worklogs.workloads if worklog.user_email == username])

    def __map_workloads_to_model(self, workloads_response: dict) -> list[Worklog]:
        """Map workloads in Workload model"""
        worklogs = workloads_response.get("worklogs", [])
        return [Worklog(
            id=worklog["id"],
            user_email=worklog["author"]["emailAddress"],
            date_started=datetime.strptime(worklog["started"], "%Y-%m-%dT%H:%M:%S.%f%z"),
            time_spent_minutes=worklog["timeSpentSeconds"] / 60,
            issue_id=worklog["issueId"]
        ) for worklog in worklogs]

    def __map_issues_to_model(self, issue_response: dict) -> Issues:
        """Map issues in Issue model"""
        issues = []
        for issue in issue_response.get("issues", []):
            issues.append(self.get_issue_details(issue["id"]))
        return Issues(issues)
