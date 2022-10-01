from model import Statement


def organize_ynab_statement_data(statement: Statement, categories:dict) -> dict:

    for entry in statement:
        print(entry)


    return {}