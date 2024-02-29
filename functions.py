import csv
from datetime import datetime
from datetime import timedelta
import os.path
from rich.console import Console
from rich.table import Table
import xlsxwriter
from main import *
import sys

# Buy and sell items

def last_bought():
    """
    Gives the ID number of the last bought item
    """
    with open('bought.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        bought_list = []
        for rows in reader:
            bought_list.append(rows)
    return bought_list[len(bought_list) - 1]


def buy_product(product_name, buy_price, expiration_date, amount):
    """
    Writes a bought item from the user input into a csv file called bought.csv
    """
    file_exists_csv = os.path.exists('bought.csv')
    fieldnames = ['id', 'product_name', 'buy_price', 'buy_date', 'expiration_date', 'amount']
    buy_date = todays_date()
    expiration_date_string = f'{expiration_date[8:10]}/{expiration_date[5:7]}/{expiration_date[2:4]}'
    expiration_date_object = datetime.strptime(expiration_date_string, '%d/%m/%y').date()
    with open('bought.csv', 'a', newline='') as csvfile:
        sys.tracebacklimit = 0
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        class ExpirationError(Exception):
            pass

        if expiration_date_object > todays_date():
            if file_exists_csv == False:
                writer.writeheader()
                id = 1
            else:
                id = int(last_bought()['id']) + 1
            writer.writerow({'id': id, 'product_name': product_name, 'buy_price': buy_price, 'buy_date': buy_date, 'expiration_date': expiration_date, 'amount': amount,})
        if expiration_date_object <= todays_date():
            raise ExpirationError("product expired")


def last_sold():
    """
    Gives the ID number of the last sold item
    """
    with open('sold.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        sold_list = []
        for rows in reader:
            sold_list.append(rows)
    return sold_list[len(sold_list) - 1]       

def sell_product(product_name, sell_price, amount):
    """
    Writes a sold item from the user input into a csv file called sold.csv
    """
    file_exists = os.path.exists('sold.csv')
    fieldnames_sell = ['id', 'bought_id', 'product_name', 'buy_price', 'sell_price', 'sell_date', 'amount']
    fieldnames_buy = ['id', 'product_name', 'buy_price', 'buy_date', 'expiration_date', 'amount']
    bought_id = None
    buy_price = None
    sell_date = todays_date()

    with open('bought.csv', 'r+', newline='') as boughtfile:
        sys.tracebacklimit = 0
        reader = csv.DictReader(boughtfile)
        product_list = []

        class ProductError(Exception):
            pass
        class AmountError(Exception):
            pass
        class ExpirationError(Exception):
            pass

        for row in reader:
            product_list.append(row['product_name'])
            expiration_date_string = f'{row["expiration_date"][8:10]}/{row["expiration_date"][5:7]}/{row["expiration_date"][2:4]}'
            expiration_date_object = datetime.strptime(expiration_date_string, '%d/%m/%y').date()
        if product_name not in product_list:
            raise ProductError("product not in stock")
        if product_name == row['product_name'] and amount > int(row['amount']):
            raise AmountError("not enough in stock")
        if product_name == row['product_name'] and expiration_date_object <= todays_date():
            raise ExpirationError("product expired")

                
    with open('bought.csv', 'r+', newline='') as boughtfile:
        reader = csv.DictReader(boughtfile)
        for row in reader:
            if row['product_name'] == product_name:
                bought_id = row['id']
                buy_price = row['buy_price']
                

    with open('sold.csv', 'a', newline='') as soldfile:
        writer = csv.DictWriter(soldfile, fieldnames=fieldnames_sell, delimiter=',')
        if file_exists == False:
            writer.writeheader()
            id = 1
        else:
            id = int(last_sold()['id']) + 1
        writer.writerow({'id': id, 'bought_id': bought_id, 'product_name': product_name, 'buy_price': buy_price, 'sell_price': sell_price, 'sell_date': sell_date, 'amount': amount})
        

    with open('bought.csv', 'r+', newline='') as boughtfile:
        reader = csv.DictReader(boughtfile)
        rows = []
        product_found = False
        for row in reader:
            expiration_date_string = f'{row["expiration_date"][8:10]}/{row["expiration_date"][5:7]}/{row["expiration_date"][2:4]}'
            expiration_date_object = datetime.strptime(expiration_date_string, '%d/%m/%y').date()
            if row['product_name'] == product_name and expiration_date_object > todays_date() and not product_found:
                row['amount'] = int(row['amount']) - amount
                if int(row['amount']) > 0:
                    rows.append(row)
                    product_found = True
            else:        
                rows.append(row)

    with open('bought.csv', 'w', newline='') as boughtfile:
        writer = csv.DictWriter(boughtfile, fieldnames=fieldnames_buy)
        writer.writeheader()
        writer.writerows(rows)
       
# Date

def todays_date():
    """
    Reads the date provided in the date.txt file and returns a datetime object with that date
    """
    with open('date.txt', 'r', newline='') as file:
        string = file.read()
        todays_date = datetime.strptime(string, '%d/%m/%y').date()
        return todays_date
    

def advance_time(days):
    """
    Advances the date with a number of days given by the user
    """
    date = todays_date()
    new_date = date + timedelta(days=days)
    string = new_date.strftime('%d/%m/%y')
    with open('date.txt', 'w', newline='') as file:
        file.write(string)
    print('OK')      

# Reports

def report_inventory(now, yesterday):
    """
    Gives a report of the current or yesterday's inventory in the form of a table
    """
    console = Console() 
    if now is not None:
        with open('bought.csv', 'r', newline='') as boughtfile:
            reader = csv.DictReader(boughtfile)
            table = Table(show_header=True, header_style='light_sea_green', title='Inventory Report Now', title_style='magenta', show_lines=True)
            table.add_column('Product Name', style="navajo_white1", width=12)
            table.add_column('Count', style="navajo_white1")
            table.add_column('Buy Price', style="navajo_white1")
            table.add_column('Expiration Date', style="navajo_white1")
            for row in reader:
                table.add_row(row['product_name'], row['amount'], row['buy_price'], row['expiration_date'])
        console.print(table)
           
    if yesterday is not None: 
        with open('bought.csv', 'r', newline='') as boughtfile:
            reader = csv.DictReader(boughtfile)
            table = Table(show_header=True, header_style="light_sea_green", title="Inventory Report Yesterday", title_style="magenta", show_lines=True)
            table.add_column("Product Name", style="navajo_white1", width=12)
            table.add_column("Count", style="navajo_white1")
            table.add_column("Buy Price", style="navajo_white1")
            table.add_column("Expiration Date", style="navajo_white1")
            for row in reader:
                buy_date_string = f'{row["buy_date"][8:10]}/{row["buy_date"][5:7]}/{row["buy_date"][2:4]}'
                buy_date = datetime.strptime(buy_date_string, '%d/%m/%y').date()
                if buy_date < todays_date():
                    table.add_row(row['product_name'], row['amount'], row['buy_price'], row['expiration_date'])   
        console.print(table)  


def report_sold_and_expired(today, yesterday):
    """
    Gives a report of the sold and expired items in the form of a table
    """
    console = Console()
    if today is not None:
        with open('sold.csv', 'r', newline='') as soldfile: 
            reader = csv.DictReader(soldfile)
            table = Table(show_header=True, header_style="light_sea_green", title="Sold and Expired Report Today", title_style="magenta", show_lines=True)
            table.add_column("Product Name", style="navajo_white1", width=12)
            table.add_column("Count", style="navajo_white1")
            table.add_column("Sell Price", style="navajo_white1")
            table.add_column("Expired", style="navajo_white1")
            for row in reader:
                sell_date_string = f'{row["sell_date"][8:10]}/{row["sell_date"][5:7]}/{row["sell_date"][2:4]}'
                sell_date = datetime.strptime(sell_date_string, '%d/%m/%y').date()
                if sell_date == todays_date():
                    table.add_row(row['product_name'], row['amount'], row['sell_price'], 'no')  
        
        with open('bought.csv', 'r', newline='') as boughtfile:
            reader = csv.DictReader(boughtfile)
            for row in reader:
                expiration_date_string = f'{row["expiration_date"][8:10]}/{row["expiration_date"][5:7]}/{row["expiration_date"][2:4]}'
                expiration_date = datetime.strptime(expiration_date_string, '%d/%m/%y').date()
                if expiration_date < todays_date():
                    table.add_row(row['product_name'], row['amount'], '0', 'yes')
        console.print(table)

    if yesterday is not None:
        with open('sold.csv', 'r', newline='') as soldfile: 
            reader = csv.DictReader(soldfile)
            table = Table(show_header=True, header_style="light_sea_green", title="Sold and Expired Report Yesterday", title_style="magenta", show_lines=True)
            table.add_column("Product Name", style="navajo_white1", width=12)
            table.add_column("Count", style="navajo_white1")
            table.add_column("Sell Price", style="navajo_white1")
            table.add_column("Expired", style="navajo_white1")
            for row in reader:
                sell_date_string = f'{row["sell_date"][8:10]}/{row["sell_date"][5:7]}/{row["sell_date"][2:4]}'
                sell_date = datetime.strptime(sell_date_string, '%d/%m/%y').date()
                if sell_date == todays_date() - timedelta(days=1):
                    table.add_row(row['product_name'], row['amount'], row['sell_price'], 'no')  
        
        with open('bought.csv', 'r', newline='') as boughtfile:
            reader = csv.DictReader(boughtfile)
            for row in reader:
                expiration_date_string = f'{row["expiration_date"][8:10]}/{row["expiration_date"][5:7]}/{row["expiration_date"][2:4]}'
                expiration_date = datetime.strptime(expiration_date_string, '%d/%m/%y').date()
                if expiration_date < todays_date():
                    table.add_row(row['product_name'], row['amount'], '0', 'yes')
        console.print(table)
    

def report_revenue(today, yesterday, date):
    """
    Gives a report of the revenue for today, yesterday or a specified month by the user
    """
    if today is not None:
        with open('sold.csv', 'r', newline='') as soldfile:
            reader = csv.DictReader(soldfile)
            sell_price_list = []
            for row in reader:
                sell_date_string = f'{row["sell_date"][8:10]}/{row["sell_date"][5:7]}/{row["sell_date"][2:4]}'
                sell_date = datetime.strptime(sell_date_string, '%d/%m/%y').date()
                if sell_date == todays_date():
                    sell_price_list.append(float(row['sell_price'])*int(row['amount']))
            revenue = sum(sell_price_list)
        print(f"Today's revenue so far: {revenue} euro's.")
    if yesterday is not None:
        with open('sold.csv', 'r', newline='') as soldfile:
            reader = csv.DictReader(soldfile)
            sell_price_list = []
            for row in reader:
                sell_date_string = f'{row["sell_date"][8:10]}/{row["sell_date"][5:7]}/{row["sell_date"][2:4]}'
                sell_date = datetime.strptime(sell_date_string, '%d/%m/%y').date()
                if sell_date == todays_date() - timedelta(days=1):
                    sell_price_list.append(float(row['sell_price'])*int(row['amount']))
            revenue = sum(sell_price_list)
        print(f"Yesterday's revenue: {revenue} euro's.")
    if date is not None:
        with open('sold.csv', 'r', newline='') as soldfile:
            reader = csv.DictReader(soldfile)
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


def report_profit(today, yesterday, date):
    """
    Gives a report of the profit for today, yesterday or a specified month by the user
    """
    if today is not None:
        with open('sold.csv', 'r', newline='') as soldfile:
            reader = csv.DictReader(soldfile)
            sell_price_list = []
            expenses_bought = []
            expenses_sold = []
            for row in reader:
                sell_date_string = f'{row["sell_date"][8:10]}/{row["sell_date"][5:7]}/{row["sell_date"][2:4]}'
                sell_date = datetime.strptime(sell_date_string, '%d/%m/%y').date()
                if sell_date == todays_date():
                    sell_price_list.append(float(row['sell_price'])*int(row['amount']))
                expenses_sold.append(int(row['amount'])*float(row['buy_price']))
            revenue = sum(sell_price_list)

            with open('bought.csv', 'r', newline='') as boughtfile:
                reader = csv.DictReader(boughtfile)
                for row in reader:
                    expenses_bought.append(float(row['buy_price'])*int(row['amount']))
        total_expenses = sum(expenses_bought) + sum(expenses_sold)    
        profit = revenue - total_expenses
        print(f"Today's profit: {profit} euro's")


    if yesterday is not None:
        with open('sold.csv', 'r', newline='') as soldfile:
            reader = csv.DictReader(soldfile)
            sell_price_list = []
            expenses_bought = []
            expenses_sold = []
            for row in reader:
                sell_date_string = f'{row["sell_date"][8:10]}/{row["sell_date"][5:7]}/{row["sell_date"][2:4]}'
                sell_date = datetime.strptime(sell_date_string, '%d/%m/%y').date()
                if sell_date == todays_date() - timedelta(days=1):
                    sell_price_list.append(float(row['sell_price'])*int(row['amount']))
                expenses_sold.append(int(row['amount'])*float(row['buy_price']))
            revenue = sum(sell_price_list)

            with open('bought.csv', 'r', newline='') as boughtfile:
                reader = csv.DictReader(boughtfile)
                for row in reader:
                    expenses_bought.append(float(row['buy_price'])*int(row['amount']))
        total_expenses = sum(expenses_bought) + sum(expenses_sold)    
        profit = revenue - total_expenses
        print(f"Yesterday's profit: {profit} euro's")

    if date is not None:
        with open('sold.csv', 'r', newline='') as soldfile:
            reader = csv.DictReader(soldfile)
            sell_price_list = []
            expenses_bought = []
            expenses_sold = []
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
                    expenses_sold.append(int(row['amount'])*float(row['buy_price']))
            revenue = sum(sell_price_list)
        with open('bought.csv', 'r', newline='') as boughtfile:
            reader = csv.DictReader(boughtfile)
            for row in reader:
                expenses_bought.append(float(row['buy_price'])*int(row['amount']))
        total_expenses = sum(expenses_bought) + sum(expenses_sold)    
        profit = revenue - total_expenses
        print(f"Profit from {months[input_date_month - 1]} {input_date_year}: {profit} euro's.")


def report_inventory_excel():
    """
    Gives a report of the inventory in an excel file with the data from bought.csv
    """
    workbook = xlsxwriter.Workbook('bought.xlsx')
    worksheet = workbook.add_worksheet()
    with open('bought.csv', 'rt', encoding='utf8') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
    workbook.close()
    print(f"Excel report created")


def report_sold_excel():
    """
    Gives a report of the sold items in an excel file with the data from sold.csv
    """
    workbook = xlsxwriter.Workbook('sold.xlsx')
    worksheet = workbook.add_worksheet()
    with open('sold.csv', 'rt', encoding='utf8') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
    workbook.close()
    print(f"Excel report created")