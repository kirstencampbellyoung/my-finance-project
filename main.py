# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from ingest_sources import ingest_source_files
from get_payment_dates import get_payment_dates
# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    source = ingest_source_files('/Users/kirsten.young/Library/CloudStorage/GoogleDrive-kirstencyoung@gmail.com/My Drive/' \
                        'My GoogleDrive/5. Finance/Banking/Accounts/')

    source_modified = get_payment_dates(source)

    print(source_modified.head())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
