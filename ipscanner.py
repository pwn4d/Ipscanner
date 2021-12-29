#!/usr/bin/env python3
import subprocess

from colorama import Fore
import os
import socket
import random
import argparse
s = socket.socket()
s.settimeout(3)

#variables
ips = []
ip = ''
ports = []
port_info = ''
current_open = ''
hostname = ''
parser = argparse.ArgumentParser()

#arguments
parser.add_argument('--verbose' , "-v",help="Verbose (prints every action (Usefull for debugging))" , action="store_true")
parser.add_argument('--ports' , "-p",help="Select Ports" , action="store_true")
parser.add_argument('--search' , "-s",help="Searches logs for IPs with open ports" , action="store_true")
parser.add_argument("port", type=str, help="Ports (seperate each one with a comma -p 80,443,21 |Default ports are 1-1000)", nargs='?')
args = parser.parse_args()

#creating scans directory
if not os.path.exists('~/scans'):
    os.system('mkdir ~/scans')

if not args.ports:
    for i in range(1000):
        ports.append(i)



#changing variables according to arguments
if args.ports:
    ports = []
    try:
        ports = args.port.replace(',',' ')
        ports = (ports.split())
        ports = list(map(int, ports))
    except Exception as e:
        print(e)
        print(f'{Fore.RED}No Arguments given for --ports')
    if not args.search:
        print(f"Scanning Ports {' '.join(str(e) for e in ports)}")
    elif args.search:
        print(f"All Found Records Of Port/s {' '.join(str(e) for e in ports)}" )


#searches through the ip logs for open ports
def search_ips():
    if args.search:
        if args.ports:
            for port in ports:
                try:
                    os.system(f'cat ~/scans/* |grep "Port {port} is open for " ')
                except Exception as e:
                    print(e)
                    print(f'Could Not Find {os.getenv("HOME")}/scans')
        else:
            try:
                os.system(f'cat ~/scans/* |grep " is open for " ')
            except Exception as e:
                print(e)
                print(f'Could Not Find {os.getenv("HOME")}/scans')
    exit()





#find valid IPs
def find_ip():
    global ip
    ip = []
    for i in range(4):
        ip.append(str(random.randint(0,255)))
    ip = '.'.join(ip)




#logs the ips along with the valid ports
def log_ip(ip):
    scan(ip)
    os.system(f'touch ~/scans/{ip}_{current_open}------{hostname}')

    f = open(f"{os.getenv('HOME')}/scans/{ip}", "a")

    f.write(str(port_info))
    print(f'Writen to file ~/scans/{ip}')
    f.close()

    ips.append(ip)




#scans the selected ports of the valid IPs
def scan(ip):


    global port_info
    global current_open
    port_info = ''
    current_open = []
    for port in ports:
        if args.verbose:
            print(f'Scanning Port {port}',end='\r')

        try:
            adress = (f"{ip}", port)
            check_if_open = s.connect_ex(adress)
            if check_if_open  == 0:
                if args.verbose:
                    print(f'{Fore.GREEN} OPEN {Fore.WHITE}', end = '\r')

                hostname = socket.gethostbyaddr(ip)
                current_open.append(f'{port}')
                port_info += (f"{Fore.GREEN} Port {port} is open for {ip} {hostname[0]} {Fore.WHITE}\n\n")
                print(socket.gethostbyaddr(ip))
            else:
                if args.verbose:
                    print(f'{Fore.RED} CLOSED {Fore.WHITE}')

                port_info += (f"{Fore.RED}Port {port } is not open for {ip} {Fore.WHITE}\n\n")
        except Exception as e:
            port_info += (f'{port} Couldnt Connect: {e}\n')
            continue





#checks the host is up
def check_ip(ip):
    response = bool
    try:
        subprocess.check_output(["ping", "-c", "1", '-w 1',ip])
        response = True
    except subprocess.CalledProcessError:
        response = False

    if response:
        print(f'({Fore.GREEN}+{Fore.WHITE}) {ip} is an IP')
        log_ip(ip)



    elif not response:
        print(f'({Fore.RED}-{Fore.WHITE}) {ip} is not an IP')

#runs all the code
def main():
    if args.search:
        search_ips()

    find_ip()
    check_ip(ip)
    main()


if __name__ == '__main__':

    main()


