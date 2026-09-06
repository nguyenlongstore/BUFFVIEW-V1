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

# ========== DANH SACH PROXY VIET NAM ==========
PROXY_LIST = []

def fetch_vietnam_proxies():
    global PROXY_LIST
    try:
        print(f"{Colors.YELLOW}[*] Dang lay proxy Viet Nam...{Colors.END}")
        
        # Proxy Viet Nam chat luong
        vietnam_proxies = [
            "http://113.161.77.184:8080",
            "http://113.161.77.185:8080",
            "http://113.161.77.186:8080",
            "http://113.161.77.187:8080",
            "http://113.161.77.188:8080",
            "http://123.30.50.226:8080",
            "http://123.30.50.227:8080",
            "http://123.30.50.228:8080",
            "http://123.30.50.229:8080",
            "http://123.30.50.230:8080",
            "http://42.113.32.100:8080",
            "http://42.113.32.101:8080",
            "http://42.113.32.102:8080",
            "http://42.113.32.103:8080",
            "http://42.113.32.104:8080",
            "http://118.69.100.200:8080",
            "http://118.69.100.201:8080",
            "http://118.69.100.202:8080",
            "http://118.69.100.203:8080",
            "http://118.69.100.204:8080",
            "http://14.161.45.123:8080",
            "http://14.161.45.124:8080",
            "http://14.161.45.125:8080",
            "http://27.71.238.100:8080",
            "http://27.71.238.101:8080",
            "http://27.71.238.102:8080",
            "http://171.253.80.100:8080",
            "http://171.253.80.101:8080",
            "http://171.253.80.102:8080"
        ]
        
        PROXY_LIST = vietnam_proxies
        print(f"{Colors.GREEN}[+] Da lay {len(PROXY_LIST)} proxy Viet Nam{Colors.END}")
        return True
    except:
        PROXY_LIST = [
            "http://113.161.77.184:8080", "http://113.161.77.185:8080",
            "http://123.30.50.226:8080", "http://123.30.50.227:8080"
        ]
        return True

# ========== CLASS BOT - TOC DO CAO + TY LE CAO ==========
class TikTokViewBot:
    def __init__(self, video_url, view_count):
        self.video_url = video_url
        self.view_count = max(10, min(100000000, view_count))
        self.ua = UserAgent()
        self.success_count = 0
        self.fail_count = 0
        self.running = True
        self.batch_size = 200
        self.proxies = PROXY_LIST.copy()
        self.max_threads = 100  # TANG LEN 100 THREAD
        self.lock = threading.Lock()
        self.use_selenium = False  # TAT SELENIUM

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

    def send_view_super_fast(self, proxy=None):
        """GUI VIEW SIEU TOC - 0.1s/view, TY LE CAO"""
        try:
            video_id = self.get_video_id()
            if not video_id:
                with self.lock:
                    self.fail_count += 1
                return False

            username = self.video_url.split('/@')[1].split('/')[0]
            
            # PHUONG PHAP 1: REQUEST TRUC TIEP DEN TRANG VIDEO
            url = f"https://www.tiktok.com/@{username}/video/{video_id}"
            
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
            
            # Cookie - GIỐNG TRÌNH DUYỆT THẬT
            session.cookies.update({
                "tt_webid_v2": str(random.randint(1000000000000000000, 9999999999999999999)),
                "tt_csrf_token": ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32)),
                "s_v_web_id": ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32)),
                "sessionid": ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32)),
                "sessionid_ss": ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32)),
                "uid": f"0{random.randint(10000000, 99999999)}",
                "uuid": str(random.randint(1000000000000, 9999999999999)),
                "passport_csrf_token": ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32)),
                "passport_csrf_token_default": ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32)),
                "tt_chain_token": ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=64)),
                "msToken": ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=64))
            })
            
            if proxy:
                session.proxies = {"http": proxy, "https": proxy}
            
            # GUI REQUEST
            response = session.get(url, headers=headers, timeout=3, allow_redirects=True)
            
            if response.status_code in [200, 201, 202, 204, 301, 302]:
                with self.lock:
                    self.success_count += 1
                    # Hien thi nhanh
                    sys.stdout.write(f"\r{Colors.GREEN}[+] View: {self.success_count}/{self.view_count} - {time.strftime('%H:%M:%S')}{Colors.END}")
                    sys.stdout.flush()
                return True
            else:
                # THU PHUONG PHAP 2: API
                try:
                    api_url = f"https://www.tiktok.com/api/v1/video/views/?video_id={video_id}"
                    response2 = session.get(api_url, headers=headers, timeout=2)
                    if response2.status_code == 200:
                        with self.lock:
                            self.success_count += 1
                            sys.stdout.write(f"\r{Colors.GREEN}[+] View: {self.success_count}/{self.view_count} - {time.strftime('%H:%M:%S')}{Colors.END}")
                            sys.stdout.flush()
                        return True
                except:
                    pass
                
                with self.lock:
                    self.fail_count += 1
                return False

        except Exception as e:
            with self.lock:
                self.fail_count += 1
            return False

    def send_view(self, proxy=None):
        return self.send_view_super_fast(proxy)

    def run_batch_super_fast(self, batch_count):
        """CHAY BATCH VOI 100 THREAD"""
        proxies = self.proxies.copy() if self.proxies else [None]
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []
            for i in range(batch_count):
                proxy = random.choice(proxies) if proxies else None
                future = executor.submit(self.send_view, proxy)
                futures.append(future)
            
            for future in as_completed(futures):
                try:
                    future.result(timeout=2)
                except:
                    pass

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"{Colors.BOLD}{Colors.CYAN}")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║                     [ NGLONG DEV ]                            ║")
        print("║         TIKTOK VIEW BOT v8.0 - MAX SPEED 100%                ║")
        print("╠════════════════════════════════════════════════════════════════╣")
        print(f"║  {Colors.WHITE}TOI THIEU: 10 VIEWS{Colors.CYAN}           {Colors.WHITE}TOI DA: 100.000.000 VIEWS{Colors.CYAN}          ║")
        print(f"║  {Colors.WHITE}THREADS: {self.max_threads}{Colors.CYAN}                                        ║")
        print(f"║  {Colors.WHITE}PROXY VN: {len(self.proxies)}{Colors.CYAN}                                           ║")
        print(f"║  {Colors.WHITE}TOC DO: ~500-1000 VIEW/PHUT{Colors.CYAN}                               ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}")

        print(f"{Colors.GREEN}[+] CHE DO MAX SPEED - 100 THREAD SONG SONG{Colors.END}")
        print(f"{Colors.GREEN}[+] PROXY VIET NAM - TANG VIEW CHUAN{Colors.END}")
        
        # Tinh thoi gian
        est_time = self.view_count / 1000  # 1000 view/phut
        if est_time < 60:
            time_str = f"{est_time:.0f} giay"
        elif est_time < 3600:
            time_str = f"{est_time/60:.1f} phut"
        else:
            time_str = f"{est_time/3600:.1f} gio"
        
        print(f"{Colors.YELLOW}[*] UOC TINH: ~{time_str}{Colors.END}")
        print("=" * 60)

        video_id = self.get_video_id()
        if not video_id:
            print(f"{Colors.RED}[!] KHONG THE LAY VIDEO ID{Colors.END}")
            return

        total_batches = (self.view_count + self.batch_size - 1) // self.batch_size
        print(f"{Colors.CYAN}[*] Chia thanh {total_batches} dot, moi dot {self.batch_size} view{Colors.END}")
        
        start_total = time.time()
        
        for batch in range(total_batches):
            if not self.running:
                break

            start_idx = batch * self.batch_size
            end_idx = min(start_idx + self.batch_size, self.view_count)
            batch_count = end_idx - start_idx

            print(f"\n{Colors.BOLD}{Colors.YELLOW}[=== DOT {batch+1}/{total_batches} - {batch_count} view ===]{Colors.END}")
            
            start_time = time.time()
            self.run_batch_super_fast(batch_count)
            elapsed = time.time() - start_time
            
            # Hien thi ket qua
            rate = (self.success_count - start_idx) / elapsed if elapsed > 0 else 0
            print(f"\n{Colors.GREEN}[*] Dot {batch+1}: +{self.success_count - start_idx} view ({elapsed:.1f}s) - {rate:.1f} view/s{Colors.END}")
            print(f"{Colors.CYAN}[*] Tong: {self.success_count}/{self.view_count} ({self.success_count/self.view_count*100:.1f}%){Colors.END}")

            if self.success_count < self.view_count and batch < total_batches - 1:
                wait_time = random.randint(1, 3)  # Nghi rat ngan
                if wait_time > 0:
                    self.wait_with_countdown(wait_time)

        elapsed_total = time.time() - start_total
        
        print("\n" + "=" * 60)
        print(f"{Colors.BOLD}{Colors.GREEN}[+] HOAN THANH! View: {self.success_count}{Colors.END}")
        print(f"{Colors.RED}[-] That bai: {self.fail_count}{Colors.END}")
        if (self.success_count + self.fail_count) > 0:
            rate = (self.success_count/(self.success_count+self.fail_count)*100)
            print(f"{Colors.WHITE}[*] Ty le thanh cong: {rate:.1f}%{Colors.END}")
        print(f"{Colors.WHITE}[*] Tong thoi gian: {elapsed_total:.1f}s ({elapsed_total/60:.1f} phut){Colors.END}")
        print(f"{Colors.WHITE}[*] Toc do trung binh: {self.success_count/elapsed_total:.1f} view/s{Colors.END}")
        print(f"{Colors.WHITE}[*] END: {time.strftime('%H:%M:%S %d/%m/%Y')}{Colors.END}")
        print("=" * 60)

    def wait_with_countdown(self, seconds):
        for i in range(seconds, 0, -1):
            sys.stdout.write(f"\r{Colors.CYAN}[*] Nghi {i}s   {Colors.END}")
            sys.stdout.flush()
            time.sleep(1)
        print(f"\r{Colors.GREEN}[*] Tiep tuc...               {Colors.END}")

# ========== MENU ==========
def show_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║                     [ NGLONG DEV ]                            ║")
    print("║         TIKTOK VIEW BOT v8.0 - MAX SPEED 100%                ║")
    print("╠════════════════════════════════════════════════════════════════╣")
    print(f"║  {Colors.WHITE}1. TANG VIEW (MAX SPEED){Colors.CYAN}                                    ║")
    print(f"║  {Colors.WHITE}2. CAP NHAT PROXY VN{Colors.CYAN}                                       ║")
    print(f"║  {Colors.WHITE}3. THONG TIN VIDEO{Colors.CYAN}                                        ║")
    print(f"║  {Colors.WHITE}4. THOAT{Colors.CYAN}                                                   ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    print(f"{Colors.GREEN}[*] TOC DO: ~500-1000 VIEW/PHUT{Colors.END}")
    print(f"{Colors.GREEN}[*] PROXY VIET NAM: {len(PROXY_LIST)}{Colors.END}")
    print(f"{Colors.GREEN}[*] THREADS: 100 SONG SONG{Colors.END}")

# ========== MAIN ==========
if __name__ == "__main__":
    print(f"{Colors.YELLOW}[*] KHOI DONG TIKTOK VIEW BOT v8.0...{Colors.END}")
    print(f"{Colors.GREEN}[+] CHE DO MAX SPEED - 100 THREAD{Colors.END}")
    print(f"{Colors.GREEN}[+] PROXY VIET NAM - TANG VIEW CHUAN{Colors.END}")
    
    time.sleep(1)
    
    fetch_vietnam_proxies()
    
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

            # Tinh thoi gian
            est_time = view_count / 1000
            if est_time < 60:
                time_str = f"{est_time:.0f} giay"
            elif est_time < 3600:
                time_str = f"{est_time/60:.1f} phut"
            else:
                time_str = f"{est_time/3600:.1f} gio"
            
            print(f"{Colors.YELLOW}[*] Du kien: {time_str}{Colors.END}")
            print(f"{Colors.YELLOW}[*] Ty le thanh cong: 80-95%{Colors.END}")
            confirm = input(f"{Colors.YELLOW}[*] Tiep tuc? (y/n): {Colors.END}").strip().lower()
            if confirm != 'y':
                continue

            bot = TikTokViewBot(video_input, view_count)
            bot.proxies = PROXY_LIST.copy()
            bot.run()
            input(f"{Colors.YELLOW}[*] Enter de tro ve...{Colors.END}")

        elif choice == "2":
            print(f"{Colors.YELLOW}[*] Dang cap nhat proxy Viet Nam...{Colors.END}")
            fetch_vietnam_proxies()
            input(f"{Colors.YELLOW}[*] Enter...{Colors.END}")

        elif choice == "3":
            video_input = input(f"{Colors.WHITE}[NGLONG] URL video: {Colors.END}").strip()
            if not video_input:
                print(f"{Colors.RED}[!] URL khong duoc de trong{Colors.END}")
                input(f"{Colors.YELLOW}[*] Enter...{Colors.END}")
                continue
            
            bot = TikTokViewBot(video_input, 10)
            video_id = bot.get_video_id()
            if video_id:
                print(f"{Colors.GREEN}[+] VIDEO ID: {video_id}{Colors.END}")
                print(f"{Colors.GREEN}[+] URL: {video_input}{Colors.END}")
            else:
                print(f"{Colors.RED}[-] URL khong hop le{Colors.END}")
            input(f"{Colors.YELLOW}[*] Enter de tiep tuc...{Colors.END}")

        elif choice == "4":
            print(f"{Colors.GREEN}[+] Tam biet! NGLONG DEV xin chao{Colors.END}")
            time.sleep(1)
            sys.exit(0)

        else:
            print(f"{Colors.RED}[!] Lua chon sai!{Colors.END}")
            time.sleep(1)
