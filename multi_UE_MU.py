import paramiko
import time

def ssh_login(ip,username,password):
    sshClient=""
    try:
        sshClient = paramiko.SSHClient()
        sshClient.load_system_host_keys()
        sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshClient.connect(ip, username=username, password=password,)
#        print("\n logged in :", ip, "\n")
    except Exception as error:
        print("\n error from ssh_login : ", error, "\n")
    return sshClient

def ssh_writepid(sshclient,command):
        data=""
        _stdin, _stdout, _stderr = sshclient.exec_command(command, get_pty=True)
        time.sleep(.5)
        data=_stdout.read().decode()
        filename = 'pids.txt'
        with open (filename, 'w') as file:  
            file.write(data)

def sshclose(sshclient,ip):
    try:
        sshclient.close()
        print("\n Connection closed with: "+ip+" \n")
    except Exception as error:
        print("\n error from sshclose : ", error, "\n")


def ssh_write(sshclient,command):
        data=""
        _stdin, _stdout, _stderr = sshclient.exec_command(command, get_pty=True)
        time.sleep(.5)
        data=_stdout.read().decode()
        return data

def ran_moduleUp(command,sshClient,modulename,):
    try:
        
        ssh_stdin, ssh_stdout, ssh_stderr = sshClient.exec_command(command)
        time.sleep(4)
    
    except Exception as error:
        print("\n error from ran_module : ", error, "\n")
        


def SSHCheckPID(sshclient,ModuleName,username):
    PIDStatus=0
    PId =""
    try:
        time.sleep(3)
        command="sudo pidof "+ModuleName
        ssh_writepid(sshclient,command)
        filename = 'pids.txt'
        with open (filename, 'r') as file:  
            lines = file.readlines()
        for line in lines:
            if "Could not chdir to home directory /home/"+username+"@Netprizm.local: No such file or directory" in line:
                pass
            else:
                PId = line

        if PId:
            PIDStatus=1
    except Exception as error:
        print("\n Error from CheckPID Func :",error, "\n")

    return PIDStatus,PId


def SShKillPID(loginobject,pid,modulename,username):
    Killed_Status = 0
    PId =""
    str = "Could not chdir to home directory /home/"+username+"@Netprizm.local: No such file or directory"
    try:
        command=f'sudo kill -9 {int(pid)}'
        ssh_writepid(loginobject,command)
        filename = 'pids.txt'
        with open (filename, 'r') as file:  
            lines = file.readlines()
        for line in lines:
            if line:
                if str in line:
                    continue
                else:
                    PId = line
        if PId=="":
            Killed_Status = 1
        else:
            print("\n",modulename," is not killed properly \n")


    except Exception as error:
        print("\n Error from KillPID Func :",error)

    return Killed_Status

