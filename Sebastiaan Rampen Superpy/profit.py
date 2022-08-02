import os
import csv
import datetime, os

def profit(args, general):

    sold_list = []
    bought_dictionary = {}
    sum_profit = 0
    if os.path.exists(general.bought_address) and os.path.exists(general.sold_address):
        try:
            with open(general.sold_address, 'r', encoding="utf-8") as file:                   
                sold_file = csv.DictReader(file)
                for line in sold_file:
                    if datetime.datetime.strptime(line['date'], "%Y-%m-%d") ==  datetime.datetime.strptime(args.action_date, "%Y-%m-%d"):
                        sold_list.append(line)
                        if not line['in_id'] in bought_dictionary:
                            bought_dictionary[line['in_id']] = 0

            with open(general.bought_address, 'r', encoding='utf-8') as file:
                bought_file = csv.DictReader(file)
                for line in bought_file:
                    if line['id'] in bought_dictionary:
                        bought_dictionary[line['id']] = line['price']


            for line in sold_list:
                if line['price'] == 'expired':
                    sum_profit += int(line['amount']) * - float(bought_dictionary[line['in_id']])
                else:    
                    sum_profit += int(line['amount']) * (float(line['price']) - float(bought_dictionary[line['in_id']]))

            if sum_profit == 0:
                print("No profit for",args.action_date)
            else:
                print('Profit for',args.action_date, 'is:', str(round(sum_profit, 2)) )

        except:
            print("File 'bought.csv' and/or 'sold.csv' corrupt")
    else:
        print("File 'bought.csv' and/or 'sold.csv' missing")

