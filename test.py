import paramiko
import time
import yaml

# with open("config.yaml") as commonfile:
#     config = yaml.load(commonfile, Loader=yaml.FullLoader)

username = "amtvphy"
password = "0pal1"

def MasterSSH(ip):
    # sshClient=""
    try:
        sshClient = paramiko.SSHClient()
        sshClient.load_system_host_keys()
        sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshClient.connect(ip, username, password=password)
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

command = "ifconfig"

# ssh = MasterSSH("10.20.249.6")
# data1 = MasterWrite(ssh,command)
# print(data1)

str = "10.20.249.9"
a = str.split(".")
print(a)
x = a[-1]
print(a[-1])
print(type(x))

# filename = 'logs/UEVcsm.txt'
# with open (filename, 'w') as file:  
#     file.write(data)

# with open(filename, 'r') as log:
#         lines = log.readlines()
# uestackcore = []
# for line in lines:
#     if "#Cores" in line:
#         pass
#     elif "Cores" in line:
#         print(line)