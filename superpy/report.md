SuperPy

This program keeps track of the inventory. Depending on the Python-version, the program is called by 'main.py' or 'python3 main.py', followed by the appropriate comment-list. It is obligatory to enter a 'task'. This is the action that is requested by the user, and the task-options are:
'in': to add a product to the inventory list
'out': to remove a product from the inventory list
'stock': to display which items are currently in stock
'inv': to provide an inventory at the beginning of a selected date
'exp': to remove expired items from the list of available products
'rev': to display the revenue of a specific date
'prof': to display the profit of a specific date
'prod': to display the revenue and profit per day, over a period of time. Some of the figures consist of line-plots, and they can only display data if more than one date is provided; it takes more than one data point to draw a line.

Other input items are:
'-n' or '--name': to enter the name of the product
'-a' or '--amount': to enter the the number of items that are added or removed
'-p' or '--price': to enter the the price for which an item is bought or sold
'-e' or '--expired': to enter the the expiration date of a product
'-d' or 'action_date': to enter the the date for which the action is performed, i.e. the purchase date or selling date. The standard format is YYYY-MM-DD. If no date is entered, the program will use the current date. Additional options are 'today' or 'yesterday'
'-s' or '--start': to enter the the start-date when data-info from several days is requested
'--end': to enter the the end-date when data-info from several days is requested
'-f' or '--filename': to enter the the filename, in case the data has to be stored in a file

Below, the different tasks are discussed in more detail.

'in' - add a new product to the inventory.
Obligatory info is the name of the product (-n or --name), the amount of items (-a or --amount), the price of one item (-p or --price) and the expiring date (-e or --expired). An example is:

> > > main.py in --name tomato --amount 10 --price 0.6 --expired 2022-08-02

'out' - remove a product from the inventory.
Obligatory info is the name of the product (-n or --name), the amount of items (-a or --amount), the price of one item (-p or --price) and the expiring date (-e or --expired) of the product. An example is:

> > > main.py out --name tomato --amount 10 --price 0.6 --expired 2022-08-02

'stock' - displays which items are currently in stock.
Obligatory info is only the word 'stock'; optional is to display the stock for a specific item, and/or to save the info under the provided file-name. An example is:

> > > main.py stock --name tomato --filename current_stock.csv

'inv' - displays the inventory from a selected date.
Obligatory info is only the word 'inv'; optional is to add the 'action_date' i.e. the date for which the inventory should be given. If no date is provided, the current date is used. Also optional is to save the info under the provided file-name. An example is:

> > > main.py inv --action_date 2022-08-02 --filename inventory_2022_08_02.csv

'exp' - indicates and removes products from the inventory that are expired.
Obligatory info is the word 'exp'. An example is:

> > > main.py exp

'rev' - indicates the revenue of a specific date.
Obligatory info is only the word 'rev'; optional is to add the 'action_date' i.e. the date for which the revenue should be calculated. If no date is provided, the current date is used. An example is:

> > > main.py rev --action_date 2022-08-02

'prof' - indicates the profit of a specific date.
Obligatory info is only the word 'rev'; optional is to add the 'action_date' i.e. the date for which the profit should be calculated. If no date is provided, the current date is used. An example is:

> > > main.py prof --action_date 2022-08-02

'prod' - indicates the revenue and profit per day, over a period of time. It also indicates the amount of days before the expiration-date that items are sold, and it shows the info in graphs. With this option, bought products are ignored if not all items are sold or expired.
Obligatory info is only the word 'prod'; optional is to enter a start and/or end date, to enter the name of a particular product, and it is optional to save the info under the provided file-name. An example is:

> > > main.py prod --start 2022-05-01 --end 2022-08-02 --name tomato --filename product_info.csv
