import CommonFunc
from CommonFunc import*
import time
import yaml
import CommonFunc

with open("udpmoduleupconfig.yaml") as commonfile:
    config = yaml.load(commonfile, Loader=yaml.FullLoader)

print("Select Enviornment \n 0 DEV \n 1 SIT \n ")
choice = int(input(">>> "))
if choice == 0:
    
    cu_ip = config["credentials"]["cu_ip"]
    chv_iplist = config["credentials"]["chv_ip"]

    chv_extbroker = config["paths"]["chv_extbroker"]
    uev_localpubsub = config["paths"]["uev_localpubsub"]
    ran_localpubsub = config["paths"]["ran_localpubsub"]
    gnb_cu = config["paths"]["gnb_cu"]
    ran_csm = config["paths"]["ran_csm"]
    uev_csm = config["paths"]["uev_csm"]
    ran_ranp = config["paths"]["ran_ranp"]
    uev_uemp = config["paths"]["uev_uemp"]
    gnb_du = config["paths"]["gnb_du"]
    chv_localpubsub = config["paths"]["chv_localpubsub"]
    chv_csm = config["paths"]["chv_csm"]
    chv_chv =  config["paths"]["chv_chv"]

    core_chv_extbroker = config["corecommads"]["chv_extbroker"]
    core_chv_localpubsub = config["corecommads"]["chv_localpubsub"]
    core_chv_csm = config["corecommads"]["chv_csm"]
    core_chv_chv = config["corecommads"]["chv_chv"]
    core_ran_localpubsub = config["corecommads"]["ran_localpubsub"]
    core_ran_ranp = config["corecommads"]["ran_ranp"]
    core_ran_csm = config["corecommads"]["ran_csm"]
    core_gnb_du = config["corecommads"]["gnb_du"]
    core_gnb_cu = config["corecommads"]["gnb_cu"]

    core_uev_localpubsub = config["corecommads"]["uev_localpubsub"]
    core_uev_csm = config["corecommads"]["uev_csm"]
    core_uev_uemp = config["corecommads"]["uev_uemp"]
    pkill = config["cleancommad"]["pkill"]
    Ue_list=[config["UEs"]["Ue_ip_1"],config["UEs"]["Ue_ip_2"],config["UEs"]["Ue_ip_3"],config["UEs"]["Ue_ip_4"],config["UEs"]["Ue_ip_5"]]

    ranmodule = config["modules"]["ranmodule"]
    uemodule = config["modules"]["uemodule"]
    cumodule = config["modules"]["cumodule"]
    chvmodule = config["modules"]["chvmodule"]

    rancorelist =[core_ran_localpubsub,core_ran_csm,core_ran_ranp,core_gnb_du]
    uecorelist = [core_uev_localpubsub,core_uev_csm,core_uev_uemp]
    cucorelist = [core_gnb_cu]
    chvcorelist = [core_chv_extbroker,core_chv_localpubsub,core_chv_csm,core_chv_chv]

    username = config["credentials"]["username"]
    password = config["credentials"]["password"]
    raniplist = config["credentials"]["ran_ips"]
    ueiplist = config["credentials"]["ue_ips"]

elif choice == 1:
    cu_ip = config["sitcredential"]["cu_ip"]
    chv_iplist = config["sitcredential"]["chv_ip"]
    chv_extbroker = config["paths"]["chv_extbroker"]

    uev_localpubsub = config["sitpath"]["uev_localpubsub"]
    ran_localpubsub = config["sitpath"]["ran_localpubsub"]
    gnb_cu = config["sitpath"]["gnb_cu"]
    ran_csm = config["sitpath"]["ran_csm"]
    uev_csm = config["sitpath"]["uev_csm"]
    ran_ranp = config["sitpath"]["ran_ranp"]
    uev_uemp = config["sitpath"]["uev_uemp"]
    gnb_du = config["sitpath"]["gnb_du"]
    chv_localpubsub = config["sitpath"]["chv_localpubsub"]
    chv_csm = config["sitpath"]["chv_csm"]
    chv_chv =  config["sitpath"]["chv_chv"]

    core_chv_extbroker = config["sitcorecommands"]["chv_extbroker"]
    core_chv_localpubsub = config["sitcorecommands"]["chv_localpubsub"]
    core_chv_csm = config["sitcorecommands"]["chv_csm"]
    core_chv_chv = config["sitcorecommands"]["chv_chv"]
    core_ran_localpubsub = config["sitcorecommands"]["ran_localpubsub"]
    core_ran_ranp = config["sitcorecommands"]["ran_ranp"]
    core_ran_csm = config["sitcorecommands"]["ran_csm"]
    core_gnb_du = config["sitcorecommands"]["gnb_du"]
    core_gnb_cu = config["sitcorecommands"]["gnb_cu"]

    core_uev_localpubsub = config["sitcorecommands"]["uev_localpubsub"]
    core_uev_csm = config["sitcorecommands"]["uev_csm"]
    core_uev_uemp = config["sitcorecommands"]["uev_uemp"]
    pkill = config["cleancommad"]["pkill"]
    Ue_list=[config["sitUE"]["Ue_ip_1"],config["sitUE"]["Ue_ip_2"],config["sitUE"]["Ue_ip_3"],config["sitUE"]["Ue_ip_4"],config["sitUE"]["Ue_ip_5"],config["sitUE"]["Ue_ip_6"]]

    ranmodule = config["modules"]["ranmodule"]
    uemodule = config["modules"]["uemodule"]
    cumodule = config["modules"]["cumodule"]
    chvmodule = config["modules"]["chvmodule"]

    rancorelist =[core_ran_localpubsub,core_ran_csm,core_ran_ranp,core_gnb_du]
    uecorelist = [core_uev_localpubsub,core_uev_csm,core_uev_uemp]
    cucorelist = [core_gnb_cu]
    chvcorelist = [core_chv_extbroker,core_chv_localpubsub,core_chv_csm,core_chv_chv]


    username = config["sitcredential"]["username"]
    password = config["sitcredential"]["password"]
    raniplist = config["sitcredential"]["ran_ips"]
    ueiplist = config["sitcredential"]["ue_ips"]


print("\n1 : Run  UE and RAN modules\n2 : Run only RAN modules\n3 : Run CHV and RAN modules")
mchoice = int(input("Choose one : "))
if mchoice == 1:
    print("Ran Machines : ")
    for i in range(len(raniplist)):
        print(i, " : ", raniplist[i] )
    ranchoice = int(input("Choose RAN machine : "))
    ran_ip = raniplist[ranchoice]

    print("UE Machines : ")
    for i in range(len(ueiplist)):
        print(i, " : ", ueiplist[i] )
    uechoice = int(input("Choose UE machine : "))
    ue_ip = ueiplist[uechoice]

    paths = [chv_extbroker,uev_localpubsub,ran_localpubsub,gnb_cu,ran_csm,uev_csm,ran_ranp,uev_uemp,gnb_du]
    all_IP =[ran_ip,ue_ip,ran_ip,cu_ip,ran_ip,ue_ip,ran_ip,ue_ip,ran_ip]
    modulenames = ["extbroker","localPubSub","localPubSub","gnb_cu","csm","csm","ranp","uemp","gnb_du"]
    killlist = [ran_ip,ue_ip]
elif mchoice == 2:
    print("Ran Machines : ")
    for i in range(len(raniplist)):
        print(i, " : ", raniplist[i])
    choice = int(input("Choose RAN machine : "))
    ran_ip = raniplist[choice]

    paths = [chv_extbroker,ran_localpubsub,gnb_cu,ran_csm,ran_ranp,gnb_du]
    all_IP =[ran_ip,ran_ip,cu_ip,ran_ip,ran_ip,ran_ip]
    modulenames = ["extbroker","localPubSub","gnb_cu","csm","ranp","gnb_du"]
    killlist = [ran_ip]
elif mchoice == 3:
    print("Ran Machines : ")
    for i in range(len(raniplist)):
        print(i, " : ", raniplist[i])
    choice = int(input("Choose RAN machine : "))
    ran_ip = raniplist[choice]

    print("CHV Machines : ")
    for i in range(len(chv_iplist)):
        print(i, " : ", chv_iplist[i])
    choice = int(input("Choose CHV machine : "))
    chv_ip = chv_iplist[choice]
    paths = [chv_extbroker,chv_localpubsub,ran_localpubsub,gnb_cu,chv_csm,chv_chv,ran_csm,ran_ranp,gnb_du]
    all_IP =[chv_ip,chv_ip,ran_ip,cu_ip,chv_ip,chv_ip,ran_ip,ran_ip,ran_ip]
    modulenames = ["extbroker","localPubSub","localPubSub","gnb_cu","csm","chv","csm","ranp","gnb_du"]
    killlist = [ran_ip,chv_ip]



def SSHModule(path,ip,name):
    SSHModuleUpStatus=0
    loginobject=CommonFunc.ssh_login(ip,username,password)
    time.sleep(2) 
    if loginobject:
        PIDStatus1,PID1=CommonFunc.SSHCheckPID(loginobject,name,username)
        if PIDStatus1==1 and name=="gnb_cu":
            SSHModuleUpStatus=1
            print(name , "on",ip,"is already running with PID :",PID1)
        elif PIDStatus1==1:
            killstatus=CommonFunc.SShKillPID(loginobject,PID1,name,username)
            if killstatus==1:
                if name=="gnb_cu":
                    moduleup=ran_moduleUp(path,ip,name,username,password)
                    time.sleep(15)
                elif name=="gnb_du":
                    time.sleep(2)
                    moduleup=ran_moduleUp(path,ip,name,username,password)
                    time.sleep(.8)
                else:
                    moduleup=ran_moduleUp(path,ip,name,username,password)
        
                PIDStatus2,PID2=CommonFunc.SSHCheckPID(loginobject,name,username)
                if PIDStatus2==1 and name=="gnb_du":
                    if moduleup==1:
                        print(name , "on",ip,"is UP with PID :",PID2)
                        SSHModuleUpStatus=1
                    else:
                        print("\n",name,"not Up.....\n")
                        SSHModuleUpStatus=0

                elif PIDStatus2==1:
                    SSHModuleUpStatus=1
                    print(name , "on",ip,"is UP with PID :",PID2)
                else:
                    print("\n",name,"not Up.....\n")
            else:
                print("\n",name,"not killed.......\n")

        else:
            if name=="gnb_cu":
                moduleup=ran_moduleUp(path,ip,name,username,password)
                time.sleep(1)
            elif name=="gnb_du":
                time.sleep(1)
                moduleup=ran_moduleUp(path,ip,name,username,password)
                time.sleep(.8)

            else:
                moduleup=ran_moduleUp(path,ip,name,username,password)
        
            PIDStatus3,PID3=CommonFunc.SSHCheckPID(loginobject,name,username)
            if PIDStatus3==1 and name=="gnb_du":
                    if moduleup==1:
                        print(name , "on",ip,"is UP with PID :",PID3)
                        SSHModuleUpStatus=1
                    else:
                        print("\n",name,"not Up.....\n")
                        SSHModuleUpStatus=0
            elif PIDStatus3==1:
                SSHModuleUpStatus=1
                print(name , "on",ip,"is UP with PID :",PID3)
            else:
                print("\n",name,"not Up.....\n")


    return SSHModuleUpStatus

def moduletracing(ip,module,corecommands):
    try:
        for name ,command in zip(module,corecommands):
            loginobject=CommonFunc.ssh_login(ip,username,password)
            if loginobject:
                PIDStatus,PID=CommonFunc.SSHCheckPID(loginobject,name,username)
                if PIDStatus == 1:
                    print(name , "on",ip,"is running with PID :",PID)
                
                elif PIDStatus == 0:
                    corecheckflag = CommonFunc.corecheck(loginobject,command)
                    if corecheckflag == 1:
                        print(name,"on",ip,"is killed and Core generated")
                    else:
                        print(name,"on",ip,"is killed")


    except Exception as error :
        print("Error from Func moduletracing : ",error)


def PIDCycle():
    try:
        tracemachinelist =[]
        machinelist = [ran_ip,cu_ip,chv_ip]
        for ip in Ue_list :
            machinelist.append(ip)
        print("RAN UE and CU machines  \n")
        for i in range(len(machinelist)):
            print(i , " : ",machinelist[i])
        tracechoice = str(input("Choose machines to trace modules : "))
        tcr = tracechoice.split(" ")
        for c in tcr:
            tracemachinelist.append(machinelist[int(c)])

        while True :
            print("\n.......................PID cycle is Running ......................\n")
        
            for ip in tracemachinelist:
                if ip in raniplist:
                    moduletracing(ip,ranmodule,rancorelist)  
                elif ip == cu_ip:
                    print("\n")
                    moduletracing(ip,cumodule,cucorelist)
                elif ip in Ue_list:
                    print("\n")
                    moduletracing(ip,uemodule,uecorelist)
                elif ip == chv_ip:
                    print("\n")
                    moduletracing(ip,chvmodule,chvcorelist)

                else:
                    pass
    except Exception as error:
        print("Error from Func PIDCycle :",error)


for ip in killlist:
   object=CommonFunc.ssh_login(ip,username,password)
   object.exec_command(pkill)

for path,ip,name in zip(paths,all_IP,modulenames):
    
    if name == "gnb_du":
        SSHModuleUpStatus=SSHModule(path,ip,name)
        if SSHModuleUpStatus!=1:
            break
        else:
            PIDCycle()
    else:
        SSHModuleUpStatus=SSHModule(path,ip,name)
        if SSHModuleUpStatus!=1:
            break



                    





    
