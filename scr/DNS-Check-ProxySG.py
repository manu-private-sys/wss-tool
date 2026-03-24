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

# Defning site check function
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

# Otherwise continue
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

# Reading in Test Site Name

testsitename = input("\nEnter the Site name for which DNS test is to be done\n(DO NOT INCLUDE http:// or https:// IN THE SITE NAME)  : ")

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

# Creating full test dns Command Line

start1 = "test dns"
fullcommand1 = (start1+" "+testsitename)

# Creating full test http get Command Line

start2 = "test http get"
fullcommand2 = (start2+" "+testsitename)

# Creating full test threat-risk Command Line

start3 = "test threat-risk https://"
fullcommand3 = (start3+testsitename)

print ("\nUsing Command values on ProxySG: ")
command = [fullcommand1,fullcommand2,fullcommand3]
print(command)

# Login information
username = "admin"
password = (base64.b64decode(b'YzEwdWRibHUz').decode("utf-8"))

# Get data from ProxySG
def getdata(host,username,password,cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    a = (stdout.read().decode())
    print(Fore.GREEN + a)

    # Writing success details to log file

    log_user = os.getlogin()
    log_script_name = os.path.basename(__file__)
    log_filename = log_script_name.replace("py","log")
    log_program_status = "Job Successful."
    command = cmd
    message1 = "Entered site name is : "
    message2 = "Entered test site name is : "
    log_message = (message1+entered_site+"\n"+message2+testsitename+"\n"+command+"\n"+a)
    logger.log_add(log_user,log_filename,log_message,log_program_status)

    # Close ssh connection
    ssh.close()

# for loop with command list
def cmdlist(command,host,username,password):
    if len(command) != 0:
        for cmd in command:
            getdata(host,username,password,cmd)
    else:
        print("Command length is 0 -ZERO. Please input atlease 1 command")

cmdlist(command,host,username,password)
