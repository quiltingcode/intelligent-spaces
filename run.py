import gspread
from google.oauth2.service_account import Credentials
from datetime import date

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
citations = sheet.get_all_records()


# def update_worksheet(data):
#     """
#     Upload the cleaned data back into the citations worksheet
#     """
#     cleaned_data_ws = GSPREAD_CLIENT.open('intelligent-spaces-test').sheet1
#     cleaned_data_ws.append_col(data)


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
    """
    If the time field is only 2 or 3 characters long, zeros are inserted to make
    it a four digit character, ready for formatting with a ':'
    """

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
# print(combined_columns)


""" Challenge 2 - Convert the plate expiry value into a date value with the day as the last day of the month """

plate_expiry_date_col = list(sheet.col_values(7))

cleaned_expiry_dates = []

today = date.today()
set_date_format = today.strftime("%Y-%m-%d")


def clean_expiry_dates(data):
    """
    If no date exists, set expiry as today's date
    """
    if data == "":
        data = set_date_format
        cleaned_expiry_dates.append(data)
    else:
        cleaned_expiry_dates.append(data)


for plate in plate_expiry_date_col:
    clean_expiry_dates(plate)

print(cleaned_expiry_dates)

# cleaned_expiry_dates = [f"{el[:4]}-{el[2:]}-{el[2:]}" for el in cleaned_expiry_dates]

# print(cleaned_expiry_dates)


""" Challenge 3 - Convert invalid latitude and longitude values into none values (rather than the current magic 
numbers) """

latitude_col = list(sheet.col_values(18))
longitude_col = list(sheet.col_values(19))
cleaned_latitude = []
cleaned_longitude = []


def clean_latitude(data):
    """ 
    Convert latitudes of '99999' to 'none'
    """
    if data == '99999':
        data = 'none'
        cleaned_latitude.append(data)
    else:
        cleaned_latitude.append(data)


def clean_longitude(data):
    """ 
    Convert longitudes of '99999' to 'none'
    """
    if data == '99999':
        data = 'none'
        cleaned_longitude.append(data)
    else:
        cleaned_longitude.append(data)


for row in latitude_col:
    clean_latitude(row)

for row in longitude_col:
    clean_longitude(row)


# update_worksheet(cleaned_latitude)

"""
Challenge 4 - An additional crib sheet provides the agency names that match the Agency ID in 
the data. Extend the data set to hold both the ID and the name of the agency.
"""



"""
Part 2
Challenge 1 - Total of fines issues per year per make of vehicle
"""


fine_amount_col = sheet.col_values(17)
fine_without_header = fine_amount_col[1:]

formatted_nums = []


def remove_empty_str(data):
    """
    If the fine field is an empty string, zeros are inserted to make
    it a one digit character, ready for summing
    """

    if len(data) < 1:
        new_num = str(data.zfill(1))
        formatted_nums.append(new_num)
    else:
        formatted_nums.append(data)


for row in fine_without_header:
    remove_empty_str(row)

sum_fines = sum(map(int, formatted_nums))

print(f"The total of fines issued per year is {sum_fines}")


veh_make_col = sheet.col_values(9)
makes_without_header = veh_make_col[1:]

cleaned_makes = []


def clean_makes(data):
    """ 
    Convert makes of '' to 'none'
    """
    if data == '':
        data = 'none'
        cleaned_makes.append(data)
    else:
        cleaned_makes.append(data)


for row in makes_without_header:
    clean_makes(row)



""" make a dictionary of makes with fine amount """

make_fines_dict = {cleaned_makes[i]: formatted_nums[i] for i in range(len(cleaned_makes))}

# print(make_fines_dict)



