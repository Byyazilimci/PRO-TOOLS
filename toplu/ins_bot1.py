#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import logging
from getpass import getpass
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException
)

class InstagramVideoWatcherPro:
    def __init__(self):
        self.setup_logging()
        self.driver = None
        self.credentials = {}
        self.video_urls = []  # Birden fazla video URL'si için liste
        self.watch_count = 0
        self.current_watch = 0
        self.setup_config()

    def setup_logging(self):
        """Loglama sistemini kur"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('instagram_bot.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def setup_config(self):
        """Kullanıcıdan gerekli bilgileri al"""
        try:
            self.logger.info("\n=== Instagram Video İzleme Botu Pro ===")
            
            self.credentials['username'] = input("Instagram Kullanıcı Adı: ").strip()
            if not self.credentials['username']:
                raise ValueError("Kullanıcı adı boş olamaz")
            
            self.credentials['password'] = getpass("Şifre: ").strip()
            if not self.credentials['password']:
                raise ValueError("Şifre boş olamaz")
            
            # Birden fazla video URL'si al
            url_count = int(input("Kaç video izlenecek? (1-5): "))
            if not 1 <= url_count <= 5:
                raise ValueError("Geçersiz video sayısı (1-5 aralığında olmalı)")
            
            for i in range(url_count):
                url = input(f"Video {i+1} URL: ").strip()
                if not url.startswith(('https://www.instagram.com/', 'http://www.instagram.com/')):
                    raise ValueError("Geçersiz Instagram URL formatı")
                self.video_urls.append(url)
            
            self.watch_count = int(input("Toplam İzleme Sayısı (1-1000): "))
            if not 1 <= self.watch_count <= 1000:
                raise ValueError("Geçersiz izleme sayısı (1-1000 aralığında olmalı)")
            
        except ValueError as e:
            self.logger.error(f"Hata: {str(e)}")
            sys.exit(1)

    def setup_driver(self):
        """Chrome WebDriver ayarları"""
        try:
            chrome_options = Options()
            
            # Gelişmiş tarayıcı ayarları
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument("--lang=tr-TR")
            chrome_options.add_argument("--mute-audio")
            chrome_options.add_argument("--start-maximized")
            
            # Headless mod (isteğe bağlı)
            if input("Gizli modda çalıştırılsın mı? (e/h): ").lower() == 'e':
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--window-size=1920,1080")  # Headless için pencere boyutu
            
            # Otomatik ChromeDriver yükleme
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Tarayıcı özelliklerini maskeleme
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            
            self.driver.implicitly_wait(10)
            return True
            
        except Exception as e:
            self.logger.error(f"Driver kurulum hatası: {str(e)}")
            return False

    def human_like_wait(self, min_sec=2, max_sec=5):
        """İnsan benzeri rastgele bekleme"""
        wait_time = random.uniform(min_sec, max_sec)
        time.sleep(wait_time)

    def login(self):
        """Instagram'a giriş yap"""
        try:
            self.logger.info("Instagram'a giriş yapılıyor...")
            self.driver.get("https://www.instagram.com/accounts/login/")
            self.human_like_wait(3, 7)
            
            # Çerezleri kabul et
            try:
                accept_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'İzin Ver') or contains(text(), 'Allow')]"))
                )
                accept_button.click()
                self.human_like_wait()
            except (NoSuchElementException, TimeoutException):
                pass
            
            # Kullanıcı adı ve şifre girişi
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            
            # İnsan benzeri yazma
            for char in self.credentials['username']:
                username_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
                
            self.human_like_wait(1, 2)
            
            for char in self.credentials['password']:
                password_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
                
            password_field.send_keys(Keys.RETURN)
            self.human_like_wait(5, 8)
            
            # Bildirimleri sonraya bırak
            try:
                not_now_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Şimdi Değil') or contains(text(), 'Not Now')]"))
                )
                not_now_button.click()
                self.human_like_wait()
            except (NoSuchElementException, TimeoutException):
                pass
            
            self.logger.info("Başarıyla giriş yapıldı")
            return True
            
        except Exception as e:
            self.logger.error(f"Giriş hatası: {str(e)}")
            return False

    def watch_video_cycle(self):
        """Geliştirilmiş video izleme döngüsü"""
        try:
            for self.current_watch in range(1, self.watch_count + 1):
                # Rastgele bir video seç
                current_video = random.choice(self.video_urls)
                self.logger.info(f"İzleme #{self.current_watch}/{self.watch_count} başlatılıyor ({current_video})...")
                
                # 1. Videoya git
                self.driver.get(current_video)
                self.human_like_wait(5, 8)
                
                # 2. Video konteynerını bekle
                try:
                    video_container = WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'x1ey2m1c') and contains(@class,'x9f619')]"))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView();", video_container)
                except TimeoutException:
                    self.logger.warning("Video konteynerı bulunamadı, sayfa yenileniyor...")
                    self.driver.refresh()
                    self.human_like_wait()
                    continue
                
                # 3. Video oynatma düğmesini bul ve tıkla
                try:
                    play_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and contains(@class,'x1i10hfl')]"))
                    )
                    play_button.click()
                    self.logger.info("Video başlatıldı")
                except (ElementClickInterceptedException, TimeoutException):
                    # Alternatif tıklama yöntemi
                    try:
                        self.driver.execute_script("document.querySelector('video').play();")
                        self.logger.info("JavaScript ile video başlatıldı")
                    except Exception as e:
                        self.logger.warning(f"Video başlatılamadı: {str(e)}")
                        continue
                
                # 4. Kısa süre izle (3-5 saniye)
                watch_time = random.uniform(3, 5)
                self.logger.info(f"Video {watch_time:.1f} saniye izleniyor...")
                time.sleep(watch_time)
                
                # 5. Video bitiminde rastgele bekleme
                if len(self.video_urls) > 1:
                    # Eğer birden fazla video varsa, bir sonrakine geçmeden önce bekle
                    wait_between_videos = random.uniform(5, 15)
                    self.logger.info(f"Sonraki videoya geçmeden önce {wait_between_videos:.1f} saniye bekleniyor...")
                    time.sleep(wait_between_videos)
                
                # 6. Bazen daha uzun bekleme süreleri ekle
                if self.current_watch % 5 == 0:
                    extended_wait = random.uniform(15, 30)
                    self.logger.info(f"Uzatılmış bekleme süresi: {extended_wait:.1f} saniye...")
                    time.sleep(extended_wait)
                
                self.logger.info(f"İzleme #{self.current_watch} tamamlandı\n")
                
            return True
            
        except Exception as e:
            self.logger.error(f"İzleme döngüsü hatası: {str(e)}")
            return False

    def logout(self):
        """Instagram'dan çıkış yap"""
        try:
            self.logger.info("Çıkış yapılıyor...")
            
            # Profil menüsüne git
            self.driver.get("https://www.instagram.com/accounts/edit/")
            self.human_like_wait(3, 5)
            
            # Çıkış butonunu bul
            menu_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[local-name()='svg' and @aria-label='Ayarlar'] | //*[local-name()='svg' and @aria-label='Settings']"))
            )
            menu_button.click()
            self.human_like_wait()
            
            logout_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Çıkış Yap') or contains(text(), 'Log Out')]"))
            )
            logout_button.click()
            self.human_like_wait(3, 5)
            
            self.logger.info("Başarıyla çıkış yapıldı")
            return True
            
        except Exception as e:
            self.logger.error(f"Çıkış hatası: {str(e)}")
            return False

    def run(self):
        """Botu çalıştır"""
        try:
            if not self.setup_driver():
                raise Exception("Driver başlatılamadı")
                
            if not self.login():
                raise Exception("Giriş başarısız")
                
            start_time = datetime.now()
            self.logger.info(f"Bot başlatıldı - {start_time.strftime('%d/%m/%Y %H:%M:%S')}")
            
            if not self.watch_video_cycle():
                raise Exception("İzleme işlemi başarısız")
                
            end_time = datetime.now()
            duration = end_time - start_time
            self.logger.info(
                f"Bot çalışması tamamlandı - "
                f"Toplam süre: {duration} - "
                f"Başarılı izlemeler: {self.current_watch}/{self.watch_count}"
            )
            
        except Exception as e:
            self.logger.error(f"Çalışma hatası: {str(e)}")
            
        finally:
            if self.driver:
                self.driver.quit()
            self.logger.info("Tarayıcı kapatıldı")

if __name__ == "__main__":
    bot = InstagramVideoWatcherPro()
    bot.run()