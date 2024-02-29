Report Superpy Miranda Little
To have the program have an internal idea of the current date, the date was saved in a text file in the format DD/MM/YY. Then this string was turned into a datetime object using the following code:

def todays_date():
    with open('date.txt', 'r', newline='') as file:
        string = file.read()
        todays_date = datetime.strptime(string, '%d/%m/%y').date()
The "strptime" method takes the string from the text file and turns it into a datetime object, called todays_date. This object can be used to advance the date by using the timedelta class, where 'days' is the number of days that the user input.

def advance_time(days):
    date = todays_date()
    new_date = date + timedelta(days=days)
    with open('date.txt', 'w', newline='') as file:
        file.write(string)
    print('OK')   
The date text file is opened again and the old date is overwritten by the new date.

To get the total revenue or profit for a particular month, slicing is used to get the products that have a sell date that corresponds to the month and year that the user input. To get the revenue, the following code was used:

sell_price_list = []
input_date_month = int(date[5:7])
input_date_year = int(date[0:4])
input_date_string = f'{date[5:7]}/{date[2:4]}'
if input_date_month < 10:
    input_date_month = int(date[6:7])
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
for row in reader:
    sell_date_string = f'{row["sell_date"][8:10]}/{row["sell_date"][5:7]}/{row["sell_date"][2:4]}'
    if input_date_string in sell_date_string:
        sell_price_list.append(float(row['sell_price'])*int(row['amount']))
revenue = sum(sell_price_list)
print(f"Revenue from {months[input_date_month - 1]} {input_date_year}: {revenue} euro's.")
The user input is in the format YYYY-MM, the month is saved as an integer in the variable input_date_month, the full year is saved as an integer in the variable input_date_year and the full date is saved as a string in the format MM/YY in the input_date_string variable. The input_date_month variable is used to slice the correct month from the list with months and printed in the print statement. If the month number is less than 10 the zero is omitted. For every row in the sold.csv file the sell date is saved as a string in the variable sell_date_string, in the format DD/MM/YY. If the input_date_string is present in sell_date_string, the sell_price times the amount of products is added to the sell_price_list. The revenue is the sum of this list.

Two functions were created to export reports to excel files: report_inventory_excel() and report_sold_excel(). Within these functions the xlsxwriter module was used to export the bought.csv and sold.csv files to excel files (.xlsx). Each row and column was added to the excel file with the following code:

for r, row in enumerate(reader):
    for c, col in enumerate(row):
        worksheet.write(r, c, col)
This solved the problem of having to assign each value in the csv file to a cell number in the excel file, which doesn't work if you have to add multiple rows using a for loop.