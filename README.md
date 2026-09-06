# 🚀 TIKTOK VIEW BOT - NGLONG DEV

### Tự động tăng view TikTok không giới hạn | Auto IP Resolver | Không cần Proxy

[![Version](https://img.shields.io/badge/version-4.0-blue)](https://github.com/nglongdev)
[![Python](https://img.shields.io/badge/python-3.8+-green)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/license-MIT-red)](LICENSE)

---

## 📌 TỔNG QUAN

**TikTok View Bot** là công cụ tự động tăng lượt xem cho video TikTok với công nghệ **Auto IP Resolver** - tự động tìm và xoay vòng địa chỉ IP của TikTok để tránh bị phát hiện và giới hạn. Không cần sử dụng proxy, không cần API key, chỉ cần chạy code và nhập URL video.

### ✨ Tính năng nổi bật

- 🔍 **Auto IP Resolver** - Tự động tìm danh sách IP của TikTok từ nhiều domain khác nhau
- 🔄 **Xoay IP liên tục** - Mỗi request sử dụng 1 IP khác nhau, tránh bị phát hiện
- 🔁 **Tự động cập nhật IP** - Refresh danh sách IP sau mỗi 500 view hoặc 5 phút
- 📊 **Không giới hạn view** - Hỗ trợ tối đa 100.000.000 view mỗi lần chạy
- 🎨 **Giao diện menu đẹp** - Dễ sử dụng, hiển thị màu sắc và tiến trình rõ ràng
- 🛡️ **Fallback thông minh** - Tự động chuyển sang URL thường nếu IP bị chết
- ⚡ **Multi-threading** - Chạy đa luồng để tăng tốc độ xử lý
- 📝 **Log chi tiết** - Ghi lại tất cả view đã gửi vào file log
- 🚀 **Batch processing** - Chia nhỏ thành các đợt 500 view, tự động delay 30-60s

---

## 📋 YÊU CẦU HỆ THỐNG

| Thành phần | Yêu cầu tối thiểu | Khuyến nghị |
|------------|-------------------|-------------|
| **Hệ điều hành** | Windows 7 | Windows 10/11 |
| **Python** | 3.8 | 3.11+ |
| **Kết nối Internet** | Có | Cáp quang/FTTH |
| **RAM** | 512MB | 2GB+ |
| **CPU** | 1 Core | 2 Core+ |
| **Ổ cứng trống** | 50MB | 100MB |

---

## 📥 BƯỚC 1: CÀI ĐẶT PYTHON

### 1.1 Tải Python
- Mở trình duyệt, truy cập: **https://www.python.org/downloads/**
- Click vào nút màu vàng **"Download Python 3.x.x"**
- Chọn file: `Windows installer (64-bit)`

### 1.2 Cài đặt Python
- Mở file vừa tải về
- ⚠️ **QUAN TRỌNG**: Tích chọn ô **"Add Python to PATH"** ở dưới cùng
- Click **"Install Now"**
- Đợi quá trình cài đặt hoàn tất
- Click **"Close"**

### 1.3 Kiểm tra cài đặt
- Nhấn tổ hợp phím `Windows + R`
- Gõ `cmd` và nhấn Enter
- Trong cửa sổ CMD, gõ lệnh:
```cmd
python --version
```

· Kết quả hiển thị: Python 3.x.x => Cài đặt thành công

---

📂 BƯỚC 2: TẠO THƯ MỤC VÀ FILE BOT

2.1 Tạo thư mục làm việc

· Mở CMD (Command Prompt)
· Gõ lần lượt các lệnh:

```cmd
mkdir C:\TikTokBot
cd C:\TikTokBot
```

2.2 Tạo file bot.py

· Mở Notepad (hoặc bất kỳ text editor nào: VS Code, Sublime, Notepad++)
· Copy toàn bộ code bot từ file bot.py
· Dán vào Notepad
· Vào menu File -> Save As...
· Đặt tên: bot.py
· Chọn "Save as type": All Files (.)
· Click Save

2.3 Tạo file run.bat

· Mở Notepad mới
· Copy nội dung từ file run.bat
· Vào File -> Save As...
· Đặt tên: run.bat
· Chọn "Save as type": All Files (.)
· Click Save

---

📦 BƯỚC 3: CÀI ĐẶT THƯ VIỆN

3.1 Mở CMD (nếu chưa mở)

· Nhấn Windows + R, gõ cmd, Enter

3.2 Di chuyển đến thư mục bot

```cmd
cd C:\TikTokBot
```

3.3 Cài đặt thư viện

```cmd
pip install requests fake-useragent dnspython
```

3.4 Kiểm tra thư viện đã cài

```cmd
pip list | findstr requests
pip list | findstr fake-useragent
pip list | findstr dnspython
```

Nếu hiển thị tên và phiên bản => Cài đặt thành công.

---

🚀 BƯỚC 4: CHẠY BOT

Cách 1: Double-click vào run.bat (ĐƠN GIẢN NHẤT)

· Mở thư mục C:\TikTokBot
· Double-click vào file run.bat
· Bot sẽ tự động chạy

Cách 2: Chạy từ CMD

```cmd
cd C:\TikTokBot
python bot.py
```

Cách 3: Tạo Shortcut trên Desktop

· Click chuột phải trên Desktop
· Chọn New -> Shortcut
· Nhập đường dẫn: C:\TikTokBot\run.bat
· Đặt tên: TikTok View Bot
· Click Finish
· Double-click vào shortcut để chạy

---

🎮 BƯỚC 5: HƯỚNG DẪN SỬ DỤNG

GIAO DIỆN MENU

Khi bot chạy, màn hình sẽ hiển thị:

```
╔════════════════════════════════════════════════════════════════╗
║                     [ NGLONG DEV ]                            ║
║         TIKTOK VIEW BOT - AUTO IP RESOLVER                   ║
╠════════════════════════════════════════════════════════════════╣
║  1. TANG VIEW (AUTO IP)                                     ║
║  2. XEM DANH SACH IP TIKTOK                                 ║
║  3. THONG TIN VIDEO                                         ║
║  4. CAP NHAT IP MOI                                         ║
║  5. THOAT                                                   ║
╚════════════════════════════════════════════════════════════════╝

[NGLONG] Nhap lua chon (1-5):
```

---

CHỨC NĂNG 1: TĂNG VIEW (AUTO IP)

Mô tả: Tự động tăng view cho video TikTok với IP xoay vòng

Các bước thực hiện:

1️⃣ Nhập số 1 -> Nhấn Enter

2️⃣ Nhập URL video TikTok

```
[NGLONG] Nhap URL video TikTok: https://www.tiktok.com/@username/video/1234567890123456789
```

3️⃣ Nhập số lượng view (500 - 100.000.000)

```
[NGLONG] Nhap so luong view (500-100000000): 10000
```

4️⃣ Bot tự động chạy, hiển thị tiến trình

5️⃣ Sau khi hoàn thành, nhấn Enter để quay lại menu

---

CHỨC NĂNG 2: XEM DANH SÁCH IP TIKTOK

Mô tả: Hiển thị tất cả IP của TikTok đã tìm thấy

Các bước thực hiện:

1️⃣ Nhập số 2 -> Nhấn Enter

2️⃣ Màn hình hiển thị danh sách IP

3️⃣ Nhấn Enter để quay lại menu

---

CHỨC NĂNG 3: THÔNG TIN VIDEO

Mô tả: Kiểm tra ID và trạng thái của video

Các bước thực hiện:

1️⃣ Nhập số 3 -> Nhấn Enter

2️⃣ Nhập URL video

3️⃣ Màn hình hiển thị thông tin video

4️⃣ Nhấn Enter để quay lại menu

---

CHỨC NĂNG 4: CẬP NHẬT IP MỚI

Mô tả: Refresh danh sách IP TikTok mới nhất

Các bước thực hiện:

1️⃣ Nhập số 4 -> Nhấn Enter

2️⃣ Bot tự động quét và cập nhật IP mới

3️⃣ Nhấn Enter để quay lại menu

---

CHỨC NĂNG 5: THOÁT

Mô tả: Đóng chương trình

Các bước thực hiện:

1️⃣ Nhập số 5 -> Nhấn Enter

2️⃣ Bot tự động đóng

---

⚙️ CẤU HÌNH NÂNG CAO

Chỉnh sửa file bot.py

Mở file bot.py bằng Notepad hoặc text editor, tìm các dòng sau để chỉnh sửa:

Tham số Dòng code Mô tả Giá trị mặc định
batch_size self.batch_size = 500 Số view mỗi đợt 500
max_threads max_threads = 30 Số luồng chạy đồng thời 30
delay min wait_time = random.randint(30, 60) Thời gian delay tối thiểu (giây) 30
delay max wait_time = random.randint(30, 60) Thời gian delay tối đa (giây) 60
request delay delay = random.uniform(0.2, 0.8) Delay giữa các request 0.2 - 0.8s
update interval self.update_interval = 300 Tự động refresh IP (giây) 300 (5 phút)

---

🛠️ XỬ LÝ LỖI THƯỜNG GẶP

LỖI CÀI ĐẶT

Lỗi Nguyên nhân Cách khắc phục
'python' is not recognized Python chưa trong PATH Cài lại Python, tích "Add to PATH"
ModuleNotFoundError Chưa cài thư viện pip install requests fake-useragent dnspython
pip is not recognized Pip chưa được cài Cài lại Python, đảm bảo tích pip

LỖI KHI CHẠY

Lỗi Nguyên nhân Cách khắc phục
Connection timed out Mạng chậm / bị chặn Kiểm tra internet, dùng VPN
SSL: CERTIFICATE_VERIFY_FAILED Lỗi chứng chỉ SSL Đã có verify=False trong code
Khong the lay video ID URL sai định dạng Kiểm tra lại URL, phải là link video
No IP found Không resolve được IP Kiểm tra DNS, dùng Google DNS (8.8.8.8)

---

📁 CẤU TRÚC THƯ MỤC

```
C:\TikTokBot\
│
├── bot.py                      # File code chính
├── run.bat                     # File chạy bot
├── requirements.txt            # Danh sách thư viện
├── proxies.txt                 # Proxy (tùy chọn)
├── view_log.txt                # Log view đã gửi
└── README.md                   # File hướng dẫn này
```

---

🔒 LƯU Ý QUAN TRỌNG

⚠️ View ảo chỉ có tác dụng trong 24-48 giờ - TikTok sẽ lọc view bất thường

⚠️ Không dùng cho mục đích thương mại - Vi phạm ToS của TikTok

⚠️ Sử dụng với tần suất hợp lý - Chạy quá nhiều có thể bị khóa IP

⚠️ Tốc độ view không được công nhận - View ảo không tăng tương tác thực tế

---

👨‍💻 TÁC GIẢ

NGLONG DEV

Kênh Link
GitHub github.com/nguyenlongstore
Tiktok tiktok.com/@nguyenlongsupport.store

---

📜 LICENSE

MIT License - Sử dụng miễn phí cho mục đích học tập và nghiên cứu.

---

📢 TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM

Công cụ này chỉ dành cho mục đích học tập và nghiên cứu.

Tác giả (NGLONG DEV) không chịu trách nhiệm về bất kỳ hậu quả nào phát sinh từ việc sử dụng công cụ này. Bạn sử dụng hoàn toàn với rủi ro của riêng mình.

---

© 2026 NGLONG DEV - Made with ❤️ for the community

```
NGUYENLONG LOVE YOU
```
