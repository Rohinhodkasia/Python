import time
import subprocess
import threading
import multi_UE_MU
import CommonFunc
import sys

dl_data= sys.argv[1]
dl_time= sys.argv[2]
dlport = sys.argv[3]
logfile = sys.argv[4]
dn_ip = sys.argv[5]
username = sys.argv[6]
password = sys.argv[7]

t1 = "Downlink_"+time.ctime().replace(" ", "_")+".log"
DL_logfile = logfile+t1


#Downlink Commands
def execute_cmd_downlink(ssh,attched_ip):
    print("Downlink process Started",attched_ip)
    
    #Calling arp common Commands
    CommonFunc.arp_common_cmd(ssh,attched_ip)
    
     #Executing the UE server command
    thread_dl = threading.Thread(target=run_data)
    thread_dl.start()
   
    # proc = subprocess.Popen("sudo iperf -s -u -i 1 -p 8001",stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin=subprocess.PIPE,shell=True,bufsize=0)
    # print("Executed iperf command successfully on UE server")
    time.sleep(10)
    print("Executing Iperf command at DN")
    _,stdout,_=ssh.exec_command("sudo iperf -u -c  "+str(attched_ip)+" -p "+ dlport +" -l 1380 -b "+dl_data+"m -t "+dl_time+" -i 1"+"\n")
    time.sleep(5)
    print("Command executed succesfully")

   
    #stopping the thread
    thread_dl.join()
    
    print("starting capturing logs")
    out=CommonFunc.read_last_line(DL_logfile)
    if not None:
        try:
            result=out[-2].split(" ")
            my_dict = {'Time_Interval':[result[3], "sec"], 
                'Transfer_Data': [result[6],"MBytes"],
                'Bandwidth':[result[9],"Mbits/sec"],
                'Avg_Data_Loss':[result[18],result[19]]
                }
            print(my_dict)
        except (IndexError, ValueError):
            print("Error: The Data has not processed")
    
    print("Downlink Process completed")
    print("Logfile at path: ",DL_logfile)
    return True

#downlink iperf command
def iperf_at_DN_Downlink(ssh,attched_ip):
    #Passing iperf command to DN Client
    
    ssh.exec_command("sudo iperf -u -c  "+str(attched_ip)+" -p "+dlport +" -l 1380 -b "+dl_data+"m -t "+dl_time+" -i 1")
    # time.sleep(10)


def run_data():
    proc = subprocess.Popen("sudo iperf -s -u -i 1 -p "+dlport,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin=subprocess.PIPE,shell=True,bufsize=0)
    print("Executed iperf command successfully on UE server")

    tstart=time.time()+float(dl_time)+10
    print("start",tstart)
    with open(DL_logfile, "w") as f:
        while 1:
            line = proc.stdout.readline()
            f.write(line.decode() + "\n")
            tstop=time.time()
            #print("stop",tstop)
            if tstop>tstart:
                break
            else:
                #print("..............")
                pass


ssh_client=multi_UE_MU.ssh_login(dn_ip,username,password)
fetched_ip= CommonFunc.fetch_ip()
execute_cmd_downlink(ssh_client,fetched_ip)
