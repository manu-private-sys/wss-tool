#!/usr/bin/python3

# Imports Section
import argparse, os, stat, sys, subprocess
from colorama import Fore

# Function Menu start
def menu():
    os.system('clear')
    print (Fore.RED + "\n\t\t######################\n\t\t#" + Fore.GREEN + " WSS\tOPS\tTOOL " + Fore.RED + "#\n\t\t######################")
    print (Fore.BLUE + "\nSelect the function you want to perform :\n")
    print (Fore.GREEN + "a)" + Fore.MAGENTA + " Information about the tool's functionality\n\n" + Fore.GREEN + "b)" + Fore.MAGENTA + " Active Session Download from ProxySG\n\n" + Fore.GREEN + "c)" + Fore.MAGENTA + " DNS Check from ProxySG\n\n" + Fore.GREEN + "d)" + Fore.MAGENTA + " Fetch Concentrator Status of a Region\n\n" + Fore.GREEN + "e)" + Fore.MAGENTA + " Force Core Dump on ProxySG\n\n" + Fore.GREEN + "f)" + Fore.MAGENTA + " ProxySG Restart Regular\n\n" + Fore.GREEN + "g)" + Fore.MAGENTA + " ProxySG Status\n\n" + Fore.GREEN + "h)" + Fore.MAGENTA + " Clear SSL CACHE on ProxySG\n\n" + Fore.GREEN + "x)" + Fore.MAGENTA + " Exit")
# Function Menu End

# Function Sub menu Start
def sub_menu():
    print (Fore.BLUE + "\n Do you want to continue, press : ")
    print (Fore.GREEN + "m)" + Fore.MAGENTA + " Return to main menu\n" + Fore.GREEN + "x)" + Fore.MAGENTA + " Exit ")
    sub_char = input(Fore.BLUE + "\n Enter your choice (m/x) : " + Fore.RESET)
    choice = sub_char

    if choice == 'm':
            menu()
    elif choice == 'x':
            print(Fore.RESET)
            exit()

    else:
            sub_menu()
# Function sub_menu End

# Function action start
def action(input):
    choice = input

    # Based on the value derived for choice run respective functionality
    if choice == 'b':
        active_fullcommand = ("python3 /tmp/WSS-TOOL/SCRIPTS/PYTHON-SCRIPTS/Active-Session-Download.py")
        p1 = subprocess.run(active_fullcommand,shell=True)
        sub_menu()

    elif choice == 'c':
        dns_fullcommand = ("python3 /tmp/WSS-TOOL/SCRIPTS/PYTHON-SCRIPTS/DNS-Check-ProxySG.py")
        p2 = subprocess.run(dns_fullcommand,shell=True)
        sub_menu()

    elif choice == 'd':
        fetch_fullcommand = ("python3 /tmp/WSS-TOOL/SCRIPTS/PYTHON-SCRIPTS/Fetch-Concentrator-Status.py")
        p3 = subprocess.run(fetch_fullcommand,shell=True)
        sub_menu()

    elif choice == 'e':
        force_fullcommand = ("python3 /tmp/WSS-TOOL/SCRIPTS/PYTHON-SCRIPTS/Force-Core-Dump.py")
        p4 = subprocess.run(force_fullcommand,shell=True)
        sub_menu()

    elif choice == 'a':
        print ("\nTo view the info file, please open a new session to bastion host and execute the below command on it : \n")
        print ("cat /tmp/WSS-TOOL/SCRIPTS/help-and-info.txt\n")
        sub_menu()

    elif choice == 'f':
        restart_fullcommand = ("python3 /tmp/WSS-TOOL/SCRIPTS/PYTHON-SCRIPTS/ProxySG-Restart-Regular.py")
        p5 = subprocess.run(restart_fullcommand,shell=True)
        sub_menu()

    elif choice == 'g':
        status_fullcommand = ("python3 /tmp/WSS-TOOL/SCRIPTS/PYTHON-SCRIPTS/ProxySG-Status.py")
        p6 = subprocess.run(status_fullcommand,shell=True)
        sub_menu()

    elif choice == 'h':
        cert_fullcommand = ("python3 /tmp/WSS-TOOL/SCRIPTS/PYTHON-SCRIPTS/ProxySG-Certificate-Revocation.py")
        p7 = subprocess.run(cert_fullcommand,shell=True)
        sub_menu()

    elif choice == 'x':
        print ("Exiting" + Fore.RESET)
        exit()

    else:
        print ("Invalid Choice entered, please enter correct choice")
        sub_menu()
# Function action end

# Function action_argument start
def action_argument(input):
    choice = input

    # Based on the value derived for choice run respective functionality
    if choice == 'b':
        active_fullcommand = ("python3 /tmp/WSS-TOOL/SCRIPTS/PYTHON-SCRIPTS/Active-Session-Download.py")
        p1 = subprocess.run(active_fullcommand,shell=True)

    elif choice == 'c':
        dns_fullcommand = ("python3 /tmp/WSS-TOOL/SCRIPTS/PYTHON-SCRIPTS/DNS-Check-ProxySG.py")
        p2 = subprocess.run(dns_fullcommand,shell=True)

    elif choice == 'd':
        fetch_fullcommand = ("python3 /tmp/WSS-TOOL/SCRIPTS/PYTHON-SCRIPTS/Fetch-Concentrator-Status.py")
        p3 = subprocess.run(fetch_fullcommand,shell=True)

    elif choice == 'e':
        force_fullcommand = ("python3 /tmp/WSS-TOOL/SCRIPTS/PYTHON-SCRIPTS/Force-Core-Dump.py")
        p4 = subprocess.run(force_fullcommand,shell=True)

    elif choice == 'a':
        print ("\nTo view the info file, please open a new session to bastion host and execute the below command on it : \n")
        print ("cat /tmp/WSS-TOOL/SCRIPTS/help-and-info.txt\n")

    elif choice == 'f':
        restart_fullcommand = ("python3 /tmp/WSS-TOOL/SCRIPTS/PYTHON-SCRIPTS/ProxySG-Restart-Regular.py")
        p5 = subprocess.run(restart_fullcommand,shell=True)

    elif choice == 'g':
        status_fullcommand = ("python3 /tmp/WSS-TOOL/SCRIPTS/PYTHON-SCRIPTS/ProxySG-Status.py")
        p6 = subprocess.run(status_fullcommand,shell=True)

    elif choice == 'h':
        cert_fullcommand = ("python3 /tmp/WSS-TOOL/SCRIPTS/PYTHON-SCRIPTS/ProxySG-Certificate-Revocation.py")
        p7 = subprocess.run(cert_fullcommand,shell=True)

    elif choice == 'x':
        print ("Exiting" + Fore.RESET)
        exit()

    else:
        print ("Invalid Choice entered, please re-run and enter correct choice")
# Function action_argument end

# Setting options for input
selection = {
        'a': "Information about the tool's functionality",
        'b': "Active Session Download from ProxySG",
        'c': "DNS Check from ProxySG",
        'd': "Fetch Concentrator Status of a Region",
        'e': "Force Core Dump on ProxySG",
        'f': "ProxySG Restart Regular",
        'g': "ProxySG Status",
        'h': "ProxySG Clear SSL Cache",
        'x': "Exit"
        }

# Catching selected option
def get_selection(selection_char):
    return selection.get(selection_char.lower())

# Initializing Parser
parser = argparse.ArgumentParser()

# Adding Argument
parser.add_argument("-", "--selection", type=str, help="Enter the selection character representing the choice - a b c d e f g h x")
args = parser.parse_args()

# Argument Passed Options, Assign Passed Argument to variable
if args.selection:
    choice = args.selection
    # print (choice)
    # Based on the value derived for choice run respective functionality
    action_argument(choice)

else:
    # Menu Driven Options, Loop in menu screen until exit

    # Calling menu function to print the menu screen at start
    menu()

    # Loop Menu until exit
    while True:
        selection_char = input(Fore.BLUE + "\nEnter a character representing the choice (a - x): " + Fore.RESET)
        choice = selection_char
        # Based on the value derived for choice run respective functionality
        action(choice)
