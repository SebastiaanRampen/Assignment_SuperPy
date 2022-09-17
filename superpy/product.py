import os
import csv
import datetime
import collections
from matplotlib import pyplot as plt
# getcontext().prec = 2

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

    data_dictionary = {}
    time_before_expired_dictionary = {}

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
        for day, day_data in data_dictionary.items():
            if id in day_data:
                return day
        return None

    if os.path.exists(general.bought_address) and os.path.exists(general.sold_address):
        try:
# list relevant bought-data in 'data_dictionary'
            with open(general.bought_address, 'r', encoding='utf-8') as file:
                bought_file = csv.DictReader(file)
                for line in bought_file:
                    if comply_bought(args, line):
                        if not line['date_in'] in data_dictionary:
                            data_dictionary[line['date_in']] = {}
                        data_dictionary[line['date_in']][line['id']] = item(line['date_in'], line['exp_date'], line['amount'], \
                            0, line['price'], 0)

# complement 'data-dictionary' info with relevant sold-data
            with open(general.sold_address, 'r', encoding='utf-8') as file:
                sold_file = csv.DictReader(file)
                for line in sold_file:
                    id_date = id_in_dictionary(line['in_id']) 
                    if id_date != None:
                        data_dictionary[id_date][line['in_id']].amount_out += int(line['amount'])
                        if line['price'] != 'expired':
                            data_dictionary[id_date][line['in_id']].sold += int(line['amount']) * float(line['price'])

                        if line['price'] == 'expired':
                            days_before_expired = -1  
                        else:
                            days_before_expired = round((datetime.datetime.strptime(data_dictionary[id_date][line['in_id']].date_expired, "%Y-%m-%d") \
                                - datetime.datetime.strptime(line['date'], "%Y-%m-%d")).total_seconds() / (24 * 60 * 60))

                        if not str(days_before_expired) in time_before_expired_dictionary:
                            time_before_expired_dictionary[str(days_before_expired)] = 0
                        time_before_expired_dictionary[str(days_before_expired)] += int(line['amount'])

# these lists are later used as data in figures
            date_list = []
            nr_of_items_list = []
            bought_list = []
            sold_list = []
            profit_list = []
            profit_per_item_list = []

# print relevant info per day, and fill the figure-data-lists            
            print('')
            if args.name == None:
                print('Info in time on all products')
            else:
                print('Info in time on', args.name)
            for data_info, date_data in data_dictionary.items():
                sum_amount = 0
                sum_bought = 0
                sum_sold = 0

                for id_data in date_data:
                    if int(date_data[id_data].amount_in) == int(date_data[id_data].amount_out):
                        sum_amount += int(date_data[id_data].amount_out)
                        sum_bought += int(date_data[id_data].amount_out) * float(date_data[id_data].bought)
                        sum_sold += float(date_data[id_data].sold)
                        
                if sum_amount > 0:
                    date_list.append(data_info)
                    nr_of_items_list.append(sum_amount)
                    bought_list.append(sum_bought)
                    sold_list.append(sum_sold)
                    profit_list.append(sum_sold - sum_bought)
                    profit_per_item_list.append((sum_sold - sum_bought) / sum_amount)
                    print(data_info + ', nr. of items:', str(sum_amount) + ', bought for:', "%.2f" % (sum_bought) + ', sold for:', "%.2f" % sum_sold + \
                        ', profit per item:', "%.2f" % ((sum_sold - sum_bought) / sum_amount))

# these lists indicate the number of days that items are sold before expiring-date, and the number of items per day
            barplot_day_list = []
            barplot_nr_of_items = []

            print('')
            print('nr. of days before expired')
            time_before_expired_dictionary = collections.OrderedDict(sorted(time_before_expired_dictionary.items(), reverse=True))
            for days in time_before_expired_dictionary:
                barplot_day_list.append(days)
                barplot_nr_of_items.append(time_before_expired_dictionary[days])
                if days == str(-1):
                    print('Expired, nr. of items:', time_before_expired_dictionary[days])
                else:
                    print('days:', days + ', nr. of items:', time_before_expired_dictionary[days])

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
                    for i in range(len(barplot_day_list)):
                        if barplot_day_list[i] == str(-1):
                            info_out_file.writerow(['', 'Expired',  'nr. of items:', barplot_nr_of_items[i]])
                        else:
                            info_out_file.writerow(['Days:', barplot_day_list[i] , 'nr. of items:', barplot_nr_of_items[i]])    



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


        except:
            print("File 'bought.csv' and/or 'sold.csv' corrupt")
    else:
        print("File 'bought.csv' and/or 'sold.csv' missing")

