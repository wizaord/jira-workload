"""
Main entry to extract workload for a specific user
"""
import configparser
import logging
from datetime import date

from src import ROOT_DIR
from src.main.adapters.csv_adapter import CsvAdapter
from src.main.adapters.jira_adapter import JiraAdapter
from src.main.domain.WorkloadForUserService import WorklogsForUserService

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

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    service = WorklogsForUserService(jira_adapter, csv_adapter)
    service.extract_workloads_for_user_and_save_in_csv_file("c.guegnon@seiitra.com", date.today())
