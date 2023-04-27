import random
import socket
import subprocess
import os
from datetime import datetime 

# variables that dont need to be changed
count_packets = str()
packet_timeout = str()
port = 80

def main():
    os_settings()
    while True:
  
        # variables that must be reinitialized every iteration
        hostname = "No Hostname"
        checked = str()
        scan = str()
        ip = generate_ip()
        checked = check_ip(ip)

        match checked:
            case 0: 
                scan = scan_ip(ip,port)
            case 1:
                print_result(ip,port,0,hostname)
                continue
        match scan:
            case 0:
                get_hostname(ip)
                print_result(ip,port,2,hostname)
            case _:
                print_result(ip,port,1,hostname)
# sets the switches for the ping command based on the current os
def os_settings():
    global count_packets
    global packet_timeout
    if os.name == 'nt':
        count_packets = "-n"
        packet_timeout = "-w"
    elif os.name == 'posix':
        count_packets = "-c"
        packet_timeout = "-W"
# generate IP
def generate_ip():
    ip = []
    # generates a random number between 0 and 255 4 times. Adds them to a list
    for i in range(4):
        ip.append(str(random.randint(0,255)))
    # joins the list together with .'s
    return '.'.join(ip)
# check if IP is up
def check_ip(ip):
    # creates a new subprocess the pings the IP address with 1 packet with a timeout of 1 second
    up = subprocess.run(['ping', packet_timeout, '1', count_packets, '1', ip],stdout=subprocess.DEVNULL)
    return up.returncode
# scan IP
def scan_ip(ip, port):
    # creates new socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set a timeout of 1 second
    sock.settimeout(1)
    try:
        # attempts to connect the the ip:port
        checkForPort = sock.connect_ex((ip, port))
    except socket.error:
        print("Couldn't connect to %s:%d" % (ip, port))
    return checkForPort
# get current time
def get_time():
    return datetime.now().strftime('%H:%M:%S')
# get the hostname from the IP address
def get_hostname(ip):
    global hostname
    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return
# prints the resuts out
def print_result(ip,port,result,hostname):
    match result:
        case 0:
            print(f"\r{get_time()} - {ip} is not a valid IP address \033[K ", end="\r")
        case 1:
            print(f"\r{get_time()} - {ip}:{port}  is not open \033[K ", end="\r")
        case 2:
            print(f"\033[K{get_time()} - {ip}:{port} ({hostname}) is open")


main()