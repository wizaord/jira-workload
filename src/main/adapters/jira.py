import logging

import requests
from requests.auth import HTTPBasicAuth

from src.main.model.exceptions import JiraGetIssueException, JiraGetWorkloadFromIssue
from src.main.model.issue import Issue
from src.main.model.workload import Workload

logger = logging.getLogger(__name__)


class JiraAdapter:
    """Class to access to Jira"""
    __jira_url = "https://seiitra.atlassian.net"

    def __init__(self, username: str, api_token: str):
        self.__jira_url = "https://seiitra.atlassian.net"
        self.__auth = HTTPBasicAuth(username, api_token)
        self.__request_default_headers = {"Accept": "application/json"}

    def get_issues_from_components(self, component_name: str) -> list[Issue]:
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
                                params=params)

        logger.debug("ISSUE => %s", response.json())
        if response.status_code == 200:
            return self.__map_issues_to_model(response.json())
        else:
            raise JiraGetIssueException()

    def get_worklogs_from_issue(self, issue_key: str) -> list[Workload]:
        url = f"{self.__jira_url}/rest/api/3/issue/{issue_key}/worklog"
        response = requests.get(url,
                                headers=self.__request_default_headers,
                                auth=self.__auth)
        logger.debug("WORKLOAD => %s", response.json())
        if response.status_code == 200:
            return self.__map_workloads_to_model(response.json())
        else:
            raise JiraGetWorkloadFromIssue()

    def __map_workloads_to_model(self, workloads_response: dict) -> list[Workload]:
        """Map workloads in Workload model"""
        worklogs = workloads_response.get("worklogs", [])
        return [Workload(
            id=worklog["id"],
            username=worklog["author"]["displayName"],
            date_started=worklog["started"],
            time_spent_seconds=worklog["timeSpentSeconds"],
            issue_id=worklog["issueId"]
        ) for worklog in worklogs]

    def __map_issues_to_model(self, issue_response: dict) -> list[Issue]:
        """Map issues in Issue model"""
        issues = issue_response.get("issues", [])
        return [Issue(issue["id"], issue["key"]) for issue in issues]
