"""
Main entry to extract workload for a specific user
"""
import configparser
import logging
from datetime import date, timedelta

from src import ROOT_DIR
from src.main.adapters.csv_adapter import CsvAdapter
from src.main.adapters.jira_adapter import JiraAdapter
from src.main.domain.WorkloadForTechnicalStory import WorklogsForTechnicalStory

# Global project configuration
logger = logging.getLogger(__name__)

# load configuration file
config = configparser.ConfigParser()
config.read(ROOT_DIR + '/configuration.ini')
__jira_username = config['JIRA']['Username']
__jira_api_token = config['JIRA']['Api_token']

# Factory
jira_adapter = JiraAdapter(__jira_username, __jira_api_token)

today = date.today()
csv_file_name = f"workload_user_epic_ts_day_{today.strftime('%Y-%m-%d')}.csv"
csv_adapter = CsvAdapter(csv_file_name)


def main():
    service = WorklogsForTechnicalStory(jira_adapter, csv_adapter)
    date_limit = date.today() - timedelta(weeks=1)
    service.extract_workloads_group_by_user_date_ts_in_csv_file(date_limit)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
