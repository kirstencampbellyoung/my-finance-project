import pandas as pd
import numpy as np
from banking_functions import give_primary_key
from banking_functions import date_cols


accounts_path = '/Users/kirsten.young/Library/CloudStorage/GoogleDrive-kirstencyoung@gmail.com/My Drive/' \
                'My GoogleDrive/5. Finance/Banking/Accounts/'


CreditCard = pd.read_excel(accounts_path + '112_Credit Card.xlsx', dtype=object)
CreditCard['Value Date'] = pd.to_datetime(CreditCard['Value Date'], format='%Y-%m-%d')
CreditCard['Account'] = 'CreditCard'
CreditCard['Amount'].sum()


KirstSurance = pd.read_excel(accounts_path + '109_Kirst-Surance.xlsx')
KirstSurance['Account'] = 'KirstSurance'
KirstSurance['Amount'].sum()


Debit = pd.read_excel(accounts_path + '151_Subscriptions.xlsx')
Debit['Value Date'] = pd.to_datetime(Debit['Value Date'], format='%Y-%m-%d')
DebitCard = Debit[Debit['Value Date'] <= '2022-12-17'].copy()
DebitCard['Account'] = 'DebitCard'
DebitCard['Amount'].sum()


Subscriptions = Debit[Debit['Value Date'] > '2022-12-17'].copy()
Subscriptions['Account'] = 'Subscriptions'
Subscriptions['Amount'].sum()


NoticeSavings = pd.read_excel(accounts_path + '181_Notice Savings.xlsx')
NoticeSavings['Account'] = 'NoticeSavings'
NoticeSavings['Amount'].sum()


TravelFund = pd.read_excel(accounts_path + '194_Travel fund.xlsx')
TravelFund['Account'] = 'TravelAccount'
TravelFund['Amount'].sum()


WhiskenHousehold = pd.read_excel(accounts_path + '146_WhiskenHousehold.xlsx')
WhiskenHousehold['Account'] = 'WhiskenHousehold'
WhiskenHousehold['Amount'].sum()


# Merge all datasets together
source = pd.concat([CreditCard, KirstSurance, DebitCard, Subscriptions, NoticeSavings, TravelFund, WhiskenHousehold],
                   axis=0)

# Convert Dates and times
source['Value Date'] = pd.to_datetime(source['Value Date'], format='%Y-%m-%d')
source['Value Time'] = pd.to_datetime(source['Value Time'], format='%H:%M:%S')

# Fix
source['Beneficiary or Cardholder'].replace(np.nan, '', regex=True, inplace=True)

source = give_primary_key(source)

# Combine 'duplicate' rows into 1

source = source.groupby(['PrimaryKey']).agg({
                        'Value Date': 'max',
                        'Value Time': 'max',
                        'Type': 'max',
                        'Account': 'max',
                        'Description': 'max',
                        'Beneficiary or Cardholder': 'max',
                        'Amount': 'sum'}).reset_index()

# Add an index agian
source = give_primary_key(source)
source = date_cols(source, 'Value Date')
print(source)
