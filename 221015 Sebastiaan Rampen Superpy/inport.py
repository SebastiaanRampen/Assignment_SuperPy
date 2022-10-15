import os
import csv
import datetime
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({ "no_data" : "orange3", "error" : "bold red", "info" : "bright_yellow" })
console = Console(theme = custom_theme)



def inport(args, general):
    print('')
    if args.name != None and args.amount != None and args.price != None and args.expired != None:
        if datetime.datetime.strptime(args.action_date, "%Y-%m-%d") > datetime.datetime.strptime(args.expired, "%Y-%m-%d"):
            console.print("The 'in-date' must be before the 'expired-date'", style = "error")
            print('')
        else:
            try:
                if not os.path.exists(general.bought_address):
                    args.id = 1
                    with open(general.bought_address, 'w', newline ="", encoding="utf-8") as file:
                        input_file = csv.writer(file)
                        input_file.writerow(general.bought_fieldnames)
                        input_file.writerow([args.id, args.action_date, args.name, args.amount, args.price, args.expired, args.amount])
                else:
                    in_list = []
                    with open(general.bought_address, 'r', encoding="utf-8") as file:
                        original_file = csv.DictReader(file)
                        for line in original_file:
                            in_list.append(line)

                    args.id = int(in_list[-1]["id"])+1

                    with open(general.bought_address, 'a', newline ="", encoding="utf-8") as file:
                        input_file = csv.writer(file)
                        input_file.writerow([args.id, args.action_date, args.name, args.amount, args.price, args.expired, args.amount])

                console.print(f"Bought [info]{args.amount}[/info] items of [info]{args.name}[/info] for [info]{args.price}[/info] with expiring date [info]{args.expired}[/info]")
                print('')
            except:
                console.print('Incorrect input. Need input of product-name, amount, price and expiration data', style = "error")
                print('')
    else:
        console.print('Incomplete input. Need input of product-name, amount, price and expiration data', style = "error")
        print('')
# https://youtu.be/q5uM4VKywbA
# Python Tutorial: CSV Module - How to Read, Parse, and Write CSV Files
