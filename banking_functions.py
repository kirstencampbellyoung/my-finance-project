#!/usr/bin/env python
# coding: utf-8


from dateutil.relativedelta import relativedelta
from datetime import datetime
import pandas as pd

banking_path = '/Users/kirsten.young/Library/CloudStorage/GoogleDrive-kirstencyoung@gmail.com/My Drive/' \
               'My GoogleDrive/5. Finance/Banking/my-finance-project/'


def give_primary_key(df):
    merge_on_fields: [list] = ["PrimaryKey"]

    df['PrimaryKey'] = df['Value Date'].dt.strftime("%Y-%m-%d") + df['Value Time'].dt.strftime('%H:%M') + \
                       df['Description'].str.strip().astype(str) + df['Beneficiary or Cardholder'] + \
                       df['Amount'].astype(str)
    df['PrimaryKey'] = df['PrimaryKey'].replace(to_replace="\.0+$", value="", regex=True)

    try:
        df.set_index(merge_on_fields, drop=True, append=False, inplace=True, verify_integrity=True)
    except:
        df.set_index(merge_on_fields, drop=True, append=False, inplace=True, verify_integrity=False)

    return df


def is_current(date, today):
    if date.month == today.month and date.year == today.year and date.day <= 25:
        return True
    else:
        return False


def all_display(date, today):
    if date.month == today.month and date.year == today.year and date.day <= 25:
        return True
    elif date <= today:
        return True
    else:
        return False


def date_cols(df, date_col):
    # Get new cols
    df['Year'] = df[date_col].dt.year
    df['Month'] = df[date_col].dt.month
    df['YearMonth'] = df['Year'].astype(str) + "-" + df['Month'].astype(str).str.pad(2, fillchar='0')
    return df


def value_date_modify(value_date, payment_date):
    # print("Value Date: " + str(value_date))
    # print("Payment Date: " + str(payment_date))

    if pd.isna(payment_date):
        ValueDate_Modified = value_date
    elif value_date < payment_date:
        ValueDate_Modified = value_date
    else:
        ValueDate_Modified = value_date + relativedelta(months=1)
        ValueDate_Modified = str(ValueDate_Modified.year) + '-' + str(ValueDate_Modified.month) + '-' + '01'
        ValueDate_Modified = datetime.strptime(ValueDate_Modified, '%Y-%m-%d')

    return ValueDate_Modified
