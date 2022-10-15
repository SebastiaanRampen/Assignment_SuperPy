import os
import csv
import datetime
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({ "no_data" : "orange3", "error" : "bold red", "info" : "bright_yellow" })
console = Console(theme = custom_theme)


def profit(args, general):
    print('')
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
                console.print(f"No profit for [info]{args.action_date}[/info]")
            else:
                console.print(f"Profit for [info]{args.action_date}[/info] is: [info]{str(round(sum_profit, 2))}[/info]" )
            print('')

        except:
            console.print("File 'bought.csv' and/or 'sold.csv' corrupt", style = "error")
            print('')
    else:
        console.print("File 'bought.csv' and/or 'sold.csv' missing", style = "error")
        print('')
