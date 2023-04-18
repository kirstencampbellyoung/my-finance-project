from banking_functions import value_date_modify, date_cols
import pandas as pd


def get_payment_dates(source):
    salary_descriptions = ['CASHFOCUS SALARIS / SALARY', 'PRICE WATEPWC T842', 'PRICE WATEPWC T843']

    salary = source[source['Description'].isin(salary_descriptions)]
    salary = salary[['YearMonth', 'Value Date']]

    salary.rename(columns={'Value Date': 'Payment Date'}, inplace=True)

    source_modified = pd.merge(source, salary, on="YearMonth", how='left').set_axis(source.index)

    # Function to determine new Value Date

    source_modified['ValueDate_Modified'] = source_modified.apply(lambda x: value_date_modify(x['Value Date'], x['Payment Date']), axis=1)

    source_modified = date_cols(source_modified, 'ValueDate_Modified')

    return source_modified



