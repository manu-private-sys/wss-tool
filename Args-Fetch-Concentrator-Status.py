#!/usr/bin/python3
# Python program
# Final Version

#Imports Section
import subprocess, sys, os, stat, string, threading
import paramiko, datetime, logger, base64


# Argument passed values function call
def arg_fetch_status(arg1):
    # Passing sitename as argument
    entered_site = arg1
    return entered_site
# End of argument passing function

site = arg_fetch_status(sys.argv[1])
entered_site = site

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

    print ("\nCould not get any IPs!\nMAKE SURE YOU'VE ENTERED SITE-NAME CORRECTLY!!!")

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
    print ("\nConcentrator IP addresses are :")
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

# Start of threading function
outlock = threading.Lock()

def workon(host):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(command)
    a = (stdout.read().decode())
    print (a)

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
# End of threading function

# Start of main function
def main():
    hosts = ips # Pass in all the IP Addresses
    threads = []
    for h in hosts:
        t = threading.Thread(target=workon, args=(h,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
# End of main function

main()
