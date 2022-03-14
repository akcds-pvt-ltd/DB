from csv import reader, writer
from ping3 import ping, verbose_ping 
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def csv_option():
    csv_name = "Client.csv" #input("\nWhat is the name of your CSV file?: ")
    with open(csv_name, 'r') as read_obj, open('outfile.csv', 'w', newline='') as file:
        csv_reader = reader(read_obj)
        csv_writer = writer(file)
        csv_writer.writerow(['Hostname', 'RAM Usage', 'Disk Usage', 'OS Version'])
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
                csv_writer.writerow([str(ip) + " is down"])
                print(str(ip) + " is down!")
            else:
                ssh.connect(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2], list_of_rows[rows][3])
                #ssh.connect(host, port, username, password)
                stdin, stdout, stderr = ssh.exec_command("hostname")
                pcname = stdout.readline()
                print(pcname)
                stdin, stdout, stderr = ssh.exec_command("wmic ComputerSystem get TotalPhysicalMemory")
                totalram = stdout.readlines()[1]
                print(totalram)
                stdin, stdout, stderr = ssh.exec_command("wmic OS get FreePhysicalMemory")
                freeram = stdout.readlines()[1]
                print(freeram)
                ramusage = ((int(totalram)-(int(freeram)*1024))/int(totalram))*100 
                print(str(ramusage))
                stdin, stdout, stderr = ssh.exec_command("ver")
                version = stdout.readlines()[1]
                print(version)
                stdin, stdout, stderr = ssh.exec_command("wmic logicaldisk get size, freespace, caption")
                disk1 = stdout.readlines()[1]
                a,b= [int(word) for word in str(disk1).split() if word.isdigit()]
                c=(a/b)*100
                print("Disk Usage:" + str("%.0f" % c)+"%")
                fileName = "Remote"
               	backupFile = open(fileName + ".txt", "a")
               	backupFile.write("\n\n" + str(pcname) + "Ram Usage:" + str("%.0f" % ramusage) + "%" + "\nDisk Usage:" + str("%.0f" % c) +"%" +"\n"+ str(version))
               	csv_writer.writerow([str(pcname), str("%.0f" % ramusage), str("%.0f" % c), str(version)])
          
csv_option()

