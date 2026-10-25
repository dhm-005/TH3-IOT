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

### Bài 3

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

## 6. Kết quả đạt được

### Bài 1

### Bài 2

- Xây dựng thành công CoAP Server cung cấp dữ liệu cảm biến thông qua tài nguyên `/iot/lab/sensor01/data`.
- Mô phỏng dữ liệu nhiệt độ và độ ẩm, tự động cập nhật sau mỗi 3 giây.
- Xây dựng Monitoring CoAP Client sử dụng phương thức GET để truy vấn dữ liệu từ server.
- Hiển thị thông tin cảm biến và thời điểm nhận dữ liệu trên terminal.
- Phát hiện và hiển thị cảnh báo khi nhiệt độ vượt ngưỡng 35 °C hoặc độ ẩm thấp hơn 40%.
- Xử lý trường hợp truy vấn thất bại.