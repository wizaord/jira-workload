import configparser
import json
import logging
from dataclasses import asdict

from src import ROOT_DIR
from src.main.adapters.jira_adapter import JiraAdapter
from src.main.model.worklogs_user import WorklogsForUser

# Global project configuration
logger = logging.getLogger(__name__)

# load configuration file
config = configparser.ConfigParser()
config.read(ROOT_DIR + '/configuration.ini')
__jira_username = config['JIRA']['Username']
__jira_api_token = config['JIRA']['Api_token']

# Factory
jira_adapter = JiraAdapter(__jira_username, __jira_api_token)

def extract_workload_for_user(username: str):
    """Main entry point of the program."""
    logger.info('Starting the workload extraction for user %s', username)

    issues_for_user = jira_adapter.get_issues_where_user_has_worked_on_it(username)

    logger.info("User %s has worked on issues: %s", username, json.dumps(asdict(issues_for_user), indent=2, default=str))
    user_global_worklogs = WorklogsForUser(username, [])
    for issue in issues_for_user.issues:
        logger.info("Fetching worklogs for issue %s", issue.key)
        user_global_worklogs.append_worklogs(jira_adapter.get_user_worklogs_for_issue(issue.id, username).workloads)

    spent_time_by_day = user_global_worklogs.get_time_spent_group_by_day()
    for day, time_spent in spent_time_by_day.items():
        logger.info("User %s has spent %s minutes on %s", username, time_spent, day)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    extract_workload_for_user("c.guegnon@seiitra.com")
    # extract_workload_for_user("d.simonazzi@seiitra.com")
