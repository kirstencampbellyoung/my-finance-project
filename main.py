from ingest_sources import ingest_source_files
from get_payment_dates import get_payment_dates
from banking_functions import value_date_modify, date_cols, give_primary_key
from create_dimDates import create_dimDates
from get_forecasted_spend import get_forecasted_spend
import pandas as pd
import numpy as np

banking_path = '/Users/kirsten.young/Library/CloudStorage/GoogleDrive-kirstencyoung@gmail.com/My Drive/' \
               'My GoogleDrive/5. Finance/Banking/my-finance-project/PowerBi_inputs/'
account_path = '/Users/kirsten.young/Library/CloudStorage/GoogleDrive-kirstencyoung@gmail.com/My Drive/' \
               'My GoogleDrive/5. Finance/Banking/my-finance-project/Raw source files/'

if __name__ == '__main__':
    source = ingest_source_files(account_path)

    source_modified = get_payment_dates(source)

    target = pd.read_excel(banking_path + 'classified.xlsx', sheet_name='classified', skiprows=1)
    target['Beneficiary or Cardholder'].replace(np.nan, '', regex=True, inplace=True)
    target['Value Date'] = pd.to_datetime(target['Value Date'], format='%Y/%m/%d')
    target['ValueDate_Modified'] = pd.to_datetime(target['Value Date'], format='%Y/%m/%d')
    target['PaymentDate'] = pd.to_datetime(target['PaymentDate'], format='%Y/%m/%d')
    target['ValueDate_Modified'] = target.apply(lambda x: value_date_modify(x['Value Date'], x['PaymentDate']), axis=1)
    target['Value Time'] = pd.to_datetime(target['Value Time'], format='%H:%M')
    target = date_cols(target, 'ValueDate_Modified')
    target = give_primary_key(target)
    target.sort_values(by='Value Date', ascending=False)

    # What stays in the target
    keep_from_target = target[target.index.isin(source.index)]
    print("How many records stay in the target: " + str(keep_from_target.shape[0]))

    # What needs to be inserted into target
    inserts_from_source = source[~source.index.isin(target.index)]
    print("How many new records are inserted into the target: " + str(inserts_from_source.shape[0]))

    full_df = pd.concat([inserts_from_source,
                         keep_from_target])  # SQL merge aka upsert the two dfs using index as "merged on" field
    full_df = full_df.sort_values(by=['Value Date', 'Value Time'])

    if source.shape[0] != full_df.shape[0]:
        print("Error with merge: " + str(source.shape[0]) + " records in Source, " + str(
            full_df.shape[0]) + " records in merged.")

    if round(source['Amount'].sum(), 0) != round(full_df['Amount'].sum(), 0):
        print("Amounts not equal")

        print("Source: " + str(round(source['Amount'].sum(), 0)))
        print("Target: " + str(round(full_df['Amount'].sum(), 0)))

    full_df['ValueDate_Modified'] = full_df.apply(
        lambda x: value_date_modify(x['Value Date'], x['PaymentDate']), axis=1)

    full_df['Value Date'] = full_df['Value Date'].dt.strftime('%Y/%m/%d')
    full_df['Value Time'] = full_df['Value Time'].dt.strftime('%H:%M')
    full_df['ValueDate_Modified'] = full_df['ValueDate_Modified'].dt.strftime('%Y/%m/%d')
    full_df['PaymentDate'] = full_df['PaymentDate'].dt.strftime('%Y/%m/%d')

    final_df = full_df[['Value Date', 'Value Time', 'PaymentDate', 'ValueDate_Modified', 'YearMonth', 'Year', 'Month',
                        'Type', 'Account', 'Description', 'Beneficiary or Cardholder', 'Amount', 'Classification',
                        'INOUT']]

    with pd.ExcelWriter(banking_path + "classified.xlsx", engine='openpyxl', date_format='yyyy-mm-dd', mode='a',
                        if_sheet_exists='overlay') as writer:
        final_df.to_excel(writer, sheet_name="classified", startrow=2, header=False)
        print("Records exported to excel.")

    dimDates = create_dimDates(source)
    dimDates.to_csv(banking_path + 'dimDates.csv')

    forecast = get_forecasted_spend(banking_path, dimDates)
    forecast.to_csv(banking_path + 'forecast.csv')
    