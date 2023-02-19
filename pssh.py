import paramiko
from decouple import config
import argparse
from colorama import init, Fore
import socket
import subprocess

init()

GREEN = Fore.GREEN
RED   = Fore.RED
RESET = Fore.RESET
BLUE  = Fore.BLUE

user1=config('user1')
pass1=config('pass1')
user2=config('user2')
pass2=config('pass2')

parser = argparse.ArgumentParser("Connect to device with various login and password")
parser.add_argument("host", help="Hostname or IP Address of device")
args=parser.parse_args()
host=args.host

def is_ssh_open(hostname, username, password):
    # initialize SSH client
    client = paramiko.SSHClient()
    # add to know hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password, timeout=3)
    except socket.timeout:
        # this is when host is unreachable
        print(f"{RED}[!] Host: {hostname} is unreachable, timed out.{RESET}")
        return False
    except paramiko.AuthenticationException:
        print(f"[!] Invalid credentials for {username}:{password}")
        return False
    except paramiko.SSHException:
        print(f"{BLUE}[*] Quota exceeded, retrying with delay...{RESET}")
        # sleep for a minute
        time.sleep(60)
        return is_ssh_open(hostname, username, password)
    else:
        # connection was established successfully
        print(f"{GREEN}[+] Found combo:\n\tHOSTNAME: {hostname}\n\tUSERNAME: {username}\n\tPASSWORD: {password}{RESET}")
        return True


if __name__ == "__main__":
    print ("Connecting to",host)
    if  is_ssh_open(host,user1,pass1):
       cmd = user1 + "@"+host
       subprocess.run(["sshpass","-p",pass1, "ssh",cmd])
       exit 
    cmd = user2 + "@"+host
    subprocess.run(["sshpass","-p",pass2, "ssh",cmd])
    

   