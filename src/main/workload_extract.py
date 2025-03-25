"""
This module is the main entry point of the program.
"""
import configparser
import logging

from src import ROOT_DIR
from src.main.adapters.jira_adapter import JiraAdapter
from src.main.domain.model.worklogs_component import WorklogsForComponent

# Global project configuration
logger = logging.getLogger(__name__)

# load configuration file
config = configparser.ConfigParser()
config.read(ROOT_DIR + '/configuration.ini')
__jira_username = config['JIRA']['Username']
__jira_api_token = config['JIRA']['Api_token']

# Factory
jira_adapter = JiraAdapter(__jira_username, __jira_api_token)

def main():
    """Main entry point of the program."""
    logger.info('Starting the workload extraction')
    jira_component_name = config['JIRA']['ComponentName']

    jira_issues = jira_adapter.get_issues_for_component(jira_component_name)
    logger.info("Issues ids from component %s: %s", jira_component_name, jira_issues)

    worklogs = WorklogsForComponent(jira_component_name, [])
    for issue in jira_issues.issues:
        logger.info("Loading workload from issue %s", issue)
        issue_worklogs = jira_adapter.get_worklogs_for_issue(issue.id)
        worklogs.extend(issue_worklogs.workloads)
    logger.info("Workloads from component %s: %s", jira_component_name, worklogs)

    logger.info("La liste des issues pour le composant %s est %s",
                jira_component_name, worklogs.get_component_issues())
    logger.info("La liste des worklogs pour le composant %s est %s",
                jira_component_name, worklogs.workloads)
    for username in worklogs.get_usernames():
        user_workloads = worklogs.get_worklogs_for_user(username)
        logger.info("username : %s - %s", username, user_workloads.get_time_spent_group_by_day())

    logger.info('End of the workload extraction')

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
