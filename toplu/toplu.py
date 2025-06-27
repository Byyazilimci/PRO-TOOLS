import os
import subprocess
import time
import sys
from colorama import init, Fore, Style, Back

init(autoreset=True)  # Renkleri otomatik sıfırla

# Düzeltilmiş ve hizalı "PRO TOOLS" banner
def show_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = f"""
{Fore.BLUE}╔══════════════════════════════════════════════════════════════
{Fore.BLUE}║  {Fore.MAGENTA}██████╗ ██████╗  ██████╗      ████████╗ ██████╗  ██████╗ ██╗     {Fore.BLUE}
{Fore.BLUE}║  {Fore.MAGENTA}██╔══██╗██╔══██╗██╔═══██╗     ╚══██╔══╝██╔═══██╗██╔═══██╗██║     {Fore.BLUE}
{Fore.BLUE}║  {Fore.MAGENTA}██████╔╝██████╔╝██║   ██║█████╗  ██║   ██║   ██║██║   ██║██║     {Fore.BLUE}
{Fore.BLUE}║  {Fore.MAGENTA}██╔═══╝ ██╔══██╗██║   ██║╚════╝  ██║   ██║   ██║██║   ██║██║     {Fore.BLUE}
{Fore.BLUE}║  {Fore.MAGENTA}██║     ██║  ██║╚██████╔╝        ██║   ╚██████╔╝╚██████╔╝███████╗{Fore.BLUE}
{Fore.BLUE}║  {Fore.MAGENTA}╚═╝     ╚═╝  ╚═╝ ╚═════╝         ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝{Fore.BLUE}
{Fore.BLUE}║                                                          {Fore.BLUE}
{Fore.BLUE}║  {Fore.CYAN}┌──────────────────────────────────────────────┐        {Fore.BLUE}
{Fore.BLUE}║  {Fore.CYAN}│{Fore.YELLOW}           P R O   T O O L S   v1.0          {Fore.CYAN}      {Fore.BLUE}
{Fore.BLUE}║  {Fore.CYAN}└──────────────────────────────────────────────┘        {Fore.BLUE}
{Fore.BLUE}║  {Fore.WHITE}Developer: {Fore.RED}Gökhan Yakut / @gokhan.yakut.04                       {Fore.BLUE}
{Fore.BLUE}║  {Fore.WHITE}GitHub:    {Fore.GREEN}github.com/byyazilimci            {Fore.BLUE}
{Fore.BLUE}║  {Fore.WHITE}YouTube:   {Fore.RED}youtube.com/@Bygokhanyakut        {Fore.BLUE}
{Fore.BLUE}╚══════════════════════════════════════════════════════════════
{Style.RESET_ALL}
"""
    print(banner)

# Menü gösterimi (orijinal kodla aynı)
def show_menu():
    menu = f"""
{Fore.BLUE}┌─────────────── {Fore.MAGENTA}M A I N   M E N U {Fore.BLUE}
{Fore.BLUE}│                                                          
{Fore.BLUE}│  {Fore.MAGENTA}[{Fore.CYAN}1{Fore.MAGENTA}]{Fore.WHITE} PhishingTools çalıştır                           {Fore.BLUE}
{Fore.BLUE}│  {Fore.MAGENTA}[{Fore.CYAN}2{Fore.MAGENTA}]{Fore.WHITE} PhishDark çalıştır                         {Fore.BLUE}
{Fore.BLUE}│  {Fore.MAGENTA}[{Fore.CYAN}3{Fore.MAGENTA}]{Fore.WHITE} panel çalıştır                          {Fore.BLUE}
{Fore.BLUE}│  {Fore.MAGENTA}[{Fore.CYAN}4{Fore.MAGENTA}]{Fore.WHITE} ins_bot1 çalıştır                          {Fore.BLUE}
{Fore.BLUE}│  {Fore.MAGENTA}[{Fore.CYAN}5{Fore.MAGENTA}]{Fore.WHITE} İGHacker çalıştır                          {Fore.BLUE}
{Fore.BLUE}│  {Fore.MAGENTA}[{Fore.CYAN}6{Fore.MAGENTA}]{Fore.YELLOW} Kurulum ve Kullanım Kılavuzu                  {Fore.BLUE}
{Fore.BLUE}│  {Fore.MAGENTA}[{Fore.RED}0{Fore.MAGENTA}]{Fore.RED} Çıkış                                     {Fore.BLUE}
{Fore.BLUE}│                                                          
{Fore.BLUE}└──────────────────────────────────────────────────────────
{Style.RESET_ALL}
"""
    print(menu)

# Kurulum bilgilerini göster (orijinal kodla aynı)
def show_installation():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n{Fore.YELLOW}⍟ {Fore.CYAN}KURULUM ve KULLANIM KILAVUZU {Fore.YELLOW}⍟{Style.RESET_ALL}\n")
    print(f"{Fore.GREEN}1. Gerekliliklerin Kurulumu:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}pip install colorama requests bs4 selenium{Style.RESET_ALL}\n")
    
    print(f"{Fore.GREEN}2. Kullanım:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}- Menüden istediğiniz aracı seçerek çalıştırabilirsiniz")
    print(f"- Her araç kendi içinde kullanım talimatlarını gösterecektir{Style.RESET_ALL}\n")
    
    print(f"{Fore.GREEN}3. Önemli Notlar:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}- Araçları kullanmadan önce gerekli izinlere sahip olduğunuzdan emin olun")
    print(f"- Sadece etik hackleme ve eğitim amaçlı kullanın{Style.RESET_ALL}\n")
    
    input(f"{Fore.CYAN}Devam etmek için Enter'a basın...{Style.RESET_ALL}")

# Python dosyası çalıştırma fonksiyonu (orijinal kodla aynı)
def run_python_file(file_name):
    try:
        subprocess.run(["python", file_name], check=True)
    except FileNotFoundError:
        print(f"\n{Fore.RED}✘ Hata: {file_name} dosyası bulunamadı!{Style.RESET_ALL}")
    except subprocess.CalledProcessError:
        print(f"\n{Fore.RED}✘ Hata: {file_name} çalıştırılırken bir hata oluştu!{Style.RESET_ALL}")
    input(f"\n{Fore.CYAN}Devam etmek için Enter'a basın...{Style.RESET_ALL}")

# Ana program (orijinal kodla aynı)
def main():
    while True:
        show_banner()
        show_menu()
        
        choice = input(f"{Fore.MAGENTA}┌──({Fore.CYAN}root@pro-tools{Fore.MAGENTA})-[{Fore.YELLOW}~{Fore.MAGENTA}]\n└─{Fore.CYAN}$ {Style.RESET_ALL}")
        
        if choice == "1":
            run_python_file("PhishingTools.py")
        elif choice == "2":
            run_python_file("PhishDark.py")
        elif choice == "3":
            run_python_file("panel.py")
        elif choice == "4":
            run_python_file("ins_bot1.py")
        elif choice == "5":
            run_python_file("İGHacker.py")
        elif choice == "6":
            show_installation()
        elif choice == "0":
            print(f"\n{Fore.BLUE}» {Fore.MAGENTA}Pro Tools kapatılıyor... {Fore.BLUE}«{Style.RESET_ALL}")
            time.sleep(1)
            sys.exit()
        else:
            print(f"\n{Fore.RED}✘ Geçersiz seçim! Lütfen 0-6 arasında bir sayı girin.{Style.RESET_ALL}")
            time.sleep(1)

if __name__ == "__main__":
    main()