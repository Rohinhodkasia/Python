import paramiko
import time
import yaml

with open("config.yaml") as commonfile:
    config = yaml.load(commonfile, Loader=yaml.FullLoader)

username = config["credentials"]["username"]
password = config["credentials"]["password"]

def MasterSSH(ip):
    # sshClient=""
    try:
        sshClient = paramiko.SSHClient()
        sshClient.load_system_host_keys()
        sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshClient.connect(ip, username=username, password=password)
        print("logged in :", ip, "\n")
    except Exception as error:
        print("\n error from ssh_login : ", error, "\n")
    return sshClient


def MasterWrite(sshClient,command):
    try:
        ssh_stdin, ssh_stdout, ssh_stderr = sshClient.exec_command(command)
        data = ssh_stdout.read().decode()

    except Exception as error:
        print("Error from MasterWrite Func :",error)
    return data


def Modulecheck(sshClient, modulename,ip):
    try:
        command = "sudo pidof "+modulename
        PID = MasterWrite(sshClient,command)
    except Exception as error:
        print("Error from ModuleCheck Func :",error)
    return PID


def CuBinaryCheck(sshClient,command):
    binary =""
    try:
        data = MasterWrite(sshClient,command)
        length = len(data)
        idx = data.index("->") + 2
        binary = str(data[idx:length])

    except Exception as error:
        print("\n error from CuBinaryCheck : ", error, "\n")
    return binary


def DUBinaryCheck(sshClient,command):
    binary =""
    try:
        data = MasterWrite(sshClient,command)
        length = len(data)
        idx = data.index("->") + 2
        binary = str(data[idx:length])

    except Exception as error:
        print("\n error from DuBinaryCheck Func : ", error, "\n")
    return binary


def MemoCheck(sshClient,command,ip):
    try: 
        data = MasterWrite(sshClient,command)
        idx = data.index("%")-2
        size = data[idx:idx+3]
    except Exception as error:
        print("\n error from MemoCheck Func : ", error, "\n")
    return size


def FreeMemo(sshClient,command):
    # freespace =""
    try:
        freespace = MasterWrite(sshClient,command)

    except Exception as error:
        print("\n error from FreeMemo Func : ", error, "\n")

    return freespace


def IRQBalancerStatus(sshClient,command):
    IRQstatus = 0
    try:
        data = MasterWrite(sshClient,command)
        if "active (running)" in data:
            IRQstatus = 1
        else:
            IRQstatus = 0

    except Exception as error:
        print("\n error from ssh_login : ", error, "\n")
    return IRQstatus


def IRQBalancerStop(sshClient,command):
    # IRQStatus = 1
    try:
        MasterWrite(sshClient,command)
        # data = IRQBalancerStatus(sshClient,command)
        # if "active (running)" not in data:
        #     IRQStatus = 0

    except Exception as error:
        print("Error from IRQBalancerStop Func :",error)
    
    # return IRQStatus



def checkHugePages(sshClient,command):
    try:
        # command = "grep HugePages_Free /proc/meminfo "
        data = MasterWrite(sshClient,command)
        length = len(data)
        idx = data.index(":") + 1
        HugePages_Free = int(data[idx:length])
        # print(HugePages_Free)
    except Exception as error:
        print("Exception from Func checkHugePages : ",error)   
    return HugePages_Free

def CleanHugePages(sshClient,command):
    try:
        channel= sshClient.invoke_shell()
        channel.send("sudo -i"+"\n")
        time.sleep(1)
        channel.send(command+"\n")
        time.sleep(1)

    except Exception as error:
        print("Error from CleanHugePages Func :",error)

def podsStatus(ssh,command):
    try:
        time.sleep(1)
        channel= ssh.invoke_shell()
        channel.send("sudo -i"+"\n")
        time.sleep(1)
        channel.send(command+"\n")
        time.sleep(2)
        resp= channel.recv(9999).decode()
    except Exception as error:
        print("Error from podsStatus func :",error )
    return resp


def datastore(data):
    try:
        filename = 'logs/pods.txt'
        with open (filename, 'w') as file:  
            file.write(data)  
    except Exception as error:
        print("Error from datastore Func :",error)
    return filename


def dataread(filename):
    try:
        with open(filename, 'r') as log:
            lines = log.readlines()

        for line in lines:
            if "<none>" in line:
                print(line)
            else:
                pass
    except Exception as error:
        print("Error from dataread Func :",error)

def PTPcheck(sshClient,command):
    ptpstatus = 0
    try:
        data = MasterWrite(sshClient,command)
        idx = data.index("et") + 3
        ptp = int(data[idx:len(data)])
        if ptp in range(-300,300):
            ptpstatus =1
        else:
            ptpstatus = 0

    except Exception as error:
        print("Error from PTPcheck Func :",error)
    return ptp,ptpstatus


def UpfCheck(sshClient,command):
    try:
        data = MasterWrite(sshClient,command)
    except Exception as error:
        print("Error from UpfCheck Func :",error)
    return data



def spacecheck(sshClient,command):
    try: 
        data = MasterWrite(sshClient,command)
        # idx = data.index("%")-2
        # size = data[idx:idx+3]
        print(data)
    except Exception as error:
        print("\n error from spacecheck Func : ", error, "\n")

    return data









    


    
    