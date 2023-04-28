import random
import socket
import subprocess
import os
from datetime import datetime 
from urllib.request import urlopen  
import urllib
import re
import ssl

# variables that dont need to be changed
count_packets = str()
packet_timeout = str()
port = 80
matches = []

web_services = {

    "Adobe Experience Manager": ["Adobe Experience Manager", "AEM"],
    "Akamai": ["Akamai"],
    "Alibaba Cloud": ["Alibaba Cloud"],
    "Amazon Web Services": ["Amazon Web Services", "AWS"],
    "Apache": ["Apache", "httpd"],
    "ASP.NET": ["ASP.NET"],
    "Atlassian": ["Atlassian"],
    "Bluehost": ["Bluehost"],
    "Bootstrap": ["Bootstrap"],
    "cPanel": ["cPanel"],
    "Cloudflare": ["Cloudflare"],
    "Comodo": ["Comodo"],
    "cPanel": ["cPanel"],
    "Drupal": ["Drupal"],
    "Dynatrace": ["Dynatrace"],
    "F5 BIG-IP": ["F5 BIG-IP"],
    "Facebook": ["Facebook"],
    "Fastly": ["Fastly"],
    "Firebase": ["Firebase"],
    "GitLab": ["GitLab"],
    "GitHub": ["GitHub"],
    "Gmail": ["Gmail"],
    "GoDaddy": ["GoDaddy"],
    "Google Ads": ["Google Ads", "AdWords"],
    "Google Analytics": ["Google Analytics"],
    "Google Cloud": ["Google Cloud"],
    "Google Maps": ["Google Maps"],
    "Google Tag Manager": ["Google Tag Manager"],
    "Heroku": ["Heroku"],
    "Hikvision": ["Hikvision"],
    "IBM Cloud": ["IBM Cloud"],
    "Joomla": ["Joomla"],
    "jQuery": ["jQuery"],
    "Jetty": ["Jetty"],
    "Kubernetes": ["Kubernetes"],
    "Let's Encrypt": ["Let's Encrypt"],
    "Lighttpd": ["Lighttpd"],
    "Magento": ["Magento"],
    "Mailchimp": ["Mailchimp"],
    "MaxCDN": ["MaxCDN"],
    "Microsoft Azure": ["Microsoft Azure"],
    "Microsoft IIS": ["Microsoft IIS"],
    "Nginx": ["Nginx"],
    "Node.js": ["Node.js"],
    "Oracle Cloud": ["Oracle Cloud"],
    "Plesk": ["Plesk"],
    "Python": ["Python"],
    "Qualys": ["Qualys"],
    "Rackspace": ["Rackspace"],
    "React": ["React"],
    "Red Hat": ["Red Hat"],
    "Salesforce": ["Salesforce"],
    "SAP": ["SAP"],
    "Shopify": ["Shopify"],
    "Sitecore": ["Sitecore"],
    "Squarespace": ["Squarespace"],
    "SSL.com": ["SSL.com"],
    "Stripe": ["Stripe"],
    "Sucuri": ["Sucuri"],
    "Tawk.to": ["Tawk.to"],
    "TeamViewer": ["TeamViewer"],
    "Tencent Cloud": ["Tencent Cloud"],
    "Tomcat": ["Tomcat"],
    "Travis CI": ["Travis CI"],
    "Twilio": ["Twilio"],
    "Twitter": ["Twitter"],
    "Ubuntu": ["Ubuntu"],
    "Varnish": ["Varnish"],
    "Vimeo": ["Vimeo"],
    "VMware": ["VMware"],
    "W3 Total Cache": ["W3 Total Cache"],
    "Wix": ["Wix"],
    "Weebly": ["Weebly"],
    "WHM": ["WHM"],
    "Windows Server": ["Windows Server"],
    "WordPress": ["WordPress"],
    "XenForo": ["XenForo"],
    "Yahoo!": ["Yahoo!"]}


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
                print_result(ip,port,0,hostname,matches)
                continue
        match scan:
            case 0:
                get_hostname(ip)
                fingerprint(ip)
                print_result(ip,port,2,hostname,matches)

            case _:
                print_result(ip,port,1,hostname,matches)

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
def print_result(ip,port,result,hostname, matches):
    match result:
        case 0:
            print(f"\r{get_time()} - {ip} is not a valid IP address  ", end="\r")
        case 1:
            print(f"\r{get_time()} - {ip}:{port}  is not open  ", end="\r")
        case 2:
            print(f"\033[K{get_time()} - {ip}:{port} ({hostname}) is open ({', '.join(matches)})")

# attempt to fingerprint what type of service is running
def fingerprint(ip):
    global matches
    if port == 80 or port == 443:
        try:
            website = urlopen(f"https://{ip}:{port}").read().decode("utf8")
        except (ssl.SSLError,urllib.error.URLError):
            matches = ["Could not fingerprint services, if you know what service is running please make a pull request at https://github.com/pwn4d/Ipscanner"]
            return
        for service, keywords in web_services.items():
         
            for keyword in keywords:
                matches += re.findall(keyword, website, re.IGNORECASE)
            if matches:
                print(matches)
            else:
                matches = ["Could not fingerprint services, if you know what service is running please make a pull request at https://github.com/pwn4d/Ipscanner"]
                print(matches)





main()
