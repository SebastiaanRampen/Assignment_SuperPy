import os
import csv
import datetime
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({ "no_data" : "orange3", "error" : "bold red", "info" : "bright_yellow" })
console = Console(theme = custom_theme)


def outport(args, general):
    print('')
    if not os.path.exists(general.bought_address):
        console.print("No file of bought products available", style = "error")
        print('')
    elif args.name != None and args.amount != None and args.price != None:
        try:
            in_list_bought = []
            in_list_match = []
            product_left = 0
            closest_to_expiring = None
            no_expired = True

# check presence in storage, put relevant 'bought' data in 'in_list_bought',
# and their data in 'in_list_match'
            with open(general.bought_address, 'r', encoding="utf-8") as file:
                bought_file = csv.DictReader(file)
                for line in bought_file:

                    if datetime.datetime.strptime(args.action_date, "%Y-%m-%d") > datetime.datetime.strptime(line["exp_date"], "%Y-%m-%d")\
                        and line["amount_left"] != '0':
                        no_expired = False
                    in_list_bought.append(line)
                    if line["name"] == args.name and line["amount_left"] != '0'\
                        and datetime.datetime.strptime(args.action_date, "%Y-%m-%d") <= datetime.datetime.strptime(line["exp_date"], "%Y-%m-%d")\
                        and datetime.datetime.strptime(args.action_date, "%Y-%m-%d") >= datetime.datetime.strptime(line["date_in"], "%Y-%m-%d"):

                        in_list_match.append(line)
                        product_left += int(line["amount_left"])
                        if closest_to_expiring == None:
                            closest_to_expiring = datetime.datetime.strptime(line["exp_date"], "%Y-%m-%d")
                        else:
                            if closest_to_expiring > datetime.datetime.strptime(line["exp_date"], "%Y-%m-%d"):
                                closest_to_expiring = datetime.datetime.strptime(line["exp_date"], "%Y-%m-%d")


            if product_left < args.amount:
                console.print(f"[error]Entered amount is higher than number of items currently present.[/error] [info]({product_left} items left)[/info]")
                print('')
            else:

# only continue when sufficient products are available
                if not os.path.exists(general.sold_address):
                    with open(general.sold_address, 'w', newline ="", encoding="utf-8") as file:
                        input_file = csv.writer(file)
                        input_file.writerow(general.sold_fieldnames)
                    sold_id = 1

                else:  #else, find last id-value
                    with open(general.sold_address, 'r', encoding="utf-8") as file:
                        sold_file = csv.DictReader(file)
                        for line in sold_file:
                            pass
                        sold_id = int(line['id']) + 1

                    next_closest_to_expiring = None

# append lines to 'sold.csv, and update lines that should later go back in bought.csv
                with open(general.sold_address, 'a', newline ="", encoding="utf-8") as file:
                    input_file = csv.writer(file)
                    amount = args.amount
                    index = 0
                    while amount > 0:
                        while datetime.datetime.strptime(in_list_match[index]["exp_date"], "%Y-%m-%d") != closest_to_expiring:
                            if datetime.datetime.strptime(in_list_match[index]["exp_date"], "%Y-%m-%d") > closest_to_expiring:
                                if next_closest_to_expiring == None:
                                    next_closest_to_expiring = datetime.datetime.strptime(in_list_match[index]["exp_date"], "%Y-%m-%d")
                                else:
                                    if next_closest_to_expiring > datetime.datetime.strptime(in_list_match[index]["exp_date"], "%Y-%m-%d"):
                                        next_closest_to_expiring = datetime.datetime.strptime(in_list_match[index]["exp_date"], "%Y-%m-%d")
                            index += 1
                            if index > len(in_list_match) - 1:
                                index = 0
                                closest_to_expiring = next_closest_to_expiring
                                next_closest_to_expiring = None

                        if int(in_list_match[index]["amount_left"]) >= amount:
                            in_list_match[index]["amount_left"] = \
                                int(in_list_match[index]["amount_left"]) - amount
                            input_file.writerow([sold_id, in_list_match[index]["id"], args.name, amount, args.price, args.action_date])
                            amount = 0
                        else:
                            amount -= int(in_list_match[index]["amount_left"])
                            input_file.writerow([sold_id, in_list_match[index]["id"], args.name, in_list_match[index]["amount_left"], args.price, args.action_date])
                            in_list_match[index]["amount_left"] = 0

                        index += 1
                        if index > len(in_list_match) - 1:
                            if amount > 0:
                                index = 0
                                closest_to_expiring = next_closest_to_expiring
                                next_closest_to_expiring = None

                        sold_id += 1


                with open(general.bought_address, 'w', newline ="", encoding="utf-8") as file:
                    bought_file = csv.DictWriter(file, fieldnames= general.bought_fieldnames)
                    bought_file.writeheader()

                    index = 0
                    for line in in_list_match:
                        while in_list_bought[index]['id'] != line['id']:
                            bought_file.writerow(in_list_bought[index])
                            index += 1

                        in_list_bought[index]['amount_left'] = line['amount_left']
                        bought_file.writerow(in_list_bought[index])
                        index += 1

                    while index < len(in_list_bought):
                        bought_file.writerow(in_list_bought[index])
                        index += 1

                console.print(f"Sold [info]{args.amount}[/info] items of [info]{args.name}[/info] for [info]{args.price}[/info]")
                print('')

            if no_expired == False:
                print('')
                console.print("For some products, the 'current' date exceeds the expiring date.", style = "info")
                console.print("Consider removing the expired products.", style = "info")
                print('')
        except:
            console.print('Incorrect input. Need input of product-name, amount, and price', style = "error")
            print('')
    else:
        console.print('Incomplete input. Need input of product-name, amount, and price', style = "error")
        print('')
