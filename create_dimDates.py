import pandas as pd
import calendar
import numpy as np
from banking_functions import value_date_modify, date_cols, is_current, all_display
from get_payment_dates import get_salaries


def create_dimDates(source):

    today = pd.to_datetime("today")
    this_year = today.year

    salary = get_salaries(source)

    created_dimDates = pd.DataFrame({"Value Date": pd.date_range('2019-01-01', str(this_year) + '-12-31')})
    created_dimDates["Year"] = created_dimDates['Value Date'].dt.year
    created_dimDates['Month'] = pd.DatetimeIndex(created_dimDates['Value Date']).month
    created_dimDates['YearMonth'] = created_dimDates['Year'].astype(str) + "-" + created_dimDates["Month"].astype(str).str.pad(
        2, fillchar='0')

    try:
        payment_this_month = salary[salary['YearMonth'] == int(str(pd.to_datetime("today").year) +
                                                               str(pd.to_datetime("today").month))]['Payment Date'].iloc[0]
    except:
        payment_this_month = np.nan

    today = value_date_modify(pd.to_datetime("today"), payment_this_month)

    dimDates = pd.merge(created_dimDates, salary, on="YearMonth", how='left')

    # Function to determine new Value Date

    dimDates['ValueDate_Modified'] = dimDates.apply(lambda x:
                                                    value_date_modify(x['Value Date'], x['Payment Date']), axis=1)
    dimDates = date_cols(dimDates, 'ValueDate_Modified')

    dimDates["Day of month"] = pd.DatetimeIndex(dimDates['Value Date']).day
    dimDates["Week"] = dimDates['Value Date'].dt.isocalendar().week

    dimDates["Year"] = dimDates['ValueDate_Modified'].dt.year
    dimDates['Month'] = pd.DatetimeIndex(dimDates['ValueDate_Modified']).month

    dimDates['MonthShort'] = dimDates['Month'].apply(lambda x: calendar.month_abbr[x])
    dimDates['Initial'] = dimDates['MonthShort'].str[0]

    dimDates["Quarter"] = "Q" + dimDates['ValueDate_Modified'].dt.quarter.astype(str)
    dimDates['Month & Year'] = dimDates['MonthShort'].astype(str) + " " + dimDates["Year"].astype(str)
    dimDates['Qtr & Year'] = dimDates['Quarter'].astype(str) + " " + dimDates["Year"].astype(str)

    dimDates['IsCurrentMonth'] = dimDates.apply(lambda x: is_current(x['ValueDate_Modified'], today), axis=1)
    dimDates['AllDisplay'] = dimDates.apply(lambda x: all_display(x['ValueDate_Modified'], today), axis=1)

    return dimDates




