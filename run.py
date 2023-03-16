import gspread
from google.oauth2.service_account import Credentials
from datetime import date
import pandas as pd


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
        data = 'none'
        cleaned_expiry_dates.append(data)
    else:
        cleaned_expiry_dates.append(data)


for plate in plate_expiry_date_col:
    clean_expiry_dates(plate)


"""
Add a '-' divider symbol between the year and the month
"""

cleaned_expiry_dates = [f"{el[:4]}-{el[4:]}" for el in cleaned_expiry_dates]


"""
Add a '-' divider symbol and then the last day of the month, 30, 31 or 28
depending on the month of expiry
"""

completed_plates = []
length_plates = len(completed_plates)


# 30 day months
april = '-04'
june = '-06'
sept = '-09'
nov = '-11'

#31 day months
jan = '-01'
mar = '-03'
may = '-05'
july = '-07'
aug = '-08'
oct = '-10'
dec = '-12'

#odd dates
feb = '-02'
auto_date = '--'

for plate in cleaned_expiry_dates:
    if april in plate:
        new_30_plate = f"{plate}-30"
        completed_plates.append(new_30_plate)
    elif jan in plate:
        new_31_plate = f"{plate}-31"
        completed_plates.append(new_31_plate)
    elif feb in plate:
        new_feb_plate = f"{plate}-28"
        completed_plates.append(new_feb_plate)
    elif mar in plate:
        new_mar_plate = f"{plate}-31"
        completed_plates.append(new_mar_plate)
    elif may in plate:
        new_may_plate = f"{plate}-31"
        completed_plates.append(new_may_plate)
    elif june in plate:
        new_june_plate = f"{plate}-30"
        completed_plates.append(new_june_plate)
    elif july in plate:
        new_july_plate = f"{plate}-31"
        completed_plates.append(new_july_plate)
    elif aug in plate:
        new_aug_plate = f"{plate}-31"
        completed_plates.append(new_aug_plate)
    elif sept in plate:
        new_sept_plate = f"{plate}-30"
        completed_plates.append(new_sept_plate)
    elif oct in plate:
        new_oct_plate = f"{plate}-31"
        completed_plates.append(new_oct_plate)
    elif nov in plate:
        new_nov_plate = f"{plate}-30"
        completed_plates.append(new_nov_plate)
    elif dec in plate:
        new_dec_plate = f"{plate}-31"
        completed_plates.append(new_dec_plate)
    else:
        completed_plates.append(plate)


# print(completed_plates)



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

# print(formatted_nums)
sum_fines = sum(map(int, formatted_nums))

# print(f"The total of fines issued per year is {sum_fines}")


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

# print(cleaned_makes)

d = sheet.get_all_records()
df = pd.DataFrame(d)

print('Fine amount per make of vehicle')
print('_____________________________________________________')

# acur_total = df.loc[df['Make'] == 'ACUR', 'Fine amount'].sum()
# print("Total ACUR fines:", acur_total)

gmc_total = df.loc[df['Make'] == 'GMC', 'Fine amount'].sum()
print("Total GMC fines:", gmc_total)

bmw_total = df.loc[df['Make'] == 'BMW', 'Fine amount'].sum()
print("Total BMW fines:", bmw_total)

cadi_total = df.loc[df['Make'] == 'CADI', 'Fine amount'].sum()
print("Total CADI fines:", cadi_total)

# chev_total = df.loc[df['Make'] == 'CHEV', 'Fine amount'].sum()
# print("Total CHEV fines:", chev_total)

chry_total = df.loc[df['Make'] == 'CHRY', 'Fine amount'].sum()
print("Total CHRY fines:", chry_total)

dodg_total = df.loc[df['Make'] == 'DODG', 'Fine amount'].sum()
print("Total DODG fines:", dodg_total)

# ford_total = df.loc[df['Make'] == 'FORD', 'Fine amount'].sum()
# print("Total FORD fines:", ford_total)

frei_total = df.loc[df['Make'] == 'FREI', 'Fine amount'].sum()
print("Total FREI fines:", frei_total)

hino_total = df.loc[df['Make'] == 'HINO', 'Fine amount'].sum()
print("Total HINO fines:", hino_total)

hond_total = df.loc[df['Make'] == 'HOND', 'Fine amount'].sum()
print("Total HOND fines:", hond_total)

hyun_total = df.loc[df['Make'] == 'HYUN', 'Fine amount'].sum()
print("Total HYUN fines:", hyun_total)

infi_total = df.loc[df['Make'] == 'INFI', 'Fine amount'].sum()
print("Total INFI fines:", infi_total)

jeep_total = df.loc[df['Make'] == 'JEEP', 'Fine amount'].sum()
print("Total JEEP fines:", jeep_total)

kia_total = df.loc[df['Make'] == 'KIA', 'Fine amount'].sum()
print("Total KIA fines:", kia_total)

kw_total = df.loc[df['Make'] == 'KW', 'Fine amount'].sum()
print("Total KW fines:", kw_total)

linc_total = df.loc[df['Make'] == 'LINC', 'Fine amount'].sum()
print("Total LINC fines:", linc_total)

lind_total = df.loc[df['Make'] == 'LIND', 'Fine amount'].sum()
print("Total LIND fines:", lind_total)

lrov_total = df.loc[df['Make'] == 'LROV', 'Fine amount'].sum()
print("Total LROV fines:", lrov_total)

mase_total = df.loc[df['Make'] == 'MASE', 'Fine amount'].sum()
print("Total MASE fines:", mase_total)

mazd_total = df.loc[df['Make'] == 'MAZD', 'Fine amount'].sum()
print("Total MAZD fines:", mazd_total)

mbnz_total = df.loc[df['Make'] == 'MBNZ', 'Fine amount'].sum()
print("Total MBNZ fines:", mbnz_total)

merc_total = df.loc[df['Make'] == 'MERC', 'Fine amount'].sum()
print("Total MERC fines:", merc_total)

mits_total = df.loc[df['Make'] == 'MITS', 'Fine amount'].sum()
print("Total MITS fines:", mits_total)

# niss_total = df.loc[df['Make'] == 'NISS', 'Fine amount'].sum()
# print("Total NISS fines:", niss_total)

olds_total = df.loc[df['Make'] == 'OLDS', 'Fine amount'].sum()
print("Total OLDS fines:", olds_total)

pont_total = df.loc[df['Make'] == 'PONT', 'Fine amount'].sum()
print("Total PONT fines:", pont_total)

ptrb_total = df.loc[df['Make'] == 'PTRB', 'Fine amount'].sum()
print("Total PTRB fines:", ptrb_total)

scio_total = df.loc[df['Make'] == 'SCIO', 'Fine amount'].sum()
print("Total SCIO fines:", scio_total)

suba_total = df.loc[df['Make'] == 'SUBA', 'Fine amount'].sum()
print("Total SUBA fines:", suba_total)

tesl_total = df.loc[df['Make'] == 'TESL', 'Fine amount'].sum()
print("Total TESL fines:", tesl_total)

# toyo_total = df.loc[df['Make'] == 'TOYO', 'Fine amount'].sum()
# print("Total TOYO fines:", toyo_total)

volk_total = df.loc[df['Make'] == 'VOLK', 'Fine amount'].sum()
print("Total VOLK fines:", volk_total)

volv_total = df.loc[df['Make'] == 'VOLV', 'Fine amount'].sum()
print("Total VOLV fines:", volv_total)

print('_____________________________________________________')

print('Fine amount per agency')
print('_____________________________________________________')

agency_1_total = df.loc[df['Agency'] == 1, 'Fine amount'].sum()
print("Total Agency 1 fines:", agency_1_total)

# agency_2_total = df.loc[df['Agency'] == 2, 'Fine amount'].sum()
# print("Total Agency 2 fines:", agency_2_total)

# agency_11_total = df.loc[df['Agency'] == 11, 'Fine amount'].sum()
# print("Total Agency 11 fines:", agency_11_total)

agency_34_total = df.loc[df['Agency'] == 34, 'Fine amount'].sum()
print("Total Agency 34 fines:", agency_34_total)

agency_36_total = df.loc[df['Agency'] == 36, 'Fine amount'].sum()
print("Total Agency 36 fines:", agency_36_total)

agency_54_total = df.loc[df['Agency'] == 54, 'Fine amount'].sum()
print("Total Agency 54 fines:", agency_54_total)

print('_____________________________________________________')

average_fine_per_agency = (sum_fines // 6)
print(f"Average fine amount per agency is ${average_fine_per_agency}")

print('_____________________________________________________')
print('Standard Deviation')
print('_____________________________________________________')

agency_1_deviation = ((agency_1_total - average_fine_per_agency) ** 2)
agency_34_deviation = ((agency_34_total - average_fine_per_agency) ** 2)
agency_36_deviation = ((agency_36_total - average_fine_per_agency) ** 2)
agency_54_deviation = ((agency_54_total - average_fine_per_agency) ** 2)

# deviations = sum(agency_1_deviation + agency_34_deviation + agency_36_deviation + agency_54_deviation)
# print(deviations)




cleaned_data_ws = SHEET.worksheet('cleaned_data')

# for row in cleaned_latitude:
#     cleaned_data_ws.update('R2:R60', [[row]])


# cleaned_data_ws.update_cells(crange='R2',values = cleaned_latitude)

# print(cleaned_latitude)

# s_range = SHEET.worksheet("citations").get("A1:W200")
# new_worksheet = SHEET.add_worksheet(title="COPY of citations", 
#     rows=len(s_range), cols=len(s_range[0]))

# cleaned_data_ws.update("A1:A200", [cleaned_latitude])

"""
Part 2
Challenge 2 - Average and Standard Deviation of the fine amount per year per agency
"""
