#!/usr/bin/python
import sys
import argparse

import pygsheets

from calculations.statistics import moving_average

if not len(sys.argv) == 1:
    parser = argparse.ArgumentParser(description='GoogleSheetRobot v1.1', add_help=True)
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

    for sheet_title in list_of_worksheets:

        worksheet = spreadsheet.worksheet_by_title(sheet_title)
        sheet_values = worksheet.all_values()
        available_columns = sheet_values[0]

        if 'date' not in available_columns or 'visitors' not in available_columns:
            print('{} worksheet has incorrect spreadsheet. Skipping...'.format(sheet_title))
            break

        visitors_position = available_columns.index('visitors') + 1
        fetched_visitors_list = [
            int(i) for i in worksheet.get_col(visitors_position)[1:]
            ]
        ma = list(moving_average(fetched_visitors_list, 2))
        ma.insert(0, "Moving average")
        # Adding moving average column to the worksheet
        worksheet.insert_cols(len(available_columns), values=ma)
else:
    print('Use --help for more detail')
