#!/usr/bin/python3
# Python program
# Final Version

#Imports Section
import subprocess, sys, os, stat, string, threading
import paramiko, datetime, logger, base64
import pandas as pd
import numpy as np
from colorama import Fore

# Getting username for file identification and logging purposes
user = os.getlogin()
userid = (user+"-")


# Defning site name check functionality
def site_check(site):

    # Set input file as Global ProxySG cache file
    inputFile = "/tmp/WSS-TOOL/SITE-REGIONS/concentrator.csv"

    # Remove if there is file with same name at the destination path
    ssh_cred_file = ("/tmp/WSS-TOOL/SSH-CREDS/"+userid+"temp-site-ips.csv")
    if os.path.exists(ssh_cred_file):
        os.remove(ssh_cred_file)

    # Create new file - proxysg-site-ips.csv under SSH-CREDS to store the details of ProxySG of particular site
    file1 = open(ssh_cred_file, "w")
    os.chmod(ssh_cred_file,stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)

    # Opening the given file in read-only mode
    with open(inputFile, 'r') as filedata:
        # Traverse in each line of the file
        for line in filedata:
            # Checking whether the given string is found in the line data
            if site in line:
                 # Print the line, if the given string(Sitename) is found in the current line
                 # Write the contents to the above opened new file
                file1.write(line)
    # Closing the input file
    filedata.close()
    file1.close()

    # Check if site name is correctly provided or not
    if os.path.getsize(ssh_cred_file) == 0:
        print ("\nUh. Ohh... Entered Site - " + Fore.MAGENTA + "\"" + site + "\"" + Fore.BLUE + " Could not be found!!!\nPlease try providing correct Site-Name next time!!!\n")

        # Writing error details to log file
        log_user = os.getlogin()
        log_script_name = os.path.basename(__file__)
        log_filename = log_script_name.replace("py","log")
        command_error = "Entered site name is (incorrect sitename): "
        entered_site = site
        log_message = (command_error+entered_site)
        log_program_status = "Job Failed."
        logger.log_add(log_user,log_filename,log_message,log_program_status)

        exit()

# End of Site name check function

# Site up or not checking function
def HostUp(hostname):
        if os.system("ping -c 1 " + hostname.strip(";") + " > /dev/null 2>&1") == 0:
            HOST_UP = True
        else:
            HOST_UP = False
        return HOST_UP

# End of Site up or not checking function

# Start of threading SSH function
outlock = threading.Lock()

def workon(host):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(command)
    a = (stdout.read().decode())
    print (Fore.GREEN + a)

    # Writing success details to log file

    log_user = os.getlogin()
    log_script_name = os.path.basename(__file__)
    log_filename = log_script_name.replace("py","log")
    log_program_status = "Job Successful."
    log_message = a
    logger.log_add(log_user,log_filename,log_message,log_program_status)

    # Closing SSH connection
    ssh.close()

    if not outlock:
	# This section comes into action, whenever there's an issue with threaded jobs

        print ("Could not SSH to : "+host+"\n!!! PLEASE TRY CHECKING STATUS MANUALLY !!!")

        # Writing error details to log file

        log_user = os.getlogin()
        log_script_name = os.path.basename(__file__)
        log_filename = log_script_name.replace("py","log")
        command_message = "Entered site name is : "
        tail_message = ("\nFailed to SSH to : "+host)
        log_message = (command_message+entered_site+tail_message)
        log_program_status = "Job Failed."
        logger.log_add(log_user,log_filename,log_message,log_program_status)
# End of threading SSH function

# Start of main function
def main():
    hosts = ips # Pass in all the IP Addresses
    threads = []
    for h in hosts:
        # Check if the provided Concentrator is up or not
        value = HostUp(h)

        # If it is up, continue with fetching status procedure
        if value == True:
            t = threading.Thread(target=workon, args=(h,))
            t.start()
            threads.append(t)
        else:
            print (Fore.MAGENTA + h + Fore.MAGENTA + " is DOWN OR NOT REACHABLE, PLEASE TRY STARTING IT BACK USING GCLOUD CONSOLE")

            # Writing error details to log file

            log_user = os.getlogin()
            log_script_name = os.path.basename(__file__)
            log_filename = log_script_name.replace("py","log")
            command = "HOST IS NOT UP OR REACHABLE!!!\nEntered site name was: "
            host = "\nHost IP is: "
            tail = "\nPLEASE TRY STARTING IT BACK USING GCLOUD GCONSOLE!!!"
            log_message = (command+entered_site+host+h+tail)
            log_program_status = "Job Failed."
            logger.log_add(log_user,log_filename,log_message,log_program_status)

    for t in threads:
        t.join()
  # End of main function

# Prompt user for input
site = input("Enter site name(Ex - For Google Sites : ginmu1/gitmi11, for Azure Sites acnbj2/acnsh2) : ")
site_check(site)
entered_site = site

# Prompt user for further input into dp selection
dp = input("Press \"Enter\" for all the Concentrator Status of this site / Type in DP No(1/2/3) for any specific Concentrator Status : ")

# Split input into site and concentrator IDs
args = site.split()
site = args[0] + "-"
concentrator_ids = args[1:] if len(args) > 1 else []

# Load the data from the file
with open('/tmp/WSS-TOOL/SITE-REGIONS/concentrator.csv', 'r', newline='') as f:
    data = f.readlines()

# Extract the relevant lines from the data
lines = [line for line in data if site in line]

# Extract the IP addresses of the relevant concentrators
ips = []
for line in lines:
    parts = line.split(",")
    concentrator_id = parts[0].split("-")[-2] # Extract concentrator ID from name
    if concentrator_ids and concentrator_id not in concentrator_ids:
        continue
    ip = parts[2]
    ip = ip.split()
    ips.append(ip[0])

# Check if ips list is empty or not
if not ips:

    print ("\nUh. Ohh... Entered Site - " + Fore.MAGENTA + "\"" + entered_site + "\"" + Fore.BLUE + " Could not be found!!!\nPlease try providing correct Site-Name next time!!!\n")

    # Writing error details to log file
    log_user = os.getlogin()
    log_script_name = os.path.basename(__file__)
    log_filename = log_script_name.replace("py","log")
    command_error = "Entered site name is (incorrect sitename): "
    log_message = (command_error+entered_site)
    log_program_status = "Job Failed."
    logger.log_add(log_user,log_filename,log_message,log_program_status)

else:
    # Print the IP addresses
    print (Fore.MAGENTA + "\nConcentrator IP addresses for all DP's in the site " + Fore.BLUE + entered_site + Fore.MAGENTA + " are :" + Fore.BLUE)
    print (*ips,sep = ", ")
    print ("\n")

    # Writing success details to log file

    log_user = os.getlogin()
    log_script_name = os.path.basename(__file__)
    log_filename = log_script_name.replace("py","log")
    command_site_success = "Entered site name is : "
    log_message = (command_site_success+entered_site)
    log_program_status = "CHECK THREAD EXECUTION OUTPUT BELOW :"
    logger.log_add(log_user,log_filename,log_message,log_program_status)

    # Login information
    username = "rescue"
    password = (base64.b64decode(b'Ymx1M2YwZyE=').decode("utf-8"))

    # Creating Commnand for exection once logged in
    command = ('password=`echo "Ymx1M2YwZyE="|base64 --decode`;echo $HOSTNAME && echo $password | sudo -S clishell -e sdc show detail|grep state')

# Making decision based on input whether status are to be displayed for all Concentrator or specific Concentrator
if dp == "":
    main()
else:
    # Do a site name check
    dpno = ("dp"+dp+"-")
    site = (site+dpno)
    site_check(site)

    # Opening the given file in read-only mode
    inputFile = "/tmp/WSS-TOOL/SITE-REGIONS/concentrator.csv"

    # Remove if there is file with same name at the destination path
    ssh_conc_cred_file = ("/tmp/WSS-TOOL/SSH-CREDS/"+userid+"check-conc-site-ips.csv")
    if os.path.exists(ssh_conc_cred_file):
        os.remove(ssh_conc_cred_file)

    # Create new file - check-conc-site-ips.csv under SSH-CREDS to store the details of Concentrator IP of particular DP
    file1 = open(ssh_conc_cred_file, "w")
    os.chmod(ssh_conc_cred_file,stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)

    with open(inputFile, 'r') as filedata:
    # Traverse in each line of the file
        for line in filedata:
        # Checking whether the given string is found in the line data
            if site in line:
            # Print the line, if the given string(Sitename) is found in the current line
            # Write the contents to the above opened new file
                file1.write(line)
    # Closing the input file
    filedata.close()
    file1.close()

    # Extracting exact Concentrator IP alone from Concentrator details file

    df=pd.read_csv(ssh_conc_cred_file,usecols=[2], names=['name'], header=None)
    ip=df['name'].to_string(header=False, index=False)
    ip = ip.strip()
    print (Fore.MAGENTA + "Concentrator IP is: ")
    print (Fore.BLUE + ip + "\n")
    host = ip
    workon(host)
