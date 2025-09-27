from colorama import Fore,init
init(autoreset=True)

def err_msg(msg):
    #print error msg in red
    print(Fore.RED+msg)

def display_menu(menu):
    print(Fore.LIGHTGREEN_EX+"menu: ")
    #for index, item in enumerate(menu,start = 0)
    for index,item in enumerate(menu):
        print(Fore.LIGHTGREEN_EX+f"{index}. "+Fore.RESET + f"{item}")
def user_prompt(prompt):
    return input(Fore.CYAN+prompt)
