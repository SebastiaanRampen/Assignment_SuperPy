import os
import csv

def outport(args, general):
    if not os.path.exists(general.bought_address):
        print("No file of bought products available")
    elif args.name != None and args.amount != None and args.price != None and args.expired != None:    
        try:
            in_list_bought = []
            in_list_match = []
            product_left = 0
# check presence in storage, put relevant 'bought' data in 'in_list_bought', 
# and their ids in 'in_list_match'
            with open(general.bought_address, 'r', encoding="utf-8") as file:
                    bought_file = csv.DictReader(file)
                    for line in bought_file:
                        in_list_bought.append(line)    
                        if line["exp_date"] == args.expired and line["name"] == args.name \
                            and line["amount_left"] != 0:
                            in_list_match.append(line["id"])
                            product_left += int(line["amount_left"])

            if product_left < args.amount:
                print("Entered amount is higher than items currently present")
            else:
               
                if not os.path.exists(general.sold_address):  
#if needed, create sold.csv
                    with open (general.sold_address, 'w', newline ="", encoding="utf-8") as file:
                        input_file = csv.writer(file)
                        input_file.writerow(general.sold_fieldnames)
                    sold_id = 1

                else:
#else, find last id-value
                    out_list = []
                    with open(general.sold_address, 'r', encoding="utf-8") as file:
                        sold_file = csv.DictReader(file)
                        for line in sold_file:
                            out_list.append(line)

                    sold_id = int(out_list[-1]["id"] ) +1

# append lines to 'sold.csv, and update lines that should later go back in bought.csv
                with open (general.sold_address, 'a', newline ="", encoding="utf-8") as file:
                    input_file = csv.writer(file)
                    amount = args.amount
                    i = 0
                    index = 0
                    while amount > 0:
                        while in_list_match[i] != in_list_bought[index]["id"]:
                            index += 1

                        if int(in_list_bought[index]["amount_left"]) >= amount:
                            in_list_bought[index]["amount_left"] = \
                                int(in_list_bought[index]["amount_left"]) - amount
                            input_file.writerow([ sold_id, in_list_match[i], args.name, amount, args.price, args.action_date])                    
                            amount = 0
                        else:
                            amount -= int(in_list_bought[index]["amount_left"])
                            input_file.writerow([ sold_id, in_list_match[i], args.name, in_list_bought[index]["amount_left"], args.price, args.action_date])
                            in_list_bought[index]["amount_left"] = 0
                            i += 1
                            sold_id += 1

# save modified bought.csv data            
            with open (general.bought_address, 'w', newline ="", encoding="utf-8") as file:
                bought_file = csv.DictWriter(file, fieldnames= general.bought_fieldnames)
                bought_file.writeheader()
 
                for line in in_list_bought:
                    bought_file.writerow(line)

        except:
            print('Incorrect input. Need input of product-name, amount, price and expiration data')
    else:
        print('Incomplete input. Need input of product-name, amount, price and expiration data')


