# TH3 - Lập trình IoT với giao thức CoAP

## 1. Thông tin sinh viên / nhóm thực hiện

| STT | Họ và tên | Mã sinh viên | Lớp | Bài làm |
|---:|---|---|---|---|
| 1 | Đỗ Thị Thu Huế | ... | N8 | Bài 1 |
| 2 | Đào Hà My | B23DCCN571 | N8 | Bài 2 |
| 3 | Cao Thị Thanh Nhàn | B23DCCN618 | N8 | Bài 3 |

## 2. Môi trường và thư viện sử dụng

- **Hệ điều hành:** Windows
- **Ngôn ngữ lập trình:** Python
- **Phiên bản Python:** ...
- **Giao thức truyền thông:** CoAP
- **Các thư viện sử dụng:**
  - `aiocoap`: Xây dựng CoAP server, CoAP client và trao đổi dữ liệu qua giao thức CoAP.
  - `asyncio`: Hỗ trợ lập trình bất đồng bộ, cho phép cập nhật dữ liệu cảm biến và xử lý các yêu cầu mạng.

## 3. Cách cài đặt môi trường

Mở terminal tại thư mục gốc của dự án.

### Bước 1: Kiểm tra Python

```powershell
python --version
```

### Bước 2: Tạo môi trường ảo

```powershell
python -m venv .venv
```

### Bước 3: Kích hoạt môi trường ảo

```powershell
.\.venv\Scripts\Activate.ps1
```

### Bước 4: Cài đặt thư viện

```powershell
python -m pip install aiocoap
```

## 4. Cách chạy từng bài

### Bài 1

### Bài 2. Xây dựng hệ thống giám sát cảm biến sử dụng CoAP

Bài 2 gồm hai chương trình: CoAP Server mô phỏng cảm biến và Monitoring CoAP Client thu thập, hiển thị dữ liệu cảm biến.

**a. Chạy Sensor CoAP Server**

Mở terminal thứ nhất tại thư mục gốc của dự án và kích hoạt môi trường ảo nếu chưa kích hoạt.

Chạy lệnh:

```powershell
python -m bai2.sensor_server_bai2
```

Server khởi chạy và cung cấp tài nguyên cảm biến để client truy cập. Dữ liệu nhiệt độ và độ ẩm được cập nhật định kỳ 3 giây một lần.

**b. Chạy Monitoring CoAP Client**

Mở terminal thứ hai tại thư mục gốc của dự án và kích hoạt cùng môi trường ảo.

Chạy lệnh:

```powershell
python -m bai2.monitor_client_bai2
```

Client gửi yêu cầu GET đến CoAP Server định kỳ, nhận dữ liệu cảm biến và hiển thị các thông tin sau:

- Mã thiết bị cảm biến.
- Nhiệt độ và độ ẩm.
- Thời điểm nhận dữ liệu.
- Cảnh báo nếu nhiệt độ lớn hơn 35 °C hoặc độ ẩm nhỏ hơn 40%.

Chương trình tiếp tục giám sát cho đến khi người dùng nhấn `Ctrl + C`. Nếu không nhận được dữ liệu, client hiển thị thông báo lỗi và thử gửi yêu cầu lại sau 3 giây.

### Bài 3. Mô phỏng hệ thống giám sát và điều khiển đèn thông minh bằng CoAP Observe

Mô hình gồm ba chương trình: Server quản lý trạng thái thiết bị, Controller gửi lệnh GET/PUT, và Monitor nhận cập nhật bằng CoAP Observe. Server mô phỏng `light01`, `fan01`, `pump01`; mỗi thiết bị có trạng thái riêng, khởi tạo là `OFF`.

**Chạy chương trình**

Mở ba terminal tại thư mục `TH3-IOT`. Trong mỗi terminal, kích hoạt môi trường ảo nếu chưa kích hoạt:

```powershell
.\.venv\Scripts\Activate.ps1
```

Chạy mỗi lệnh trong một terminal riêng:

```powershell
python -m bai3.light_server_bai3
```
```powershell
python -m bai3.light_controller_bai3
```
```powershell
python -m bai3.light_monitor_bai3
```

Controller mặc định chọn `light01`. Nhập từng lệnh rồi nhấn Enter; ví dụ sau chọn quạt, bật, kiểm tra trạng thái rồi tắt:

```text
DEVICE fan01
ON
STATUS
OFF
EXIT
```

`DEVICE <id>` chọn thiết bị; `ON`/`OFF` điều khiển thiết bị đang chọn; `STATUS` đọc trạng thái; `EXIT` thoát. Nếu nhập lệnh khác, chẳng hạn `a`, Controller gửi lệnh để Server trả mã lỗi CoAP.

Monitor mặc định theo dõi cả ba thiết bị nên thay đổi ở `fan01` hoặc `pump01` cũng được hiển thị. Có thể giới hạn thiết bị cần theo dõi:

```powershell
python -m bai3.light_monitor_bai3 fan01
```
```powershell
python -m bai3.light_monitor_bai3 light01 fan01
```

Mở thêm terminal và chạy Monitor lần nữa để có nhiều client Observe cùng theo dõi. Mỗi Monitor hiển thị trạng thái ban đầu và các cập nhật, không polling GET. Nhấn `Ctrl+C` để dừng Monitor hoặc Server.

## 5. Địa chỉ IP, cổng và URI tài nguyên CoAP

### Bài 1

### Bài 2
| Thông tin | Giá trị |
|---|---|
| Địa chỉ IP Server | `127.0.0.1` |
| Giao thức | CoAP |
| Cổng | `5683` |
| Mã thiết bị | `sensor01` |
| Phương thức truy cập | `GET` |
| URI tài nguyên | `coap://127.0.0.1:5683/iot/lab/sensor01/data` |
| Định dạng dữ liệu trả về | JSON |
| Chu kỳ cập nhật dữ liệu cảm biến | 3 giây |

Server sử dụng địa chỉ loopback `127.0.0.1`, do đó client được chạy trên cùng máy tính. Tài nguyên cảm biến trả về dữ liệu JSON bao gồm mã thiết bị, nhiệt độ và độ ẩm.

Ví dụ dữ liệu trả về:

```json
{
  "device_id": "sensor01",
  "temperature": 32.5,
  "humidity": 55.2
}
```

Các giá trị trên chỉ mang tính minh họa; dữ liệu thực tế được tạo ngẫu nhiên và thay đổi theo từng lần cập nhật.

### Bài 3

| Thông tin | Giá trị |
|---|---|
| Địa chỉ / giao thức | `localhost` (`127.0.0.1`), CoAP qua UDP cổng `5683` |
| Thiết bị | `light01`, `fan01`, `pump01` |
| URI | `coap://localhost:5683/iot/lab/<device_id>/status` |
| GET / PUT / Observe | Đọc trạng thái / điều khiển / nhận thông báo khi trạng thái đổi |

Payload PUT có dạng `{"device_id":"fan01","command":"ON"}`; trạng thái trả về có dạng `{"device_id":"fan01","status":"ON"}`. Thay `fan01` bằng mã thiết bị tương ứng. Khi chạy trên máy khác, thay `localhost` bằng IP Server và mở UDP `5683` trên tường lửa.

## 6. Kết quả đạt được

### Bài 1

### Bài 2

- Xây dựng thành công CoAP Server cung cấp dữ liệu cảm biến thông qua tài nguyên `/iot/lab/sensor01/data`.
- Mô phỏng dữ liệu nhiệt độ và độ ẩm, tự động cập nhật sau mỗi 3 giây.
- Xây dựng Monitoring CoAP Client sử dụng phương thức GET để truy vấn dữ liệu từ server.
- Hiển thị thông tin cảm biến và thời điểm nhận dữ liệu trên terminal.
- Phát hiện và hiển thị cảnh báo khi nhiệt độ vượt ngưỡng 35 °C hoặc độ ẩm thấp hơn 40%.
- Xử lý trường hợp truy vấn thất bại.

### Bài 3

- Xây dựng Server quản lý riêng ba thiết bị `light01`, `fan01`, `pump01`; mỗi thiết bị có trạng thái ban đầu `OFF` và URI CoAP riêng.
- Controller dùng GET để đọc trạng thái, PUT để bật/tắt thiết bị và cho phép chuyển thiết bị bằng `DEVICE <id>`.
- Lệnh điều khiển hợp lệ nhận `2.04 Da cap nhat`; GET thành công nhận `2.05 Noi dung`. Lệnh hoặc payload không hợp lệ bị Server từ chối với `4.00 Yeu cau khong hop le`.
- Monitor đăng ký CoAP Observe cho các thiết bị, hiển thị trạng thái ban đầu và tự nhận cập nhật từ Server khi trạng thái đổi; không truy vấn GET định kỳ.
- Nhiều Monitor có thể cùng theo dõi một thiết bị. Cập nhật của một thiết bị không làm thay đổi trạng thái các thiết bị khác.

**Ví dụ kết quả chạy**

Terminal Server:

```text
CoAP Server da khoi dong.
Thiet bi mo phong: light01, fan01, pump01
Co Monitor dang ky theo doi fan01
Nhan lenh PUT: thiet bi=fan01, lenh=ON
Trang thai fan01 thay doi: OFF -> ON
Da gui thong bao Observe: ON
Nhan lenh PUT: thiet bi=fan01, lenh=OFF
Trang thai fan01 thay doi: ON -> OFF
Da gui thong bao Observe: OFF
```

Terminal Controller:

```text
[light01] Nhap lenh: DEVICE fan01
Da chon thiet bi fan01
[fan01] Nhap lenh: ON
Ma phan hoi CoAP: 2.04 Da cap nhat
Da bat den thiet bi fan01
[fan01] Nhap lenh: STATUS
Ma phan hoi CoAP: 2.05 Noi dung
Du lieu: {"device_id":"fan01","status":"ON"}
[fan01] Nhap lenh: a
Ma phan hoi CoAP: 4.00 Yeu cau khong hop le
Thong tin: Lenh khong hop le. Chi chap nhan ON hoac OFF.
```

Terminal Monitor:

```text
Monitor se theo doi: light01, fan01, pump01
[16:45:12] Trang thai ban dau
Thiet bi: fan01
Trang thai: OFF
[16:46:06] Trang thai vua cap nhat
Thiet bi: fan01
Trang thai: ON
[16:46:38] Trang thai vua cap nhat
Thiet bi: fan01
Trang thai: OFF
```
