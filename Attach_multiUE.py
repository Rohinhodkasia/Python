import subprocess
import os
import time
import threading
import sys
import time
import yaml
import CommonFunc
from CommonFunc import *

with open("cfg/multiUE_config.yaml") as commonfile:
    config = yaml.load(commonfile, Loader=yaml.FullLoader)
    

logfile = sys.argv[1]
gctpath = sys.argv[2]
chv_ip = sys.argv[3]
chv = sys.argv[4]
username = sys.argv[5]
password = sys.argv[6]
t1 = "Attach_"+time.ctime().replace(" ", "_")+".log"
attlogfile =logfile+t1

def nfnReset():
    resetStatus = 0
    try:
        ssh = CommonFunc.ssh_login(chv_ip,username,password)
        out = CommonFunc.ssh_write(ssh,chv)
        if "VA response:ok" in out :
            resetStatus = 1
            time.sleep(10)
        
        return resetStatus
    except Exception as error:
        print("Error from nfnReset Func :",error)


def CheckAttach(attlogfile):
        print("Started Attaching Process")
        os.chdir(gctpath)
        flag=0
        try:
            with open(attlogfile, "w") as f:
                proc = subprocess.Popen("sudo ./run.sh",stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin=subprocess.PIPE,shell=True,bufsize=0)
                while 1:
                    out=proc.stdout.readline()
                    
                    f.write(out.decode())
                    if  b'[LIB:Sock]bind done' in out:
                        status = nfnReset()
                        if status == 1:
                            time.sleep(10)
                            break
                    
                
                my_thread = threading.Thread(target=atfun, args=(proc,attlogfile),)
                # Start the thread
                my_thread.start()

                #print("thrread started")       
                time.sleep(20)
                
                #print("after sleep")
                #Checking if ip is attached to tun0pdn7
                fetched_ip= fetch_ip()

                if not fetched_ip == 0:
                    flag=1
                    print("Attach successfully on IP: ",fetched_ip)
                    proc.stdin.write(b'dbg sim 1')
                    time.sleep(3)
                else:
                    print("Not found IP,Unable to attach")
                    # time.sleep(10)
                    subprocess.Popen("sudo ./kill.sh",stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin=subprocess.PIPE,shell=True,bufsize=0)
                    print("Process Killed")
                    my_thread.join(10)
            print("Logfile at path: ",attlogfile)
            return flag        
                                                                          
        except Exception as error:
            print("Error occured",error)

def atfun(proc,attlogfile):
    with open(attlogfile, "a+") as f:
        
        proc.stdin.write(b'\n')
        time.sleep(2)            
        proc.stdin.write(b'at+cfun=1 \n')
        print("at+cfun=1 cmd executed succesfully")
        tstart=time.time()+30
        while 1:
            out=proc.stdout.readline()
            print(out.decode())
            f.write(out.decode())
            tstop=time.time()
            if tstop>tstart:
                break


#To check UE attached and fetch its IP address
def fetch_ip():
    proc1 = subprocess.Popen("ifconfig",stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin=subprocess.PIPE,shell=True,bufsize=0)
    attatchdata = proc1.stdout.readlines()
    length=len(attatchdata)
    fetched_ip=0
    for i in range(0,length):
        if "tun0pdn7" in str(attatchdata[i]):
            if 'inet' in str(attatchdata[i+1]):
                ip=str(attatchdata[i+1])
                split_wrds=ip.split(" ")
                print("IP Found in tun0pdn7",split_wrds[9])
                fetched_ip=split_wrds[9]
                print("type",type(fetched_ip))
                # if "192.68." in str(fetched_ip):
                #     pass
                # else:
                #     fetched_ip=0
                break
    print(fetched_ip)
    return fetched_ip

#Calling the attch
CheckAttach(attlogfile)
