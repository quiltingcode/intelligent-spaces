# Intelligent Spaces Technical Assessment #

## Cleaned Data

combined_columns variable contains the combined and cleaned data and time field.

completed_plates variable contains the cleaned plate expiry values

cleaned_latitude variable contains the cleaned latitude data

cleaned_longitude variable contains the cleaned longitude data


I have printed to the terminal the total amount of fines issued per make of vehicle for all makes apart from 5. The code is there to run, but it currently errors as the current code is run on the original data and not the cleaned data (see Problems Encountered). The missing makes cause an error as the columns of data have cells containing no data. This issue does not occur with the cleaned data, so once the cleaned data has been updated into the worksheet, I can run the totals again on the updated columns and output the correct results for all makes. 

I have printed to the terminal the average fine amount per agency currently using the original data (see Problems Encountered) and from this data, I have calculated the standard deviation.

## Problems Encountered

1. I have managed to clean all the data. However, I was unable to find the correct code to update the worksheet with this cleaned data. I tried to investigate solutions online, but I wasn't able to resolve the issue. Therefore, I was unable to run the part two challenges on the cleaned data, but you can see that the code is there ready to run on the cleaned data worksheet once I overcome this issue. 

I tried:

cleaned_data_ws.update("R1:R200", [cleaned_latitude])

but this gives me an error message

I tried: 

cleaned_data_ws.update_cells(crange='R2',values = cleaned_latitude)

but crange is not recognised

I tried: 

for row in cleaned_latitude:
    cleaned_data_ws.update('R2:R60', [[row]])

This loops all the data into the worksheet but only through row 1, so it doesn't seem to work it's way down the column. And then eventually, I get an error in the terminal saying that I have reached my daily allowed quota of Google API requests, as i'm only allowed to make 60 udpates per minute, according to Google. I can not overcome this problem with the Google API in the time allotted for this test, so I had to eventually leave the worksheet without it being updated. 

2. As I was unable to update data back to the worksheet, I also didn't manage to append the agency data to the clean data worksheet, which I would have done if I had figured out how to update data back to the worksheet.

## Credits

* I referred back to the Cave of Query portfolio project that I created, when joining two columns of data together; the issue date and issue time columns

* I found this [Stack Overflow](https://stackoverflow.com/questions/21620602/add-leading-zero-python) article to help format the time data, to add missing zeros to make all the times 4 digits and then I added a ':' between each time, before concatenating it with the date

* I've imported date from the datatime library to help format the missing date fields in the Plate Expiry Date column

* I have never used the Pandas library before, but when i'm trying to figure out how to sum one column based on a given condition in another, a lot of search results on google keep pointing me towards the Pandas package, so i'm going to give it a go, following the example on the [includehelp.com site](https://www.includehelp.com/python/how-to-sum-values-in-a-column-that-matches-a-given-condition-using-pandas.aspx)

* I have imported math in order to calculate the square root of the variance.





