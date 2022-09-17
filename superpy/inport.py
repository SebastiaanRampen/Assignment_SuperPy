import os
import csv


def inport(args, general):
    if args.name != None and args.amount != None and args.price != None and args.expired != None:
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
        except:
            print('Incorrect input. Need input of product-name, amount, price and expiration data')
    else:
        print('Incomplete input. Need input of product-name, amount, price and expiration data')
# https://youtu.be/q5uM4VKywbA
# Python Tutorial: CSV Module - How to Read, Parse, and Write CSV Files
