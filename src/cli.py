import sys
import click
import configparser
from collections import defaultdict

from ynab import YNABClient
from organize import organize_ynab_statement_data
from sheet import Worksheet


def load_config(config_name: str):
    config = configparser.ConfigParser(allow_no_value=True)
    config.optionxform=str
    config.read(config_name)

    return config


@click.command()
@click.option('-m', '--months', help='Months of Data.', type=int, required=True)
def cli(months):
    config = load_config('config.ini')

    ynab = YNABClient(budget_name=config['budget']['name'])
    if not ynab.is_authenticated:
        sys.exit('ERROR: No valid YNAB_TOKEN environment variable set')

    organized_statement_data = organize_ynab_statement_data(
        statement=ynab.get_statement(months_back=months),
        categories={
            'monthly': config['monthly'].keys(),
            'yearly': config['yearly'].keys(),
            'grouped': config['yearly'].keys()
        }
    )

    print(len(organized_statement_data))

