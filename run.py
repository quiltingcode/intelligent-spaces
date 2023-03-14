import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('intelligent-spaces-test')


""" Check the data can be read through the API """
sheet = GSPREAD_CLIENT.open('intelligent-spaces-test').sheet1
data = sheet.get_all_records()

""" Challenge 1 - Combine the Issue Date and Issue time into a single Issue Date Time value """


""" Remove 00:00:00 time from issue date column """
issue_date_col = list(sheet.col_values(2))
spliced_date = []

for row in issue_date_col:
    spliced_date.append(row[0:11])


""" Format issue time column """

issue_time_col = list(sheet.col_values(3))

formatted_times = []


def make_four_digits(data):

    if len(data) <= 3:
        new_time = str(data.zfill(4))
        formatted_times.append(new_time)
    else:
        formatted_times.append(data)


for row in issue_time_col:
    make_four_digits(row)


formatted_times = [f"{el[:2]}:{el[2:]}" for el in formatted_times]


""" Concatenate the two columns together """

combined_columns = {spliced_date[i] + formatted_times[i] for i in range(len(spliced_date))}
print(combined_columns)


""" Challenge 2 - Convert the plate expiry value into a date value with the day as the last day of the month """


