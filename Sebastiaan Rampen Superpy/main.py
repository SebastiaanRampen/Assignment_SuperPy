# Imports
#from re import T
#from tkinter.messagebox import NO
from inport import inport
from outport import outport
from expired import expired
from stock import stock
from inventory import inventory
from revenue import revenue
from profit import profit
from product import product

import argparse
import csv
from datetime import date
from time import strftime
import datetime, argparse, os
from decimal import *

# https://docs.python.org/3/library/decimal.html


from attr import attrs

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.

class General_info():
    bought_address = 'bought.csv'
    sold_address = 'sold.csv'
    bought_fieldnames = ["id", "date_in", "name", "amount", "price", "exp_date", "amount_left"]
    sold_fieldnames = ["id", "in_id", "name", "amount", "price", "date"]

general = General_info    


# https://youtu.be/q94B9n_2nf0
# Python3 Advanced Tutorial 3 - Argparse

# https://youtu.be/RjMbCUpvIgw
# Datetime Module (Dates and Times) || Python Tutorial || Learn Python Programming


parser = argparse.ArgumentParser(description='Product Manager')
parser.add_argument("task", type = str, help="in (inport), out (outport), exp (expired), stock (print stock), inv (inventory at date ...), rev (revenue at date ...), prof (profit at date ...), prod (product over time)")
parser.add_argument("-n", "--name", type=str, metavar='', required=False, help="Product name")
parser.add_argument("-a", "--amount", type=int, metavar='', required=False, help="Number of items")
parser.add_argument("-p", "--price", type=Decimal, metavar='', required=False, help="Price per item")
# https://stackoverflow.com/questions/21437258/how-do-i-parse-a-date-as-an-argument-with-argparse    
parser.add_argument("-e", "--expired", type=str, metavar='', required=False, help="Expiration date (YYYY-MM-DD)")
parser.add_argument("-d", "--action_date", type=str, metavar='', required=False, help="Date of in- or output (YYYY-MM-DD)")
parser.add_argument("-s", "--start", type=str, metavar='', required=False, help="Start-date (YYYY-MM-DD)")
parser.add_argument("--end", type=str, metavar='', required=False, help="End-date (YYYY-MM-DD)")
parser.add_argument("-f", "--filename", type=str, metavar='', required=False, help="Enter FileName to Save Output")
args=parser.parse_args()




def main():
    if args.action_date == None:
        args.action_date = datetime.date.today().strftime("%F") 
    if args.action_date.lower()  == 'today':
        args.action_date = datetime.date.today().strftime("%F") 
    if args.action_date.lower()  == 'yesterday':
        args.action_date = (datetime.date.today() -1 ).strftime("%F") 
    if args.end == 'how can I deal with this properly? If I don''t add this section, I can''t use end.lower() == ''today'' - try with blocking this line out... ':
        args.end = datetime.date.today().strftime("%F")
    if args.end.lower() == 'today':
        args.end = datetime.date.today().strftime("%F")
    if args.end.lower() == 'yesterday':
        args.end = (datetime.date.today() -1 ).strftime("%F")
        
    

    if args.task == 'in':
        inport(args, general)
    elif args.task == 'out':
        outport(args, general)    
    elif args.task == 'stock':
        stock(args, general)
    elif args.task == 'inv':
        inventory(args, general)
    elif args.task == 'exp':
        expired(args, general)    
    elif args.task == 'rev':
        revenue(args, general)    
    elif args.task == 'prof':
        profit(args, general)    
    elif args.task == 'prod':
        product(args, general)    

if __name__ == "__main__":
    main()


