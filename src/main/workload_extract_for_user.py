"""
Main entry to extract workload for a specific user
"""
import configparser
import logging
from datetime import date

from src import ROOT_DIR
from src.main.adapters.csv_adapter import CsvAdapter
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
csv_adapter = CsvAdapter("workload.csv")

def extract_workload_for_user(username: str, limit_date: date) -> WorklogsForUser:
    """Main entry point of the program."""
    logger.info('Starting the workload extraction for user %s until %s', username, limit_date)

    issues_for_user = jira_adapter.get_issues_where_user_has_worked_on_it(username)

    logger.info("User %s has worked on %d issues", username, issues_for_user.count_issues())

    user_workloads = WorklogsForUser(username, [])
    for issue in issues_for_user.issues:
        logger.info("Fetching worklogs for issue %s", issue.key)
        issue_workloads = jira_adapter.get_user_worklogs_for_issue(issue.id, username)
        user_workloads.append_worklogs(issue_workloads)

    user_workloads.remove_worklogs_before_date(limit_date)
    return user_workloads

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    user_workload = extract_workload_for_user("c.guegnon@seiitra.com", date.today())

    headers = ["user_email", "date", "time_spent_in_minutes"]
    worklogs_dict_list = [
        {
            'user_email': user_workload.username,
            'date': worklog.date_started.date(),
            'time_spent_in_minutes': worklog.time_spent_minutes
        }
        for worklog in user_workload.workloads
    ]
    csv_adapter.write(headers, worklogs_dict_list)
    # extract_workload_for_user("d.simonazzi@seiitra.com")
