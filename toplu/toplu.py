import os
import subprocess
import time
import sys
from colorama import init, Fore, Style, Back

init(autoreset=True)

# Profesyonel Banner Tasarımı
def show_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = f"""
{Fore.BLUE}╔═══════════════════════════════════════════════════════════════════════════╗
{Fore.BLUE}║  {Fore.MAGENTA}██████╗ ██████╗  ██████╗      ████████╗ ██████╗  ██████╗ ██╗     {Fore.BLUE}
{Fore.BLUE}║  {Fore.MAGENTA}██╔══██╗██╔══██╗██╔═══██╗     ╚══██╔══╝██╔═══██╗██╔═══██╗██║     {Fore.BLUE}
{Fore.BLUE}║  {Fore.MAGENTA}██████╔╝██████╔╝██║   ██║█████╗  ██║   ██║   ██║██║   ██║██║     {Fore.BLUE}
{Fore.BLUE}║  {Fore.MAGENTA}██╔═══╝ ██╔══██╗██║   ██║╚════╝  ██║   ██║   ██║██║   ██║██║     {Fore.BLUE}
{Fore.BLUE}║  {Fore.MAGENTA}██║     ██║  ██║╚██████╔╝        ██║   ╚██████╔╝╚██████╔╝███████╗{Fore.BLUE}
{Fore.BLUE}║  {Fore.MAGENTA}╚═╝     ╚═╝  ╚═╝ ╚═════╝         ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝{Fore.BLUE}
{Fore.BLUE}║                                                                           
{Fore.BLUE}║  {Fore.CYAN}┌───────────────────────────────────────────────────────────┐       {Fore.BLUE}
{Fore.BLUE}║  {Fore.CYAN}│  {Fore.YELLOW}🔥  P R O   T O O L S   v2.3  {Fore.RED}(Premium Edition)  {Fore.CYAN}     {Fore.BLUE}
{Fore.BLUE}║  {Fore.CYAN}└───────────────────────────────────────────────────────────┘       {Fore.BLUE}
{Fore.BLUE}║  {Fore.WHITE}👨‍💻 Developer: {Fore.RED}Gökhan Yakut {Fore.YELLOW}/ {Fore.CYAN}@gokhan.yakut.04                     {Fore.BLUE}
{Fore.BLUE}║  {Fore.WHITE}💻 GitHub:    {Fore.GREEN}github.com/byyazilimci{Fore.YELLOW}                {Fore.BLUE}
{Fore.BLUE}║  {Fore.WHITE}📺 YouTube:   {Fore.RED}youtube.com/@Bygokhanyakut{Fore.YELLOW}              {Fore.BLUE}
{Fore.BLUE}╚═══════════════════════════════════════════════════════════════════════════
{Style.RESET_ALL}
"""
    print(banner)

# Profesyonel Menü Tasarımı
def show_menu():
    menu = f"""
{Fore.BLUE}┌─────────────── {Fore.MAGENTA}✨ M A I N   M E N U ✨ {Fore.BLUE}
{Fore.BLUE}│                                                              
{Fore.BLUE}│  {Fore.MAGENTA}[{Fore.CYAN}1{Fore.MAGENTA}] {Fore.WHITE}🚀 PhishingTools çalıştır                        {Fore.BLUE}
{Fore.BLUE}│  {Fore.MAGENTA}[{Fore.CYAN}2{Fore.MAGENTA}] {Fore.WHITE}🌑 PhishDark çalıştır                          {Fore.BLUE}
{Fore.BLUE}│  {Fore.MAGENTA}[{Fore.CYAN}3{Fore.MAGENTA}] {Fore.WHITE}🛡️  panel çalıştır                           {Fore.BLUE}
{Fore.BLUE}│  {Fore.MAGENTA}[{Fore.CYAN}4{Fore.MAGENTA}] {Fore.WHITE}🤖 ins_bot1 çalıştır                          {Fore.BLUE}
{Fore.BLUE}│  {Fore.MAGENTA}[{Fore.CYAN}5{Fore.MAGENTA}] {Fore.WHITE}👁️ İGHacker çalıştır                         {Fore.BLUE}
{Fore.BLUE}│  {Fore.MAGENTA}[{Fore.CYAN}6{Fore.MAGENTA}] {Fore.YELLOW}📚 Kurulum ve Kullanım Kılavuzu               {Fore.BLUE}
{Fore.BLUE}│  {Fore.MAGENTA}[{Fore.CYAN}7{Fore.MAGENTA}] {Fore.GREEN}✨ Etik Hacking Araç                                {Fore.BLUE}
{Fore.BLUE}│  {Fore.MAGENTA}[{Fore.CYAN}8{Fore.MAGENTA}] {Fore.GREEN}✨ Google dork                               {Fore.BLUE}
{Fore.BLUE}│  {Fore.MAGENTA}[{Fore.CYAN}9{Fore.MAGENTA}] {Fore.GREEN}✨ Yeni Araç 3                                {Fore.BLUE}
{Fore.BLUE}│  {Fore.MAGENTA}[{Fore.RED}0{Fore.MAGENTA}] {Fore.RED}🚪 Çıkış                                    {Fore.BLUE}
{Fore.BLUE}│                                                              
{Fore.BLUE}└──────────────────────────────────────────────────────────────
{Style.RESET_ALL}
"""
    print(menu)

# Her seçenek için özel arayüz renkleri
def get_theme(choice):
    themes = {
        "1": {"primary": Fore.CYAN, "secondary": Fore.BLUE, "highlight": Fore.YELLOW},
        "2": {"primary": Fore.MAGENTA, "secondary": Fore.BLUE, "highlight": Fore.WHITE},
        "3": {"primary": Fore.GREEN, "secondary": Fore.YELLOW, "highlight": Fore.RED},
        "4": {"primary": Fore.YELLOW, "secondary": Fore.RED, "highlight": Fore.WHITE},
        "5": {"primary": Fore.RED, "secondary": Fore.WHITE, "highlight": Fore.YELLOW},
        "6": {"primary": Fore.WHITE, "secondary": Fore.CYAN, "highlight": Fore.MAGENTA},
        "7": {"primary": Fore.CYAN, "secondary": Fore.GREEN, "highlight": Fore.YELLOW},
        "8": {"primary": Fore.MAGENTA, "secondary": Fore.YELLOW, "highlight": Fore.CYAN},
        "9": {"primary": Fore.YELLOW, "secondary": Fore.MAGENTA, "highlight": Fore.GREEN}
    }
    return themes.get(choice, {"primary": Fore.WHITE, "secondary": Fore.BLUE, "highlight": Fore.YELLOW})

# Seçeneklere özel başlık gösterimi
def show_option_header(choice, title):
    theme = get_theme(choice)
    header = f"""
{theme['secondary']}╔═══════════════════════════════════════════════════════════════════════════╗
{theme['secondary']}║  {theme['highlight']}{title.upper()}{' '*(70-len(title))}{theme['secondary']}
{theme['secondary']}╚═══════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(header)

# Gelişmiş Kurulum Kılavuzu
def show_installation():
    theme = get_theme("6")
    os.system('cls' if os.name == 'nt' else 'clear')
    show_option_header("6", "📦 Kurulum ve Kullanım Kılavuzu")
    
    print(f"{theme['primary']}1. {theme['highlight']}🌈 Gerekliliklerin Kurulumu:{Style.RESET_ALL}")
    print(f"{theme['secondary']}   ├── {theme['primary']}pip install colorama {theme['secondary']}(Renkli çıktılar için)")
    print(f"{theme['secondary']}   ├── {theme['primary']}pip install requests {theme['secondary']}(HTTP istekleri için)")
    print(f"{theme['secondary']}   ├── {theme['primary']}pip install bs4 {theme['secondary']}(Web scraping için)")
    print(f"{theme['secondary']}   ├── {theme['primary']}pip install selenium {theme['secondary']}(Web otomasyonu için)")
    print(f"{theme['secondary']}   └── {theme['primary']}pip install pyfiglet {theme['secondary']}(Bannerlar için)\n")
    
    print(f"{theme['primary']}2. {theme['highlight']}🚀 Ekstra Kurulumlar:{Style.RESET_ALL}")
    print(f"{theme['secondary']}   ├── {theme['primary']}Selenium için ChromeDriver")
    print(f"{theme['secondary']}   ├── {theme['primary']}Windows: {theme['highlight']}https://sites.google.com/chromium.org/driver/")
    print(f"{theme['secondary']}   └── {theme['primary']}Linux/Mac: {theme['highlight']}brew install chromedriver\n")
    
    print(f"{theme['primary']}3. {theme['highlight']}🔧 Kullanım:{Style.RESET_ALL}")
    print(f"{theme['secondary']}   ├── {theme['primary']}Menüden araç seçimi yapın")
    print(f"{theme['secondary']}   └── {theme['primary']}Her aracın kendi talimatlarını izleyin\n")
    
    print(f"{theme['primary']}4. {theme['highlight']}⚠️ Önemli Notlar:{Style.RESET_ALL}")
    print(f"{theme['secondary']}   ├── {theme['primary']}{Back.RED}YALNIZCA YASAL TESTLER İÇİN KULLANIN{Style.RESET_ALL}")
    print(f"{theme['secondary']}   └── {theme['primary']}GitHub: {theme['highlight']}github.com/byyazilimci\n")
    
    input(f"{theme['primary']}⏎ Devam etmek için Enter'a basın...{Style.RESET_ALL}")

# Gelişmiş Dosya Çalıştırma Sistemi
def run_python_file(choice, file_name):
    theme = get_theme(choice)
    try:
        show_option_header(choice, f"🚀 {file_name} Başlatılıyor...")
        print(f"{theme['primary']}⏳ Sistem hazırlığı yapılıyor...{Style.RESET_ALL}")
        time.sleep(1)
        
        # Çalıştırma öncesi animasyon
        for i in range(3):
            print(f"{theme['highlight']}{'▶'*(i+1)} {theme['secondary']}Başlatılıyor...{Style.RESET_ALL}", end='\r')
            time.sleep(0.3)
        
        subprocess.run(["python", file_name], check=True)
        
    except FileNotFoundError:
        print(f"\n{theme['secondary']}❌ {theme['primary']}Kritik Hata: {file_name} bulunamadı!")
        print(f"{theme['highlight']}   ▸ Çözüm: Dosyayı kontrol edin veya GitHub'dan indirin")
    except subprocess.CalledProcessError as e:
        print(f"\n{theme['secondary']}⚠️ {theme['primary']}Çalıştırma Hatası (Kod: {e.returncode})")
        print(f"{theme['highlight']}   ▸ Kütüphaneleri kontrol edin: {theme['primary']}pip install -r requirements.txt")
    except Exception as e:
        print(f"\n{theme['secondary']}💢 {theme['primary']}Beklenmeyen Hata: {str(e)}")
    
    input(f"\n{theme['primary']}⏎ Menüye dönmek için Enter'a basın...{Style.RESET_ALL}")

# Profesyonel Ana Yönetim Sistemi
def main():
    try:
        while True:
            show_banner()
            show_menu()
            
            # Profesyonel giriş istemi
            choice = input(f"{Fore.MAGENTA}┌──({Fore.CYAN}root@pro-tools{Fore.MAGENTA})-[{Fore.YELLOW}~/menu{Fore.MAGENTA}]\n└─{Fore.CYAN}# {Style.RESET_ALL}")
            
            if choice == "1":
                run_python_file(choice, "PhishingTools.py")
            elif choice == "2":
                run_python_file(choice, "PhishDark.py")
            elif choice == "3":
                run_python_file(choice, "panel.py")
            elif choice == "4":
                run_python_file(choice, "ins_bot1.py")
            elif choice == "5":
                run_python_file(choice, "İGHacker.py")
            elif choice == "6":
                show_installation()
            elif choice == "7":
                run_python_file(choice, "Etik Hacking Araç.py")  # Buraya yeni aracınızın dosya adını yazın
            elif choice == "8":
                run_python_file(choice, "Google dork.py")  # Buraya yeni aracınızın dosya adını yazın
            elif choice == "9":
                run_python_file(choice, "yeni_arac_3.py")  # Buraya yeni aracınızın dosya adını yazın
            elif choice == "0":
                # Profesyonel çıkış ekranı
                print(f"\n{Fore.BLUE}» {Fore.MAGENTA}Pro Tools kapatılıyor...")
                print(f"{Fore.YELLOW}┌──────────────────────────────────────┐")
                print(f"{Fore.YELLOW}│  {Fore.CYAN}Teşekkürler! {Fore.WHITE}Güvenli çıkış yapıldı  {Fore.YELLOW}")
                print(f"{Fore.YELLOW}└──────────────────────────────────────┘{Style.RESET_ALL}")
                time.sleep(1)
                sys.exit()
            else:
                print(f"\n{Fore.RED}✘ Geçersiz seçim! Lütfen 0-9 arasında bir sayı girin.{Style.RESET_ALL}")
                time.sleep(1)
                
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}✘ Kullanıcı tarafından durduruldu!{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()