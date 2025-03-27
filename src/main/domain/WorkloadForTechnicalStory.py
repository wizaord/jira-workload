"""
This class is responsible for managing the worklogs for a technical story.
"""
import logging
from datetime import date

from src.main.adapters.csv_adapter import CsvAdapter
from src.main.adapters.jira_adapter import JiraAdapter

logger = logging.getLogger(__name__)

class WorklogsForTechnicalStory:
    """Class that contains function to extract worklogs for a technical story"""

    def __init__(self, jira_adapter: JiraAdapter, csv_adapter: CsvAdapter):
        self.jira_adapter = jira_adapter
        self.csv_adapter = csv_adapter

    def extract_workloads_group_by_user_date_ts_in_csv_file(self, date_limit: date):
        technical_stories = self.jira_adapter.get_technical_stories()
        logger.info("technical_stories %s", technical_stories)

        users_with_worklogs = technical_stories.get_all_distinct_worklogs_user_emails()
        for user_email in users_with_worklogs:
            technical_story_for_user = technical_stories.filter_for_user(user_email)
            for technical_story in technical_story_for_user.issues:
                spent_time_on_issue = technical_story.get_worklogs_from_issue_and_sub_issues().get_spent_time_group_by_day()
                for day, time_spent in spent_time_on_issue.items():
                    logger.info("user <%s> - Parent <%s> - TS <%s> - day <%s> - time_spent <%s>", user_email, technical_story.parent.title, technical_story.title, day, time_spent)
