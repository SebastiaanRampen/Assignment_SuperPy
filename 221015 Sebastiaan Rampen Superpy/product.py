import os
import csv
import datetime
from matplotlib import pyplot as plt

from rich.console import Console
from rich.table import Table
from rich.theme import Theme

custom_theme = Theme({ "no_data" : "orange3", "error" : "bold red", "info" : "bright_yellow" })
console = Console(theme = custom_theme)

# https://docs.python.org/3/library/decimal.html


def product(args, general):

    class item:
        def __init__(self, date_in, date_expired, amount_in, amount_out, bought, sold):
            self.date_in = date_in
            self.date_expired = date_expired
            self.amount_in = amount_in
            self.amount_out = amount_out
            self.bought = bought
            self.sold = sold


    class before_expired:
        def __init__(self, amount_items, nr_of_days):
            self.amount_items = amount_items
            self.nr_of_days = nr_of_days

    data_dictionary = {} # contains dictionaries for specific dates that contain 'class item' info from bought products
    date_and_nr_of_days_dict = {} # contains dictionaries for specific dates that contain arrays that contain 'class before_expired' 
                                  # info on nr of items that were sold, and the number of days before expiration-date
    time_before_expired_dictionary = {} # contains info on how many products have been sold how many days before the expired-date


# check if the info from the 'bought' file meets, when relevant, the criteria of start-date, end-date, and item-name
    def comply_bought(args, line):
        if args.start == None or datetime.datetime.strptime(line["date_in"], "%Y-%m-%d") >= datetime.datetime.strptime(args.start, "%Y-%m-%d"):
            if args.end == None or datetime.datetime.strptime(line["date_in"], "%Y-%m-%d") <= datetime.datetime.strptime(args.end, "%Y-%m-%d"):
                if args.name == None:
                    return True
                elif args.name == line["name"]:
                    return True
        return False

# return, when listed in the 'data_dictionary', the purchase date
    def id_in_dictionary(id):
# day = the 'name' of the selected dictionary from data_dictionary
# day_data = the dictionary that contains several 'item' entries, which are labeled by id of the bought-products  
        for day, day_data in data_dictionary.items():
            if id in day_data:
                return day
        return None


# This is where the task 'product' starts
    print('')
    if os.path.exists(general.bought_address) and os.path.exists(general.sold_address):
        try:
# list relevant bought-data in 'data_dictionary'
            date_list_for_dictionary = []
            with open(general.bought_address, 'r', encoding='utf-8') as file:
                bought_file = csv.DictReader(file)
                for line in bought_file:
                    if comply_bought(args, line):
                        if not line['date_in'] in data_dictionary:
                            data_dictionary[line['date_in']] = {}
                            date_list_for_dictionary.append(line['date_in'])
# data_dictionary is a dictionary which contains other dictionaries.
# Those 'internal' dictionaries are labeled by the 'date_in' text, and contain classes of the type 'item', which are labeled by 'id'
# In the following part, another item with an ID-label is added to the selected date_in-dictionary inside the data_dictionary
                        data_dictionary[line['date_in']][line['id']] = item(line['date_in'], \
                             line['exp_date'], line['amount'], 0, line['price'], 0)

# complement 'data-dictionary' info with relevant sold-data
            with open(general.sold_address, 'r', encoding='utf-8') as file:
                sold_file = csv.DictReader(file)
                for line in sold_file:
                    id_date = id_in_dictionary(line['in_id']) 
                    if id_date != None:
                        data_dictionary[id_date][line['in_id']].amount_out += int(line['amount'])
                        if line['price'] != 'expired':
                            data_dictionary[id_date][line['in_id']].sold += int(line['amount']) * float(line['price'])

# add info on the number of days a product is sold before expiring
                        if line['price'] == 'expired':
                            days_before_expired = -1
                        else:
                            days_before_expired = round((datetime.datetime.strptime(data_dictionary[id_date][line['in_id']].date_expired, "%Y-%m-%d") \
                                - datetime.datetime.strptime(line['date'], "%Y-%m-%d")).total_seconds() / (24 * 60 * 60))

                        if not id_date in date_and_nr_of_days_dict:
                            date_and_nr_of_days_dict[id_date] = []
                        date_and_nr_of_days_dict[id_date].append(before_expired(line['amount'], days_before_expired))


# these lists are later used as data in figures
            date_list = []
            nr_of_items_list = []
            bought_list = []
            sold_list = []
            profit_list = []
            profit_per_item_list = []

            nr_of_days_array = []

# print relevant info per day, and fill the figure-data-lists            
            if args.name == None:
                table = Table(title='Info on all products')
            else:
                table = Table(title=f'Info on {args.name}')

            table.add_column("Date")
            table.add_column("Nr. of Items", justify = "right")
            table.add_column("Price Bought", justify = "right")
            table.add_column("Price Sold", justify = "right")
            table.add_column("Profit per Item", justify = "right")

            if len(date_list_for_dictionary) > 1:
                date_list_for_dictionary.sort() # array with all the dates for which data is stored

                for selected_date in date_list_for_dictionary:
                    date_data = data_dictionary[selected_date] # temporary store the dictionary for a specific date (date-info) 
                                                           # from the data-dictionary into 'date_data

                    sum_amount = 0
                    sum_bought = 0
                    sum_sold = 0

                    all_products_sold = True
                    for id_data in date_data:
                        if int(date_data[id_data].amount_in) != int(date_data[id_data].amount_out): 
                            all_products_sold = False


                    if all_products_sold == True:
                        for id_data in date_data:
                            sum_amount += int(date_data[id_data].amount_out)
                            sum_bought += int(date_data[id_data].amount_out) * float(date_data[id_data].bought)
                            sum_sold += float(date_data[id_data].sold)

                        for class_in in date_and_nr_of_days_dict[selected_date]:
                            if not class_in.nr_of_days in time_before_expired_dictionary:
                                time_before_expired_dictionary[class_in.nr_of_days] = 0
                                nr_of_days_array.append(class_in.nr_of_days)
                            time_before_expired_dictionary[class_in.nr_of_days] += int(class_in.amount_items)

                        if sum_amount > 0:
                            date_list.append(selected_date)
                            nr_of_items_list.append(sum_amount)
                            bought_list.append(sum_bought)
                            sold_list.append(sum_sold)
                            profit_list.append(sum_sold - sum_bought)
                            profit_per_item_list.append((sum_sold - sum_bought) / sum_amount)
                            table.add_row(selected_date, str(sum_amount), "%.2f" % (sum_bought), "%.2f" % sum_sold, "%.2f" % ((sum_sold - sum_bought) / sum_amount))
                console.print(table)



    # these lists indicate the number of days that items are sold before expiring-date, and the number of items per day
                barplot_day_list = []
                barplot_nr_of_items = []

                print('')
                table2 = Table(title='nr. of days before expire-date')
                table2.add_column('Days before Expiring', justify = "right")
                table2.add_column("nr. of Items", justify = "right")
                nr_of_days_array.sort

                for days in nr_of_days_array:
                    barplot_day_list.append(days)
                    barplot_nr_of_items.append(time_before_expired_dictionary[days])
                    if days == str(-1):
                        table2.add_row('Expired', str(time_before_expired_dictionary[days]))
                    else:
                        table2.add_row(str(days), str(time_before_expired_dictionary[days]))

                console.print(table2)


    # when required, store data in a file
                if args.filename != None:
                    with open (args.filename, 'w', newline ="", encoding="utf-8") as file:
                        info_out_file = csv.writer(file)

                        if args.name == None:
                            info_out_file.writerow(['Info in time on all products'])
                        else:
                            info_out_file.writerow(['Info in time on ' + args.name])


                        info_out_file.writerow(["Date", "nr of items", "Bought for", "Sold for", "Profit per item"])

                        for i in range(len(date_list)):
                            info_out_file.writerow([date_list[i], nr_of_items_list[i], "%.2f" % bought_list[i], \
                                "%.2f" % sold_list[i], "%.2f" % profit_per_item_list[i]])

                        info_out_file.writerow([])
                        info_out_file.writerow(['nr. of days before expired'])
                        for i in range(len(nr_of_days_array)):
                            if nr_of_days_array[i] == str(-1):
                                info_out_file.writerow(['Expired', barplot_nr_of_items[i]])
                            else:
                                info_out_file.writerow([barplot_day_list[i], barplot_nr_of_items[i]])



# https://youtu.be/UO98lJQ3QGI
# Matplotlib Tutorial (Part 1): Creating and Customizing Our First Plots

# I found it easier to indicate number of days on the x-axes instead of full date-info.
                day_list = []
                for item in date_list:
                    day_list.append(round((datetime.datetime.strptime(item, "%Y-%m-%d") \
        - datetime.datetime.strptime(date_list[0], "%Y-%m-%d")).total_seconds() / (24 * 60 * 60)) + 1 )


    #creating four figure-plots
                fig, ax = plt.subplots(2,2)
                
                ax1 = ax[0,0]
                ax1.plot(day_list, profit_list)
                ax1.set_title('Total profit per day')
                ax1.set_xlabel('Days from ''day 1'' ')
                ax1.set_ylabel('Total profit')

                ax2 = ax[0,1]
                ax2.plot(day_list, bought_list, label='Items bought')
                ax2.plot(day_list, sold_list, label = 'items sold')
                ax2.set_title('Items bought and sold per day')
                ax2.set_xlabel('Days from ''day 1'' ')
                ax2.set_ylabel('Costs / Revenue')
                ax2.legend()

                ax3 = ax[1,0]
                ax3.plot(day_list, profit_per_item_list)
                ax3.set_title('Profit per item per day')
                ax3.set_xlabel('Days from ''day 1'' ')
                ax3.set_ylabel('Profit per item')

                ax4 = ax[1,1]
                ax4.bar(barplot_day_list, barplot_nr_of_items)
                ax4.set_title('Sold before expiring')
                ax4.set_xlabel('Days (-1 = not sold but expired)')
                ax4.set_ylabel('Nr of items')

                plt.tight_layout()
                plt.show()


            if len(day_list) < 2:
                print('')
                console.print('Profit for a day can only be calculated when all items, bought on a specific day,', style = "no_data")
                if len(day_list) == 1:
                    console.print(' have been sold. In this case, only for one day, all products have been sold.', style = "no_data")
                else:
                    console.print(' have been sold. In this case, for not a single day, all products have been sold.', style = "no_data")
                console.print('As no line can be drawn between less than two datapoints, not all figures will show line-plots.', style = "no_data")
                console.print ('This is no error in the program, but a lack of suitable data.', style = "no_data")
                print('')

        except:
            console.print("File 'bought.csv' and/or 'sold.csv' corrupt", style = "error")
            print('')
    else:
        console.print("File 'bought.csv' and/or 'sold.csv' missing", style = "error")
        print('')

