import pandas as pd
from banking_functions import give_primary_key


def get_forecasted_spend(banking_path, dimDates):
    scheduled_payments = pd.read_excel(banking_path + 'classified.xlsx', sheet_name = 'forecast')

    forecast = pd.merge(scheduled_payments, dimDates, on="Day of month", how='left')
    forecast = forecast[forecast['Value Date'] > pd.Timestamp.today()]
    forecast = forecast[['Value Date', 'ValueDate_Modified', 'Description', 'Amount', 'Classification', 'INOUT', 'Year',
                         'Month', 'YearMonth']]

    forecast['Type'] = "Forecast"
    forecast['Value Time'] = '00:00'
    forecast['Value Time'] = pd.to_datetime(forecast['Value Time'], format='%H:%M')
    forecast['Beneficiary or Cardholder'] = 'Pending'

    forecast = forecast[['Value Date', 'Value Time', 'ValueDate_Modified', 'YearMonth', 'Year', 'Month', 'Type',
                         'Description', 'Beneficiary or Cardholder', 'Amount', 'Classification', 'INOUT']]
    forecast.sort_values(by=['Value Date'], inplace=True)
    forecast = give_primary_key(forecast)
    forecast['Value Time'] = forecast['Value Time'].dt.strftime('%H:%M')

    return forecast





