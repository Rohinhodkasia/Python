import yaml
import multi_UE_MU
import CommonFunc
import time
import threading

modules = ["localPubSub","csm","uemp"]

with open("cfg/multiUE_config.yaml") as commonfile:
    config = yaml.load(commonfile, Loader=yaml.FullLoader)

print("Select Enviornment \n 0 DEV \n 1 SIT \n ")
choice = int(input(">>> "))
if choice == 0:
    username = config["devcredentials"]["username"]
    password = config["devcredentials"]["password"]

    uev_localpubsub= config["devpath"]["uev_localpubsub"]
    uev_csm =config["devpath"]["uev_csm"]
    uev_uemp =config["devpath"]["uev_uemp"]

    commands=[uev_localpubsub,uev_csm,uev_uemp]

    path=config["devbinary"]["path"]
    gctpath = config["devbinary"]["gctpath"]
    dn_ip = config["devbinary"]["dn_ip"]
    chv_ip = config["devbinary"]["chv_ip"]
    chv = config["chvpaths"]["chv"]

    dlportlist = config["iperf"]["dlportlist"]
    ulportlist = config["iperf"]["ulportlist"]

    logfilepath=config["devlogfile"]["logfilepath"]

    attachcommand =config["devcommands"]["attachcommand"]
    uplinkcommand =config["devcommands"]["uplinkcommand"]
    downlinkcommand = config["devcommands"]["downlinkcommand"]

    Ue_list=[config["UEs"]["Ue_ip_1"],config["UEs"]["Ue_ip_2"],config["UEs"]["Ue_ip_3"],config["UEs"]["Ue_ip_4"],config["UEs"]["Ue_ip_5"]]


elif choice == 1:
    username = config["sitcredential"]["username"]
    password = config["sitcredential"]["password"]
    uev_localpubsub= config["sitpath"]["uev_localpubsub"]
    uev_csm =config["sitpath"]["uev_csm"]
    uev_uemp =config["sitpath"]["uev_uemp"]

    commands=[uev_localpubsub,uev_csm,uev_uemp]

    path=config["sitbinary"]["path"]
    gctpath = config["sitbinary"]["gctpath"]
    dn_ip = config["sitbinary"]["dn_ip"]
    chv_ip = config["sitbinary"]["chv_ip"]

    dlportlist = config["iperf"]["dlportlist"]
    ulportlist = config["iperf"]["ulportlist"]

    logfilepath=config["sitlogfile"]["logfilepath"]

    attachcommand =config["sitcommands"]["attachcommand"]
    uplinkcommand =config["sitcommands"]["uplinkcommand"]
    downlinkcommand = config["sitcommands"]["downlinkcommand"]

    Ue_list=[config["sitUE"]["Ue_ip_1"],config["sitUE"]["Ue_ip_2"],config["sitUE"]["Ue_ip_3"],config["sitUE"]["Ue_ip_4"],config["sitUE"]["Ue_ip_5"],config["sitUE"]["Ue_ip_6"]]



moduleup_list=[]
attach_list=[]

def module_up(ip,module_name,command):
    flag=0
    try:
        ssh=multi_UE_MU.ssh_login(ip,username,password)
        pid_status,pid=multi_UE_MU.SSHCheckPID(ssh,module_name,username)

        if pid_status==1:
            Killed_Status = multi_UE_MU.SShKillPID(ssh,pid,module_name,username)
            if Killed_Status ==1:
                multi_UE_MU.ran_moduleUp(command,ssh,module_name)
                pid_status,pid=multi_UE_MU.SSHCheckPID(ssh,module_name,username)
                if pid_status==1:
                    print(module_name+" is up successfully on machine ",ip,"PID :",pid)
                    flag = 1
                else:
                    print(module_name+" is not up on Ip: "+ip)
            else:
                print(module_name+" is not killed")
                
        else:

            multi_UE_MU.ran_moduleUp(command,ssh,module_name)
            pid_status,pid=multi_UE_MU.SSHCheckPID(ssh,module_name,username)
            if pid_status==1:
                print(module_name+" is up successfully on machine ",ip,"PID :",pid)
                flag = 1
            else:
                print(module_name+" is not up on IP: "+ip)
    except Exception as error:
        print("Error from function module_up: ",error)

    return flag


def main():
    ip_list=[]
    count=0

    #Printing the list of UEs IPs avilable
    print("List of UEs: \n")
    for i in Ue_list:
        print(str(count) +" : "+str(i))
        count=count+1

    choice = str(input("\nChoose UE to perform the Attach: "))
    result=choice.split(" ")
    for i in result:
        #appending the values of ips into list
        ip_list.append(Ue_list[int(i)])

    for ip in ip_list:
        thread = threading.Thread(target=up_thread, args=(ip,))
        thread.start()
    #waiting for thread to end
    time.sleep(5)
    thread.join()
    print("moduleup list",moduleup_list)

    if len(moduleup_list)>0:
        for ip in moduleup_list:
            thread1 = threading.Thread(target=attach_thread, args=(ip,))
            thread1.start()
        time.sleep(5)
        thread1.join()
        
        print("attach_list: ",attach_list)
        if len(attach_list)>0:
            while True:
                
                choice = str(input("To Run UL: 1\nTo run DL: 2\nTo run Bi-directional: 3\nTo Stop: 4\nEnter a value : "))
                if choice == "1":
                    uldata = str(input("UL Bandwidth : "))
                    ultime = str(input("UL time : "))
                    for ip,ulport in zip(attach_list,ulportlist):
                        thread2 = threading.Thread(target=ul_thread, args=(ip,uldata,ultime,ulport,))
                        thread2.start()
                    #waiting for thread to end
                    time.sleep(3)
                    thread2.join()
                elif choice == "2":
                    dldata = str(input("DL Bandwidth : "))
                    dltime = str(input("DL time duration : "))
                    for ip , dlport in zip(attach_list,dlportlist):
                        time.sleep(2)
                        thread3 = threading.Thread(target=dl_thread, args=(ip,dldata,dltime,dlport,))
                        thread3.start()
                    time.sleep(3)
                    thread3.join()
                elif choice == "3":
                    uldata = str(input("UL Bandwidth : "))
                    ultime = str(input("UL time duration: "))
                    dldata = str(input("DL Bandwidth : "))
                    dltime = str(input("DL time duration: "))

                    for ip,ulport,dlport in zip(attach_list,ulportlist,dlportlist):
                        time.sleep(2)
                        thread3 = threading.Thread(target=dl_thread, args=(ip,dldata,dltime,dlport,)).start()
                        thread2 = threading.Thread(target=ul_thread, args=(ip,uldata,ultime,ulport,)).start()
                        #starting the bidirectional process
                    
                    time.sleep(1)
                    thread3.join()
                    thread2.join()
                else:
                    break
            
        else:
            print("Attach is unsuccessful on all ips")
            
    else:
        print("No module is successfully up on any ip")
            


#function to up the modules for multi_ue
def up_thread(ip):
    for module_name,command in zip(modules,commands):
        status=module_up(ip,module_name,command)
    if status == 1:
        moduleup_list.append(ip)
    time.sleep(5)

#thread for attach
def attach_thread(ip):
    try:  
        ssh=CommonFunc.ssh_login(ip,username,password)
        command="cd "+ gctpath+"; pwd"
        #Checking binary if exist
        CommonFunc.ssh_writepid(ssh,command)
        filename = 'pids.txt'
        with open (filename, 'r') as file:  
            lines = file.readlines()
        for line in lines:
            if "Could not chdir to home directory /home/"+username+"@Netprizm.local: No such file or directory" in line:
                pass
            else:
                binary = str(line).strip()
        # _,stdout,_=ssh.exec_command(command)

        # binary=str(stdout.read().decode()).strip()
        if binary == gctpath:
            print(gctpath+" Binary found")

            #Running the Attach process at given IP
            print("Attaching is in process for ip: ",ip,"\n")
            _,stdout,_=ssh.exec_command(attachcommand+" "+logfilepath+" "+gctpath+" "+chv_ip+" "+chv+" "+username+" "+password)
            time.sleep(70)
            fetched_ip=CommonFunc.fetch_ip_multiUE(ssh)
            
            #Checking if UE is attached or not
            if fetched_ip != 0:
                print("Attach successful on: ",ip)
                attach_list.append(ip)
            else:
                print("Attach is unsuccessful on ",ip)
            print("Logfile at path: ",logfilepath,"\n")
            time.sleep(1)
        else:
            print("Binary not found ")

    except Exception as error:
        print("Error occured in Func attach_thread : ",error)

#threading function for uplink
def ul_thread(ip,uldata,ultime,ulport):
    ssh=multi_UE_MU.ssh_login(ip,username,password)
    print("Started the Uplink processon port ",ulport)
    
    ssh.exec_command(uplinkcommand+" "+uldata+" "+ultime+" "+ulport+" "+logfilepath+" "+dn_ip+" "+username+" "+password)
    time.sleep(int(ultime)+20)
    print("Uplink process Completed")
    
    print("Logfile at path: "+logfilepath+" in ip: "+ip,"\n")

def dl_thread(ip,dldata,dltime,dlport):
    ssh=multi_UE_MU.ssh_login(ip,username,password)
    print("Started the Downlink process on port",dlport)
    ssh.exec_command(downlinkcommand+" "+dldata+" "+dltime+" "+dlport+" "+logfilepath+" "+dn_ip+" "+username+" "+password)
    time.sleep(int(dltime)+20)
    print("Downlink process Completed")

    print("Logfile at path: "+logfilepath+" in ip: "+ip,"\n")



main()
