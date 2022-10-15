import os
import csv
import datetime
from rich.console import Console
from rich.table import Table
from rich.theme import Theme

custom_theme = Theme({ "no_data" : "orange3", "error" : "bold red" })
console = Console(theme = custom_theme)


def expired(args, general):
    print('')
    if not os.path.exists(general.bought_address):
        console.print("No file of bought products available", style = "error")
        print('')
    else:
        try:
            list_bought = []
            table = Table(title="Expired goods")
            table.add_column("Item")
            table.add_column("Count", justify = "right")
            table.add_column("Bought", justify = "right")

            with open(general.bought_address, 'r', encoding="utf-8") as file:
                bought_file = csv.DictReader(file)
                expired_goods = False
                for line in bought_file:
                    list_bought.append(line)
                    if datetime.datetime.strptime(line["exp_date"], "%Y-%m-%d") < \
                        datetime.datetime.strptime(args.action_date, "%Y-%m-%d") and line["amount_left"] != "0":
                        expired_goods = True
                        table.add_row(line['name'], line['amount_left'], line['date_in'])


            if expired_goods == False:
                console.print("No expired goods present", style = "no_data")
                print('')
            else:
                console.print(table)
                print('')
#                        do_remove = input('Remove expired items from the file? (y/n): ').lower()
                do_remove = 'y'

                if do_remove == 'y':
                    if not os.path.exists(general.sold_address):
#    if needed, create sold.csv
                        with open(general.sold_address, 'w', newline ="", encoding="utf-8") as file:
                            input_file = csv.writer(file)
                            input_file.writerow(general.sold_fieldnames)
                        sold_id = 1

                    else:
#    else, find last id-value
                        out_list = []
                        with open(general.sold_address, 'r', encoding="utf-8") as file:
                            sold_file = csv.DictReader(file)
                            for line in sold_file:
                                out_list.append(line)

                        sold_id = int(out_list[-1]["id"])

# append lines to 'sold.csv, and update lines that should later go back in bought.csv
                    with open (general.sold_address, 'a', newline ="", encoding="utf-8") as file:
                        input_file = csv.writer(file)
                        for i in range(len (list_bought)):
                            if datetime.datetime.strptime(list_bought[i]["exp_date"], "%Y-%m-%d") < \
                                datetime.datetime.strptime(args.action_date, "%Y-%m-%d") and list_bought[i]["amount_left"] != "0":
                                sold_id += 1
                                input_file.writerow([ sold_id, list_bought[i]["id"], list_bought[i]["name"],list_bought[i]["amount_left"], 'expired', list_bought[i]["exp_date"]])
                                list_bought[i]["amount_left"] = 0

                    with open (general.bought_address, 'w', newline ="", encoding="utf-8") as file:
                        bought_file = csv.DictWriter(file, fieldnames= general.bought_fieldnames)
                        bought_file.writeheader()

                        for line in list_bought:
                            bought_file.writerow(line)

        except:
            console.print("Incorrect input file", style = "error")
            print('')
