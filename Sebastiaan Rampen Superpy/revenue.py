import os
import csv
import datetime, os

def revenue(args, general):
    if os.path.exists(general.bought_address):
        try:
            sum_revenue = 0
            with open(general.sold_address, 'r', encoding="utf-8") as file:                   
                sold_file = csv.DictReader(file)
                for line in sold_file:
                    if datetime.datetime.strptime(line['date'], "%Y-%m-%d") ==  datetime.datetime.strptime(args.action_date, "%Y-%m-%d"):
                        if line['price'] != 'expired':
                            sum_revenue += (int(line['amount']) * float(line['price']))

            if sum_revenue == 0:
                print("No revenue for",args.action_date)
            else:
                print('Revenue for',args.action_date, 'is:', str(sum_revenue) )
        except:
                print("File 'sold.csv' corrupt")
    else:
        print("File 'sold.csv' missing")

