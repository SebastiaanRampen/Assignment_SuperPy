SuperPy

This program keeps track of the inventory. Depending on the Python-version, the program is called by 'main.py' or 'python3 main.py', followed by the appropriate comment-list. The following comments enable the following options:

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
