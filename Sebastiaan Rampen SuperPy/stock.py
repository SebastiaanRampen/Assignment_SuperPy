import os
import csv
import datetime

def comply(args, line):
    if int(line["amount_left"]) > 0:
        if args.name == None:
            return True
        elif args.name == line["name"]:
            return True
        else:
            return False

def stock(args, general):
    if os.path.exists(general.bought_address) and os.path.exists(general.sold_address):
        try:
            bought_dict = {}
            expired_dict = {}
            with open(general.bought_address, 'r', encoding="utf-8") as file:
                bought_file = csv.DictReader(file)
                bought_list = []

                print("Item:           Count:  Bought:         Expired:")
                for line in bought_file:
                    if comply(args, line):
                        if datetime.datetime.strptime(args.action_date, "%Y-%m-%d") > datetime.datetime.strptime(line["exp_date"], "%Y-%m-%d"):
                            print(line['name'].ljust(15), line['amount_left'].ljust(7), line['date_in'].ljust(15), line['exp_date'], 'Expired')
                            if args.filename != None:
                                bought_list.append([line['id'], line['name'], line['amount_left'], line['date_in'], line['exp_date'], 'Expired'])
                            if line['name'] in expired_dict:
                                expired_dict[ line['name'] ] = expired_dict[ line['name'] ] + int(line['amount_left'])
                            else: expired_dict[line['name'] ] = int(line['amount_left'])

                        else:
                            print(line['name'].ljust(15), line['amount_left'].ljust(7), line['date_in'].ljust(15), line['exp_date'])
                            if args.filename != None:
                                bought_list.append([line['id'], line['name'], line['amount_left'], line['date_in'], line['exp_date']])
                            if line['name'] in bought_dict:
                                bought_dict[ line['name'] ] = bought_dict[ line['name'] ] + int(line['amount_left'])
                            else: bought_dict[line['name'] ] = int(line['amount_left'])


            print('')
            print("Condensed Info in stock")
            if len(bought_dict) > 0:
                print("Item:           Count:")
                for item in bought_dict:
                    print(item.ljust(15), bought_dict[item])

            if len(expired_dict) > 0:
                print("")
                print("Condensed Info expired")
                print("Item:           Count:")
                for item in expired_dict:
                    print(item.ljust(15), expired_dict[item])
                print('')
                print("Consider removing the expired products.")
                print('')


            if args.filename != None:
                with open (args.filename, 'w', newline ="", encoding="utf-8") as file:
                    info_out_file = csv.writer(file)
                    info_out_file.writerow(["id", "name", "amount left", "Date in", "Date expired"])
                    for line in bought_list:
                        info_out_file.writerow(line)
                          
        except:
            print("File 'bought.csv' and/or 'sold.csv' corrupt")
    else:
        print("File 'bought.csv' and/or 'sold.csv' missing")    

