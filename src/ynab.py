
import os
import datetime
import requests
import requests_cache

import typing as t

from model import Statement

requests_cache.install_cache('ynab_cache', backend='sqlite', expire_after=180)


YNAB_API_URL = 'https://api.youneedabudget.com/v1/budgets'
MAX_DAYS_IN_MONTH = 31

YnabId = t.NewType('YnabId', str)
CategoryNameList = t.NewType('CategoryNameList', t.List[str])

        
def get_since_date(months_back: int) -> datetime.datetime:
    """ Determine starting date for transaction query. """

    now = datetime.datetime.now()
    duration = datetime.timedelta(days=months_back*MAX_DAYS_IN_MONTH)
    start_date = now - duration

    return start_date.isoformat()


class YNABClient:
    
    def __init__(self, budget_name: str):
        self.budget_name = budget_name

    def _query(self, endpoint: str = '', data: dict = {}) -> dict:
        res = requests.get(
            url=YNAB_API_URL + endpoint,
            headers={
                'Authorization': f'Bearer {os.environ.get("YNAB_TOKEN")}',
                'Content-Type': 'application/json'
            },
            json=data
        )
        return res.json()

    @property
    def is_authenticated(self) -> bool:
        res_json = self._query(
            endpoint='/user'
        )
        if 'error' in res_json and res_json.get('error').get('id') == '401':
            return False
        
        return True

    def get_statement(self, months_back: int) -> Statement:
        budget_id = self._get_budget_id_from_name()
        data = self._get_transaction_data(
            budget_id=budget_id, 
            months_back=months_back
        )
        return Statement.from_raw(data)

    def _get_budget_id_from_name(self) -> t.Optional[YnabId]:
        res_json = self._query()

        for budget in res_json.get('data').get('budgets'):
            if budget.get('name') == self.budget_name:
                return budget.get('id')

    def _get_transaction_data(self, budget_id: YnabId, months_back: int) -> t.List[dict]:
        res_json = self._query(
            endpoint=f'/{budget_id}/transactions',
            data={
                'since_date': get_since_date(months_back)
            }
        )
        return res_json.get('data')



    