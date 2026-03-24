#!/usr/bin/python3
# Python program to push data to log files
# This logger file is to be used as Module in other scripts for logging purposes

# Imports Section
import sys, os, datetime

def log_add(user_name,program_name,log_message,program_status):
    # Writing errors to log file
    dir_path = "/tmp/WSS-TOOL/LOGS/"

    # Change to path for clearing previous cache files
    os.chdir(dir_path)

    # Collecting data
    date = str(datetime.datetime.now())
    user = ("User is : "+user_name)
    filename = program_name
    message = log_message
    status = program_status

    # Writing to log file
    log_outputfile = (dir_path+filename)
    log_data = ("\n\n"+date+"\n"+user+"\n"+message+"\n"+status+"\n")
    log_file = open(log_outputfile, "a")
    log_file.write(log_data)
    log_file.write("\n")
    log_file.close()
