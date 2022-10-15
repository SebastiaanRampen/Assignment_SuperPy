import os
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({ "no_data" : "orange3", "error" : "bold red", "info" : "bright_yellow" })
console = Console(theme = custom_theme)


def save_set_today(args, general):
    print ('')
    try:
        different_date = True
        if os.path.exists(general.set_today):
            file = open(general.set_today)
            if args.action_date.lower == file.read().lower:
                different_date = False

        if different_date == True:
            if args.action_date == None:
                args.action_date = 'today'
            with open(general.set_today, 'w', newline ="", encoding="utf-8") as file:
                file.write(args.action_date)
            console.print(f"Set date to: [info]{args.action_date}[/info]")
        else:
            console.print(f"The provided date, [info]{args.action_date}[/info] was already stored. No changes have been made.")

        print('')
    except:
        console.print("Can't save data in file", style ="error")
        print('')