
ENABLE_TLD_SCANNING = 1 #change value to 0 to disable
import multiprocessing
import random
import subprocess
from datetime import datetime
from colorama import Fore
import os
import signal
import sys
import requests
from sys import argv
if os.geteuid() != 0:
    exit('Run As Root')
try:

    ports = [int(argv[1].strip())]
except Exception:
    exit('Usage: python3 main.py <PORT>')
os.system('ulimit -n 1000000 ')


hostname = []
data = {}
signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))
message = ''
url1 = '' #NORMAL SCANNING WEBHOOK
url2 = '' #TLD WEBHOOK

def webhook_send(ip, port,hostname, webhook):
    data["embeds"] = [
        {
            "description" : f"Port {port} is open",
            "title" : f"{ip} {hostname[0]}"
        }
    ]
    result = requests.post(webhook, json = data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as error:
        return
    else:
        print("Sent to Webhook")

def get_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def scan_ports(ip):
    global message
    import socket
    hostname = ''
    time = get_time()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    try:
        hostname = socket.gethostbyaddr(ip)
    except Exception:
        return

    for port in ports:

        checkForPort = sock.connect_ex((ip, port))

        if checkForPort == 0:


            with open('output', 'a') as f:
                f.write(f'{time} {port} is open for {ip} | {hostname[0]} \n\n')


            try:
                print(f"Port {port} is open for {ip} {hostname[0]}")
            except Exception:
                return

            webhook_send(ip, port, hostname, url1)

            if ENABLE_TLD_SCANNING == 1:
                if hostname.count('.') == 1 :
                    webhook_send(ip,port,hostname, url2)
            sock.close()


        else:
            print(f'port is not open for {ip}')
            sock.close()

def check_ip(ip):
    return True if os.system("ping -c 1 " + ip + " > /dev/null 2>&1") == 0 else False

def output_results(ip):
    response = check_ip
    if response:


        print(f' {(get_time())} ({Fore.GREEN}+{Fore.WHITE}) {ip} is an IP')

    elif not response:
        print(f' {(get_time())} ({Fore.RED}-{Fore.WHITE}) {ip} is not an IP')

def find_ip():
    ip = []
    for i in range(4):
        ip.append(str(random.randint(0, 255)))
    ip = '.'.join(ip)
    check_ip(ip)
    output_results(ip)
    scan_ports(ip)

if __name__ == "__main__":
    try:
        thing = 1
        queue = multiprocessing.Queue()
        processes = [multiprocessing.Process(target=find_ip, args=()) for i in range(100000) ]

        for p in processes:

            p.start()

        for p in processes:
            p.terminate()
        for p in processes:
            p.join()
    except Exception as ex: print(f'Usage: python3 {argv[0]} <PORT>\n{ex}')


