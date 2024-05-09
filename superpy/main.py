# Imports
import argparse
import csv
from datetime import date

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.

# importeren van de nodig modules.
import csv
import argparse
import datetime
import os
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table
import sys
from functions import *

# Uitleg SuperPy programma. 
def create_usage_guide():
    usage_guide = """
    SuperPy - Inventory Management System

    Requirements
    python
    CSV
    matplotlib
    rich
    argparse
    datetime
    sys


    Commands:

      buy                Buy a product
      sell               Sell a product
      report             Generate reports
      export             Export data to CSV
      advance_time       Advance or reverse the current date

    Examples:

    For help:
        python main.py -h

    Buy a product
    This function is for buying a product
    Usage: main.py buy [-h] --product-name PRODUCT_NAME --price PRICE [--amount AMOUNT] --exp-date EXP_DATE

    Example:
        python main.py buy --product-name banana --price 2.8  --amount 1 --exp-date 2023-06-30

    Sell a product
    This is a function for selling a product
    Usage: main.py sell [-h] --product-name PRODUCT_NAME --amount AMOUNT --price PRICE

    Example:
        python main.py sell --product-name orange --amount 2 --price 2

    Generate inventory report
    This is a function for generate a inventory report
    Usage: main.py report inventory [-h] [--now] [--start_date Year-Month-Day]

    Example:
        python main.py report inventory --now
        python main.py report inventory --start_date 2023-06-30

    Generate revenue report
    This is a function for generate a revenue report
    Usage: main.py report revenue [-h] --start-date Year/month --end-date Year/month [--visualize]

    Example:
        python main.py report revenue --start-date 2023-05 --end-date 2023-06

    Generate profit report
    This is a function for generate a profit report
    Usage: main.py report profit [-h] --start-date Year/month --end-date Year/month

    Example:
        python main.py report profit --start-date 2023-05 --end-date 2023-06

    Visualize revenue statistics
    This is a function for visualize a revenue statistics
    Usage: main.py report revenue [-h] --start-date Year/month --end-date Year/month [--visualize]

    Example:
        python main.py report revenue --start-date 2023-05 --end-date 2023-06 --visualize

    Change the time
    This is a function for changing time
    Usage: main.py advance_time [-h] days

    Example:
        python main.py advance_time 2 ( changes the date with 2 days ahead )
        python main.py advance_time -2 ( changes the date with -2 days back )

    Set the date
    This is a function for changing the date
    Usage: main.py set_date [-h] year month day 

    Example:
        python main.py set_date 2023-10-2
        
    
    Voor een meer gedetailleerde uitleg kunt u het user_guide.txt bestand bezoeken voor specificaties van de opdrachtregels en hun doeleinden.

    
    with open(USAGE_GUIDE_FILE, "w") as file:
        file.write(usage_guide)
    """

def main():
    # Implementen van argparse.
    parser = argparse.ArgumentParser(description="SuperPy - Inventory Management System")
    subparsers = parser.add_subparsers(title="commands", dest="command")

    # Buy Command
    buy_parser = subparsers.add_parser("buy", help="Buy a product")
    buy_parser.add_argument("--product-name", required=True, help="Name of the product")
    buy_parser.add_argument("--price", type=float, required=True, help="Price of the product")
    buy_parser.add_argument("--amount", type=int, help="Quantity of the product")
    buy_parser.add_argument("--exp-date", required=True, help="Expiration date of the product")
    
    # Sell Command
    sell_parser = subparsers.add_parser("sell", help="Sell a product")
    sell_parser.add_argument("--product-name", required=True, help="Name of the product")
    sell_parser.add_argument("--amount", type=int, help="Quantity of the product")
    sell_parser.add_argument("--price", type=float, required=True, help="Price of the product")

    # Report Command
    report_parser = subparsers.add_parser("report", help="Generate reports")
    report_subparsers = report_parser.add_subparsers(dest="report_type")

    # Inventory Report Subcommand
    inventory_report_parser = report_subparsers.add_parser("inventory", help="Generate inventory report")
    inventory_report_parser.add_argument("--now", action="store_true", help="Generate report for the current date")
    inventory_report_parser.add_argument("--start_date", help="Specify start date for the inventory report")

    # Revenue Report Subcommand
    revenue_report_parser = report_subparsers.add_parser("revenue", help="Generate revenue report")
    revenue_report_parser.add_argument("--start-date", required=True, help="Start date of the report")
    revenue_report_parser.add_argument("--end-date", required=True, help="End date of the report")
    revenue_report_parser.add_argument("--visualize", action="store_true", help="Visualize revenue statistics")

    # Profit Report Subcommand
    profit_report_parser = report_subparsers.add_parser("profit", help="Generate profit report")
    profit_report_parser.add_argument("--start-date", required=True, help="Start date of the report")
    profit_report_parser.add_argument("--end-date", required=True, help="End date of the report")

    # Export Subcommand
    export_parser = subparsers.add_parser("export", help="Export data to CSV")
    export_parser.add_argument("--report-type", required=True, help="Type of the report to export")
    export_parser.add_argument("--start-date", required=True, help="Start date of the report")
    export_parser.add_argument("--end-date", required=True, help="End date of the report")
    export_parser.add_argument("--export-file", required=True, help="File to export the report")

    # Advance Time Command
    advance_time_parser = subparsers.add_parser("advance_time", help="Advance or reverse the current date")
    advance_time_parser.add_argument("days", type=int, help="Number of days to advance (positive) or reverse (negative) the current date")

    # Set date Command
    set_date_parser = subparsers.add_parser("set_date", help="Set the current date")
    set_date_parser.add_argument("year", type=int, help="Year")
    set_date_parser.add_argument("month", type=int, help="Month")
    set_date_parser.add_argument("day", type=int, help="Day")

    # Parse de opgegeven argumenten.
    args = parser.parse_args()

    # Command om te kopen.
    if args.command == "buy":
        buy_product(args.product_name, args.price, args.amount, args.exp_date)

    # Command om te verkopen.
    elif args.command == "sell":
        sell_product(args.product_name, args.amount, args.price)

    # Command voor reports.
    elif args.command == "report":
        if args.report_type == "inventory":
            report_date = (
                get_current_date()
                if args.now
                else datetime.datetime.strptime(args.start_date, "%Y-%m-%d").date()
            )
            generate_inventory_report(report_date)

        elif args.report_type == "revenue":
            start_date = datetime.datetime.strptime(args.start_date, "%Y-%m").date()
            end_date = datetime.datetime.strptime(args.end_date, "%Y-%m").date()
            generate_revenue_report(start_date, end_date)

            if args.visualize:
                visualize_statistics("revenue", start_date, end_date)

        elif args.report_type == "profit":
            start_date = datetime.datetime.strptime(args.start_date, "%Y-%m").date()
            end_date = datetime.datetime.strptime(args.end_date, "%Y-%m").date()
            generate_profit_report(start_date, end_date)

        elif args.command == "advance_time":
            days = args.days
            advance_time(days)

        else:
            print("ERROR: Invalid report type.")

    elif args.command == "export":
        start_date = datetime.datetime.strptime(args.start_date, "%Y-%m").date()
        end_date = datetime.datetime.strptime(args.end_date, "%Y-%m").date()
        export_report(args.report_type, start_date, end_date, args.export_file)

        print(f"Report exported to {args.export_file} successfully.")

    elif args.command == "advance_time":
        days = args.days
        advance_time(days)
    
    elif args.command == "set_date":
        set_date(args.year, args.month, args.day)

    else:
        parser.print_help()


if __name__ == "__main__":
    if not os.path.exists(INVENTORY_FILE):
        write_csv_file(
            INVENTORY_FILE,
            [],
            ["id", "product_name", "buy_date", "buy_price", "expiration_date"],
        )

    if not os.path.exists(SALES_FILE):
        write_csv_file(SALES_FILE, [], ["id", "bought_id", "sell_date", "sell_price"])

    if not os.path.exists(DATE_FILE):
        set_current_date(datetime.date.today())

    if not os.path.exists(USAGE_GUIDE_FILE):
        create_usage_guide()

    main()
