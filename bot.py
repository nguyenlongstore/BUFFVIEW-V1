import requests
import random
import threading
import time
import os
import sys
import json
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
        PROXY_LIST = ["http://113.161.77.184:8080", "http://123.30.50.226:8080"]
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
        self.batch_size = 50
        self.proxies = PROXY_LIST.copy()
        self.max_threads = 30
        self.lock = threading.Lock()

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

    def send_view(self, proxy=None):
        """Gui view sieu toc"""
        try:
            video_id = self.get_video_id()
            if not video_id:
                with self.lock:
                    self.fail_count += 1
                return False

            username = self.video_url.split('/@')[1].split('/')[0]
            
            # URL chinh
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
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
                "DNT": "1"
            }

            session = requests.Session()
            session.trust_env = False
            
            # Cookie
            session.cookies.update({
                "tt_webid_v2": str(random.randint(1000000000000000000, 9999999999999999999)),
                "tt_csrf_token": ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32)),
                "s_v_web_id": ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32)),
                "sessionid": ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32)),
                "sessionid_ss": ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32)),
                "uid": f"0{random.randint(10000000, 99999999)}",
                "uuid": str(random.randint(1000000000000, 9999999999999))
            })
            
            if proxy:
                session.proxies = {"http": proxy, "https": proxy}
            
            response = session.get(url, headers=headers, timeout=3, allow_redirects=True)
            
            if response.status_code in [200, 201, 202, 204, 301, 302]:
                with self.lock:
                    self.success_count += 1
                return True
            else:
                # Thu API
                try:
                    api_url = f"https://www.tiktok.com/api/v1/video/views/?video_id={video_id}"
                    response2 = session.get(api_url, headers=headers, timeout=2)
                    if response2.status_code == 200:
                        with self.lock:
                            self.success_count += 1
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

    def run_batch(self, batch_count):
        """Chay batch voi thread pool"""
        proxies = self.proxies.copy() if self.proxies else [None]
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []
            for i in range(batch_count):
                proxy = random.choice(proxies) if proxies else None
                future = executor.submit(self.send_view, proxy)
                futures.append(future)
            
            # Dem ket qua
            for future in as_completed(futures):
                try:
                    future.result(timeout=3)
                except:
                    pass

    def wait_with_countdown(self, seconds):
        for i in range(seconds, 0, -1):
            sys.stdout.write(f"\r{Colors.CYAN}[*] Nghi {i}s   {Colors.END}")
            sys.stdout.flush()
            time.sleep(1)
        print(f"\r{Colors.GREEN}[*] Tiep tuc...               {Colors.END}")

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"{Colors.BOLD}{Colors.CYAN}")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║                     [ NGLONG DEV ]                            ║")
        print("║         TIKTOK VIEW BOT v8.2 - MAX SPEED                     ║")
        print("╠════════════════════════════════════════════════════════════════╣")
        print(f"║  {Colors.WHITE}TOI THIEU: 10 VIEWS{Colors.CYAN}           {Colors.WHITE}TOI DA: 100.000.000 VIEWS{Colors.CYAN}          ║")
        print(f"║  {Colors.WHITE}THREADS: {self.max_threads}{Colors.CYAN}                                        ║")
        print(f"║  {Colors.WHITE}PROXY VN: {len(self.proxies)}{Colors.CYAN}                                           ║")
        print(f"║  {Colors.WHITE}TOC DO: ~300-500 VIEW/PHUT{Colors.CYAN}                               ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}")

        print(f"{Colors.GREEN}[+] CHE DO MAX SPEED - 30 THREAD SONG SONG{Colors.END}")
        print(f"{Colors.GREEN}[+] PROXY VIET NAM - TANG VIEW CHUAN{Colors.END}")
        
        # Tinh thoi gian
        est_time = self.view_count / 300
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
            print(f"{Colors.YELLOW}[!] Kiem tra URL: https://www.tiktok.com/@username/video/123456789{Colors.END}")
            return

        total_batches = (self.view_count + self.batch_size - 1) // self.batch_size
        print(f"{Colors.CYAN}[*] Chia thanh {total_batches} dot, moi dot {self.batch_size} view{Colors.END}")
        
        start_total = time.time()
        total_success = 0  # Bien dem tong view thanh cong
        
        for batch in range(total_batches):
            if not self.running:
                break

            start_idx = batch * self.batch_size
            end_idx = min(start_idx + self.batch_size, self.view_count)
            batch_count = end_idx - start_idx

            # Luu so view thanh cong truoc khi chay
            before = self.success_count
            
            print(f"\n{Colors.BOLD}{Colors.YELLOW}[=== DOT {batch+1}/{total_batches} - {batch_count} view ===]{Colors.END}")
            
            start_time = time.time()
            self.run_batch(batch_count)
            elapsed = time.time() - start_time
            
            # Tinh so view thanh cong trong dot nay
            added = self.success_count - before
            total_success += added  # Cong don vao tong
            
            rate = added / elapsed if elapsed > 0 else 0
            
            print(f"\n{Colors.GREEN}[*] Dot {batch+1}: +{added} view ({elapsed:.1f}s) - {rate:.1f} view/s{Colors.END}")
            print(f"{Colors.CYAN}[*] Tong: {self.success_count}/{self.view_count} ({self.success_count/self.view_count*100:.1f}%){Colors.END}")

            if self.success_count < self.view_count and batch < total_batches - 1:
                wait_time = random.randint(1, 3)
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
        if elapsed_total > 0:
            print(f"{Colors.WHITE}[*] Toc do TB: {self.success_count/elapsed_total:.1f} view/s{Colors.END}")
        print(f"{Colors.WHITE}[*] END: {time.strftime('%H:%M:%S %d/%m/%Y')}{Colors.END}")
        print("=" * 60)

# ========== MENU ==========
def show_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║                     [ NGLONG DEV ]                            ║")
    print("║         TIKTOK VIEW BOT v8.2 - MAX SPEED                     ║")
    print("╠════════════════════════════════════════════════════════════════╣")
    print(f"║  {Colors.WHITE}1. TANG VIEW (MAX SPEED){Colors.CYAN}                                    ║")
    print(f"║  {Colors.WHITE}2. CAP NHAT PROXY VN{Colors.CYAN}                                       ║")
    print(f"║  {Colors.WHITE}3. THONG TIN VIDEO{Colors.CYAN}                                        ║")
    print(f"║  {Colors.WHITE}4. THOAT{Colors.CYAN}                                                   ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    print(f"{Colors.GREEN}[*] TOC DO: ~300-500 VIEW/PHUT{Colors.END}")
    print(f"{Colors.GREEN}[*] PROXY VIET NAM: {len(PROXY_LIST)}{Colors.END}")
    print(f"{Colors.GREEN}[*] THREADS: 30 SONG SONG{Colors.END}")

# ========== MAIN ==========
if __name__ == "__main__":
    print(f"{Colors.YELLOW}[*] KHOI DONG TIKTOK VIEW BOT v8.2...{Colors.END}")
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
            est_time = view_count / 300
            if est_time < 60:
                time_str = f"{est_time:.0f} giay"
            elif est_time < 3600:
                time_str = f"{est_time/60:.1f} phut"
            else:
                time_str = f"{est_time/3600:.1f} gio"
            
            print(f"{Colors.YELLOW}[*] Du kien: {time_str}{Colors.END}")
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
