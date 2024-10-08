import socket
from IPy import IP
import requests
from bs4 import BeautifulSoup
import sqlmap
import xsser

class PortScanner:
    def __init__(self, target, port_num):
        self.target = target
        self.port_num = port_num
        self.open_ports = []
        self.banners = []

    def scan(self):
        for port in range(1, self.port_num):
            self.scan_port(port)

    def check_ip(self):
        try:
            IP(self.target)
            return self.target
        except ValueError:
            return socket.gethostbyname(self.target)

    def scan_port(self, port):
        try:
            converted_ip = self.check_ip()
            sock = socket.socket()
            sock.settimeout(0.5)
            sock.connect((converted_ip, port))
            self.open_ports.append(port)
            try:
                banner = sock.recv(1024).decode().strip('\n').strip('\r')
                self.banners.append(banner)
            except:
                self.banners.append(' ')
            sock.close()
        except:
            pass

    def get_open_ports(self):
        return self.open_ports

    def get_banners(self):
        return self.banners

class VulnerabilityScanner:
    def __init__(self, target):
        self.target = target
        self.vulnerabilities = []

    def scan(self):
        self.scan_sql_injection()
        self.scan_xss()
        self.scan_csrf()

    def scan_sql_injection(self):
        sqlmap_url = f"http://{self.target}/"
        sqlmap_cmd = f"sqlmap -u {sqlmap_url} --batch"
        output = subprocess.check_output(sqlmap_cmd, shell=True)
        if "SQL injection" in output.decode():
            self.vulnerabilities.append("SQL injection")

    def scan_xss(self):
        xsser_url = f"http://{self.target}/"
        xsser_cmd = f"xsser -u {xsser_url} --batch"
        output = subprocess.check_output(xsser_cmd, shell=True)
        if "XSS" in output.decode():
            self.vulnerabilities.append("XSS")

    def scan_csrf(self):
        csrf_url = f"http://{self.target}/"
        response = requests.get(csrf_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        forms = soup.find_all('form')
        for form in forms:
            if form.get('action') and form.get('method') == 'post':
                self.vulnerabilities.append("CSRF")

    def get_vulnerabilities(self):
        return self.vulnerabilities

def main():
    target = input("Enter the target IP or domain: ")
    port_num = int(input("Enter the number of ports to scan: "))

    port_scanner = PortScanner(target, port_num)
    port_scanner.scan()
    open_ports = port_scanner.get_open_ports()
    banners = port_scanner.get_banners()

    print("Open ports:")
    for port in open_ports:
        print(port)

    print("\nBanners:")
    for banner in banners:
        print(banner)

    vulnerability_scanner = VulnerabilityScanner(target)
    vulnerability_scanner.scan()
    vulnerabilities = vulnerability_scanner.get_vulnerabilities()

    print("\nVulnerabilities:")
    for vulnerability in vulnerabilities:
        print(vulnerability)

if __name__ == "__main__":
    main()
