#!/usr/bin/python3
# Python program
# Final Version

# Imports Section
import subprocess, pexpect, os, stat, time, sys
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

# Argument passed values function call
def arg_active_session(arg1, arg2, arg3):
    # Passing in Site name
    sitename = arg1
    site_check(sitename)
    site = (sitename+"-")

    # Passing in DP no
    dp = arg2
    dpno = ("dp"+dp+"-")
    site_check(site+"dp"+dp)

    # Passing in ProxySG no
    proxysg = arg3
    proxysgno = ("proxysg"+proxysg)

    # Creating Site String
    site = (site+dpno+proxysgno)
    entered_site = site
    site_check(site)

    # Set input file as Global ProxySG cache file
    inputFile = "/tmp/WSS-TOOL/SITE-REGIONS/proxysg.csv"

    # Remove if there is file with same name at the destination path
    ssh_cred_file = ("/tmp/WSS-TOOL/SSH-CREDS/"+userid+"active-session-proxysg-site-ips.csv")
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

    # Formating Date to desired format
    date = datetime.datetime.now().strftime("%b%d%Y")

    filename = (date+"-"+value+".html")
    active_session_filename = filename

    # Creating full Curl Command Line
    # Insert the password for ProxySG admin replacing XXXXXXX in below line
    password = (base64.b64decode(b'YzEwdWRibHUz').decode("utf-8"))
    starturl = "curl -ku admin:"+password+" https://"
    endurl =  ":8082/AS/Sessions -o "
    fullcommand = (starturl+ip+endurl+filename)

    dir_path = "/tmp/WSS-TOOL/ACTIVE-SESSIONS/"
    dir_path = (dir_path+user)

    # Create Download Directory if it does not exist

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        os.chmod(dir_path,stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    # Change to path for storing Active Session files
    os.chdir(dir_path)
    filename = (dir_path+"/"+filename)

    # Remove if there is file with same name at the destination path
    if os.path.exists(filename):
        os.remove(filename)

    # Downloading Active Session Data
    print("\nDownloading Active Session ... ")

    # Writing Session Data to local file
    outputfile = open(f'{filename}', 'w')
    os.chmod(filename,stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)
    p1 = subprocess.Popen(fullcommand, shell=True, stdout=outputfile)
    # Need to check subprocess is completed or not
    p1.communicate()


    # Check if emty file is downloaded or not

    print (Fore.MAGENTA + "\nACTIVE SESSION FILE name with path is : \n")
    print (Fore.GREEN + filename)

    if os.path.getsize(filename) == 0:
        print ("\nUh. Ohh... Empty File Downloaded\nPlease try Downloading Manually!!!\n")

        # Writing error details to log file

        log_user = os.getlogin()
        log_script_name = os.path.basename(__file__)
        log_filename = log_script_name.replace("py","log")
        command = "Empty file downloaded\n"
        end = "Check command statements"
        log_message = (command+end)
        log_program_status = "Job Failed."
        logger.log_add(log_user,log_filename,log_message,log_program_status)

    else:
        print (Fore.BLUE + "\nDownload Completed!!!\n")

        # Writing success details to log file

        log_user = os.getlogin()
        log_script_name = os.path.basename(__file__)
        log_filename = log_script_name.replace("py","log")
        log_program_status = "Job Successful."
        command = "Entered site name is : "
        tail = "Active Session File downloaded Successfully to Bastion Host, and presented with GCloud SCP Command to download"
        log_message = (command+entered_site+"\n"+tail)
        logger.log_add(log_user,log_filename,log_message,log_program_status)

    # Print download command message

    print (Fore.MAGENTA + "You can download Active Sessions File to local machine using the below steps : \n")

    scpstart = "gcloud compute scp gce-prod-ops-auto-vm:"
    filename = str(filename)
    scpstart = str(scpstart)
    scpfile = scpstart+filename
    scpend = " . --project=saas-sed-wss-deployment --zone=us-west1-a"
    scpfullcommand = (scpfile+scpend)
    print (Fore.MAGENTA + "Step 1) Download Active Sessions File to CyberArk Bastion Host using (Run from CyberArk Bastion) :\n")
    print (Fore.GREEN + scpfullcommand+"\n")

    scpstart2 = "scp "
    scpuser = os.getlogin()
    filename = str(active_session_filename)
    scpstart = str(scpstart)
    scppart = "@wssops@10.2.220.231@psmpren.pam.broadcom.net:/home/wssops/"
    scpend2 = " ."
    scpfullcommand2 = (scpstart2+scpuser+scppart+filename+scpend2)
    print (Fore.MAGENTA + "Step 2) Download Active Sessions File from CyberArk Bastion Host to local system using (Run from local machine) :\n")
    print (Fore.GREEN + scpfullcommand2+"\n")

# End of Argument passed values function

arg_active_session(sys.argv[1], sys.argv[2], sys.argv[3])
