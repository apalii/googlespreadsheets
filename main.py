import sys
import collections
import itertools
# import configparser
import argparse

import pygsheets


# config = configparser.ConfigParser()
# config.read('sheet_robot.conf')
# google_api_key = config.get('credentials', 'google_api_key')

# sheet_id = "1wwudlJi5CxXmA5zjMfkdRSks-BtjBwC035HffJ-WO6I"
# sheet url "https://docs.google.com/spreadsheets/d/1wwudlJi5CxXmA5zjMfkdRSks-BtjBwC035HffJ-WO6I/edit"


def moving_average(data, subset_size):
    divisor = float(subset_size)
    data_iterator = iter(data)
    subset_deque = collections.deque(
        itertools.islice(data_iterator, subset_size)
    )

    if subset_size > len(subset_deque):
        raise ValueError('subset_size must be smaller than data set size')

    yield sum(subset_deque) / divisor
    for elem in data_iterator:
        subset_deque.popleft()
        subset_deque.append(elem)
        yield sum(subset_deque) / divisor

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='GoogleSheetRobot v0', add_help=True)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--spreadsheet", "-s", type=str, help="Spreadsheet id")
    group.add_argument("--link", "-l", type=str, help="Spreadsheet http link")
    parser.add_argument("--debug", action='store_true', help="Debug")
    parsed_args = parser.parse_args()

    google_client = pygsheets.authorize()

    # Open spreadsheet and then worksheet
    try:
        if parsed_args.spreadsheet:
            spreadsheet = google_client.open_by_key(parsed_args.spreadsheet)
        else:
            spreadsheet = google_client.open_by_url(parsed_args.link)
    except Exception as e:
        sys.exit("Spreadsheet not found. Walk on home boy.\n{}".format(e))

    list_of_worksheets = [sheet.title for sheet in spreadsheet.worksheets()]
    # qwe.insert_cols(5, values=['ma', 1,2,3,4,5,6,7])

    for sheet_title in list_of_worksheets:
        worksheet = spreadsheet.worksheet_by_title(sheet_title)
        sheet_values = worksheet.all_values()
        available_columns = sheet_values[0]

        if 'date' not in available_columns or 'visitors' not in available_columns:
            print('Incorrect spreadsheet format')
            break

        visitors_position = available_columns.index('visitors') + 1
        fetched_visitors_list = [
            int(i) for i in worksheet.get_col(visitors_position)[1:]
            ]
        ma = list(moving_average(fetched_visitors_list, 2))
        ma.insert(0, "Moving average")
        # Updating the worksheets with moving average data
        worksheet.insert_cols(len(available_columns), values=ma)
