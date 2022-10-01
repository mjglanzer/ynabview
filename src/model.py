from dataclasses import dataclass

import typing as t


@dataclass
class Transaction:
    date: str
    category: str
    payee: str
    memo: str
    amount: int

    @classmethod
    def from_raw(cls, raw):
        return cls(
            date=raw.get('date'),
            category=raw.get('category_name'),
            payee=raw.get('payee_name'),
            memo=raw.get('memo'),
            amount=raw.get('amount'),
        )

    @property
    def formatted_amount(self) -> float:
        return float(str(self.amount)[:-3] + '.' + str(self.amount)[-3:])


class Statement:
    def __init__(self, transactions: t.List[Transaction]):
        self.transactions = transactions

    @classmethod
    def from_raw(cls, response_data: list):
        transactions = []
        for t in response_data.get('transactions'):
            if t.get('subtransactions'):

                for subt in t.get('subtransactions'):
                    subt['date'] = t.get('date')
                    subt['payee_name'] = t.get('payee_name')
                    transactions.append(Transaction.from_raw(subt))
            else:
                transactions.append(Transaction.from_raw(t))

        return cls(transactions)

    def __getitem__(self, i) -> Transaction:
        return self.transactions[i]

    def __len__(self) -> int:
        return len(self.transactions)
