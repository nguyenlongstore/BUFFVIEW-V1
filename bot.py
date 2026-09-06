import requests
import random
import threading
import time
import os
import sys
import socket
import dns.resolver
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

# ========== TU DONG LAY IP TIKTOK ==========
class TikTokIPAutoResolver:
    def __init__(self):
        self.tiktok_ips = []
        self.current_index = 0
        self.last_update = 0
        self.update_interval = 300
        
    def resolve_all_domains(self):
        domains = [
            "www.tiktok.com",
            "api.tiktok.com",
            "api2.tiktok.com",
            "api3.tiktok.com",
            "v16-web.tiktok.com",
            "v19.tiktok.com",
            "v16.tiktok.com",
            "sgapi.tiktok.com",
            "vaapi.tiktok.com",
            "usapi.tiktok.com",
            "euapi.tiktok.com",
            "www.tiktokcdn.com",
            "tiktokcdn.com",
            "ib.tiktokcdn.com",
            "ib2.tiktokcdn.com",
            "p16-sign.tiktokcdn.com",
            "p19-sign.tiktokcdn.com"
        ]
        
        all_ips = []
        print(f"{Colors.CYAN}[*] Dang quet IP cua TikTok...{Colors.END}")
        
        for domain in domains:
            try:
                try:
                    ips = socket.gethostbyname_ex(domain)[2]
                    for ip in ips:
                        if ip not in all_ips and self.is_valid_ip(ip):
                            all_ips.append(ip)
                    print(f"{Colors.GREEN}[+] {domain}: {len(ips)} IP{Colors.END}")
                except:
                    pass
                
                try:
                    answers = dns.resolver.resolve(domain, 'A')
                    for rdata in answers:
                        ip = str(rdata)
                        if ip not in all_ips and self.is_valid_ip(ip):
                            all_ips.append(ip)
                except:
                    pass
                    
            except Exception as e:
                print(f"{Colors.YELLOW}[!] Loi resolve {domain}{Colors.END}")
        
        valid_ips = []
        for ip in all_ips:
            if self.is_valid_ip(ip):
                valid_ips.append(ip)
        
        self.tiktok_ips = list(set(valid_ips))
        self.last_update = time.time()
        
        print(f"{Colors.GREEN}[+] Tim thay {len(self.tiktok_ips)} IP hop le cua TikTok{Colors.END}")
        return self.tiktok_ips
    
    def is_valid_ip(self, ip):
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            try:
                num = int(part)
                if num < 0 or num > 255:
                    return False
            except:
                return False
        return True
    
    def get_ips(self):
        if not self.tiktok_ips or (time.time() - self.last_update > self.update_interval):
            self.resolve_all_domains()
        return self.tiktok_ips
    
    def get_random_ip(self):
        ips = self.get_ips()
        if ips:
            return random.choice(ips)
        return None
    
    def get_next_ip(self):
        ips = self.get_ips()
        if ips:
            ip = ips[self.current_index % len(ips)]
            self.current_index += 1
            return ip
        return None

# ========== CLASS BOT CHINH ==========
class TikTokViewBot:
    def __init__(self, video_url, view_count):
        self.video_url = video_url
        self.view_count = max(500, min(100000000, view_count))
        self.ua = UserAgent()
        self.success_count = 0
        self.fail_count = 0
        self.running = True
        self.batch_size = 500
        self.ip_resolver = TikTokIPAutoResolver()
        self.tiktok_ips = self.ip_resolver.get_ips()

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

    def send_view_direct_ip(self):
        try:
            video_id = self.get_video_id()
            if not video_id:
                self.fail_count += 1
                return False

            tiktok_ip = self.ip_resolver.get_next_ip()
            if not tiktok_ip:
                self.tiktok_ips = self.ip_resolver.resolve_all_domains()
                tiktok_ip = self.ip_resolver.get_next_ip()
                if not tiktok_ip:
                    return self.send_view_normal()

            url = f"https://{tiktok_ip}/api/v1/video/views/?video_id={video_id}"
            
            headers = {
                "User-Agent": self.ua.random,
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "vi-VN,vi;q=0.9,en;q=0.8",
                "Referer": "https://www.tiktok.com/",
                "Origin": "https://www.tiktok.com",
                "Connection": "keep-alive",
                "X-Requested-With": "XMLHttpRequest",
                "Host": "www.tiktok.com"
            }

            response = requests.get(url, headers=headers, timeout=10, verify=False)

            if response.status_code == 200:
                self.success_count += 1
                print(f"{Colors.GREEN}[+] View OK ({self.success_count}/{self.view_count}) - IP: {tiktok_ip} - {time.strftime('%H:%M:%S')}{Colors.END}")
                return True
            else:
                self.fail_count += 1
                print(f"{Colors.RED}[-] Fail status {response.status_code} - IP: {tiktok_ip} ({self.fail_count} fail){Colors.END}")
                return False

        except Exception as e:
            self.fail_count += 1
            print(f"{Colors.RED}[!] Error: {str(e)[:50]} ({self.fail_count} fail){Colors.END}")
            return False

    def send_view_normal(self):
        try:
            video_id = self.get_video_id()
            if not video_id:
                self.fail_count += 1
                return False

            url = f"https://www.tiktok.com/api/v1/video/views/?video_id={video_id}"
            headers = {
                "User-Agent": self.ua.random,
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "vi-VN,vi;q=0.9,en;q=0.8",
                "Referer": "https://www.tiktok.com/",
                "Origin": "https://www.tiktok.com",
                "Connection": "keep-alive",
                "X-Requested-With": "XMLHttpRequest"
            }

            response = requests.get(url, headers=headers, timeout=15)

            if response.status_code == 200:
                self.success_count += 1
                print(f"{Colors.GREEN}[+] View OK ({self.success_count}/{self.view_count}) - {time.strftime('%H:%M:%S')}{Colors.END}")
                return True
            else:
                self.fail_count += 1
                print(f"{Colors.RED}[-] Fail status {response.status_code} ({self.fail_count} fail){Colors.END}")
                return False

        except Exception as e:
            self.fail_count += 1
            print(f"{Colors.RED}[!] Error: {str(e)[:50]} ({self.fail_count} fail){Colors.END}")
            return False

    def send_view(self):
        if self.tiktok_ips:
            return self.send_view_direct_ip()
        else:
            return self.send_view_normal()

    def wait_with_countdown(self, seconds):
        print(f"{Colors.YELLOW}[*] Dang cho {seconds}s de tranh xung dot code...{Colors.END}")
        for i in range(seconds, 0, -1):
            sys.stdout.write(f"\r{Colors.CYAN}[*] Dem nguoc: {i}s   {Colors.END}")
            sys.stdout.flush()
            time.sleep(1)
        print(f"\r{Colors.GREEN}[*] Tiep tuc chay...               {Colors.END}")

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        self.tiktok_ips = self.ip_resolver.get_ips()
        
        print(f"{Colors.BOLD}{Colors.CYAN}")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║                     [ NGLONG DEV ]                            ║")
        print("║         TIKTOK VIEW BOT - AUTO IP RESOLVER                   ║")
        print("╠════════════════════════════════════════════════════════════════╣")
        print(f"║  {Colors.WHITE}TOI THIEU: 500 VIEWS{Colors.CYAN}          {Colors.WHITE}TOI DA: 100.000.000 VIEWS{Colors.CYAN}          ║")
        print(f"║  {Colors.WHITE}AUTO XOAY IP TIKTOK{Colors.CYAN}                                  ║")
        print(f"║  {Colors.WHITE}SO IP TIM THAY: {len(self.tiktok_ips)}{Colors.CYAN}                                         ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}")

        print(f"{Colors.BOLD}{Colors.WHITE}[*] BAT DAU TANG VIEW: {self.view_count}{Colors.END}")
        print(f"{Colors.WHITE}[*] VIDEO: {self.video_url}{Colors.END}")
        print(f"{Colors.WHITE}[*] THOI GIAN BAT DAU: {time.strftime('%H:%M:%S %d/%m/%Y')}{Colors.END}")
        print("=" * 60)

        video_id = self.get_video_id()
        if not video_id:
            print(f"{Colors.RED}[!] KHONG THE LAY VIDEO ID - Kiem tra URL{Colors.END}")
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
            max_threads = 30

            for i in range(batch_view_count):
                if not self.running:
                    break
                
                t = threading.Thread(target=self.send_view)
                threads.append(t)
                t.start()

                delay = random.uniform(0.2, 0.8)
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
                wait_time = random.randint(30, 60)
                self.wait_with_countdown(wait_time)
                
                print(f"{Colors.CYAN}[*] Tu dong cap nhat danh sach IP...{Colors.END}")
                self.tiktok_ips = self.ip_resolver.get_ips()

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
        print(f"{Colors.BOLD}{Colors.CYAN}║              NGLONG DEV - TIKTOK VIEW BOT v4.0               ║{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}╚════════════════════════════════════════════════════════════════╝{Colors.END}")

# ========== MENU CHUC NANG ==========
def show_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║                     [ NGLONG DEV ]                            ║")
    print("║         TIKTOK VIEW BOT - AUTO IP RESOLVER                   ║")
    print("╠════════════════════════════════════════════════════════════════╣")
    print(f"║  {Colors.WHITE}1. TANG VIEW (AUTO IP){Colors.CYAN}                                     ║")
    print(f"║  {Colors.WHITE}2. XEM DANH SACH IP TIKTOK{Colors.CYAN}                                 ║")
    print(f"║  {Colors.WHITE}3. THONG TIN VIDEO{Colors.CYAN}                                         ║")
    print(f"║  {Colors.WHITE}4. CAP NHAT IP MOI{Colors.CYAN}                                         ║")
    print(f"║  {Colors.WHITE}5. THOAT{Colors.CYAN}                                                   ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")

def show_ips():
    resolver = TikTokIPAutoResolver()
    ips = resolver.get_ips()
    if ips:
        print(f"{Colors.GREEN}[+] Danh sach IP TikTok ({len(ips)} IP):{Colors.END}")
        for i, ip in enumerate(ips, 1):
            print(f"  {Colors.CYAN}{i}. {ip}{Colors.END}")
    else:
        print(f"{Colors.RED}[!] Khong tim thay IP nao{Colors.END}")
    input(f"{Colors.YELLOW}[*] Nhan Enter de tiep tuc...{Colors.END}")

def get_video_info(video_url):
    try:
        bot = TikTokViewBot(video_url, 0)
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

def update_ips():
    resolver = TikTokIPAutoResolver()
    print(f"{Colors.YELLOW}[*] Dang cap nhat IP moi...{Colors.END}")
    ips = resolver.resolve_all_domains()
    print(f"{Colors.GREEN}[+] Da cap nhat {len(ips)} IP moi{Colors.END}")
    input(f"{Colors.YELLOW}[*] Nhan Enter de tiep tuc...{Colors.END}")

# ========== MAIN ==========
if __name__ == "__main__":
    try:
        import dns.resolver
    except ImportError:
        print(f"{Colors.YELLOW}[*] Dang cai dat thu vien dnspython...{Colors.END}")
        os.system("pip install dnspython -q")
        import dns.resolver
    
    while True:
        show_menu()
        choice = input(f"{Colors.BOLD}{Colors.WHITE}[NGLONG] Nhap lua chon (1-5): {Colors.END}").strip()

        if choice == "1":
            video_input = input(f"{Colors.WHITE}[NGLONG] Nhap URL video TikTok: {Colors.END}").strip()
            if not video_input:
                print(f"{Colors.RED}[!] URL khong duoc de trong{Colors.END}")
                input(f"{Colors.YELLOW}[*] Nhan Enter de tiep tuc...{Colors.END}")
                continue

            try:
                view_count = int(input(f"{Colors.WHITE}[NGLONG] Nhap so luong view (500-100000000): {Colors.END}").strip())
                if view_count < 500:
                    view_count = 500
                    print(f"{Colors.YELLOW}[!] Tu dong nang len 500 (toi thieu){Colors.END}")
                elif view_count > 100000000:
                    view_count = 100000000
                    print(f"{Colors.YELLOW}[!] Tu dong giam xuong 100.000.000 (toi da){Colors.END}")
            except:
                view_count = 500
                print(f"{Colors.YELLOW}[!] Su dung 500 view mac dinh{Colors.END}")

            bot = TikTokViewBot(video_input, view_count)
            bot.run()
            input(f"{Colors.YELLOW}[*] Nhan Enter de tro ve menu...{Colors.END}")

        elif choice == "2":
            show_ips()

        elif choice == "3":
            video_input = input(f"{Colors.WHITE}[NGLONG] Nhap URL video TikTok: {Colors.END}").strip()
            if video_input:
                get_video_info(video_input)
            else:
                print(f"{Colors.RED}[!] URL khong duoc de trong{Colors.END}")
                input(f"{Colors.YELLOW}[*] Nhan Enter de tiep tuc...{Colors.END}")

        elif choice == "4":
            update_ips()

        elif choice == "5":
            print(f"{Colors.GREEN}[+] Tam biet! NGLONG DEV xin chao...{Colors.END}")
            time.sleep(1)
            sys.exit(0)

        else:
            print(f"{Colors.RED}[!] Lua chon khong hop le!{Colors.END}")
            time.sleep(1)
