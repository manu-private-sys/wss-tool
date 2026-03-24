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

# Check if host is back online or not
port=22
delay = 10
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
# End of function

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
print (Fore.RED + "\n!!! WARNING !!!\n!!! YOU SHOULD BE RUNNING THIS ONLY WHEN PRODUCT ADVISES TO DO SO !!!\n!!! DO NOT RUN THIS SCRIPT UNNECESSARILY !!!\n!!! IT WILL FORCE REBOOT THE PROXYSG !!!")

# Start of argument passing function
def arg_force_core_dump(arg1,arg2,arg3):

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
    ssh_cred_file = ("/tmp/WSS-TOOL/SSH-CREDS/"+userid+"force-core-proxysg-site-ips.csv")
    if os.path.exists(ssh_cred_file):
        os.remove(ssh_cred_file)

    # Create new file - force-core-proxysg-site-ips.csv under SSH-CREDS to store the details of ProxySG of particular site
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

    child.sendline('restart abrupt')
    print ("\nWaiting for 5 mins for the ProxySG to complete reboot ...\n")

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
    a = 300
    while a != 0:
        print (f"{a}  ", end="\r", flush=True)
        time.sleep(1)
        a = a-1

    # Check if host is up or not
    if checkHost(ip, port):
        print (ip + " is UP")

        # To use Curl to download the ProxySG page, from which version and timestamp needs
        # to be extracted.

        # Phase 1 - Get ProxySG Console page downloaded

        curlstart = "curl -ku admin:"+password+" https://"
        curlmiddle = ":8082/CM/Core_image -o "
        dir_path = "/tmp/WSS-TOOL/TEMP-CORE-DUMP-FILES/"
        curl_filename = (userid+"webpage.txt")
        curlfullcommand = (curlstart+ip+curlmiddle+dir_path+curl_filename)
        p1 = subprocess.run(curlfullcommand,shell=True)

        # Phase 2 - Get timestamp and version from webpage.txt to detail.txt

        cat = "cat "
        grep = "| grep -i details"
        operator = " > "
        output = (userid+"temp_details.txt")
        detailsgrep = (cat+dir_path+curl_filename+grep+operator+dir_path+output)
        p2 = subprocess.run(detailsgrep,shell=True)

        # Cut the first line alone from temp-datails.txt if there are multiple timestamp lines

        head_command = "head -1 "
        output1 = (userid+"temp-details-new.txt")
        first_line_command = (head_command+dir_path+output+operator+dir_path+output1)
        p5 = subprocess.run(first_line_command,shell=True)

        # Phase 3 - Get version from details file and convert to filename format

        cut_version_1 = "cut -d \"<\" -f 3 "
        version_temp_file1 = (userid+"version-details.txt")
        version_1_fullcommand = (cut_version_1+dir_path+output1+operator+dir_path+version_temp_file1)
        p3 = subprocess.run(version_1_fullcommand,shell=True)

        # Extracting version number alone

        cut_version_2 = "cut -d \">\" -f 2 "
        version_temp_file2 = (userid+"version.txt")
        version_2_fullcommand = (cut_version_2+dir_path+version_temp_file1+operator+dir_path+version_temp_file2)
        p4 = subprocess.run(version_2_fullcommand,shell=True)

        # Converting Version number to filename format

        version_file = (dir_path+version_temp_file2)
        version_filename = (dir_path+userid+"version_filename.txt")
        with open(version_file, "rt") as fin:
            with open(version_filename, "wt") as fout:
                for line in fin:
                    fout.write(line.replace('.', '_'))

        file = open(version_filename, 'r')
        version_data = str(file.read().strip())


        # Phase 4 - Get timestamp from details file and convert to file format

        cut_timestamp_1 = "cut -d \"?\" -f 2 "
        timestamp_temp_file1 = (userid+"timestamp-details.txt")
        timestamp_1_fullcommand = (cut_timestamp_1+dir_path+output1+operator+dir_path+timestamp_temp_file1)
        p6 = subprocess.run(timestamp_1_fullcommand,shell=True)

        # Extracting timestamp alone

        cut_timestamp_2 = "cut -d \"\\\"\" -f 1 "
        timestamp2_temp_file = (userid+"timestamp.txt")
        timestamp_fullcommand = (cut_timestamp_2+dir_path+timestamp_temp_file1+operator+dir_path+timestamp2_temp_file)
        p7 = subprocess.run(timestamp_fullcommand,shell=True)

        # Generating filename

        timestamp_file = (dir_path+timestamp2_temp_file)
        file = open(timestamp_file, 'r')
        timestamp_data=int(file.read())
        date_time = (pd.Timestamp(timestamp_data).strftime('_%d-%m-%y_%H_%M_%S_'))

        filename_start = (version_data+date_time)

        # Use Curl to download Core Dump and provide Gcloud command to download it locally

        curlstart = "curl -ku admin:"+password+" https://"
        curlmiddle = ":8082/CM/Core_image/Download/Memory?"
        curlend = " -o "
        dir_path = "/tmp/WSS-TOOL/CORE-DUMPS/"
        dir_path = (dir_path+user)
        core_dump_filename = "full.cwz"

        # Create Download Directory if it does not exist

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            os.chmod(dir_path,stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

        core_dump_command = (str(curlstart)+str(ip)+str(curlmiddle)+str(timestamp_data)+str(curlend)+str(dir_path)+"/"+str(filename_start)+str(core_dump_filename))
        print (Fore.MAGENTA + "\nCORE DUMP FILE name with path is :")
        print (dir_path+"/"+filename_start+core_dump_filename)
        filename = (dir_path+"/"+filename_start+core_dump_filename)
        dump_file = (filename_start+core_dump_filename)
        print (Fore.MAGENTA + "\nDownloading CORE DUMP FILE :\n")
        p8 = subprocess.run(core_dump_command,shell=True)

        # Print Gcloud command to download it locally

        print (Fore.MAGENTA + "\nYou can download Core Dump File to local machine using the below steps : \n")

        scpstart = "gcloud compute scp gce-prod-ops-auto-vm:"
        filename = str(filename)
        scpstart = str(scpstart)
        scpfile = scpstart+filename
        scpend = " . --project=saas-sed-wss-deployment --zone=us-west1-a"
        scpfullcommand = (scpfile+scpend)
        print (Fore.MAGENTA + "Step 1) Download Core Dump File to CyberArk Bastion Host using (Run from CyberArk Bastion) :\n")
        print (Fore.GREEN + scpfullcommand+"\n")

        scpstart2 = "scp "
        scpuser = os.getlogin()
        filename = str(dump_file)
        scpstart = str(scpstart)
        scppart = "@wssops@10.2.220.231@psmpren.pam.broadcom.net:/home/wssops/"
        scpend2 = " ."
        scpfullcommand2 = (scpstart2+scpuser+scppart+filename+scpend2)
        print (Fore.MAGENTA + "Step 2) Download Core Dump File from CyberArk Bastion Host to local system using (Run from local machine) :\n")
        print (Fore.GREEN + scpfullcommand2+"\n")

        # Writing success details to log file

        log_user = os.getlogin()
        log_script_name = os.path.basename(__file__)
        log_filename = log_script_name.replace("py","log")
        log_program_status = "Job Successful."
        command = "Entered site name is : "
        end = "Full Core Dump File downloaded Successfully to Bastion Host, and presented with GCloud SCP Command to download"
        log_message = (command+entered_site+"\n"+end)
        logger.log_add(log_user,log_filename,log_message,log_program_status)

    else:
        print (ip + Fore.MAGENTA + " is DOWN, PLEASE TRY STARTING IT BACK USING GCONSOLE AND GET CORE DUMP")

        # Writing error details to log file

        log_user = os.getlogin()
        log_script_name = os.path.basename(__file__)
        log_filename = log_script_name.replace("py","log")
        command = "HOST IS NOT UP AFTER REBOOT!!!\nEntered site name was: "
        tail = "\nPLEASE TRY STARTING IT BACK USING GCONSOLE AND GET CORE DUMP!!!"
        log_message = (command+entered_site+tail)
        log_program_status = "Job Failed."
        logger.log_add(log_user,log_filename,log_message,log_program_status)

# End of argument passing function

arg_force_core_dump(sys.argv[1],sys.argv[2],sys.argv[3])
