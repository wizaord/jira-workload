"""
This class is responsible for managing the worklogs for a user.
"""
import logging
from datetime import date

from src.main.adapters.csv_adapter import CsvAdapter
from src.main.adapters.jira_adapter import JiraAdapter
from src.main.domain.model.worklogs_user import WorklogsForUser

logger = logging.getLogger(__name__)

class WorklogsForUserService:
    """Class that exposer services for worklogs for a user"""

    def __init__(self, jira_adapter: JiraAdapter, csv_adapter: CsvAdapter):
        self.jira_adapter = jira_adapter
        self.csv_adapter = csv_adapter

    def __extract_workload_for_user(self, username: str, limit_date: date) -> WorklogsForUser:
        """Main entry point of the program."""
        logger.info('Starting the workload extraction for user %s until %s', username, limit_date)

        issues_for_user = self.jira_adapter.get_issues_where_user_has_worked_on_it(username)

        logger.info("User %s has worked on %d issues", username, issues_for_user.count_issues())

        user_workloads = WorklogsForUser(username, [])
        for issue in issues_for_user.issues:
            logger.info("Fetching worklogs for issue %s", issue.key)
            issue_workloads = self.jira_adapter.get_user_worklogs_for_issue(issue.id, username)
            user_workloads.append_worklogs(issue_workloads)

        user_workloads.remove_worklogs_before_date(limit_date)
        return user_workloads

    def extract_workloads_for_user_and_save_in_csv_file(self, users_email: list[str], limit_date: date):
        headers = ["user_email", "date", "time_spent_in_minutes"]
        worklogs_dict_list = []

        for user_email in users_email:
            user_workload = self.__extract_workload_for_user(user_email, limit_date)
            for day, time_spent in user_workload.get_time_spent_group_by_day().items():
                worklogs_dict_list.append(
                    {
                        'user_email': user_workload.username,
                        'date': day,
                        'time_spent_in_minutes': time_spent
                    }
        )
        self.csv_adapter.write(headers, worklogs_dict_list)
