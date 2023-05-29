import CommomFunc
from CommomFunc import *

UEVcores = []
RANcores = []
numa0physical = []
numa1physical = []
num0logical =[]
num1logical =[]
numalist = []
def CoreIsolation(sshClient,command):
    flag = 0
    try:
        data = str(MasterWrite(sshClient,command))

        grub = data.split(" ")
        for i in range(len(grub)):
            if "isolcpus" in grub[i]:
                data = grub[i]
                cores = data[data.index("=")+1:len(data)].split(",")
                # print(grub[i].split(","))
                if cores[0] == "5-27" and cores[1] == "33-55":
                    # print("Isolation is proper")
                    flag = 1
                else:
                    pass
            else:
                pass

    except Exception as error:
        print("Error from coreisolation Func :",error)

    return flag , cores

def UEVlocalpubsub(sshClient,command):
    uevlocalpubsubcore = []
    try:
        data = str(MasterWrite(sshClient,command))
        filename = 'logs/UEVlocalpubsub.txt'
        with open (filename, 'w') as file:  
            file.write(data)

        with open(filename, 'r') as log:
                lines = log.readlines()

        for line in lines:
            if "Logger Thread" in line :
                c = int(line[:line.index(",")])
                UEVcores.append(c)
                uevlocalpubsubcore.append(c)
            elif "North Interface Thread"in line:
                c = int(line[:line.index(",")])
                UEVcores.append(c)
                uevlocalpubsubcore.append(c)
            elif "South Interface Thread " in line:
                c = int(line[:line.index("/*")])
                UEVcores.append(c)
                uevlocalpubsubcore.append(c)
            else:
                pass

    except Exception as error:
        print("Error from UEVlocalpubsub Func :",error)
    return uevlocalpubsubcore

def UEVcsm(sshClient,command):
    uevcsmcore = []
    try:
        data = str(MasterWrite(sshClient,command))
        filename = 'logs/UEVcsm.txt'
        with open (filename, 'w') as file:  
            file.write(data)

        with open(filename, 'r') as log:
                lines = log.readlines()

        for line in lines:
            if "#Cores =" in line:
                pass
            elif "Cores = " in line:
                x =line[line.index('"')+1:len(line)-3].split("-")
                for j in range(int(x[0]),int(x[1])+1):
                    UEVcores.append(j)
                    uevcsmcore.append(j)
            elif "cpu_core = " in line:
                x = int(line[line.index("["):line.index("]")].replace("[","").replace("]",""))
                uevcsmcore.append(x)
                UEVcores.append(x)
            elif "Timer Thread" in line:
                c = int(line[:line.index(",")])
                UEVcores.append(c)
                uevcsmcore.append(c)
            elif "PTP Thread" in line:
                c = int(line[:line.index(",")])
                UEVcores.append(c)
                uevcsmcore.append(c)
            elif "Interface Thread" in line:
                c = int(line[:line.index(",")])
                UEVcores.append(c)
                uevcsmcore.append(c)
            elif "Logger Thread" in line:
                c = int(line[:line.index("/*")])
                UEVcores.append(c)
                uevcsmcore.append(c)
            else:
                pass


    except Exception as error:
        print("Error from UEVcsm Func :",error)
    return uevcsmcore

def UEVuerf(sshClient,command):
    uevuerfcore = []
    try:
        data = str(MasterWrite(sshClient,command))
        filename = 'logs/UEVuerf.txt'
        with open (filename, 'w') as file:  
            file.write(data)

        with open(filename, 'r') as log:
                lines = log.readlines()

        for line in lines:
            if "#Cores =" in line:
                pass
            elif "Cores = " in line:
                list = line[line.index('"')+1:len(line)-3].split(",")
                for i in range(len(list)):
                    c = int(list[i])
                    UEVcores.append(c)
                    uevuerfcore.append(c)
            else:
                pass
    except Exception as error:
        print("Error from UEVlocalpubsub Func :",error)
    return uevuerfcore ,UEVcores
    
def UEVuemplibpubsub(sshClient,command):
    UEVuemplib = []
    try:
        data = str(MasterWrite(sshClient,command))
        filename = 'logs/UEVuemplibpubsub.txt'
        with open (filename, 'w') as file:  
            file.write(data)

        with open(filename, 'r') as log:
                lines = log.readlines()

        for line in lines:
            if "#Cores =" in line:
                pass
            elif "Cores = " in line:
                Coresdata = line[line.index('"')+1:len(line)-3].split(",")
                for i in range(len(Coresdata)):
                    if "-" in Coresdata[i]:
                        # print(i)
                        x = Coresdata[i].split("-")
                        # print(x)
                        for j in range(int(x[0]),int(x[1])+1):
                            UEVcores.append(j)
                            UEVuemplib.append(j)
                    else:

                        UEVcores.append(int(Coresdata[i]))
                        UEVuemplib.append(int(Coresdata[i]))
            else:
                pass
    except Exception as error:
        print("Error from RANranp Func :",error)
    return UEVuemplib

def UEVuempuev10(sshClient,command):
    uempuev10 = []
    try:
        data = str(MasterWrite(sshClient,command))
        filename = 'logs/UEVuempuev-1-0.txt'
        with open (filename, 'w') as file:  
            file.write(data)

        with open(filename, 'r') as log:
                lines = log.readlines()


        for line in lines:
            if "//cpu_core" in line:
                pass
            elif "cpu_core" in line:
                datacore = str(line[line.index("[")+1 : line.index("]")-1]).split(",")
                for i in range(len(datacore)):
                    UEVcores.append(int(datacore[i]))
                    uempuev10.append(int(datacore[i]))
            else:
                pass

    except Exception as error:
        print("Error from UEVuempuev10 Func :",error)

    return uempuev10 ,UEVcores




def RANlocalpubsub(sshClient,command):
    ranlocalpubsubcore = []
    try:
        data = str(MasterWrite(sshClient,command))
        filename = 'logs/RANlocalpubsub.txt'
        with open (filename, 'w') as file:  
            file.write(data)

        with open(filename, 'r') as log:
                lines = log.readlines()

        for line in lines:
            if "Logger Thread" in line :
                c = int(line[:line.index(",")])
                RANcores.append(c)
                ranlocalpubsubcore.append(c)
            elif "North Interface Thread"in line:
                c = int(line[:line.index(",")])
                RANcores.append(c)
                ranlocalpubsubcore.append(c)
            elif "South Interface Thread " in line:
                c = int(line[:line.index("/*")])
                RANcores.append(c)
                ranlocalpubsubcore.append(c)
            else:
                pass

    except Exception as error:
        print("Error from UEVlocalpubsub Func :",error)
    return ranlocalpubsubcore

def RANcsm(sshClient,command):
    rancsmcore = []
    try:
        data = str(MasterWrite(sshClient,command))
        filename = 'logs/RANcsm.txt'
        with open (filename, 'w') as file:  
            file.write(data)

        with open(filename, 'r') as log:
                lines = log.readlines()

        for line in lines:
            if "#Cores =" in line:
                pass
            elif "Cores = " in line:
                x =line[line.index('"')+1:len(line)-3].split("-")
                for j in range(int(x[0]),int(x[1])+1):
                    RANcores.append(j)
                    rancsmcore.append(j)
            elif "cpu_core = " in line:
                x = int(line[line.index("["):line.index("]")].replace("[","").replace("]",""))
                rancsmcore.append(x)
                RANcores.append(x)
            elif "Timer Thread" in line:
                c = int(line[:line.index(",")])
                RANcores.append(c)
                rancsmcore.append(c)
            elif "PTP Thread" in line:
                c = int(line[:line.index(",")])
                RANcores.append(c)
                rancsmcore.append(c)
            elif "Interface Thread" in line:
                c = int(line[:line.index(",")])
                RANcores.append(c)
                rancsmcore.append(c)
            elif "Logger Thread" in line:
                c = int(line[:line.index("/*")])
                RANcores.append(c)
                rancsmcore.append(c)
            else:
                pass


    except Exception as error:
        print("Error from UEVcsm Func :",error)
    return rancsmcore

def RANranplibpubsub(sshClient,command):
    ranranplib = []
    try:
        data = str(MasterWrite(sshClient,command))
        filename = 'logs/logRANranplibpubsub.txt'
        with open (filename, 'w') as file:  
            file.write(data)

        with open(filename, 'r') as log:
                lines = log.readlines()

        for line in lines:
            if "#Cores =" in line:
                pass
            elif "Cores = " in line:
                Coresdata = line[line.index('"')+1:len(line)-3].split(",")
                for i in range(len(Coresdata)):
                    if "-" in Coresdata[i]:
                        # print(i)
                        x = Coresdata[i].split("-")
                        # print(x)
                        for j in range(int(x[0]),int(x[1])+1):
                            RANcores.append(j)
                            ranranplib.append(j)
                    else:
                        RANcores.append(int(Coresdata[i]))
                        ranranplib.append(int(Coresdata[i]))
            else:
                pass

    except Exception as error:
        print("Error from RANranp Func :",error)
    return ranranplib 

def RANranpranv(sshClient,command):
    ranranpranv = []
    try:
        data = str(MasterWrite(sshClient,command))
        filename = 'logs/RANranpranv.txt'
        with open (filename, 'w') as file:  
            file.write(data)

        with open(filename, 'r') as log:
                lines = log.readlines()


        for line in lines:
            if "cpu_core" in line:
                datacore = str(line[line.index("[")+1 : line.index("]")-1 ]).split(",")
                for i in range(len(datacore)):
                    RANcores.append(int(datacore[i]))
                    ranranpranv.append(int(datacore[i]))
            

                

    except Exception as error:
        print("Error from RANranpranv Func :",error)

    return ranranpranv 

def RANdu(sshClient,command):
    ducores = []
    List =[]
    try:
        data = str(MasterWrite(sshClient,command))
        filename = 'logs/DU.txt'
        with open (filename, 'w') as file:  
            file.write(data)

        with open(filename, 'r') as log:
                lines = log.readlines()


        strings = ["TTI_TIMER_COREID","OAM_RX_COREID","LOWER_CL_COREID","LOG_READER_COREID","CL_RECV_COREID","CLI_AGENT_COREID","OAM_AGENT_COREID","UDP_RX_COREID","SCTP_COREID","TIMER_COREID","POOL1_WKR_COREID","POOL2_WKR_COREID","CORE_ID","TB_DUMP_CORE_ID"]

        for line in lines:
            for st in strings:
                if st in line:
                    if "=" in line:

                        idx = line.index("=")+1
                        c = line[idx:len(line)].strip()
                        List.append(c)
                        
                    else:
                        pass
                else:
                    pass

        for i in range(len(List)):
            if len(List[i]) > 2:
                c = List[i].replace("{","").replace("}","").split(",")
                for j in range(len(c)):
                    ducores.append(int(c[j]))
                    RANcores.append(int(c[j]))
            else:
                val = int(List[i])
                ducores.append(val)
                RANcores.append(val)

    except Exception as error :
        print("Error from RANdu Func :",error)
    return ducores , RANcores
            
        
def corevalidation(core):
    try:
        for i in range(len(core)):
            numalist.append(core[i].split("-"))
        
        for i in range(len(numalist)):
            if i == 0:
                for j in range(int(numalist[i][0]),int(numalist[i][1])+1):
                    numa0physical.append(j)

            elif i == 1:
                for j in range(int(numalist[i][0]),int(numalist[i][1])+1):
                    numa1physical.append(j)
            
            elif i == 2:
                for j in range(int(numalist[i][0]),int(numalist[i][1])+1):
                    num0logical.append(j)

            elif i == 3:
                for j in range(int(numalist[i][0]),int(numalist[i][1])+1):
                    num1logical.append(j)
        physicalnuma = numa0physical + numa1physical
        allnumacore = numa0physical + numa1physical +num0logical + num1logical
        physicalcores = numa0physical + numa1physical
        logicalcores = num0logical + num1logical

    
    except Exception as error:
        print("Error from corevalidation Func : ",error)
    return allnumacore ,num0logical,num1logical,numa0physical,numa1physical


def corecompare(allnumacore,assignedcore):
    try:
        diff = list(set(assignedcore) - set(allnumacore))

    except Exception as error:
        print("Error from corecompare Func : ",error)
    
    return diff

def Uestackcores(sshClient,command):
    uestackcore = []
    try:
        data = str(MasterWrite(sshClient,command))
        filename = 'logs/uestack.txt'
        with open (filename, 'w') as file:  
            file.write(data)

        with open(filename, 'r') as log:
                lines = log.readlines()
        for line in lines:
            if "taskset -c" in line:
                idx  = line.index("-c") + 2
                idx2 = line.index("/usr/local/") -1
                cores = str(line[idx:idx2]).split("-")
                for i in range(int(cores[0]),int(cores[1])+1):
                    uestackcore.append(i)
                    UEVcores.append(i)
            else:
                pass

    except Exception as error:
        print("Error from Uestackcores Func : ",error)
    return uestackcore