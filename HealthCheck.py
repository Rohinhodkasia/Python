import yaml
import time
import CommomFunc
from CommomFunc import *
import CIA
import easy_gui
from CIA import *
from easygui import *

with open("config.yaml") as commonfile:
    config = yaml.load(commonfile, Loader=yaml.FullLoader)

username = config["credentials"]["username"]
password = config["credentials"]["password"]

cu_ip = config["credentials"]["cu_ip"]
ran_ip = config["credentials"]["ran_ip"]
core_ip = config["credentials"]["core_ip"]
ue_ip =  config["credentials"]["ue_ip"]

homespace = config["Commands"]["homespace"]
rootspace = config["Commands"]["rootspace"]
Hugepages = config["Commands"]["Hugepages"]
Freehugepages = config["Commands"]["dubinary"]
dubinary = config["Commands"]["dubinary"]
IRQStatus = config["Commands"]["IRQStatus"]
IRQKiller = config["Commands"]["IRQKiller"]
pods =  config["Commands"]["pods"]
ptpcheck = config["Commands"]["ptpcheck"]
upfcheck = config["Commands"]["upfcheck"]
cubinary = config["Commands"]["cubinary"]
space = config["Commands"]["space"]
Hugepages_total =config["Commands"]["Hugepages_total"]
coreisolation = config["Commands"]["coreisolation"]

uevlocalpubsub = config["Commands"]["uevlocalpubsub"]
uevcsm = config["Commands"]["uevcsm"]
uevuempcmd = config["Commands"]["uevuempcmd"]
uevuempuev = config["Commands"]["uevuempuev"]
uestackcmd = config["Commands"]["uestack"]



ranlocalcmd = config["Commands"]["ranlocalcmd"]
rancsmcmd = config["Commands"]["rancsmcmd"]
ranranplib = config["Commands"]["ranranplib"]
ranranpranv = config["Commands"]["ranranpranv"]
fr1du11 =  config["Commands"]["fr1du11"]

AllServer = [cu_ip,core_ip,ran_ip,ue_ip]
ranmodules = ["gnb_du","extbroker","localPubSub","csm","ranp"]
uemodules = ["localPubSub","csm","uemp"]

def CU_HealthCheck(ip):
    try:
        sshClient = MasterSSH(ip)
        if sshClient:
            modulename = "gnb_cu"
            PID = Modulecheck(sshClient, modulename,ip)
            if PID:
                print("CU is Running\n")
            else:
                print("Cu is Not Running\n")
            cubinarycheck = CuBinaryCheck(sshClient,cubinary)
            
            print("Config Using as text.xml : ",cubinarycheck,"\n")
            # AVhomespace = MemoCheck(sshClient,homespace,ip)
            # print("Space Used on Home : ",AVhomespace,"\n")
            
            # AVrootspace = MemoCheck(sshClient,rootspace,ip)
            # print("Space Used on Root : ",AVrootspace,"\n")
            print("[ MEMORY INFO ]\n")
            spacedata = spacecheck(sshClient,space)
            # print("[ MEMORY INFO ]\n")
            # print(spacedata)
            TotalHugepages = checkHugePages(sshClient,Hugepages_total)
            print("Total HugePages : ",TotalHugepages,"\n")

            FreeHugepages = checkHugePages(sshClient,Hugepages)
            print("Available Free HugePages : ",FreeHugepages,"\n")

            if int(FreeHugepages)< 30:
                data = "Hugepages are less then 30"
                button=msgbox(data,"CU MACHINE STATUS","OK")
                CleanHugePages(sshClient,Freehugepages)

                FreeHugepagesafterclean = checkHugePages(sshClient,Hugepages)
                print("Available Free HugePages After Cleaning : ",FreeHugepagesafterclean,"\n")

            IRQSTS = IRQBalancerStatus(sshClient,IRQStatus)
            if IRQSTS == 1:
                data = "IRQ Balancer Is Running"
                print("IRQ Balancer Is Running \n")
                button=msgbox(data,"CU MACHINE STATUS","OK")
                KilledSTS = IRQBalancerStop(sshClient,IRQKiller)
                IRQSTS = IRQBalancerStatus(sshClient,IRQStatus)
                if IRQSTS == 0:
                    print("IRQ Balancer is Stopped Now \n")
                else:
                    print("IRQ Balancer Is Still Running\n")
                    data = "IQR BALANCER IS STILL RUNNING"
                    button=msgbox(data,"CU MACHINE STATUS","OK")
                
            else:
                print("IRQ Balancer is not Running\n")

            flag, coredata = CoreIsolation(sshClient,coreisolation)
            # print(coredata,"\n")
            if flag == 1:
                print("Core Isolation is proper and Isolated cores are :",coredata,"\n")
            else:
                data = "CORE ISOLATION IS NOT PROPER"
                print("Core Isolation is Not proper\n")
                button=msgbox(data,"CU MACHINE STATUS","OK")



                
        else:
            print("sshClient is Not Available to SSH over :",ip)
    except Exception as error:
        print("Error from CU_HealthCheck Func :",error)

def RanMachine_HealthCheck(ip):
    try:
        sshClient = MasterSSH(ip)
        if sshClient:
            for modulename in ranmodules:
                if modulename =="gnb_du":
                    dubinarycheck = DUBinaryCheck(sshClient,dubinary)
                    print("Config Using as text.xml : ",dubinarycheck,"\n")

                PID = Modulecheck(sshClient, modulename,ip)
                if PID:
                    print(modulename," is Running\n")
                else:
                    print(modulename," is not Running\n")
                    
            # AVhomespace = MemoCheck(sshClient,homespace,ip)
            # print("Space Used on Home : ",AVhomespace,"\n")
                
            # AVrootspace = MemoCheck(sshClient,rootspace,ip)
            # print("Space Used on Root : ",AVrootspace,"\n")
            print("[ MEMORY INFO ]\n")
            spacedata =spacecheck(sshClient,space)
            
            # print(spacedata)
            TotalHugepages = checkHugePages(sshClient,Hugepages_total)
            print("Total HugePages : ",TotalHugepages,"\n")

            FreeHugepages = checkHugePages(sshClient,Hugepages)
            print("Available Free HugePages : ",FreeHugepages,"\n")

            if int(FreeHugepages)< 30:
                data = "Hugepages are less then 30"
                button=msgbox(data,"DU MACHINE STATUS","OK")
                CleanHugePages(sshClient,Freehugepages)

                FreeHugepagesafterclean = checkHugePages(sshClient,Hugepages)
                print("Available Free HugePages After Cleaning : ",FreeHugepagesafterclean,"\n")

            IRQSTS = IRQBalancerStatus(sshClient,IRQStatus)
            if IRQSTS == 1:
                data = "IRQ Balancer Is Running"
                print("IRQ Balancer Is Running \n")
                button=msgbox(data,"DU MACHINE STATUS","OK")
                KilledSTS = IRQBalancerStop(sshClient,IRQKiller)
                IRQSTS = IRQBalancerStatus(sshClient,IRQStatus)
                if IRQSTS == 0:
                    print("IRQ Balancer is Stopped Now \n")
                else:
                    print("IRQ Balancer Is Still Running\n")
                    data = "IQR BALANCER IS STILL RUNNING"
                    button=msgbox(data,"CU MACHINE STATUS","OK")
                
            else:
                print("IRQ Balancer is not Running\n")

            ptp,ptpstatus = PTPcheck(sshClient,ptpcheck)
            print("master_offset : ",ptp,"\n")
            if ptpstatus == 0:
                print("Server is not synced with PTP master [ PTP SERVICE RESTART RECOMMENDED ]\n")
                data = "PTP SERVICE RESTART RECOMMENDED"
                button=msgbox(data,"DU MACHINE STATUS","OK")

            else:
                print("Server is synced with PTP master\n")
            
            flag, coredata = CoreIsolation(sshClient,coreisolation)
            # print(coredata,"\n")
            if flag == 1:
                print("Core Isolation is proper and Isolated cores are :",coredata,"\n")
            else:
                print("Core Isolation is Not proper\n")
                data = "CORE ISOLATION IS NOT PROPER"
                button=msgbox(data,"DU MACHINE STATUS","OK")

            numallcore,num0logical,num1logical,numa0physical,numa1physical = corevalidation(coredata)
            # print(numallcore)
            ranlpsb = RANlocalpubsub(sshClient,ranlocalcmd)
            diffranlpsb = corecompare(numa1physical,ranlpsb)
        
            ranc = RANcsm(sshClient,rancsmcmd)
            diffrancsm = corecompare(numa1physical,ranc)
            
            ranranv = RANranpranv(sshClient,ranranpranv)
            diffranranv = corecompare(numa1physical,ranranv)

            ranrf = RANranplibpubsub(sshClient,ranranplib)
            diffranlibpub = corecompare(numa1physical,ranrf)

            ducore , ranallcore= RANdu(sshClient,fr1du11)
            diffrandu = corecompare(numa0physical,ducore)

            numa0 = list(set(numa0physical) - set(list(set(ranallcore))))
            lennuma0 = len(numa0)
            numa1 = list(set(numa1physical) - set(list(set(ranallcore))))
            lennuma1 = len(numa1)
            numa0l = list(set(num0logical) - set(list(set(ranallcore))))
            lennuma0l = len(numa0l)
            numa1l = list(set(num1logical) - set(list(set(ranallcore))))
            lennuma1l = len(numa1l)

            # print("numa1",numa1)
            totalwrongcore = diffrandu + diffranlibpub + diffranranv + diffrancsm + diffranlpsb
            ranvnewcore = []
            if diffranranv != []:
                length = len(diffranranv)
                if length <= lennuma1:
                    for i in range(length):
                        ranvnewcore.append(numa1[i])
                    del numa1[0:length]

                else:
                    for i in range(length):
                        ranvnewcore.append(numa1l[i])
                    
                    del numa1l[0:length]
                 
                print("Previously assigned cores to RANP ranv are ",ranranv,"and",diffranranv,"are not proper, reassigning correct cores ",ranvnewcore,"\n")
                data="Previously assigned cores to RANP ranv are "+str(ranranv)+" and "+str(diffranranv)+" are not proper reassigning correct cores "+str(ranvnewcore)
                button=msgbox(data,"RANV CORE STATUS","OK")
            else:
                print("Cores Assigned to RANP ranv :",ranranv,"are proper\n")
            # print("numa1",numa1,"\n")
            
            ranplibpubcorenew = []
            if diffranlibpub != []:
                length = len(diffranlibpub)
                if length <= len(numa1):
                    for i in range(length):
                        ranplibpubcorenew.append(numa1[i])
                    
                    del numa1[0:length]
                else:
                    for i in range(length):
                        ranplibpubcorenew.append(numa1l[i])
                    
                    del numa1l[0:length]
                print("Cores Assigned to RANP libpubsub are",ranrf,"and",diffranlibpub,"are not proper, reassigning correct cores ",ranplibpubcorenew,"\n")
                data = "Cores Assigned to RANP libpubsub are "+str(ranrf)+" and "+str(diffranlibpub)+" are not proper, reassigning correct cores "+str(ranplibpubcorenew)
                button=msgbox(data,"RAN LIBPUSUB CORE STATUS","OK")
            else:
                print("Cores Assigned to RANP libpubsub :",ranrf,"are proper\n")
            
            rancsmnewcore = []
            if diffrancsm != []:
                length = len(diffrancsm)
                if length <= len(numa1):
                    for i in range(length):
                        rancsmnewcore.append(numa1[i])
                    
                    del numa1[0:length]  
                else:
                    for i in range(length):
                        rancsmnewcore.append(numa1l[i])
                    
                    del numa1l[0:length]

                print("Cores assigned to CSM : ",ranc,"and",diffrancsm,"are not proper, reassigning correct cores ",rancsmnewcore,"\n")
                data = "Cores assigned to CSM : "+str(ranc)+" and "+str(diffrancsm)+" are not proper, reassigning correct cores "+str(rancsmnewcore)
                button=msgbox(data,"CSM CORE STATUS","OK")
            else:
                print("Cores assigned to CSM : ",ranc,"are proper\n")

            dunewcores =[]
            if diffrandu != []:
                length = len(diffrandu)
                if length <= numa0:
                    for i in range(length):
                        dunewcores.append(numa0[i])
                    
                    del numa0[0:length]

                else:
                    for i in range(length):
                        dunewcores.append(numa0l[i])
                    del numa0l[0:length]
                    
                print("Cores Assigned to DU :",ducore,"and",diffrandu,"are not proper reassigning correct cores to module ",dunewcores,"\n")
                data = "Cores Assigned to DU :"+str(ducore)+" and "+str(diffrandu)+" are not proper, reassigning correct cores to module "+str(dunewcores)
                button=msgbox(data," DU CORE STATUS","OK")
            else:
                print("Cores Assigned to DU :",ducore,"are proper\n")

            ranlocalpubsubnewcore = []
            if diffranlpsb != []:
                length = len(diffranlpsb)
                if length <= len(numa1):
                    for i in range(length):
                        ranlocalpubsubnewcore.append(numa1[i])
                    
                    del numa1[0:length]  
                else:
                    if length <= len(numa1l):
                        for i in range(length):
                            ranlocalpubsubnewcore.append(numa1l[i])
                        
                        del numa1l[0:length]

                    else:
                        for i in range(length):
                            ranlocalpubsubnewcore.append(numa0l[i])
                        
                        del numa0l[0:length]



                print("Cores assigned to localPubSub : ",ranlpsb,"and",diffranlpsb,"are not proper, reassigning correct cores ",ranlocalpubsubnewcore,"\n")
                length = len(diffranlpsb)
                
                
                data = "Cores assigned to localPubSub : "+str(ranlpsb)+" and "+str(diffranlpsb)+" are not proper, reassigning correct cores "+str(ranlocalpubsubnewcore)
                button=msgbox(data,"LOCALPUBSUB CORE STATUS","OK")
            else:
                print("Cores assigned to localPubSub : ",ranlpsb,"are proper\n")

            
                

            # print("Total assigned Cores to RAN :",list(set(ranallcore)),"\n")
            # print("Number of Cores in use :",len(ranallcore),"\n")
            # print("Free cores in Physical NUMA :",list(set(physicalcores) - set(list(set(ranallcore)))),"\n")

            print("Available cores in Physical NUMA0 :",numa0,"\n")

            print("Available cores in Physical NUMA1 :",numa1,"\n")

            print("Available cores in Logical NUMA 0 :",numa0l,"\n")
                
            print("Available cores in Logical NUMA 0 :",numa1l,"\n")

        else:
            print("sshClient is Not Available to SSH over :",ip)

    except Exception as error:
        print("Error from RanMachine_HealthCheck Func :",error)   
        
def UEMachine_HealthCheck(ip):
    try:
        sshClient = MasterSSH(ip)
        if sshClient:
            for modulename in uemodules:
                PID = Modulecheck(sshClient, modulename,ip)
                if PID:
                    print(modulename," is Running\n")
                else:
                    print(modulename," is not Running\n")
            
            # AVhomespace = MemoCheck(sshClient,homespace,ip)
            # print("Space Used on Home : ",AVhomespace,"\n")
                
            # AVrootspace = MemoCheck(sshClient,rootspace,ip)
            # print("Space Used on Root : ",AVrootspace,"\n")
            print("[ MEMORY INFO ]\n")
            spacedata =spacecheck(sshClient,space)
            
            # print(spacedata)
            TotalHugepages = checkHugePages(sshClient,Hugepages_total)
            print("Total HugePages : ",TotalHugepages,"\n")

            FreeHugepages = checkHugePages(sshClient,Hugepages)
            print("Available Free HugePages : ",FreeHugepages,"\n")
            
            if int(FreeHugepages)< 30:
                data = "Hugepages are less then 30"
                button=msgbox(data,"UE MACHINE STATUS","OK")
                CleanHugePages(sshClient,Freehugepages)

                FreeHugepagesafterclean = checkHugePages(sshClient,Hugepages)
                print("Available Free HugePages After Cleaning : ",FreeHugepagesafterclean,"\n")

            IRQSTS = IRQBalancerStatus(sshClient,IRQStatus)
            if IRQSTS == 1:
                data = "IRQ Balancer Is Running"
                button=msgbox(data,"UE MACHINE STATUS","OK")
                print("IRQ Balancer Is Running \n")
                KilledSTS = IRQBalancerStop(sshClient,IRQKiller)

                IRQSTS = IRQBalancerStatus(sshClient,IRQStatus)
                if IRQSTS == 0:
                    print("IRQ Balancer is Stopped Now \n")
                else:
                    print("IRQ Balancer Is Still Running\n")
                    data = "IQR BALANCER IS STILL RUNNING"
                    button=msgbox(data,"UE MACHINE STATUS","OK")
                
            else:
                print("IRQ Balancer is not Running\n")

            ptp,ptpstatus = PTPcheck(sshClient,ptpcheck)
            print("master_offset : ",ptp,"\n")
            if ptpstatus == 0:
                print("Server is not synced with PTP master [ PTP SERVICE RESTART RECOMMENDED ]\n")
                data = "PTP SERVICE RESTART RECOMMENDED"
                button=msgbox(data,"UE MACHINE STATUS","OK")


            else:
                print("Server is synced with PTP master \n")

            flag, coredata = CoreIsolation(sshClient,coreisolation)
            # print(coredata,"\n")
            if flag == 1:
                print("Core Isolation is proper and Isolated cores are :",coredata,"\n")
            else:
                print("Core Isolation is Not proper\n")
                data = "CORE ISOLATION IS NOT PROPER"
                button=msgbox(data,"UE MACHINE STATUS","OK")

            
            numallcore ,num0logical,num1logical,numa0physical,numa1physical = corevalidation(coredata)

            uevlpsb = UEVlocalpubsub(sshClient,uevlocalpubsub)
            diffuevlpsb = corecompare(numa0physical,uevlpsb)

            uevc = UEVcsm(sshClient,uevcsm)
            diffuev = corecompare(numa0physical,uevc)

            uevur = UEVuemplibpubsub(sshClient,uevuempcmd)
            diffuevur = corecompare(numa0physical,uevur)

            uestack = Uestackcores(sshClient,uestackcmd)
            diffuestack = corecompare(numa0physical,uestack)

            uev10 , allcore = UEVuempuev10(sshClient,uevuempuev)
            diffuev10 = corecompare(numallcore,uev10)
                                                
            freenuma0 = list(set(numa0physical) - set(list(set(allcore))))
            freenuma1 = list(set(numa1physical) - set(list(set(allcore))))
            freenuma0l = list(set(num0logical) - set(list(set(allcore))))
            freenuma1l = list(set(num1logical) - set(list(set(allcore))))
            
            uev10newcore =[]
            if diffuev10 != []:
                length = len(diffuev10)
                if length <= len(freenuma0):
                    for i in range(length):
                        uev10newcore.append(freenuma0[i])
                    del freenuma0[0:length]

                else:
                    if length <= len(freenuma0l):
                        for i in range(length):
                            uev10newcore.append(freenuma0l[i])
                        del freenuma0l[0:length]


                print("Cores assigned to UEMP uev_1_0 : ",uev10,"and",diffuev10,"are not proper, reassigning correct cores",uev10newcore,"\n")
                data = "Cores assigned to UEMP uev_1_0 : "+str(uev10)+" and "+str(diffuev10)+" are not proper, reassigning correct cores"+str(uev10newcore)
                button=msgbox(data,"UEMP UEV_1_0 CORE STATUS","OK")
            else:
                print("Cores assigned to UEMP uev_1_0 : ",uev10,"are proper\n")

            uevlibpubnewcore =[]
            if diffuevur != []:
                length = len(diffuevur)
                if length <= len(freenuma0):
                    for i in range(length):
                        uevlibpubnewcore.append(freenuma0[i])
                    del freenuma0[0:length]

                else:
                    if length <= len(freenuma0l):
                        for i in range(length):
                            uevlibpubnewcore.append(freenuma0l[i])
                        del freenuma0l[0:length]

                print("Cores assigned to UEMP_libpubsub : ",uevur,"and",diffuevlpsb,"are not proper, reassigning correct cores",uevlibpubnewcore,"\n")
                data = "Cores assigned to UEMP_libpubsub : "+str(uevur)+" and "+str(diffuevlpsb)+" are not proper, reassigning correct cores"+str(uevlibpubnewcore)
                button=msgbox(data,"UEMP LIBPUBSUB CORE STATUS","OK")
                
            else:
                print("Cores assigned to UEMP_libpubsub : ",uevur,"are proper\n")
            csmnewcore =[]
            if diffuev != []:
                length = len(diffuev)
                if length <= len(freenuma0):
                    for i in range(length):
                        csmnewcore.append(freenuma0[i])
                    del freenuma0[0:length]

                else:
                    if length <= len(freenuma0l):
                        for i in range(length):
                            csmnewcore.append(freenuma0l[i])
                        del freenuma0l[0:length]

                print("Cores assigned to CSM : ",uevc,"and",diffuev,"are not proper ,reassigning correct cores",csmnewcore,"\n")
                data = "Cores assigned to CSM : "+str(uevc)+" and "+str(diffuev)+" are not proper ,reassigning correct cores"+str(csmnewcore)
                button=msgbox(data,"UE CSM CORE STATUS","OK")
            else:
                print("Cores assigned to CSM : ",uevc,"are proper\n")
           
            uevlocalpubnewcore = []
            if diffuevlpsb != []:
                length = len(diffuevlpsb)
                if length <= len(freenuma0):
                    for i in range(length):
                        uevlocalpubnewcore.append(freenuma0[i])
                    del freenuma0[0:length]

                else:
                    if length <= len(freenuma0l):
                        for i in range(length):
                            uevlocalpubnewcore.append(freenuma0l[i])
                        del freenuma0l[0:length]

                print("Cores assigned to localPubSub : ",uevlpsb,"and",diffuevlpsb,"are not proper, reassigning correct cores",uevlocalpubnewcore,"\n")
                data = "Cores assigned to localPubSub : "+str(uevlpsb)+" and "+str(diffuevlpsb)+" are not proper, reassigning correct cores"+str(uevlocalpubnewcore)
                button=msgbox(data,"UE LOCALPUBSUB CORE STATUS","OK")
                
            else:
                print("Cores assigned to localPubSub : ",uevlpsb,"are proper\n")

            uestacknewcores = []
            if diffuestack != []:
                length = len(diffuevlpsb)
                if length <= len(diffuestack):
                    for i in range(length):
                        uestacknewcores.append(freenuma0[i])
                    del freenuma0[0:length]

                else:
                    if length <= len(freenuma0l):
                        for i in range(length):
                            uestacknewcores.append(freenuma0l[i])
                        del freenuma0l[0:length]

                print("Cores assigned to UE STACK are ",uestack,"and",diffuestack,"are not proper, reassigning correct cores",uestacknewcores,"\n")
                data = "Cores assigned to UE STACK : "+str(uestack)+" and "+str(diffuestack)+" are not proper, reassigning correct cores"+str(uestacknewcores)
                button=msgbox(data,"UE UE STACK CORE STATUS","OK")
                
            else:
                print("Cores assigned to UE STACK : ",uestack,"are proper\n")

            
            
            print("Available cores in Physical NUMA0 :",freenuma0,"\n")
            print("Available cores in Physical NUMA1 :",freenuma1,"\n")
            print("Available cores in Logical NUMA 0 :",freenuma0l,"\n")    
            print("Available cores in Logical NUMA 1 :",freenuma1l,"\n")
                            
        else:
            print("sshClient is Not Available to SSH over :",ip)
        
    except Exception as error:
        print("Error from UEMachine_HealthCheck Func :",error) 
        
def COREMachine_HealthCheck(ip):
    try:
        sshClient = MasterSSH(ip)
        if sshClient:    
            print("[ MEMORY INFO ]\n")
            spacedata =spacecheck(sshClient,space)
            
            # print(spacedata)
            TotalHugepages = checkHugePages(sshClient,Hugepages_total)
            print("Total HugePages : ",TotalHugepages,"\n")


            FreeHugepages = checkHugePages(sshClient,Hugepages)
            print("Available Free HugePages : ",FreeHugepages,"\n")

            if int(FreeHugepages)< 30:
                data = "Hugepages are less then 30"
                button=msgbox(data,"CORE MACHINE STATUS","OK")
                CleanHugePages(sshClient,Freehugepages)
                FreeHugepagesafterclean = checkHugePages(sshClient,Hugepages)
                print("Available Free HugePages After Cleaning : ",FreeHugepagesafterclean,"\n")

            

            IRQSTS = IRQBalancerStatus(sshClient,IRQStatus)
            if IRQSTS == 1:
                data = "Hugepages are less then 30"
                button=msgbox(data,"CORE MACHINE STATUS","OK")
                print("IRQ Balancer Is Running \n")
                KilledSTS = IRQBalancerStop(sshClient,IRQKiller)
                IRQSTS = IRQBalancerStatus(sshClient,IRQStatus)
                if IRQSTS == 0:
                    print("IRQ Balancer is Stopped Now \n")
                else:
                    print("IRQ Balancer Is Still Running\n")
                    data = "IQR BALANCER IS STILL RUNNING"
                    button=msgbox(data,"CORE MACHINE STATUS","OK")
                
            else:
                print("IRQ Balancer is not Running\n")


            
            print("[ UPF STATUS ] \n")
            upfstatus = UpfCheck(sshClient,upfcheck)
            print(upfstatus)

            print("[ PODS STATUS ]\n")
            podsdata = podsStatus(sshClient,pods)   
            filename = datastore(podsdata)
            dataread(filename)

            
            
        else:
            print("sshClient is Not Available to SSH over :",ip)

    except Exception as error:
        print("Error from COREMachine_HealthCheck Func :",error)

for Server in AllServer:
    if Server == cu_ip:
        print("\n:::::::::::: CU Machine Status :::::::::::: \n")
        CU_HealthCheck(cu_ip)

    elif Server == ran_ip:
        print("\n:::::::::::: DU Machine Status :::::::::::: \n")
        RanMachine_HealthCheck(ran_ip)

    elif Server == ue_ip:
        print("\n:::::::::::: UEV Machine Status :::::::::::: \n")
        UEMachine_HealthCheck(ue_ip)   

    else:
        print("\n:::::::::::: CORE Machine Status :::::::::::: \n")
        COREMachine_HealthCheck(core_ip)
        



