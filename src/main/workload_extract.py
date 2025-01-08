import configparser
import logging

from src import ROOT_DIR
from src.main.adapters.jira import JiraAdapter

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

    jira_issues = jira_adapter.get_issues_from_components(jira_component_name)
    logger.info("Issues ids from component %s: %s", jira_component_name, jira_issues)

    worklogs = []
    for issue in jira_issues:
        logger.info("Loading workload from issue %s", issue)
        issue_worklogs = jira_adapter.get_worklogs_from_issue(issue.id)
        worklogs.extend(issue_worklogs)
    logger.info("Workloads from component %s: %s", jira_component_name, worklogs)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
