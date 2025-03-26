"""
Adapter to access to Jira
"""
import json
import logging
from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth

from src.main.domain.model.exceptions import JiraGetIssueException, JiraGetWorkloadFromIssue
from src.main.domain.model.issues import Issues, Issue
from src.main.domain.model.worklog import Worklog
from src.main.domain.model.worklogs_issue import WorklogsForIssue
from src.main.domain.model.worklogs_user import WorklogsForUser

logger = logging.getLogger(__name__)

class JiraAdapter:
    """Class to access to Jira"""
    __jira_url = "https://seiitra.atlassian.net"

    def __init__(self, username: str, api_token: str):
        self.__jira_url = "https://seiitra.atlassian.net"
        self.__auth = HTTPBasicAuth(username, api_token)
        self.__request_default_headers = {"Accept": "application/json"}

    def get_technical_stories(self) -> Issues:
        """Function to get technical stories"""
        logger.info("Extract technical stories from JIRA")
        jql = "project = ThetraReprise AND type = 'Technical Story' AND component IN (EquipeRose, EquipeOrange, EquipeVerte)"
        return self.__fetch_issues(jql, True, True)

    def get_sub_issues_from_issue(self, issue_key: str) -> Issues:
        """Function to get sub issues from a parent issue"""
        logger.info("Extract sub issues from issue %s", issue_key)
        jql = f"parent = {issue_key}"
        return self.__fetch_issues(jql)

    def get_issues_where_user_has_worked_on_it(self, user_email: str) -> Issues:
        """Function to get issues associated to a user"""
        logger.info("Get issues ids from user %s", user_email)
        jql = f"worklogAuthor = '{user_email}'"
        return self.__fetch_issues(jql)

    def get_issues_for_component(self, component_name: str) -> Issues:
        """Function to get issues associated to a component"""
        logger.info("Get issues ids from component %s", component_name)
        jql = f"component = '{component_name}'"
        return self.__fetch_issues(jql)

    def __fetch_issues(self, jql: str, fetch_sub_issues: bool = False, fetch_parent: bool = False) -> Issues:
        url = f"{self.__jira_url}/rest/api/3/search"
        #TODO: Add pagination
        params = {
            "jql": jql,
            "fields": "key, summary, parent, worklog",
            "maxResults": 100,
            # "startAt": 100
        }
        response = requests.get(url,
                                headers=self.__request_default_headers,
                                auth=self.__auth,
                                params=params,
                                timeout=1000)

        if response.status_code == 200:
            issues = self.__map_issues_to_model(response)
            if fetch_sub_issues:
                for issue in issues.issues:
                    issue.sub_issues = self.get_sub_issues_from_issue(issue.key)
            if fetch_parent:
                for issue in issues.issues:
                    if issue.parent_key is not None:
                        issue.parent = self.get_issue_details(issue.parent_key)
            return issues

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
        logger.info("Get issue details for issue %s", issue_id)
        if response.status_code == 200:
            return self.__map_issue_to_model(response.json())

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

    def __map_issues_to_model(self, response):
        issues = []
        for issue in response.json().get("issues", []):
            issues.append(self.__map_issue_to_model(issue))
        return Issues(issues)

    def __map_issue_to_model(self, issue):
        fields = issue["fields"] if issue.get("fields") else {}
        parent_key = fields["parent"]["key"] if fields.get("parent") else None
        title = fields["summary"] if fields.get("summary") else None
        key = issue["key"] if issue.get("key") else None
        worklogs = self.__map_workloads_to_model(fields.get("worklog", {}))

        return Issue(id = issue["id"],
                     key = key,
                     title = title,
                     worklogs= worklogs,
                     parent_key = parent_key)

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
