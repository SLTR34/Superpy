# Imports
import functions
import argparse


# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
def main():
    parser = argparse.ArgumentParser(description='Welcome to the inventory')
    subparsers = parser.add_subparsers(dest='command')

    buy_parser = subparsers.add_parser('buy', help='input a product that was bought', description='add a bought product')
    buy_parser.add_argument('-pn', '--product_name', type=str, help='product name')
    buy_parser.add_argument('-bp', '--buy_price', type=float, help='buy price of product')
    buy_parser.add_argument('-ed', '--expiration_date', type=str, help='expiration date of product in format YYYY-MM-DD')
    buy_parser.add_argument('-a', '--amount', type=int, help='amount of products')

    sell_parser = subparsers.add_parser('sell', help='input a product that was sold', description='add a sold product')
    sell_parser.add_argument('-pn','--product_name', type=str, help='product name')
    sell_parser.add_argument('-sp', '--sell_price', type=float, help='sell price of product')
    sell_parser.add_argument('-a', '--amount', type=int, help='amount of products')

    time_parser = subparsers.add_parser('advance_time', help='input number of days to advance time', description='advance the time with a number of days')
    time_parser.add_argument('days', type=int, help='number of days')

    report_inventory_parser = subparsers.add_parser('report_inventory', help='get a report for the inventory', description='get an inventory report with bought items for now or yesterday')
    report_inventory_parser.add_argument('-n', '--now', action='store', nargs='*')
    report_inventory_parser.add_argument('-y', '--yesterday', action='store', nargs='*')

    report_sold_parser = subparsers.add_parser('report_sold', help='get a report of sold items and expired items', description='get a report of sold items and expired items for today or yesterday')
    report_sold_parser.add_argument('-t', '--today', action='store', nargs='*')
    report_sold_parser.add_argument('-y','--yesterday', action='store', nargs='*')

    report_revenue_parser = subparsers.add_parser('report_revenue', help='get a report of the revenue', description='get a report of the revenue for today, yesterday or a particular month')
    report_revenue_parser.add_argument('-t', '--today', action='store', nargs='*')
    report_revenue_parser.add_argument('-y','--yesterday', action='store', nargs='*')
    report_revenue_parser.add_argument('-d','--date', type=str, help='input a date in format YYYY-MM')

    report_profit_parser = subparsers.add_parser('report_profit', help='get a report of the profit', description='get a report of the profit for today, yesterday or a particular month')
    report_profit_parser.add_argument('-t', '--today', action='store', nargs='*')
    report_profit_parser.add_argument('-y', '--yesterday', action='store', nargs='*')
    report_profit_parser.add_argument('-d', '--date', type=str, help='input a date in format YYYY-MM')

    report_inventory_excel_parser = subparsers.add_parser('report_inventory_excel', help='export a report of the current inventory to an excel file (.xlsx)', description='export a report of the current inventory to an excel file (.xlsx)')
    
    report_sold_excel_parser = subparsers.add_parser('report_sold_excel', help='export a report of sold items to an excel file (.xlsx)', description='export a report of sold items to an excel file (.xlsx)')
        
    args = parser.parse_args()

    if args.command == 'buy':
        functions.buy_product(args.product_name, args.buy_price, args.expiration_date, args.amount)

    if args.command == 'sell':
        functions.sell_product(args.product_name, args.sell_price, args.amount)

    if args.command == 'advance_time':
        functions.advance_time(args.days)

    if args.command == 'report_inventory':
        functions.report_inventory(now=args.now, yesterday=args.yesterday)

    if args.command == 'report_sold':
        functions.report_sold_and_expired(today=args.today, yesterday=args.yesterday)

    if args.command == 'report_revenue':
        functions.report_revenue(today=args.today, yesterday=args.yesterday, date=args.date)

    if args.command == 'report_profit':
        functions.report_profit(today=args.today, yesterday=args.yesterday, date=args.date)

    if args.command == 'report_inventory_excel':
        functions.report_inventory_excel()

    if args.command == 'report_sold_excel':
        functions.report_sold_excel()


if __name__ == "__main__":
    main()   