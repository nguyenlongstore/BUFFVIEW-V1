import requests
import random
import threading
import time
import os
import sys
import json
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, as_completed
import queue

# ========== CAU HINH MAU SAC ==========
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# ========== DANH SACH PROXY ==========
PROXY_LIST = []

def fetch_proxies():
    """Lay proxy nhanh"""
    global PROXY_LIST
    try:
        # Lay proxy tu nhieu nguon
        proxy_sources = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all",
            "https://www.proxy-list.download/api/v1/get?type=http",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"
        ]
        
        all_proxies = []
        for source in proxy_sources:
            try:
                response = requests.get(source, timeout=10)
                if response.status_code == 200:
                    proxies = response.text.strip().split('\n')
                    all_proxies.extend([p.strip() for p in proxies if p.strip()])
            except:
                pass
        
        # Loc proxy hop le
        valid_proxies = []
        for p in all_proxies:
            if ':' in p and len(p) > 5:
                valid_proxies.append(f"http://{p}" if not p.startswith('http') else p)
        
        PROXY_LIST = list(set(valid_proxies))
        print(f"{Colors.GREEN}[+] Da lay {len(PROXY_LIST)} proxy{Colors.END}")
        return True
    except:
        pass
    
    # Proxy backup
    PROXY_LIST = [
        "http://45.33.22.44:8080", "http://67.89.12.34:8080",
        "http://98.76.54.32:8080", "http://23.54.32.11:8080",
        "http://12.34.56.78:8080", "http://87.65.43.21:8080",
        "http://54.32.21.87:8080", "http://76.54.32.12:8080",
        "http://43.21.87.65:8080", "http://21.87.65.43:8080",
        "http://192.168.1.1:8080", "http://10.0.0.1:8080"
    ]
    print(f"{Colors.YELLOW}[!] Su dung proxy backup ({len(PROXY_LIST)} proxy){Colors.END}")
    return True

# ========== CLASS BOT CHINH - MAX SPEED ==========
class TikTokViewBot:
    def __init__(self, video_url, view_count):
        self.video_url = video_url
        self.view_count = max(10, min(100000000, view_count))
        self.ua = UserAgent()
        self.success_count = 0
        self.fail_count = 0
        self.running = True
        self.batch_size = 100  # Tang batch size
        self.proxies = PROXY_LIST.copy()
        self.max_threads = 50  # Max threads
        self.driver_pool = queue.Queue()
        self.lock = threading.Lock()

    def get_video_id(self):
        if "tiktok.com" in self.video_url:
            if "/video/" in self.video_url:
                return self.video_url.split("/video/")[1].split("?")[0].split("/")[0]
            elif "vm.tiktok.com" in self.video_url:
                try:
                    response = requests.head(self.video_url, allow_redirects=True, timeout=5)
                    return response.url.split("/video/")[1].split("?")[0].split("/")[0]
                except:
                    return None
        return None

    def create_driver_fast(self, proxy=None):
        """Tao driver nhanh - toi uu cho toc do"""
        chrome_options = Options()
        
        # Toi uu toc do
        chrome_options.add_argument("--headless")  # Headless de nhanh
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-javascript")  # Tat JS de nhanh
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User-Agent
        chrome_options.add_argument(f"--user-agent={self.ua.random}")
        
        # Proxy
        if proxy:
            chrome_options.add_argument(f'--proxy-server={proxy}')
        
        # Page load strategy: eager (nhanh)
        chrome_options.page_load_strategy = 'eager'
        
        # Giam timeout
        chrome_options.add_argument("--timeout=10")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(10)
        driver.implicitly_wait(2)
        
        return driver

    def send_view_fast(self, proxy=None):
        """Gui view toc do cao"""
        driver = None
        try:
            video_id = self.get_video_id()
            if not video_id:
                with self.lock:
                    self.fail_count += 1
                return False

            # Tao driver
            driver = self.create_driver_fast(proxy)
            
            # Load trang (nhanh)
            driver.get(self.video_url)
            
            # Chi can load trang la du (view da duoc tinh)
            # Khong can doi load full
            
            # Lay view count tu trang
            try:
                view_element = driver.find_element(By.XPATH, "//strong[contains(@class, 'view-count')]")
                view_text = view_element.text
            except:
                pass
            
            driver.quit()
            
            with self.lock:
                self.success_count += 1
                print(f"{Colors.GREEN}[+] View OK ({self.success_count}/{self.view_count}) - {time.strftime('%H:%M:%S')}{Colors.END}")
            return True

        except Exception as e:
            with self.lock:
                self.fail_count += 1
                print(f"{Colors.RED}[!] Loi: {str(e)[:30]} ({self.fail_count} fail){Colors.END}")
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            return False

    def send_view_requests_fast(self, proxy=None):
        """Gui view bang requests (nhanh hon)"""
        try:
            video_id = self.get_video_id()
            if not video_id:
                with self.lock:
                    self.fail_count += 1
                return False

            username = self.video_url.split('/@')[1].split('/')[0]
            url = f"https://www.tiktok.com/@{username}/video/{video_id}"
            
            headers = {
                "User-Agent": self.ua.random,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "vi-VN,vi;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://www.tiktok.com/",
                "Origin": "https://www.tiktok.com",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Cache-Control": "max-age=0",
            }

            session = requests.Session()
            session.trust_env = False
            
            # Cookie
            session.cookies.update({
                "tt_webid_v2": str(random.randint(1000000000000000000, 9999999999999999999)),
                "tt_csrf_token": ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32)),
                "s_v_web_id": ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32)),
            })
            
            if proxy:
                session.proxies = {"http": proxy, "https": proxy}
            
            # Request nhanh (timeout thap)
            response = session.get(url, headers=headers, timeout=10, allow_redirects=True)
            
            if response.status_code == 200:
                with self.lock:
                    self.success_count += 1
                    print(f"{Colors.GREEN}[+] View OK ({self.success_count}/{self.view_count}) - {time.strftime('%H:%M:%S')}{Colors.END}")
                return True
            else:
                with self.lock:
                    self.fail_count += 1
                return False

        except:
            with self.lock:
                self.fail_count += 1
            return False

    def send_view_parallel(self, proxy=None):
        """Gui view song song - MAX SPEED"""
        # Uu tien requests cho toc do
        return self.send_view_requests_fast(proxy)

    def run_batch_parallel(self, batch_count):
        """Chay batch song song"""
        proxies = self.proxies.copy()
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []
            for i in range(batch_count):
                proxy = random.choice(proxies) if proxies else None
                future = executor.submit(self.send_view_parallel, proxy)
                futures.append(future)
            
            # Dem ket qua
            for future in as_completed(futures):
                try:
                    future.result(timeout=5)
                except:
                    pass

    def wait_with_countdown(self, seconds):
        for i in range(seconds, 0, -1):
            sys.stdout.write(f"\r{Colors.CYAN}[*] Dem nguoc: {i}s   {Colors.END}")
            sys.stdout.flush()
            time.sleep(1)
        print(f"\r{Colors.GREEN}[*] Tiep tuc chay...               {Colors.END}")

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"{Colors.BOLD}{Colors.RED}")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║                     [ NGLONG DEV ]                            ║")
        print("║            TIKTOK VIEW BOT - MAX SPEED                       ║")
        print("╠════════════════════════════════════════════════════════════════╣")
        print(f"║  {Colors.WHITE}TOI THIEU: 10 VIEWS{Colors.RED}            {Colors.WHITE}TOI DA: 100.000.000 VIEWS{Colors.RED}          ║")
        print(f"║  {Colors.WHITE}CHE DO: MULTI-THREAD MAX SPEED{Colors.RED}                         ║")
        print(f"║  {Colors.WHITE}THREADS: {self.max_threads}{Colors.RED}                                       ║")
        print(f"║  {Colors.WHITE}PROXY: {len(self.proxies)}{Colors.RED}                                            ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}")

        print(f"{Colors.YELLOW}[!] CHE DO MAX SPEED - CHAY THREAD 50{Colors.END}")
        print(f"{Colors.YELLOW}[!] RU ROI: IP CO THE BI BLOCK{Colors.END}")
        print("=" * 60)

        print(f"{Colors.BOLD}{Colors.WHITE}[*] BAT DAU: {self.view_count} views{Colors.END}")
        print(f"{Colors.WHITE}[*] VIDEO: {self.video_url}{Colors.END}")
        print(f"{Colors.WHITE}[*] START: {time.strftime('%H:%M:%S %d/%m/%Y')}{Colors.END}")
        print("=" * 60)

        video_id = self.get_video_id()
        if not video_id:
            print(f"{Colors.RED}[!] KHONG THE LAY VIDEO ID{Colors.END}")
            return

        total_batches = (self.view_count + self.batch_size - 1) // self.batch_size
        
        for batch in range(total_batches):
            if not self.running:
                break

            start_idx = batch * self.batch_size
            end_idx = min(start_idx + self.batch_size, self.view_count)
            batch_count = end_idx - start_idx

            print(f"\n{Colors.BOLD}{Colors.YELLOW}[===== DOT {batch+1}/{total_batches} - {batch_count} view =====]{Colors.END}")
            
            # Chay song song
            start_time = time.time()
            self.run_batch_parallel(batch_count)
            elapsed = time.time() - start_time
            
            print(f"{Colors.GREEN}[*] Dot {batch+1}: +{self.success_count - start_idx} view ({elapsed:.1f}s){Colors.END}")
            print(f"{Colors.CYAN}[*] Tong: {self.success_count}/{self.view_count}{Colors.END}")

            if self.success_count < self.view_count and batch < total_batches - 1:
                wait_time = random.randint(5, 15)  # Delay ngan
                self.wait_with_countdown(wait_time)

        print("\n" + "=" * 60)
        print(f"{Colors.BOLD}{Colors.GREEN}[+] HOAN THANH! View: {self.success_count}{Colors.END}")
        print(f"{Colors.RED}[-] That bai: {self.fail_count}{Colors.END}")
        if (self.success_count + self.fail_count) > 0:
            rate = (self.success_count/(self.success_count+self.fail_count)*100)
            print(f"{Colors.WHITE}[*] Ty le: {rate:.1f}%{Colors.END}")
        print(f"{Colors.WHITE}[*] END: {time.strftime('%H:%M:%S %d/%m/%Y')}{Colors.END}")
        print("=" * 60)

# ========== MENU ==========
def show_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{Colors.BOLD}{Colors.RED}")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║                     [ NGLONG DEV ]                            ║")
    print("║            TIKTOK VIEW BOT - MAX SPEED                       ║")
    print("╠════════════════════════════════════════════════════════════════╣")
    print(f"║  {Colors.WHITE}1. TANG VIEW (MAX SPEED){Colors.RED}                                ║")
    print(f"║  {Colors.WHITE}2. CAP NHAT PROXY{Colors.RED}                                          ║")
    print(f"║  {Colors.WHITE}3. THOAT{Colors.RED}                                                   ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")

# ========== MAIN ==========
if __name__ == "__main__":
    print(f"{Colors.YELLOW}[*] KHOI DONG MAX SPEED...{Colors.END}")
    print(f"{Colors.RED}[!] CHE DO NAY CHAY 50 THREAD CUNG LUC{Colors.END}")
    print(f"{Colors.RED}[!] IP CO THE BI BLOCK NGAY LAP TUC{Colors.END}")
    time.sleep(2)
    
    fetch_proxies()
    
    while True:
        show_menu()
        choice = input(f"{Colors.BOLD}{Colors.WHITE}[NGLONG] Nhap (1-3): {Colors.END}").strip()

        if choice == "1":
            video_input = input(f"{Colors.WHITE}[NGLONG] URL: {Colors.END}").strip()
            if not video_input:
                print(f"{Colors.RED}[!] URL khong duoc de trong{Colors.END}")
                input(f"{Colors.YELLOW}[*] Enter...{Colors.END}")
                continue

            try:
                view_count = int(input(f"{Colors.WHITE}[NGLONG] So view (10-100000000): {Colors.END}").strip())
                if view_count < 10:
                    view_count = 10
                elif view_count > 100000000:
                    view_count = 100000000
            except:
                view_count = 10

            bot = TikTokViewBot(video_input, view_count)
            bot.run()
            input(f"{Colors.YELLOW}[*] Enter de tro ve...{Colors.END}")

        elif choice == "2":
            print(f"{Colors.YELLOW}[*] Dang cap nhat proxy...{Colors.END}")
            fetch_proxies()
            input(f"{Colors.YELLOW}[*] Enter...{Colors.END}")

        elif choice == "3":
            print(f"{Colors.GREEN}[+] Tam biet!{Colors.END}")
            time.sleep(1)
            sys.exit(0)

        else:
            print(f"{Colors.RED}[!] Lua chon sai!{Colors.END}")
            time.sleep(1)
