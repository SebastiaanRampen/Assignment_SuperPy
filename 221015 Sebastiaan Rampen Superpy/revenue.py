import os
import csv
import datetime
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({ "no_data" : "orange3", "error" : "bold red", "info" : "bright_yellow" })
console = Console(theme = custom_theme)


def revenue(args, general):
    print('')
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
                console.print(f"No revenue for [info]{args.action_date}[/info]")
            else:
                console.print(f"Revenue for [info]{args.action_date}[/info] is: [info]{str(sum_revenue)}[/info]" )
            print('')

        except:
            console.print("File 'sold.csv' corrupt", style = "error")
            print('')
    else:
        console.print("File 'sold.csv' missing", style = "error")
        print('')
