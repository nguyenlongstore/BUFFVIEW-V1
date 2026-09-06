import requests
import random
import threading
import time
import os
import sys
import json
import subprocess
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor, as_completed

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

# ========== KIEM TRA SELENIUM ==========
def install_selenium():
    try:
        import selenium
        print(f"{Colors.GREEN}[+] Selenium da duoc cai dat!{Colors.END}")
        return True
    except ImportError:
        print(f"{Colors.YELLOW}[*] Dang cai dat Selenium...{Colors.END}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium", "-q"])
            print(f"{Colors.GREEN}[+] Da cai dat Selenium thanh cong!{Colors.END}")
            return True
        except:
            print(f"{Colors.RED}[!] Khong the cai Selenium. Vui long tu cai: pip install selenium{Colors.END}")
            return False

selenium_installed = install_selenium()

if selenium_installed:
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException, WebDriverException
        USE_SELENIUM = True
        print(f"{Colors.GREEN}[+] Che do Selenium san sang!{Colors.END}")
    except Exception as e:
        USE_SELENIUM = False
        print(f"{Colors.RED}[!] Loi import Selenium: {str(e)[:50]}{Colors.END}")
else:
    USE_SELENIUM = False

# ========== DANH SACH PROXY ==========
PROXY_LIST = []

def fetch_proxies():
    global PROXY_LIST
    try:
        print(f"{Colors.YELLOW}[*] Dang lay proxy...{Colors.END}")
        urls = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all",
            "https://www.proxy-list.download/api/v1/get?type=http"
        ]
        all_proxies = []
        for url in urls:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    proxies = response.text.strip().split('\n')
                    for p in proxies:
                        p = p.strip()
                        if p and ':' in p:
                            if not p.startswith('http'):
                                p = f"http://{p}"
                            all_proxies.append(p)
            except:
                pass
        
        PROXY_LIST = list(set(all_proxies))
        if PROXY_LIST:
            print(f"{Colors.GREEN}[+] Da lay {len(PROXY_LIST)} proxy{Colors.END}")
        else:
            PROXY_LIST = []
            print(f"{Colors.YELLOW}[!] Khong lay duoc proxy, chay khong proxy{Colors.END}")
        return True
    except:
        PROXY_LIST = []
        return True

# ========== CLASS BOT CHINH - SELENIUM REAL ==========
class TikTokViewBot:
    def __init__(self, video_url, view_count):
        self.video_url = video_url
        self.view_count = max(10, min(100000000, view_count))
        self.ua = UserAgent()
        self.success_count = 0
        self.fail_count = 0
        self.running = True
        self.batch_size = 5  # Giam xuong de tranh bi phat hien
        self.proxies = PROXY_LIST.copy()
        self.max_threads = 3  # Giam thread de tranh overload
        self.lock = threading.Lock()
        self.use_selenium = USE_SELENIUM

    def get_video_id(self):
        if "tiktok.com" in self.video_url:
            if "/video/" in self.video_url:
                video_id = self.video_url.split("/video/")[1].split("?")[0].split("/")[0]
                return video_id
            elif "vm.tiktok.com" in self.video_url:
                try:
                    response = requests.head(self.video_url, allow_redirects=True, timeout=5)
                    return response.url.split("/video/")[1].split("?")[0].split("/")[0]
                except:
                    return None
        return None

    def send_view_selenium_real(self, proxy=None):
        """GUI VIEW BANG SELENIUM - TRINH DUYET THAT (KHONG HEADLESS)"""
        driver = None
        try:
            video_id = self.get_video_id()
            if not video_id:
                with self.lock:
                    self.fail_count += 1
                return False

            # Cau hinh Chrome - KHONG HEADLESS (hien thi trinh duyet)
            chrome_options = Options()
            # KHONG dung headless - mo trinh duyet that
            # chrome_options.add_argument("--headless")  # COMMENT LAi
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # User-Agent nguoi that
            chrome_options.add_argument(f"--user-agent={self.ua.random}")
            
            # Proxy neu co
            if proxy:
                chrome_options.add_argument(f'--proxy-server={proxy}')
            
            # Tao driver
            driver = webdriver.Chrome(options=chrome_options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.set_page_load_timeout(30)
            
            # 1. MO TRANG VIDEO
            print(f"{Colors.CYAN}[*] Dang mo trang video...{Colors.END}")
            driver.get(self.video_url)
            time.sleep(random.uniform(3, 5))
            
            # 2. CHO VIDEO LOAD
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "video"))
                )
                print(f"{Colors.GREEN}[+] Video da load{Colors.END}")
            except:
                print(f"{Colors.YELLOW}[!] Video chua load, tiep tuc...{Colors.END}")
            
            # 3. PLAY VIDEO
            try:
                video = driver.find_element(By.TAG_NAME, "video")
                driver.execute_script("arguments[0].play();", video)
                print(f"{Colors.GREEN}[+] Dang phat video{Colors.END}")
            except:
                try:
                    driver.execute_script("document.querySelector('video').play();")
                except:
                    pass
            
            # 4. CUON TRANG NHU NGUOI THAT
            for i in range(random.randint(3, 6)):
                scroll = random.randint(200, 600)
                driver.execute_script(f"window.scrollBy(0, {scroll});")
                time.sleep(random.uniform(1, 2))
            
            # 5. DI CHUYEN CHUOT
            try:
                video = driver.find_element(By.TAG_NAME, "video")
                actions = ActionChains(driver)
                actions.move_to_element(video).perform()
                time.sleep(1)
            except:
                pass
            
            # 6. XEM VIDEO TRONG 30-60 GIAT
            watch_time = random.randint(30, 60)
            print(f"{Colors.YELLOW}[*] Dang xem video trong {watch_time}s...{Colors.END}")
            
            for i in range(watch_time // 5):
                if random.random() > 0.5:
                    driver.execute_script("window.scrollBy(0, 50);")
                else:
                    driver.execute_script("window.scrollBy(0, -30);")
                time.sleep(5)
            
            # 7. LIKE VIDEO
            try:
                like_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@data-e2e='like-icon']"))
                )
                like_btn.click()
                print(f"{Colors.GREEN}[+] Da like video{Colors.END}")
                time.sleep(1)
            except:
                pass
            
            # 8. XEM BINH LUAN
            try:
                comment_btn = driver.find_element(By.XPATH, "//div[@data-e2e='comment-icon']")
                comment_btn.click()
                time.sleep(2)
                driver.execute_script("window.scrollBy(0, 200);")
                time.sleep(1)
            except:
                pass
            
            # 9. CUON LEN DAU
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            # 10. DONG TRINH DUYET
            driver.quit()
            
            with self.lock:
                self.success_count += 1
                print(f"{Colors.GREEN}[+] VIEW THANH CONG! ({self.success_count}/{self.view_count}) - {time.strftime('%H:%M:%S')}{Colors.END}")
            return True

        except Exception as e:
            with self.lock:
                self.fail_count += 1
                print(f"{Colors.RED}[!] Loi Selenium: {str(e)[:50]} ({self.fail_count} fail){Colors.END}")
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            return False

    def send_view_requests(self, proxy=None):
        """FALLBACK: GUI VIEW BANG REQUESTS"""
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
                "Cache-Control": "no-cache",
            }

            session = requests.Session()
            session.trust_env = False
            
            session.cookies.update({
                "tt_webid_v2": str(random.randint(1000000000000000000, 9999999999999999999)),
                "tt_csrf_token": ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32)),
                "s_v_web_id": ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32)),
            })
            
            if proxy:
                session.proxies = {"http": proxy, "https": proxy}
            
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

    def send_view(self, proxy=None):
        """Chon phuong thuc gui view"""
        if self.use_selenium:
            return self.send_view_selenium_real(proxy)
        else:
            return self.send_view_requests(proxy)

    def wait_with_countdown(self, seconds):
        for i in range(seconds, 0, -1):
            sys.stdout.write(f"\r{Colors.CYAN}[*] Dem nguoc: {i}s   {Colors.END}")
            sys.stdout.flush()
            time.sleep(1)
        print(f"\r{Colors.GREEN}[*] Tiep tuc...               {Colors.END}")

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"{Colors.BOLD}{Colors.CYAN}")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║                     [ NGLONG DEV ]                            ║")
        print(f"║         TIKTOK VIEW BOT v6.0 - {'SELENIUM REAL' if self.use_selenium else 'REQUESTS'} MODE     ║")
        print("╠════════════════════════════════════════════════════════════════╣")
        print(f"║  {Colors.WHITE}TOI THIEU: 10 VIEWS{Colors.CYAN}           {Colors.WHITE}TOI DA: 100.000.000 VIEWS{Colors.CYAN}          ║")
        print(f"║  {Colors.WHITE}THREADS: {self.max_threads}{Colors.CYAN}                                         ║")
        print(f"║  {Colors.WHITE}PROXY: {len(self.proxies)}{Colors.CYAN}                                            ║")
        print(f"║  {Colors.WHITE}MODE: {'SELENIUM REAL' if self.use_selenium else 'REQUESTS'}{Colors.CYAN}                                  ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}")

        if self.use_selenium:
            print(f"{Colors.YELLOW}[!] CHE DO SELENIUM REAL - MO TRINH DUYET THAT{Colors.END}")
            print(f"{Colors.YELLOW}[!] MOI VIEW MAT 30-60s DE XEM VIDEO{Colors.END}")
        else:
            print(f"{Colors.YELLOW}[!] CHE DO REQUESTS - NHANH NHUNG VIEW CO THE KHONG TANG{Colors.END}")
        
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
            
            start_time = time.time()
            
            # Chay tung view (khong thread de tranh bi phat hien)
            for i in range(batch_count):
                if not self.running:
                    break
                
                proxy = random.choice(self.proxies) if self.proxies else None
                if proxy:
                    print(f"{Colors.CYAN}[*] Proxy: {proxy}{Colors.END}")
                
                self.send_view(proxy)
                
                # Delay giua cac view (30-60s) de giong nguoi that
                if i < batch_count - 1:
                    delay = random.randint(30, 60)
                    print(f"{Colors.CYAN}[*] Cho {delay}s truoc view tiep...{Colors.END}")
                    self.wait_with_countdown(delay)
            
            elapsed = time.time() - start_time
            
            print(f"{Colors.GREEN}[*] Dot {batch+1}: +{self.success_count - start_idx} view ({elapsed:.1f}s){Colors.END}")
            print(f"{Colors.CYAN}[*] Tong: {self.success_count}/{self.view_count}{Colors.END}")

            if self.success_count < self.view_count and batch < total_batches - 1:
                wait_time = random.randint(60, 120)
                print(f"{Colors.YELLOW}[*] Nghi giua cac dot {wait_time}s...{Colors.END}")
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
    
    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║                     [ NGLONG DEV ]                            ║")
    print("║         TIKTOK VIEW BOT v6.0 - REAL BROWSER                  ║")
    print("╠════════════════════════════════════════════════════════════════╣")
    print(f"║  {Colors.WHITE}1. TANG VIEW (REAL BROWSER){Colors.CYAN}                              ║")
    print(f"║  {Colors.WHITE}2. TANG VIEW (REQUESTS){Colors.CYAN}                                  ║")
    print(f"║  {Colors.WHITE}3. CAP NHAT PROXY{Colors.CYAN}                                          ║")
    print(f"║  {Colors.WHITE}4. THONG TIN VIDEO{Colors.CYAN}                                        ║")
    print(f"║  {Colors.WHITE}5. THOAT{Colors.CYAN}                                                   ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    if USE_SELENIUM:
        print(f"{Colors.GREEN}[*] MODE: SELENIUM REAL (TRINH DUYET THAT){Colors.END}")
    else:
        print(f"{Colors.YELLOW}[*] MODE: REQUESTS (KHONG CO SELENIUM){Colors.END}")

def get_video_info():
    video_url = input(f"{Colors.WHITE}[NGLONG] URL video: {Colors.END}").strip()
    if not video_url:
        print(f"{Colors.RED}[!] URL khong duoc de trong{Colors.END}")
        return
    
    bot = TikTokViewBot(video_url, 10)
    video_id = bot.get_video_id()
    if video_id:
        print(f"{Colors.GREEN}[+] VIDEO ID: {video_id}{Colors.END}")
        print(f"{Colors.GREEN}[+] URL: {video_url}{Colors.END}")
    else:
        print(f"{Colors.RED}[-] URL khong hop le{Colors.END}")
    input(f"{Colors.YELLOW}[*] Enter de tiep tuc...{Colors.END}")

# ========== MAIN ==========
if __name__ == "__main__":
    print(f"{Colors.YELLOW}[*] KHOI DONG TIKTOK VIEW BOT v6.0...{Colors.END}")
    
    if USE_SELENIUM:
        print(f"{Colors.GREEN}[+] CHE DO SELENIUM REAL - MO TRINH DUYET THAT{Colors.END}")
        print(f"{Colors.YELLOW}[!] MOI VIEW MAT 30-60s, TOI THIEU 10 VIEW{Colors.END}")
    else:
        print(f"{Colors.YELLOW}[!] CHE DO REQUESTS - NHANH NHUNG VIEW CO THE KHONG TANG{Colors.END}")
    
    time.sleep(2)
    
    fetch_proxies()
    
    while True:
        show_menu()
        choice = input(f"{Colors.BOLD}{Colors.WHITE}[NGLONG] Nhap (1-5): {Colors.END}").strip()

        if choice == "1":
            if not USE_SELENIUM:
                print(f"{Colors.RED}[!] SELENIUM CHUA DUOC CAI DAT!{Colors.END}")
                print(f"{Colors.YELLOW}[*] Vui long cai: pip install selenium{Colors.END}")
                print(f"{Colors.YELLOW}[*] Va tai Chromedriver: https://chromedriver.chromium.org/{Colors.END}")
                input(f"{Colors.YELLOW}[*] Enter de tiep tuc...{Colors.END}")
                continue
            
            video_input = input(f"{Colors.WHITE}[NGLONG] URL video: {Colors.END}").strip()
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
            bot.use_selenium = True
            bot.run()
            input(f"{Colors.YELLOW}[*] Enter de tro ve...{Colors.END}")

        elif choice == "2":
            video_input = input(f"{Colors.WHITE}[NGLONG] URL video: {Colors.END}").strip()
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
            bot.use_selenium = False
            bot.run()
            input(f"{Colors.YELLOW}[*] Enter de tro ve...{Colors.END}")

        elif choice == "3":
            print(f"{Colors.YELLOW}[*] Dang cap nhat proxy...{Colors.END}")
            fetch_proxies()
            input(f"{Colors.YELLOW}[*] Enter...{Colors.END}")

        elif choice == "4":
            get_video_info()

        elif choice == "5":
            print(f"{Colors.GREEN}[+] Tam biet! NGLONG DEV xin chao{Colors.END}")
            time.sleep(1)
            sys.exit(0)

        else:
            print(f"{Colors.RED}[!] Lua chon sai!{Colors.END}")
            time.sleep(1)
