import os


def save_set_today(args, general):
    if args.action_date != None:
        try:
            with open(general.set_today, 'w', newline ="", encoding="utf-8") as file:
                file.write(args.action_date)
            print("set date to:", args.action_date)
            print('')
        except:
            print("Can't save data in file")
    else:
        print("Incomplete input. Need input of a date, or 'today' or 'yesterday'")




#  if args.action_date == None:
#         if os.path.exists(general.set_today):
#             file = open(general.set_today)
#             main.args.action_date = file.read()
#         else:
#             args.action_date = datetime.date.today().strftime("%F")
#     if args.action_date.lower() == 'today':
#         args.action_date = datetime.date.today().strftime("%F")
#     if args.action_date.lower() == 'yesterday':
#         args.action_date = (datetime.date.today()-1).strftime("%F")

#     if args.end != None: