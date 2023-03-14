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

""" Single out the data from the Issue Date column """
issue_date_col = list(sheet.col_values(2))
issue_time_col = list(sheet.col_values(3))

combined_columns = {issue_date_col[i] + issue_time_col[i] for i in range(len(issue_date_col))}
print(combined_columns)


