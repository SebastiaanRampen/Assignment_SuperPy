import os
import csv
import datetime, os

def inventory(args, general):

    bought_dictionary = {} 

    class item:
        def __init__(self, name, amount, bought, expired):
            self.name = name
            self.amount = amount
            self.bought = bought
            self.expired = expired

# check if the line in the bought-file meets the requirements, i.e. bought before or at the 'action_date
# the expire-date after or at the 'action_date', and when info provided, if it contains the correct item
    def comply_bought(args, line):
        if datetime.datetime.strptime(line["date_in"], "%Y-%m-%d") <= datetime.datetime.strptime(args.action_date, "%Y-%m-%d"):
            if datetime.datetime.strptime(line["exp_date"], "%Y-%m-%d") >= datetime.datetime.strptime(args.action_date, "%Y-%m-%d"):
                if args.name == None:
                    return True
                elif args.name == line["name"]:
                    return True
        return False        


    def comply_sold(args, line):
        if datetime.datetime.strptime(line["date"], "%Y-%m-%d") <= datetime.datetime.strptime(args.action_date, "%Y-%m-%d"):
            if line['in_id'] in bought_dictionary:
                return True
        return False        


    if os.path.exists(general.bought_address) and os.path.exists(general.sold_address):
        try:
            bought_dict = {}  

# create a 'bought_dict' which contains relevant info from items that meet the requirements
            with open(general.bought_address, 'r', encoding="utf-8") as file:                   
                bought_file = csv.DictReader(file)
                for line in bought_file:
                    if comply_bought(args, line):
                        bought_dictionary[line['id']] = item(line['name'], line['amount'], line['date_in'], line['exp_date'])


# add relevant 'sold' info to the 'bought_dict'
            with open(general.sold_address, 'r', encoding="utf-8") as file:                   
                sold_file = csv.DictReader(file)
                for line in sold_file:
                    if comply_sold(args, line):
                        if line['in_id'] in bought_dictionary:
                            bought_dictionary[line['in_id']].amount = int(bought_dictionary[line['in_id']].amount) -  int(line['amount'])



# here, all relevant available info on bought items is provided
            print("Item:           Count:  Bought:         Expired:")
            for class_item in bought_dictionary:
                if int(bought_dictionary[class_item].amount) > 0:
                    print(bought_dictionary[class_item].name.ljust(15), str(bought_dictionary[class_item].amount).ljust(7), \
                        bought_dictionary[class_item].bought.ljust(15), bought_dictionary[class_item].expired)

                    if bought_dictionary[class_item].name in bought_dict:
                        bought_dict[ bought_dictionary[class_item].name ] = bought_dict[ bought_dictionary[class_item].name ] + int(bought_dictionary[class_item].amount)
                    else: bought_dict[bought_dictionary[class_item].name ] = int(bought_dictionary[class_item].amount)


# here, info on bought items is condenced to one line per item
            print("")
            print("Condensed Info")
            if len(bought_dict) > 0:    
                print("Item:           Count:")
                for item in bought_dict:
                    print(item.ljust(15), bought_dict[item])

# if required, data is stored in a file
            if args.filename != None:
                with open (args.filename, 'w', newline ="", encoding="utf-8") as file:
                    info_out_file = csv.writer(file)
                    info_out_file.writerow(["id", "name", "amount left", "Date in", "Date expired"])

                    for class_item in bought_dictionary:
                        if int(bought_dictionary[class_item].amount) > 0:
                            info_out_file.writerow(class_item, (bought_dictionary[class_item].name), (bought_dictionary[class_item].amount), \
                        bought_dictionary[class_item].bought, bought_dictionary[class_item].expired)

        except:
            print("File 'bought.csv' and/or 'sold.csv' corrupt")
    else:
        print("File 'bought.csv' and/or 'sold.csv' missing")

