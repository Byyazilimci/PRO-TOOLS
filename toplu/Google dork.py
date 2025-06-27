#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import argparse
import time
import random
import sys
import os
from urllib.parse import quote_plus, urlparse
import socket
import whois
from datetime import datetime
import json
import dns.resolver
import re
from colorama import init, Fore, Back, Style

# Renkleri başlat
init(autoreset=True)

class DorkMasterPro:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.results = []
        self.total_results = 0
        self.cache = {}
        self.deep_scan_enabled = False
        self.advanced_dorks = {
            '1': {'name': 'Gizli Admin Panelleri', 'dork': 'intitle:"admin login" "password"', 'desc': 'Gizli yönetim panellerini bulur'},
            '2': {'name': 'Açık Veritabanları', 'dork': 'intitle:"index of" "database"', 'desc': 'Açık veritabanı dizinlerini bulur'},
            '3': {'name': 'Gizli API Uçları', 'dork': 'inurl:"/api/v1" intext:"api key"', 'desc': 'Gizli API uç noktalarını bulur'},
            '4': {'name': 'Güvenlik Açıkları', 'dork': 'filetype:pdf "vulnerability report"', 'desc': 'Güvenlik açığı raporlarını bulur'},
            '5': {'name': 'Şifreler', 'dork': 'filetype:txt "password"', 'desc': 'Düz metin şifre dosyalarını bulur'},
            '6': {'name': 'Gizli Git Dizinleri', 'dork': 'intitle:"index of" /.git', 'desc': 'Açık .git dizinlerini bulur'},
            '7': {'name': 'SSH Anahtarları', 'dork': 'filetype:key "BEGIN RSA PRIVATE KEY"', 'desc': 'SSH private keylerini bulur'},
            '8': {'name': 'Gizli Backup Dosyaları', 'dork': 'filetype:bak intext:"backup"', 'desc': 'Yedek dosyalarını bulur'},
            '9': {'name': 'Gizli FTP Sunucuları', 'dork': 'intitle:"index of" "ftp"', 'desc': 'Açık FTP sunucularını bulur'},
            '10': {'name': 'Gizli Kameralar', 'dork': 'inurl:"/view.shtml" intitle:"Live View"', 'desc': 'Açık IP kameralarını bulur'},
            '11': {'name': 'Gizli Log Dosyaları', 'dork': 'filetype:log "error"', 'desc': 'Hata log dosyalarını bulur'},
            '12': {'name': 'Gizli SQL Dump', 'dork': 'filetype:sql "INSERT INTO"', 'desc': 'SQL dump dosyalarını bulur'},
            '13': {'name': 'Gizli E-posta Listeleri', 'dork': 'filetype:xls "email"', 'desc': 'E-posta listelerini bulur'},
            '14': {'name': 'Gizli Config Dosyaları', 'dork': 'filetype:conf "password"', 'desc': 'Yapılandırma dosyalarını bulur'},
            '15': {'name': 'Gizli Shell Scriptleri', 'dork': 'filetype:sh "#!/bin/bash"', 'desc': 'Shell scriptlerini bulur'},
            '16': {'name': 'Google Önbellek', 'dork': 'cache:', 'desc': 'Google önbelleğindeki sayfaları bulur'},
            '17': {'name': 'Gizli Dizinler', 'dork': 'intitle:"index of /"', 'desc': 'Açık dizinleri bulur'},
            '18': {'name': 'Gizli PHP Sayfaları', 'dork': 'inurl:".php?id="', 'desc': 'Dinamik PHP sayfalarını bulur'},
            '19': {'name': 'Gizli ASP Sayfaları', 'dork': 'inurl:".asp?id="', 'desc': 'Dinamik ASP sayfalarını bulur'},
            '20': {'name': 'Gizli JS Dosyaları', 'dork': 'filetype:js "API_KEY"', 'desc': 'JavaScript dosyalarındaki gizli bilgileri bulur'}
        }

    def show_dynamic_banner(self):
        """Dinamik banner göster"""
        banner = f"""
{Fore.RED}
██████╗  ██████╗ ██████╗ ██╗  ██╗███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗ 
██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
██║  ██║██║   ██║██████╔╝█████╔╝ ██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝
██║  ██║██║   ██║██╔══██╗██╔═██╗ ██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗
██████╔╝╚██████╔╝██║  ██║██║  ██╗██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║
╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
                                                                                      
{Fore.YELLOW}════════════════════════════════════════════════════════════════════════════════
   Gelişmiş Google Dork Arama Aracı v4.0 | By DorkMaster Pro Team
════════════════════════════════════════════════════════════════════════════════
{Style.RESET_ALL}"""
        
        # Animasyon efekti
        for line in banner.split('\n'):
            print(line)
            time.sleep(0.03)

    def enable_deep_scan(self):
        """Derin tarama modunu etkinleştir"""
        self.deep_scan_enabled = True
        print(f"{Fore.MAGENTA}[*] Derin tarama modu etkinleştirildi!{Style.RESET_ALL}")

    def search_with_proxy(self, proxy=None):
        """Proxy ile arama yap"""
        if proxy:
            self.session.proxies = {
                'http': proxy,
                'https': proxy
            }
            print(f"{Fore.CYAN}[*] Proxy kullanılıyor: {proxy}{Style.RESET_ALL}")

    def search(self, dork, pages=1, delay=3, verbose=False):
        """Google'da dork araması yapar ve sonuçları döndürür"""
        self.results = []
        self.total_results = 0
        
        for page in range(pages):
            try:
                start = page * 10
                url = f"https://www.google.com/search?q={quote_plus(dork)}&start={start}"
                
                if verbose:
                    print(f"{Fore.YELLOW}[*] Sayfa {page + 1}/{pages} aranıyor...{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}[i] Sorgu URL: {url}{Style.RESET_ALL}")
                
                # Rastgele gecikme ekle
                sleep_time = delay + random.uniform(-1, 1)
                if verbose:
                    print(f"{Fore.MAGENTA}[i] {sleep_time:.1f} saniye bekleniyor...{Style.RESET_ALL}")
                time.sleep(max(2, sleep_time))
                
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                if "detected unusual traffic" in response.text:
                    print(f"{Back.RED}{Fore.WHITE}[!] Google tarafından engellendi! CAPTCHA gösteriliyor olabilir.{Style.RESET_ALL}")
                    return False
                
                soup = BeautifulSoup(response.text, 'html.parser')
                self._parse_results(soup, dork)
                
            except requests.RequestException as e:
                print(f"{Back.RED}{Fore.WHITE}[!] Arama hatası: {e}{Style.RESET_ALL}")
                return False
        
        return True

    def _parse_results(self, soup, dork):
        """Google sonuç sayfasını ayrıştırır"""
        result_block = soup.find_all('div', attrs={'class': 'g'})
        
        for result in result_block:
            link = result.find('a', href=True)
            title = result.find('h3')
            description = result.find('div', {'class': 'IsZvec'})
            
            if link and title:
                url = link['href']
                if url.startswith('/url?q='):
                    url = url[7:].split('&')[0]
                
                # Geçerli bir URL mi kontrol et
                if url.startswith('http'):
                    # Cache kontrolü
                    if url in self.cache:
                        continue
                    
                    self.cache[url] = True
                    
                    # Domain bilgilerini topla
                    domain_info = self._get_domain_info(url)
                    
                    # Derin tarama yap
                    if self.deep_scan_enabled:
                        deep_info = self._deep_scan(url)
                        domain_info.update(deep_info)
                    
                    result_data = {
                        'title': title.text,
                        'url': url,
                        'description': description.text if description else '',
                        'dork': dork,
                        'domain': domain_info.get('domain', ''),
                        'ip': domain_info.get('ip', ''),
                        'server': domain_info.get('server', ''),
                        'country': domain_info.get('country', ''),
                        'technologies': domain_info.get('technologies', []),
                        'dns': domain_info.get('dns', []),
                        'hidden_paths': domain_info.get('hidden_paths', []),
                        'cached_url': f"https://webcache.googleusercontent.com/search?q=cache:{quote_plus(url)}"
                    }
                    
                    self.results.append(result_data)
                    self.total_results += 1

    def _get_domain_info(self, url):
        """Domain hakkında bilgi toplar"""
        domain_info = {}
        
        try:
            parsed_uri = urlparse(url)
            domain = parsed_uri.netloc
            
            # www'yi kaldır
            if domain.startswith('www.'):
                domain = domain[4:]
            
            domain_info['domain'] = domain
            
            # IP adresini bul
            try:
                ip = socket.gethostbyname(domain)
                domain_info['ip'] = ip
                
                # Ters DNS sorgusu
                try:
                    rev_dns = socket.gethostbyaddr(ip)
                    domain_info['reverse_dns'] = rev_dns[0]
                except:
                    pass
            except:
                domain_info['ip'] = 'Bilinmiyor'
            
            # WHOIS bilgisi
            try:
                w = whois.whois(domain)
                if w.country:
                    domain_info['country'] = w.country
                else:
                    domain_info['country'] = 'Bilinmiyor'
                
                if w.creation_date:
                    if isinstance(w.creation_date, list):
                        domain_info['creation_date'] = w.creation_date[0].strftime('%Y-%m-%d')
                    else:
                        domain_info['creation_date'] = w.creation_date.strftime('%Y-%m-%d')
            except:
                domain_info['country'] = 'Bilinmiyor'
            
            # Sunucu bilgisi (HEAD isteği ile)
            try:
                response = requests.head(url, headers=self.headers, timeout=5, allow_redirects=True)
                if 'Server' in response.headers:
                    domain_info['server'] = response.headers['Server']
                else:
                    domain_info['server'] = 'Bilinmiyor'
                
                # Teknoloji tespiti
                tech = []
                if 'X-Powered-By' in response.headers:
                    tech.append(response.headers['X-Powered-By'])
                domain_info['technologies'] = tech
            except:
                domain_info['server'] = 'Bilinmiyor'
            
            # DNS kayıtları
            try:
                dns_records = []
                for qtype in ['A', 'AAAA', 'MX', 'NS', 'TXT']:
                    try:
                        answers = dns.resolver.resolve(domain, qtype, raise_on_no_answer=False)
                        for rdata in answers:
                            dns_records.append(f"{qtype}: {rdata.to_text()}")
                    except:
                        pass
                domain_info['dns'] = dns_records
            except:
                domain_info['dns'] = []
                
        except Exception as e:
            print(f"{Fore.RED}[!] Domain bilgisi alınırken hata: {e}{Style.RESET_ALL}")
        
        return domain_info

    def _deep_scan(self, url):
        """Derin tarama yapar"""
        deep_info = {
            'hidden_paths': [],
            'technologies': []
        }
        
        try:
            parsed_uri = urlparse(url)
            base_url = f"{parsed_uri.scheme}://{parsed_uri.netloc}"
            
            # Yaygın gizli dizinleri kontrol et
            common_paths = [
                '/admin', '/backup', '/config', '/database', 
                '/logs', '/tmp', '/secret', '/api', '/.git',
                '/.env', '/wp-admin', '/phpmyadmin'
            ]
            
            for path in common_paths:
                try:
                    test_url = f"{base_url}{path}"
                    response = requests.head(test_url, headers=self.headers, timeout=3, allow_redirects=True)
                    
                    if response.status_code == 200:
                        deep_info['hidden_paths'].append({
                            'path': path,
                            'status': response.status_code,
                            'url': test_url
                        })
                except:
                    pass
            
            # Teknoloji tespiti
            try:
                response = requests.get(base_url, headers=self.headers, timeout=5)
                html = response.text
                
                # CMS tespiti
                if 'wp-content' in html:
                    deep_info['technologies'].append('WordPress')
                if 'Joomla' in html:
                    deep_info['technologies'].append('Joomla')
                if 'Drupal' in html:
                    deep_info['technologies'].append('Drupal')
                
                # Framework tespiti
                if 'laravel' in html.lower():
                    deep_info['technologies'].append('Laravel')
                if 'react' in html.lower():
                    deep_info['technologies'].append('React')
                if 'vue' in html.lower():
                    deep_info['technologies'].append('Vue.js')
                
                # Sunucu bilgileri
                if 'X-Powered-By' in response.headers:
                    deep_info['technologies'].append(response.headers['X-Powered-By'])
                
            except:
                pass
            
        except Exception as e:
            print(f"{Fore.RED}[!] Derin tarama hatası: {e}{Style.RESET_ALL}")
        
        return deep_info

    def print_results(self):
        """Sonuçları ekrana yazdırır"""
        print(f"\n{Back.GREEN}{Fore.WHITE}════════════════════════════════════════════════════════════════════════════════{Style.RESET_ALL}")
        print(f"{Back.GREEN}{Fore.WHITE}  TOPLAM {self.total_results} SONUÇ BULUNDU  {Style.RESET_ALL}")
        print(f"{Back.GREEN}{Fore.WHITE}════════════════════════════════════════════════════════════════════════════════{Style.RESET_ALL}\n")
        
        for i, result in enumerate(self.results, 1):
            print(f"{Fore.YELLOW}════════════════════════════════════════════════════════════════════════════════{Style.RESET_ALL}")
            print(f"{Fore.CYAN}SONUÇ #{i} | Dork: {result['dork']}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}════════════════════════════════════════════════════════════════════════════════{Style.RESET_ALL}")
            
            print(f"{Fore.GREEN}║{Style.RESET_ALL}")
            print(f"{Fore.GREEN}╠▶ BAŞLIK:{Style.RESET_ALL} {result['title']}")
            print(f"{Fore.GREEN}╠▶ URL:{Style.RESET_ALL} {Fore.BLUE}{result['url']}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}╠▶ ÖNBELLEK:{Style.RESET_ALL} {Fore.MAGENTA}{result['cached_url']}{Style.RESET_ALL}")
            
            if result['description']:
                print(f"{Fore.GREEN}╠▶ AÇIKLAMA:{Style.RESET_ALL} {result['description']}")
            
            print(f"{Fore.GREEN}╠▶ DOMAİN:{Style.RESET_ALL} {result['domain']}")
            print(f"{Fore.GREEN}╠▶ IP:{Style.RESET_ALL} {result['ip']}")
            
            if 'reverse_dns' in result:
                print(f"{Fore.GREEN}╠▶ TERS DNS:{Style.RESET_ALL} {result['reverse_dns']}")
            
            if result['country'] != 'Bilinmiyor':
                print(f"{Fore.GREEN}╠▶ ÜLKE:{Style.RESET_ALL} {result['country']}")
            
            if result['server'] != 'Bilinmiyor':
                print(f"{Fore.GREEN}╠▶ SUNUCU:{Style.RESET_ALL} {result['server']}")
            
            if 'creation_date' in result:
                print(f"{Fore.GREEN}╠▶ OLUŞTURMA TARİHİ:{Style.RESET_ALL} {result['creation_date']}")
            
            if result['technologies']:
                print(f"{Fore.GREEN}╠▶ TEKNOLOJİLER:{Style.RESET_ALL} {', '.join(result['technologies'])}")
            
            if result['dns']:
                print(f"{Fore.GREEN}╠▶ DNS KAYITLARI:{Style.RESET_ALL}")
                for record in result['dns']:
                    print(f"   {record}")
            
            if result['hidden_paths']:
                print(f"{Fore.GREEN}╠▶ KEŞFEDİLEN GİZLİ YOLLAR:{Style.RESET_ALL}")
                for path in result['hidden_paths']:
                    print(f"   {path['path']} ({path['status']}) - {Fore.BLUE}{path['url']}{Style.RESET_ALL}")
            
            print(f"{Fore.GREEN}║{Style.RESET_ALL}")
            print()

    def save_results(self, filename, format='txt'):
        """Sonuçları dosyaya kaydeder"""
        try:
            if format == 'txt':
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("╔══════════════════════════════════════════════════════════════════╗\n")
                    f.write("║                  DORKMASTER PRO - ARAMA SONUÇLARI               ║\n")
                    f.write("╠══════════════════════════════════════════════════════════════════╣\n")
                    f.write(f"║ Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"║ Toplam Sonuç: {self.total_results}\n")
                    f.write("╚══════════════════════════════════════════════════════════════════╝\n\n")
                    
                    for i, result in enumerate(self.results, 1):
                        f.write(f"════════════════════════════════════════════════════════════════════\n")
                        f.write(f"SONUÇ #{i} | Dork: {result['dork']}\n")
                        f.write(f"════════════════════════════════════════════════════════════════════\n")
                        f.write(f"BAŞLIK: {result['title']}\n")
                        f.write(f"URL: {result['url']}\n")
                        f.write(f"ÖNBELLEK: {result['cached_url']}\n")
                        
                        if result['description']:
                            f.write(f"AÇIKLAMA: {result['description']}\n")
                        
                        f.write(f"DOMAİN: {result['domain']}\n")
                        f.write(f"IP: {result['ip']}\n")
                        
                        if 'reverse_dns' in result:
                            f.write(f"TERS DNS: {result['reverse_dns']}\n")
                        
                        if result['country'] != 'Bilinmiyor':
                            f.write(f"ÜLKE: {result['country']}\n")
                        
                        if result['server'] != 'Bilinmiyor':
                            f.write(f"SUNUCU: {result['server']}\n")
                        
                        if 'creation_date' in result:
                            f.write(f"OLUŞTURMA TARİHİ: {result['creation_date']}\n")
                        
                        if result['technologies']:
                            f.write(f"TEKNOLOJİLER: {', '.join(result['technologies'])}\n")
                        
                        if result['dns']:
                            f.write(f"DNS KAYITLARI:\n")
                            for record in result['dns']:
                                f.write(f"   {record}\n")
                        
                        if result['hidden_paths']:
                            f.write(f"KEŞFEDİLEN GİZLİ YOLLAR:\n")
                            for path in result['hidden_paths']:
                                f.write(f"   {path['path']} ({path['status']}) - {path['url']}\n")
                        
                        f.write("\n")
            
            elif format == 'json':
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump({
                        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'total_results': self.total_results,
                        'results': self.results
                    }, f, indent=4, ensure_ascii=False)
            
            print(f"{Back.GREEN}{Fore.WHITE}[+] Sonuçlar '{filename}' dosyasına kaydedildi.{Style.RESET_ALL}")
        except IOError as e:
            print(f"{Back.RED}{Fore.WHITE}[!] Dosya yazma hatası: {e}{Style.RESET_ALL}")

def clear_screen():
    """Ekranı temizler"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu(scanner):
    """Ana menüyü gösterir"""
    print(f"\n{Fore.YELLOW}╔══════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}║{Fore.RED}                      ANA MENÜ                          {Fore.YELLOW}║{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}╠══════════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}║{Style.RESET_ALL} {Fore.GREEN}1.{Style.RESET_ALL} Önceden Tanımlanmış Dorklarla Ara                   {Fore.YELLOW}║{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}║{Style.RESET_ALL} {Fore.GREEN}2.{Style.RESET_ALL} Manuel Dork Arama                              {Fore.YELLOW}║{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}║{Style.RESET_ALL} {Fore.GREEN}3.{Style.RESET_ALL} Dork Listesini Görüntüle                        {Fore.YELLOW}║{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}║{Style.RESET_ALL} {Fore.GREEN}4.{Style.RESET_ALL} Derin Tarama Modunu Aç/Kapat                    {Fore.YELLOW}║{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}║{Style.RESET_ALL} {Fore.GREEN}5.{Style.RESET_ALL} Çıkış                                         {Fore.YELLOW}║{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")

def show_dork_list(scanner):
    """Dork listesini gösterir"""
    print(f"\n{Fore.YELLOW}╔══════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}║{Fore.RED}              ÖN TANIMLI DORK LİSTESİ                   {Fore.YELLOW}║{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}╠══════════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
    
    for key, value in scanner.advanced_dorks.items():
        print(f"{Fore.YELLOW}║{Style.RESET_ALL} {Fore.GREEN}{key:>2}.{Style.RESET_ALL} {value['name']:<30} {Fore.CYAN}{value['dork']:<40}{Fore.YELLOW}║{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}║{Style.RESET_ALL}    {value['desc']:<70}{Fore.YELLOW}║{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}║{Style.RESET_ALL}    {'-'*70}{Fore.YELLOW}║{Style.RESET_ALL}")
    
    print(f"{Fore.YELLOW}╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")

def predefined_search(scanner):
    """Ön tanımlı dorklarla arama yapar"""
    show_dork_list(scanner)
    
    while True:
        choice = input(f"{Fore.YELLOW}[?] Seçim yapın (1-20) veya 'q' ile çıkın: {Style.RESET_ALL}").strip().lower()
        
        if choice == 'q':
            return
        
        if choice in scanner.advanced_dorks:
            dork = scanner.advanced_dorks[choice]['dork']
            desc = scanner.advanced_dorks[choice]['desc']
            name = scanner.advanced_dorks[choice]['name']
            
            print(f"\n{Fore.YELLOW}════════════════════════════════════════════════════════════════════{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Seçilen Dork:{Style.RESET_ALL} {Fore.GREEN}{name}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Dork Sorgusu:{Style.RESET_ALL} {dork}")
            print(f"{Fore.CYAN}Açıklama:{Style.RESET_ALL} {desc}")
            print(f"{Fore.YELLOW}════════════════════════════════════════════════════════════════════{Style.RESET_ALL}")
            
            try:
                pages = int(input(f"{Fore.YELLOW}[?] Kaç sayfa taranacak? (1-5): {Style.RESET_ALL}").strip())
                pages = max(1, min(5, pages))  # 1-5 arasında sınırla
            except ValueError:
                print(f"{Fore.RED}[!] Geçersiz sayı! Varsayılan olarak 1 kullanılıyor.{Style.RESET_ALL}")
                pages = 1
            
            output_file = input(f"{Fore.YELLOW}[?] Sonuçları kaydetmek için dosya adı (boş bırakabilirsiniz): {Style.RESET_ALL}").strip()
            
            output_format = 'txt'
            if output_file:
                output_format = input(f"{Fore.YELLOW}[?] Çıktı formatı (txt/json, varsayılan: txt): {Style.RESET_ALL}").strip().lower()
                if output_format not in ['txt', 'json']:
                    output_format = 'txt'
            
            print(f"\n{Fore.GREEN}[*] Arama başlatılıyor...{Style.RESET_ALL}")
            if scanner.search(dork, pages, verbose=True):
                scanner.print_results()
                
                if output_file:
                    scanner.save_results(output_file, output_format)
            break
        else:
            print(f"{Fore.RED}[!] Geçersiz seçim! Lütfen 1-20 arasında bir sayı girin.{Style.RESET_ALL}")

def manual_search(scanner):
    """Kullanıcının manuel dork girmesini sağlar"""
    print(f"\n{Fore.YELLOW}════════════════════════════════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.RED}                     MANUEL DORK ARAMA                     {Style.RESET_ALL}")
    print(f"{Fore.YELLOW}════════════════════════════════════════════════════════════════════{Style.RESET_ALL}")
    
    dork = input(f"{Fore.YELLOW}[?] Arama yapmak istediğiniz dork'u girin: {Style.RESET_ALL}").strip()
    
    if not dork:
        print(f"{Fore.RED}[!] Dork boş olamaz!{Style.RESET_ALL}")
        return
    
    try:
        pages = int(input(f"{Fore.YELLOW}[?] Kaç sayfa taranacak? (1-5): {Style.RESET_ALL}").strip())
        pages = max(1, min(5, pages))  # 1-5 arasında sınırla
    except ValueError:
        print(f"{Fore.RED}[!] Geçersiz sayı! Varsayılan olarak 1 kullanılıyor.{Style.RESET_ALL}")
        pages = 1
    
    output_file = input(f"{Fore.YELLOW}[?] Sonuçları kaydetmek için dosya adı (boş bırakabilirsiniz): {Style.RESET_ALL}").strip()
    
    output_format = 'txt'
    if output_file:
        output_format = input(f"{Fore.YELLOW}[?] Çıktı formatı (txt/json, varsayılan: txt): {Style.RESET_ALL}").strip().lower()
        if output_format not in ['txt', 'json']:
            output_format = 'txt'
    
    print(f"\n{Fore.GREEN}[*] Arama başlatılıyor...{Style.RESET_ALL}")
    if scanner.search(dork, pages, verbose=True):
        scanner.print_results()
        
        if output_file:
            scanner.save_results(output_file, output_format)

def toggle_deep_scan(scanner):
    """Derin tarama modunu aç/kapat"""
    if scanner.deep_scan_enabled:
        scanner.deep_scan_enabled = False
        print(f"{Fore.MAGENTA}[*] Derin tarama modu devre dışı bırakıldı!{Style.RESET_ALL}")
    else:
        scanner.enable_deep_scan()

def main():
    try:
        clear_screen()
        scanner = DorkMasterPro()
        scanner.show_dynamic_banner()
        
        # Proxy ayarı
        proxy = input(f"{Fore.YELLOW}[?] Proxy kullanmak ister misiniz? (örn: http://127.0.0.1:8080, boş bırakabilirsiniz): {Style.RESET_ALL}").strip()
        if proxy:
            scanner.search_with_proxy(proxy)
        
        while True:
            show_menu(scanner)
            choice = input(f"{Fore.YELLOW}[?] Seçiminiz (1-5): {Style.RESET_ALL}").strip()
            
            if choice == '1':
                predefined_search(scanner)
            elif choice == '2':
                manual_search(scanner)
            elif choice == '3':
                show_dork_list(scanner)
            elif choice == '4':
                toggle_deep_scan(scanner)
            elif choice == '5':
                print(f"\n{Fore.GREEN}[*] Çıkış yapılıyor...{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}[!] Geçersiz seçim! Lütfen 1-5 arasında bir sayı girin.{Style.RESET_ALL}")
            
            input(f"\n{Fore.YELLOW}[!] Devam etmek için Enter'a basın...{Style.RESET_ALL}")
            clear_screen()
            scanner.show_dynamic_banner()
    
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Program kapatıldı.{Style.RESET_ALL}")
        sys.exit(0)

if __name__ == '__main__':
    # Gerekli kütüphaneleri kontrol et
    try:
        import whois
        import dns.resolver
    except ImportError:
        print(f"{Fore.RED}[!] Gerekli kütüphaneler eksik:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[i] Kurmak için: pip install python-whois dnspython{Style.RESET_ALL}")
        sys.exit(1)
    
    main()