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


""" Remove 00:00:00 time from issue date column """
issue_date_col = list(sheet.col_values(2))
spliced_date = []

for row in issue_date_col:
    spliced_date.append(row[0:11])

# print(spliced_date)

""" Format issue time column """

issue_time_col = list(sheet.col_values(3))

""" Concatenate the two columns together """

combined_columns = {spliced_date[i] + issue_time_col[i] for i in range(len(spliced_date))}
print(combined_columns)





