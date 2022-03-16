# All pre-installed besides Netmiko.
from csv import reader
from datetime import date, datetime
from netmiko import ConnectHandler
from ping3 import ping, verbose_ping 
import getpass
import os
import sys
import re

sys.tracebacklimit = 0

# Checks if the folder exists, if not, it creates it.
if not os.path.exists('backup-config'):
    os.makedirs('backup-config')

# Current time and formats it to the North American time of Month, Day, and Year.
now = datetime.now()
dt_string = now.strftime("%m-%d-%Y_%H-%M")

# Gives us the information we need to connect.
def get_saved_config(host, username, password, enable_secret):
    cisco_ios = {
        'device_type': 'cisco_ios',
        'host': host,
        'username': username,
        'password': password,
        'secret': enable_secret,
    }
    # Creates the connection to the device.
    net_connect = ConnectHandler(**cisco_ios)
    net_connect.enable()
    # Gets the running configuration.
    memory = net_connect.send_command("show proc mem")
    processor= net_connect.send_command("show proc CPU")
    # Gets and splits the hostname for the output file name.
    hostname = net_connect.send_command("show ver | i uptime")
    hostname = hostname.split()
    hostname = hostname[0]
    #--------------------------
    fileName1 = hostname + "_memory"
    fileName2 = hostname + "_CPU"
    #--------------------------
    backupFile = open("backup-config/" + fileName1 + ".txt", "w+")
    backupFile.write(memory)
    f= open("backup-config/" + fileName1 + ".txt", "r") 	
    p= f.readline()
    #print(p)
    a,b,c= [int(word) for word in p.split() if word.isdigit()]
    d= (b/a)*100
    if (d>40): print("Memroy Status of " + hostname + "is Critical: "+ str("%.0f" % d) + "%")
    #else: print ("Memory Status of " + hostname +" is OK: " + str("%.0f" % d) + "%")
    f.close()
    #---------------------------
    backupFile = open("backup-config/" + fileName2 + ".txt", "w+")
    backupFile.write(processor)
    f= open("backup-config/" + fileName2 + ".txt", "r")
    q= f.readline()
    #print(q)
    A= re.split(r" |%", q)
    m= A[5]
    if (int(m)>40): print("CPU Status of " + hostname + " is Critical: " + str(m) + "%")
    #else: print ("CPU Status of " + hostname + " is OK: " + str(m) + "%")
    f.close()


def csv_option():
    csv_name = "hosts.csv" #input("\nWhat is the name of your CSV file?: ")
    with open(csv_name, 'r') as read_obj:
        csv_reader = reader(read_obj)
        list_of_rows = list(csv_reader)
        #print(list_of_rows)
        rows = len(list_of_rows)
        #print(rows)
        while rows >= 2:
            rows = rows - 1
            #print(list_of_rows[rows][0])
            ip = list_of_rows[rows][0]
            ip_ping = ping(ip)
            if ip_ping == None:
                fileName = "downDevices_" + dt_string + ".txt"
                downDeviceOutput = open("backup-config/" + fileName, "a")
                downDeviceOutput.write(str(ip) + "\n")
                print(str(ip) + " is down!")
            else:
                get_saved_config(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2], list_of_rows[rows][3])
csv_option()
