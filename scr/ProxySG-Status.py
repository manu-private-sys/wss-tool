#!/usr/bin/python3
# Python program
# Final Version

# Imports Section
import subprocess, pexpect, os, stat, time, paramiko
import pandas as pd
import numpy as np
import datetime, pathlib, logger, base64
from colorama import Fore

# Getting username for file identification and logging purposes
user = os.getlogin()
userid = (user+"-")

# Defning site name check functionality
def site_check(site):

    # Set input file as Global ProxySG cache file
    inputFile = "/tmp/WSS-TOOL/SITE-REGIONS/proxysg.csv"

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

# End of function

# Site up or not checking function
def HostUp(hostname):
        if os.system("ping -c 1 " + hostname.strip(";") + " > /dev/null 2>&1") == 0:
            HOST_UP = True
        else:
            HOST_UP = False
        return HOST_UP

# End of function

# Reading in Site name
sitename = input("Enter the sitename(Ex - For Google Sites : ginmu1/gitmi11, for Azure Sites acnbj2/acnsh2) : ")
site_check(sitename)
site = (sitename+"-")

# Reading in DP no
dp = input("Enter the DP no(Ex 1/2/3 etc) : ")
dpno = ("dp"+dp+"-")
site_check(site+"dp"+dp)

# Reading in ProxySG no
proxysg = input("Enter the ProxySG no(Ex 1/2/3 etc) : ")
proxysgno = ("proxysg"+proxysg)

# Creating Site String
site = (site+dpno+proxysgno)
entered_site = site
site_check(site)

# Set input file as Global ProxySG cache file
inputFile = "/tmp/WSS-TOOL/SITE-REGIONS/proxysg.csv"

# Remove if there is file with same name at the destination path
ssh_cred_file = ("/tmp/WSS-TOOL/SSH-CREDS/"+userid+"dns-check-proxysg-site-ips.csv")
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

# Extracting ProxySG Name alone from ProxySG details file

df=pd.read_csv(ssh_cred_file,usecols=[0], names=['name'], header=None)
value=df['name'].to_string(header=False, index=False)
value = value.strip()
print (Fore.MAGENTA + "\nProxySG Name is: ")
print (Fore.BLUE + value)

# Extracting ProxySG IP alone from ProxySG details file

df=pd.read_csv(ssh_cred_file,usecols=[2], names=['name'], header=None)
ip=df['name'].to_string(header=False, index=False)
ip = ip.strip()
print (Fore.MAGENTA + "ProxySG IP is: ")
print (Fore.BLUE + ip)
host = ip

# Check if the provided ProxySG is up or not
value = HostUp(ip)

# If it is up, continue with fetching status procedure
if value == True:

    # Creating status Command Line

    cmd = "show status"
    cmd1 = "show active-sessions"

    # Login information

    username = "admin"
    password = (base64.b64decode(b'YzEwdWRibHUz').decode("utf-8"))

    # Get the Status data from ProxySG

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    a = (stdout.read().decode())
    print(Fore.GREEN + a)

    # Get Active Session Status data from ProxySG

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(cmd1)
    a = (stdout.read().decode())
    print(Fore.GREEN + a)

    # Writing success details to log file

    log_user = os.getlogin()
    log_script_name = os.path.basename(__file__)
    log_filename = log_script_name.replace("py","log")
    log_program_status = "Job Successful."
    command = cmd
    message1 = "Entered site name is : "
    message2 = "Show Status of ProxySG is completed "
    log_message = (message1+entered_site+"\n"+message2+"\n"+command+"\n"+a)
    logger.log_add(log_user,log_filename,log_message,log_program_status)

    # Close ssh connection
    ssh.close()

# If it is not up, print error message and exit
else:
    print (Fore.MAGENTA + ip + Fore.MAGENTA + " is DOWN OR NOT REACHABLE, PLEASE TRY STARTING IT BACK USING GCLOUD CONSOLE")

    # Writing error details to log file

    log_user = os.getlogin()
    log_script_name = os.path.basename(__file__)
    log_filename = log_script_name.replace("py","log")
    command = "HOST IS NOT UP OR REACHABLE!!!\nEntered site name was: "
    tail = "\nPLEASE TRY STARTING IT BACK USING GCLOUD GCONSOLE!!!"
    log_message = (command+entered_site+tail)
    log_program_status = "Job Failed."
    logger.log_add(log_user,log_filename,log_message,log_program_status)
