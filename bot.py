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

# ========== TAT SELENIUM - CHUYEN SANG REQUESTS ==========
USE_SELENIUM = False  # Tat Selenium vi bi loi
print(f"{Colors.YELLOW}[!] TAT SELENIUM - CHUYEN SANG CHE DO REQUESTS{Colors.END}")
print(f"{Colors.YELLOW}[!] CHE DO NAY NHANH HON NHUNG VIEW CO THE KHONG TANG{Colors.END}")

# ========== DANH SACH PROXY ==========
PROXY_LIST = []

def fetch_proxies():
    global PROXY_LIST
    try:
        print(f"{Colors.YELLOW}[*] Dang lay proxy...{Colors.END}")
        # Proxy tu web
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
            PROXY_LIST = [
                "http://45.33.22.44:8080", "http://67.89.12.34:8080",
                "http://98.76.54.32:8080", "http://23.54.32.11:8080",
                "http://12.34.56.78:8080", "http://87.65.43.21:8080"
            ]
            print(f"{Colors.YELLOW}[!] Su dung {len(PROXY_LIST)} proxy backup{Colors.END}")
        return True
    except:
        PROXY_LIST = ["http://45.33.22.44:8080", "http://67.89.12.34:8080"]
        return True

# ========== CLASS BOT CHINH ==========
class TikTokViewBot:
    def __init__(self, video_url, view_count):
        self.video_url = video_url
        self.view_count = max(10, min(100000000, view_count))
        self.ua = UserAgent()
        self.success_count = 0
        self.fail_count = 0
        self.running = True
        self.batch_size = 10
        self.proxies = PROXY_LIST.copy()
        self.max_threads = 10
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

    def send_view_requests(self, proxy=None):
        """Gui view bang Requests - PHUONG PHAP CHINH"""
        try:
            video_id = self.get_video_id()
            if not video_id:
                with self.lock:
                    self.fail_count += 1
                return False

            # Lay username
            try:
                username = self.video_url.split('/@')[1].split('/')[0]
            except:
                username = "tiktok"
            
            # Cac URL can request
            urls = [
                f"https://www.tiktok.com/@{username}/video/{video_id}",
                f"https://www.tiktok.com/api/v1/video/views/?video_id={video_id}",
                f"https://www.tiktok.com/api/v2/video/views/?video_id={video_id}"
            ]
            
            headers = {
                "User-Agent": self.ua.random,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://www.tiktok.com/",
                "Origin": "https://www.tiktok.com",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
                "DNT": "1"
            }

            session = requests.Session()
            session.trust_env = False
            
            # Cookie day du
            session.cookies.update({
                "tt_webid_v2": str(random.randint(1000000000000000000, 9999999999999999999)),
                "tt_csrf_token": ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32)),
                "s_v_web_id": ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32)),
                "sessionid": ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32)),
                "sessionid_ss": ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32)),
                "uid": f"0{random.randint(10000000, 99999999)}",
                "uuid": str(random.randint(1000000000000, 9999999999999)),
                "passport_csrf_token": ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32)),
                "passport_csrf_token_default": ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32))
            })
            
            if proxy:
                session.proxies = {"http": proxy, "https": proxy}
            
            # Gui request den nhieu URL
            success = False
            for url in urls:
                try:
                    response = session.get(url, headers=headers, timeout=15, allow_redirects=True)
                    if response.status_code in [200, 201, 202, 204]:
                        success = True
                        break
                except:
                    continue
            
            if success:
                with self.lock:
                    self.success_count += 1
                    print(f"{Colors.GREEN}[+] View OK ({self.success_count}/{self.view_count}) - {time.strftime('%H:%M:%S')}{Colors.END}")
                return True
            else:
                with self.lock:
                    self.fail_count += 1
                    print(f"{Colors.RED}[-] Fail ({self.fail_count} fail){Colors.END}")
                return False

        except Exception as e:
            with self.lock:
                self.fail_count += 1
                print(f"{Colors.RED}[!] Loi: {str(e)[:30]} ({self.fail_count} fail){Colors.END}")
            return False

    def send_view(self, proxy=None):
        """Gui view"""
        return self.send_view_requests(proxy)

    def run_batch(self, batch_count):
        """Chay batch song song"""
        proxies = self.proxies.copy() if self.proxies else [None]
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []
            for i in range(batch_count):
                proxy = random.choice(proxies) if proxies else None
                future = executor.submit(self.send_view, proxy)
                futures.append(future)
            
            for future in as_completed(futures):
                try:
                    future.result(timeout=15)
                except:
                    pass

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
        print("║         TIKTOK VIEW BOT v5.1 - REQUESTS MODE                 ║")
        print("╠════════════════════════════════════════════════════════════════╣")
        print(f"║  {Colors.WHITE}TOI THIEU: 10 VIEWS{Colors.CYAN}           {Colors.WHITE}TOI DA: 100.000.000 VIEWS{Colors.CYAN}          ║")
        print(f"║  {Colors.WHITE}THREADS: {self.max_threads}{Colors.CYAN}                                         ║")
        print(f"║  {Colors.WHITE}PROXY: {len(self.proxies)}{Colors.CYAN}                                            ║")
        print(f"║  {Colors.WHITE}MODE: REQUESTS (MAX SPEED){Colors.CYAN}                                ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}")

        print(f"{Colors.BOLD}{Colors.WHITE}[*] BAT DAU: {self.view_count} views{Colors.END}")
        print(f"{Colors.WHITE}[*] VIDEO: {self.video_url}{Colors.END}")
        print(f"{Colors.WHITE}[*] START: {time.strftime('%H:%M:%S %d/%m/%Y')}{Colors.END}")
        print("=" * 60)

        video_id = self.get_video_id()
        if not video_id:
            print(f"{Colors.RED}[!] KHONG THE LAY VIDEO ID{Colors.END}")
            print(f"{Colors.YELLOW}[!] Kiem tra URL: https://www.tiktok.com/@username/video/123456789{Colors.END}")
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
            self.run_batch(batch_count)
            elapsed = time.time() - start_time
            
            print(f"{Colors.GREEN}[*] Dot {batch+1}: +{self.success_count - start_idx} view ({elapsed:.1f}s){Colors.END}")
            print(f"{Colors.CYAN}[*] Tong: {self.success_count}/{self.view_count}{Colors.END}")

            if self.success_count < self.view_count and batch < total_batches - 1:
                wait_time = random.randint(3, 8)
                self.wait_with_countdown(wait_time)

        print("\n" + "=" * 60)
        print(f"{Colors.BOLD}{Colors.GREEN}[+] HOAN THANH! View: {self.success_count}{Colors.END}")
        print(f"{Colors.RED}[-] That bai: {self.fail_count}{Colors.END}")
        if (self.success_count + self.fail_count) > 0:
            rate = (self.success_count/(self.success_count+self.fail_count)*100)
            print(f"{Colors.WHITE}[*] Ty le: {rate:.1f}%{Colors.END}")
        print(f"{Colors.WHITE}[*] END: {time.strftime('%H:%M:%S %d/%m/%Y')}{Colors.END}")
        
        # Thong bao them
        print(f"{Colors.YELLOW}[!] LUU Y QUAN TRONG:{Colors.END}")
        print(f"{Colors.YELLOW}[!] - View co the khong tang ngay lap tuc{Colors.END}")
        print(f"{Colors.YELLOW}[!] - TikTok co che loc view bat thuong{Colors.END}")
        print(f"{Colors.YELLOW}[!] - View ao chi co tac dung 24-48h{Colors.END}")
        print("=" * 60)

# ========== MENU ==========
def show_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║                     [ NGLONG DEV ]                            ║")
    print("║         TIKTOK VIEW BOT v5.1 - REQUESTS MODE                 ║")
    print("╠════════════════════════════════════════════════════════════════╣")
    print(f"║  {Colors.WHITE}1. TANG VIEW TIKTOK{Colors.CYAN}                                        ║")
    print(f"║  {Colors.WHITE}2. CAP NHAT PROXY{Colors.CYAN}                                          ║")
    print(f"║  {Colors.WHITE}3. THONG TIN VIDEO{Colors.CYAN}                                        ║")
    print(f"║  {Colors.WHITE}4. THOAT{Colors.CYAN}                                                   ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    print(f"{Colors.YELLOW}[!] MODE: REQUESTS (KHONG CAN SELENIUM){Colors.END}")
    print(f"{Colors.YELLOW}[!] TOC DO: MAX SPEED{Colors.END}")

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
    print(f"{Colors.YELLOW}[*] KHOI DONG TIKTOK VIEW BOT v5.1...{Colors.END}")
    print(f"{Colors.YELLOW}[!] CHE DO REQUESTS - MAX SPEED{Colors.END}")
    print(f"{Colors.YELLOW}[!] View co the khong tang ngay lap tuc{Colors.END}")
    
    time.sleep(2)
    
    fetch_proxies()
    
    while True:
        show_menu()
        choice = input(f"{Colors.BOLD}{Colors.WHITE}[NGLONG] Nhap (1-4): {Colors.END}").strip()

        if choice == "1":
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
            bot.run()
            input(f"{Colors.YELLOW}[*] Enter de tro ve...{Colors.END}")

        elif choice == "2":
            print(f"{Colors.YELLOW}[*] Dang cap nhat proxy...{Colors.END}")
            fetch_proxies()
            input(f"{Colors.YELLOW}[*] Enter...{Colors.END}")

        elif choice == "3":
            get_video_info()

        elif choice == "4":
            print(f"{Colors.GREEN}[+] Tam biet! NGLONG DEV xin chao{Colors.END}")
            time.sleep(1)
            sys.exit(0)

        else:
            print(f"{Colors.RED}[!] Lua chon sai!{Colors.END}")
            time.sleep(1)
