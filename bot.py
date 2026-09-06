import requests
import random
import threading
import time
import os
import sys
from fake_useragent import UserAgent

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

# ========== CLASS BOT CHINH ==========
class TikTokViewBot:
    def __init__(self, video_url, view_count):
        self.video_url = video_url
        self.view_count = max(10, min(100000000, view_count))  # TOI THIEU 10 VIEW
        self.ua = UserAgent()
        self.success_count = 0
        self.fail_count = 0
        self.running = True
        self.batch_size = 50  # Giam batch size cho test

    def get_video_id(self):
        if "tiktok.com" in self.video_url:
            if "/video/" in self.video_url:
                return self.video_url.split("/video/")[1].split("?")[0].split("/")[0]
            elif "vm.tiktok.com" in self.video_url:
                try:
                    response = requests.head(self.video_url, allow_redirects=True, timeout=10)
                    return response.url.split("/video/")[1].split("?")[0].split("/")[0]
                except:
                    return None
        return None

    def send_view(self):
        try:
            video_id = self.get_video_id()
            if not video_id:
                self.fail_count += 1
                return False

            # Su dung URL thong thuong qua DNS
            url = f"https://www.tiktok.com/api/v1/video/views/?video_id={video_id}"
            
            headers = {
                "User-Agent": self.ua.random,
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "vi-VN,vi;q=0.9,en;q=0.8",
                "Referer": "https://www.tiktok.com/",
                "Origin": "https://www.tiktok.com",
                "Connection": "keep-alive",
                "X-Requested-With": "XMLHttpRequest",
                "Accept-Encoding": "gzip, deflate, br",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache"
            }

            session = requests.Session()
            session.trust_env = False
            
            response = session.get(url, headers=headers, timeout=15)

            if response.status_code == 200:
                self.success_count += 1
                print(f"{Colors.GREEN}[+] View OK ({self.success_count}/{self.view_count}) - {time.strftime('%H:%M:%S')}{Colors.END}")
                return True
            else:
                self.fail_count += 1
                print(f"{Colors.RED}[-] Fail status {response.status_code} ({self.fail_count} fail){Colors.END}")
                return False

        except requests.exceptions.Timeout:
            self.fail_count += 1
            print(f"{Colors.RED}[!] Timeout ({self.fail_count} fail){Colors.END}")
            return False
        except requests.exceptions.ConnectionError:
            self.fail_count += 1
            print(f"{Colors.RED}[!] Connection Error ({self.fail_count} fail){Colors.END}")
            return False
        except Exception as e:
            self.fail_count += 1
            print(f"{Colors.RED}[!] Error: {str(e)[:50]} ({self.fail_count} fail){Colors.END}")
            return False

    def wait_with_countdown(self, seconds):
        print(f"{Colors.YELLOW}[*] Dang cho {seconds}s de tranh xung dot code...{Colors.END}")
        for i in range(seconds, 0, -1):
            sys.stdout.write(f"\r{Colors.CYAN}[*] Dem nguoc: {i}s   {Colors.END}")
            sys.stdout.flush()
            time.sleep(1)
        print(f"\r{Colors.GREEN}[*] Tiep tuc chay...               {Colors.END}")

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # ====== BANNER ======
        print(f"{Colors.BOLD}{Colors.CYAN}")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║                     [ NGLONG DEV ]                            ║")
        print("║            TIKTOK VIEW BOT - UNLIMITED VIEWS                 ║")
        print("╠════════════════════════════════════════════════════════════════╣")
        print(f"║  {Colors.WHITE}TOI THIEU: 10 VIEWS{Colors.CYAN}           {Colors.WHITE}TOI DA: 100.000.000 VIEWS{Colors.CYAN}          ║")
        print(f"║  {Colors.WHITE}CHE DO: REQUEST QUA DNS{Colors.CYAN}                                  ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}")

        print(f"{Colors.BOLD}{Colors.WHITE}[*] BAT DAU TANG VIEW: {self.view_count}{Colors.END}")
        print(f"{Colors.WHITE}[*] VIDEO: {self.video_url}{Colors.END}")
        print(f"{Colors.WHITE}[*] THOI GIAN BAT DAU: {time.strftime('%H:%M:%S %d/%m/%Y')}{Colors.END}")
        print("=" * 60)

        video_id = self.get_video_id()
        if not video_id:
            print(f"{Colors.RED}[!] KHONG THE LAY VIDEO ID - Kiem tra URL{Colors.END}")
            print(f"{Colors.YELLOW}[!] DAM BAO URL DUNG DINH DANG:{Colors.END}")
            print(f"{Colors.YELLOW}  https://www.tiktok.com/@username/video/1234567890123456789{Colors.END}")
            return

        total_batches = (self.view_count + self.batch_size - 1) // self.batch_size
        print(f"{Colors.CYAN}[*] Chia thanh {total_batches} dot, moi dot {self.batch_size} view{Colors.END}")

        for batch in range(total_batches):
            if not self.running:
                break

            start_idx = batch * self.batch_size
            end_idx = min(start_idx + self.batch_size, self.view_count)
            batch_view_count = end_idx - start_idx

            print(f"\n{Colors.BOLD}{Colors.YELLOW}[===== DOT {batch+1}/{total_batches} - {batch_view_count} view =====]{Colors.END}")

            threads = []
            max_threads = 10  # Giam xuong cho test

            for i in range(batch_view_count):
                if not self.running:
                    break
                
                t = threading.Thread(target=self.send_view)
                threads.append(t)
                t.start()

                delay = random.uniform(0.5, 1.5)
                time.sleep(delay)

                if len(threads) >= max_threads:
                    for th in threads:
                        th.join()
                    threads = []

            for th in threads:
                th.join()

            print(f"{Colors.GREEN}[*] Dot {batch+1} hoan thanh: Thanh cong {self.success_count - start_idx} view{Colors.END}")
            print(f"{Colors.CYAN}[*] Tong thanh cong: {self.success_count}/{self.view_count}{Colors.END}")

            if self.success_count < self.view_count and batch < total_batches - 1:
                wait_time = random.randint(10, 30)  # Giam delay cho test
                self.wait_with_countdown(wait_time)

        # ====== KET THUC ======
        print("\n" + "=" * 60)
        print(f"{Colors.BOLD}{Colors.GREEN}[+] HOAN THANH! Tong view da gui: {self.success_count}{Colors.END}")
        print(f"{Colors.RED}[-] That bai: {self.fail_count}{Colors.END}")
        if (self.success_count + self.fail_count) > 0:
            rate = (self.success_count/(self.success_count+self.fail_count)*100)
            print(f"{Colors.WHITE}[*] Ty le thanh cong: {rate:.1f}%{Colors.END}")
        print(f"{Colors.WHITE}[*] THOI GIAN KET THUC: {time.strftime('%H:%M:%S %d/%m/%Y')}{Colors.END}")
        print("=" * 60)
        print(f"{Colors.BOLD}{Colors.CYAN}╔════════════════════════════════════════════════════════════════╗{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}║                    CAM ON BAN DA SU DUNG!                    ║{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}║              NGLONG DEV - TIKTOK VIEW BOT v4.2               ║{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}╚════════════════════════════════════════════════════════════════╝{Colors.END}")

# ========== MENU CHUC NANG ==========
def show_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║                     [ NGLONG DEV ]                            ║")
    print("║            TIKTOK VIEW BOT - UNLIMITED VIEWS                 ║")
    print("╠════════════════════════════════════════════════════════════════╣")
    print(f"║  {Colors.WHITE}1. TANG VIEW TIKTOK{Colors.CYAN}                                        ║")
    print(f"║  {Colors.WHITE}2. THONG TIN VIDEO{Colors.CYAN}                                        ║")
    print(f"║  {Colors.WHITE}3. THOAT{Colors.CYAN}                                                   ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")

def get_video_info(video_url):
    try:
        bot = TikTokViewBot(video_url, 10)
        video_id = bot.get_video_id()
        if video_id:
            url = f"https://www.tiktok.com/api/v1/video/info/?video_id={video_id}"
            headers = {
                "User-Agent": UserAgent().random,
                "Accept": "application/json"
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"{Colors.GREEN}[+] VIDEO ID: {video_id}{Colors.END}")
                print(f"{Colors.GREEN}[+] STATUS: {data.get('status_code', 'OK')}{Colors.END}")
            else:
                print(f"{Colors.RED}[-] Khong the lay thong tin video{Colors.END}")
        else:
            print(f"{Colors.RED}[-] URL khong hop le{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}[!] Loi: {str(e)[:50]}{Colors.END}")
    input(f"{Colors.YELLOW}[*] Nhan Enter de tiep tuc...{Colors.END}")

# ========== MAIN ==========
if __name__ == "__main__":
    while True:
        show_menu()
        choice = input(f"{Colors.BOLD}{Colors.WHITE}[NGLONG] Nhap lua chon (1-3): {Colors.END}").strip()

        if choice == "1":
            video_input = input(f"{Colors.WHITE}[NGLONG] Nhap URL video TikTok: {Colors.END}").strip()
            if not video_input:
                print(f"{Colors.RED}[!] URL khong duoc de trong{Colors.END}")
                input(f"{Colors.YELLOW}[*] Nhan Enter de tiep tuc...{Colors.END}")
                continue

            try:
                view_count = int(input(f"{Colors.WHITE}[NGLONG] Nhap so luong view (10-100000000): {Colors.END}").strip())
                if view_count < 10:
                    view_count = 10
                    print(f"{Colors.YELLOW}[!] Tu dong nang len 10 (toi thieu){Colors.END}")
                elif view_count > 100000000:
                    view_count = 100000000
                    print(f"{Colors.YELLOW}[!] Tu dong giam xuong 100.000.000 (toi da){Colors.END}")
            except:
                view_count = 10
                print(f"{Colors.YELLOW}[!] Su dung 10 view mac dinh (che do test){Colors.END}")

            bot = TikTokViewBot(video_input, view_count)
            bot.run()
            input(f"{Colors.YELLOW}[*] Nhan Enter de tro ve menu...{Colors.END}")

        elif choice == "2":
            video_input = input(f"{Colors.WHITE}[NGLONG] Nhap URL video TikTok: {Colors.END}").strip()
            if video_input:
                get_video_info(video_input)
            else:
                print(f"{Colors.RED}[!] URL khong duoc de trong{Colors.END}")
                input(f"{Colors.YELLOW}[*] Nhan Enter de tiep tuc...{Colors.END}")

        elif choice == "3":
            print(f"{Colors.GREEN}[+] Tam biet! NGLONG DEV xin chao...{Colors.END}")
            time.sleep(1)
            sys.exit(0)

        else:
            print(f"{Colors.RED}[!] Lua chon khong hop le!{Colors.END}")
            time.sleep(1)
