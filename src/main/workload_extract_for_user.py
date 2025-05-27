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
csv_adapter = CsvAdapter("workload.csv")


def main(user=None, date_debut=None, date_fin=None):
    if user is None:
        raise ValueError("Le paramètre 'user' ne peut pas être None.")
        # Create the CSV file name with the current date
    if date_debut is None:
        logger.info("Pas de date de début sélectionnée, on prend le Jour J - 2 semaines")
        date_debut = date.today() - timedelta(weeks=2)
    if date_fin is None:
        logger.info("Pas de date de fin sélectionnée, on prend le jour J")
        date_fin = date.today()
    today = date.today()
    csv_file_name = f"workload_user_{user}_epic_ts_day_{today.strftime('%Y-%m-%d')}.csv"
    csv_adapter = CsvAdapter(csv_file_name)

    service = WorklogsForTechnicalStory(jira_adapter, csv_adapter)
    service.extract_workloads_group_by_user_date_ts_in_csv_file(user, date_debut, date_fin)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
