import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

def load_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(path, parse_dates=['date', 'createdDate', 'changedDate'])
    data['income'] = data['income'].str.replace(',', '.').astype(float)
    data['outcome'] = data['outcome'].str.replace(',', '.').astype(float)
    return data

def divide_into_categories(data: pd.DataFrame) -> dict[str : pd.DataFrame]:
    required_columns = ['date', 'categoryName', 'payee', 'comment', 'createdDate', 'changedDate']
    income_columns = ['incomeAccountName', 'income', 'incomeCurrencyShortTitle']
    outcome_columns = ['outcomeAccountName', 'outcome', 'outcomeCurrencyShortTitle']

    # Выделяем таблицу incomes для информации о доходах
    incomes = data[(data['income'].isna() == False) & (data['outcome'].isna() == True)][required_columns + income_columns].reset_index(drop=True)
    
    # Выделяем таблицу outcomes для информации о расходах
    outcomes = data[(data['income'].isna() == True) & (data['outcome'].isna() == False)][required_columns + outcome_columns].reset_index(drop=True)
    
    # В таблице transfers храним все переводы между счетами
    transfers = data[(data['income'].isna() == False) & (data['outcome'].isna() == False)]

    # В таблице debts храним информацию о всех долгах, которые я давал/брал
    debts = transfers[transfers['outcomeAccountName'] == 'Долги']
    transfers = transfers[transfers['outcomeAccountName'] != 'Долги']
    return {
        'incomes' : incomes, 
        'outcomes' : outcomes, 
        'transfers' : transfers,
        'debts' : debts
        }

if __name__ == '__main__':
    PATH = './data/raw/money.csv'

    datasets = divide_into_categories(load_data(PATH))
    for name, table in tqdm(datasets.items()):
        table.to_csv(f'./data/prepared/{name}.csv', index = False)