SuperPy

This program keeps track of the inventory. Depending on the Python-version, the program is called by 'main.py' or 'python3 main.py', followed by the appropriate comment-list. It is obligatory to enter a 'task'. This is the action that is requested by the user.

The task-options are:
'set_day': to set a date that the application perceives as 'today'
'in': to add a product to the inventory list
'out': to remove a product from the inventory list
'inv': to provide an inventory at the beginning of a selected date
'exp': to remove expired items from the list of available products
'rev': to display the revenue of a specific date
'prof': to display the profit of a specific date
'prod': to display the revenue and profit of all products bought on one day day, over a period of time. Some of the figures consist of line-plots, and they can only display data if for more than one day, all products have been sold or expired; it takes more than one data point to draw a line.

Other input items are:
'-n' or '--name': to enter the name of the product
'-a' or '--amount': to enter the the number of items that are added or removed
'-p' or '--price': to enter the the price for which an item is bought or sold
'-e' or '--expired': to enter the the expiration date of a product. The standard format is YYYY-MM-DD
'-d' or 'action_date': to enter the the date for which the action is performed, i.e. the purchase date or selling date. The standard format is YYYY-MM-DD. If no date is entered, the program will use the current date. Additional options are 'today' or 'yesterday'
'-s' or '--start': to enter the the start-date when data-info from several days is requested. The standard format is YYYY-MM-DD
'--end': to enter the the end-date when data-info from several days is requested. The standard format is YYYY-MM-DD. If no date is entered, the program will use the current date. Additional options are 'today' or 'yesterday'
'-f' or '--filename': to enter the the filename, in case the data has to be stored in a file

Below, the different tasks are discussed in more detail.

'set_day' - add a date that the application perceives as 'today'.
This is a recepy for disaster, as incorrect or sloppy use of this option will f\*ck up your database, but it was part of the assignment. It is an optional setting that allows the user to perform actions with a selected date as the 'current' date. The entered date remains stored and used until replaced by another date, and should be provided as YYYY-MM-DD, or as 'yesterday' or 'today'. For other actions, the date, selected with 'set_day', is ignored when also an action date is provided. By setting the date as 'today', the application will act as if no date is stored; this is the recommended setting. if no 'action_date' is selected, 'today' will be stored. An example is:

> > > main.py set_day --action_date 2022-07-30

'in' - add a new product to the inventory.
Obligatory info is the name of the product (-n or --name), the amount of items (-a or --amount), the price of one item (-p or --price) and the expiring date (-e or --expired). The expiring date must follow the action-date. When provided, the date, stored as 'today' (see above) will be used as the 'current' date. It is optional to include an action date. An example is:

> > > main.py in --action_date 2022-07-30 --name tomato --amount 10 --price 0.6 --expired 2022-08-02

'out' - remove a product from the inventory.
Obligatory info is the name of the product (-n or --name), the amount of items (-a or --amount), the price of one item (-p or --price) of the product. Expired products will not be selected with this option, and also, products that have been bought after the date used as 'current date' will not be selected. When provided, the date, stored as 'today' (see above) will be used as the 'current' date. It is optional to include an action date. An example is:

> > > main.py out --action_date today --name tomato --amount 10 --price 0.6

'inv' - displays the inventory at the beginning of a selected date.
Obligatory info is only the word 'inv'; optional is to add the 'action_date' i.e. the date for which the inventory should be given. When provided, the date stored as 'today' (see above) will be used as the 'current' date. If no date is provided, the current date is used. Also optional is to save the info under the provided file-name. An example is:

> > > main.py inv --action_date 2022-08-02 --filename inventory_2022_08_02.csv

'exp' - indicates and removes products from the inventory that are expired.
Obligatory info is the word 'exp'. When provided, the 'set_day' date or 'action_date' (see above) will be used as the 'current' date. It is optional to include an action date. An example is:

> > > main.py exp

'rev' - indicates the revenue on the sales at the beginning of a specific date.
Obligatory info is only the word 'rev'. When provided, the date, stored as 'today' (see above) will be used as the 'current' date. It is optional to include an action date. An example is:

> > > main.py rev --action_date 2022-08-02

'prof' - indicates the total profit on the sales of products at the beginning of a specific date.
Obligatory info is only the word 'prof'. When provided, the date, stored as 'today' (see above) will be used as the 'current' date. It is optional to include an action date. An example is:

> > > main.py prof --action_date 2022-08-02

'prod' - indicates the revenue and profit per day, over a period of time. It also indicates the amount of days before the expiration-date that items are sold, and it shows the info in graphs. With this option, bought products are ignored if not all items are sold or expired.
Obligatory info is only the word 'prod'; optional is to enter a start and/or end date, to enter the name of a particular product, and it is optional to save the info under the provided file-name. An example is:

> > > main.py prod --start 2022-05-01 --end 2022-08-02 --name tomato --filename product_info.csv
