"""
This class is responsible for managing the worklogs for a technical story.
"""
import json
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

        logger.info("%s", technical_stories.get_all_worklogs())
