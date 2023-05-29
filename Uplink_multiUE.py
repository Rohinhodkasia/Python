import time
import subprocess
import threading
import multi_UE_MU
import CommonFunc
import sys


ul_time = sys.argv[2]
ul_data = sys.argv[1]
ulport = sys.argv[3]
logfile = sys.argv[4]
dn_ip = sys.argv[5]
username = sys.argv[6]
password = sys.argv[7]

t1 = "Uplink_"+time.ctime().replace(" ", "_")+".log"
UL_logfile =logfile+t1


# Common commands for both Uplink and Downlink to add IP's
def arp_common_cmd(ssh, attched_ip):

    # Passing command to DN server
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
        "sudo arp -s "+str(attched_ip)+" 48:df:37:d6:48:e9 -i ens2f0", get_pty=True)
    time.sleep(3)
    print("Passed arp command on DN server successfully")

    # Executing the UE server command
    proc = subprocess.Popen("sudo ip route add 172.20.1.20 dev tun0pdn7", stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, stdin=subprocess.PIPE, shell=True, bufsize=0)
    time.sleep(2)
    print("Added the ip route at UE server successfully")


# Uplink Iperf Commads
def execute_cmd_uplink(ssh, attched_ip):
    try:
        print("\n Started The Uplink Process")

        # Calling arp Commands
        arp_common_cmd(ssh, attched_ip)

        # passing command to DN server
        # Run the shell session in a separate thread
        shell_thread = threading.Thread(
            target=run_shell_session_uplink, args=(ssh, ul_time,))
        shell_thread.start()
        print("Executed the Iperf command at DN server")

        # Passing command at UE
        process = subprocess.Popen("sudo iperf -u -c 172.20.1.20 -p " + ulport + " -l 1380 -b "+ul_data+"m -t "+ul_time +
                                   " -i 1", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, shell=True, bufsize=0)
        time.sleep(3)
        # ue_machine_proc_iperf = process.stdout.readlines()
        print("Executed the iperf cmd at ue machine terminal")
    except Exception as error:
        print("Error while executing the uplink command", error)

    # Stopping the thread
    shell_thread.join()
    out = read_last_line(UL_logfile)
    if not None:
        try:
            result = out[-3].split(" ")
            print(result)
            my_dict = {'Time_Interval': [result[3], "sec"],
                       'Transfer_Data': [result[6], "MBytes"],
                       'Bandwidth': [result[9], "Mbits/sec"],
                       'Avg_Data_Loss': [result[18], result[19]]
                       }

            print(my_dict)
        except (IndexError, ValueError):
            print("Error: The Data has not processed")

    print("Uplink process completed")
    print("Logfile at path: ", UL_logfile)
    return True


def run_shell_session_uplink(ssh_client, ul_time):

    # Start an interactive shell session
    shell = ssh_client.invoke_shell()
    shell.send('sudo iperf -s -u -i 1 -p 7001\n')

    # Open a log file for writing
    log_file = open(UL_logfile, 'w')
    tstart = time.time()+float(ul_time)+10
    # Send and receive data from the shell session
    while True:
        if shell.recv_ready():
            # Read data from the shell
            output = shell.recv(1024).decode('utf-8')
            if not output:
                break

            log_file.write(output)
            log_file.flush()
        tstop = time.time()
        if tstop > tstart:
            break

    # Close the shell session
    shell.close()


# reading data from file
def read_last_line(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
        return lines if lines else None


ssh_client = multi_UE_MU.ssh_login(dn_ip,username,password)
fetched_ip = CommonFunc.fetch_ip()
execute_cmd_uplink(ssh_client, fetched_ip)
