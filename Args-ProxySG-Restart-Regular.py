#!/usr/bin/python3
# Python program
# Final Version

# Imports Section
import subprocess, pexpect, os, stat, time, paramiko, socket, sys
import pandas as pd
import numpy as np
import datetime, pathlib, logger, base64
from colorama import Fore

# Getting username for file identification and logging purposes
user = os.getlogin()
userid = (user+"-")

# Defning site name verification function
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
        HOST_UP = 0
        if os.system("ping -c 1 " + hostname.strip(";") + " > /dev/null 2>&1") is 0:
            HOST_UP = True
        else:
            HOST_UP = False
        return HOST_UP
# End of function

# Check if host is back online or not after reboot
port = 22
delay = 5
timeout = 3
retry = 2

# Start of port isOpen function
def isOpen(ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
                s.connect((ip, int(port)))
                s.shutdown(socket.SHUT_RDWR)
                return True
        except:
                return False
        finally:
                s.close()

# End of port isOpen function

# Start of checkHost function (site up or not functionality)
def checkHost(ip, port):
        ipup = False
        for i in range(retry):
            if isOpen(ip, port):
                ipup = True
                break
            else:
                time.sleep(delay)
        return ipup

# End of function

# Print warning notification
print (Fore.RED + "\n!!! WARNING !!!\n!!! YOU SHOULD BE RUNNING THIS ONLY WHEN PRODUCT ADVISES TO DO SO !!!\n!!! DO NOT RUN THIS SCRIPT UNNECESSARILY !!!\n!!! IT WILL REBOOT THE PROXYSG !!!")

# Start of argument passing function
def arg_proxysg_reboot_regular(arg1,arg2,arg3):
    # Reading in Site name
    sitename = arg1
    site_check(sitename)
    site = (sitename+"-")

    # Reading in DP no
    dp = arg2
    dpno = ("dp"+dp+"-")
    site_check(site+"dp"+dp)

    # Reading in ProxySG no
    proxysg = arg3
    proxysgno = ("proxysg"+proxysg)

    # Creating Site String
    site = (site+dpno+proxysgno)
    entered_site = site
    site_check(site)

    # Set input file as Global ProxySG cache file
    inputFile = "/tmp/WSS-TOOL/SITE-REGIONS/proxysg.csv"

    # Remove if there is file with same name at the destination path
    ssh_cred_file = ("/tmp/WSS-TOOL/SSH-CREDS/"+userid+"proxysg-restart-regular-ips.csv")
    if os.path.exists(ssh_cred_file):
        os.remove(ssh_cred_file)

    # Create new file - proxysg-restart-regular-ips.csv under SSH-CREDS to store the details of ProxySG of particular site
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

    df = pd.read_csv(ssh_cred_file,usecols=[0], names=['name'], header=None)
    value = df['name'].to_string(header=False, index=False)
    value = value.strip()
    print ("\nProxySG Name is: ")
    print (value)

    # Extracting ProxySG IP alone from ProxySG details file

    df = pd.read_csv(ssh_cred_file,usecols=[2], names=['name'], header=None)
    ip = df['name'].to_string(header=False, index=False)
    ip = ip.strip()
    print ("ProxySG IP is: ")
    print (ip)

    # Check if the provided ProxySG is up or not
    value = HostUp(ip)

    # If it is up, continue with reboot procedure
    if value == True:

        # Login information

        username = "admin"
        password = (base64.b64decode(b'YzEwdWRibHUz').decode("utf-8"))

        # Login to ProxySG

        print (Fore.MAGENTA + "\nEstablishing SSH Connection to ProxySG and issuing reboot command ...")
        host =(username+"@"+ip)
        child = pexpect.spawn("ssh -t -o stricthostkeychecking=no %s" %host)
        child.expect('password:')
        child.sendline(password)

        # Enable privileged mode in ProxySG

        child.sendline('en')
        child.expect('Password:')
        child.sendline(password)

        # Send in ProxySG reboot command, replace below command

        child.sendline('restart regular')
        #child.sendline('show status')
        print ("\nWaiting for 3 mins for the ProxySG to complete reboot ...\n")

        # Writing success details to log file

        log_user = os.getlogin()
        log_script_name = os.path.basename(__file__)
        log_filename = log_script_name.replace("py","log")
        log_program_status = "Reboot Initiated"
        command = "Entered site name is : "
        message = "Initiated ProxySG Restart"
        log_message = (command+entered_site+"\n"+message)
        logger.log_add(log_user,log_filename,log_message,log_program_status)

        # Printing countdown timer

        print ("Time to next job (in seconds) is: \n")
        a = 180
        while a != 0:
            print (f"{a}  ", end="\r", flush=True)
            time.sleep(1)
            a = a-1

        # Check if host is up or not after reboot command

        if checkHost(ip, port):
            print ("ProxySG - " + ip + " is UP")

            # Login to ProxySG

            print (Fore.MAGENTA + "\nEstablishing SSH Connection to ProxySG and checking status ...")
            host = ip

            # Get Status data from ProxySG

            ssh = paramiko.SSHClient()
            cmd = 'show status'
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username=username, password=password)
            stdin, stdout, stderr = ssh.exec_command(cmd)
            a = (stdout.read().decode())
            print(Fore.GREEN + a)

            # Get Active Session Status data from ProxySG

            cmd1 = 'show active-sessions'
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
            command = "Entered site name is : "
            message = "ProxySG Restart Successful"
            log_message = (command+entered_site+"\n"+message)
            logger.log_add(log_user,log_filename,log_message,log_program_status)

        else:
            # Else means it is not up after proceeding with reboot command using script

            print (ip + Fore.MAGENTA + " is DOWN, PLEASE TRY STARTING IT BACK USING GCLOUD CONSOLE")

            # Writing error details to log file

            log_user = os.getlogin()
            log_script_name = os.path.basename(__file__)
            log_filename = log_script_name.replace("py","log")
            command = "HOST IS NOT UP AFTER REBOOT!!!\nEntered site name was: "
            tail = "\nPLEASE TRY STARTING IT BACK USING GCLOUD CONSOLE!!!"
            log_message = (command+entered_site+tail)
            log_program_status = "Job Failed."
            logger.log_add(log_user,log_filename,log_message,log_program_status)

    # If it is not up before initiating reboot itself, then print error message and exit
    else:
        print (ip + Fore.MAGENTA + " is DOWN OR NOT REACHABLE, PLEASE TRY STARTING IT BACK USING GCLOUD CONSOLE")

        # Writing error details to log file

        log_user = os.getlogin()
        log_script_name = os.path.basename(__file__)
        log_filename = log_script_name.replace("py","log")
        command = "HOST IS NOT UP OR REACHABLE!!!\nEntered site name was: "
        tail = "\nPLEASE TRY STARTING IT BACK USING GCLOUD GCONSOLE!!!"
        log_message = (command+entered_site+tail)
        log_program_status = "Job Failed."
        logger.log_add(log_user,log_filename,log_message,log_program_status)

# End of argument passing function

arg_proxysg_reboot_regular(sys.argv[1],sys.argv[2],sys.argv[3])
