
# 🦇 ECHO DROP - SONAR SURVIVAL

> **Dự án nhập môn ngành - Game sinh tồn sử dụng sóng âm.**

---

## 🎮 Giới thiệu
**Echo Drop** là một tựa game sinh tồn đi cảnh (platformer) với cơ chế vật lý rơi tự do.

Điểm đặc biệt của game là môi trường hoàn toàn tối đen. Người chơi phải sử dụng cơ chế **"Sonar" (Sóng âm)** để quét và định vị các bệ đỡ vô hình trong thời gian ngắn nhằm tiếp đất an toàn.

Game được xây dựng hoàn toàn bằng **Python thuần** và thư viện đồ họa **Turtle**.

---

## 🛠 Yêu cầu hệ thống
Dự án được tối ưu để chạy ngay lập tức mà không cần cài đặt phức tạp.

* **Ngôn ngữ:** Python 3.x (Khuyên dùng 3.10 trở lên)
* **Thư viện:** Chỉ sử dụng thư viện chuẩn (Standard Libraries):
    * `turtle`
    * `random`
    * `time`

❌ **Không cần cài đặt thêm thư viện ngoài (No pip install needed).**

---

## 🚀 Hướng dẫn cài đặt & Chạy game

Bạn có thể chọn 1 trong 2 cách dưới đây để trải nghiệm game:

### Cách 1: Chạy file Game trực tiếp (Khuyên dùng)
Đây là cách nhanh nhất, không cần cài đặt Python.

1.  Truy cập mục **Releases** ở bên phải giao diện GitHub (hoặc kéo xuống dưới).
2.  Tải file nén `.zip` (hoặc `.exe`) của phiên bản mới nhất về máy.
3.  **Quan trọng:** Giải nén toàn bộ thư mục ra (nếu là file zip).
4.  Chạy file `Echo.Drop.exe` để chơi ngay!

---

### Cách 2: Chạy bằng Mã nguồn (Source Code)
Dành cho việc tham khảo code hoặc phát triển thêm.

**1. Yêu cầu:**
* Máy tính đã cài **Python 3.x**.
* Thư viện: Sử dụng thư viện chuẩn (`turtle`, `random`, `time`) nên **KHÔNG cần cài thêm gì cả** (No pip install required).

**2. Các bước thực hiện:**

* **Bước 1:** Tải mã nguồn về và giải nén.
* **Bước 2:** Mở thư mục chứa file `main.py`.
* **Bước 3:** Tại thanh địa chỉ thư mục, gõ `cmd` và nhấn Enter để mở Terminal.
* **Bước 4:** Gõ lệnh sau để chạy:

```bash
python main.py
```


## 🕹️ Hướng dẫn điều khiển

| Phím bấm | Chức năng |
| :---: | :--- |
| `⬅️` / `➡️` | Di chuyển nhân vật sang **Trái / Phải** |
| `Space` | **Kích hoạt Sonar** (Quét sóng âm để soi đường) |
| `R` | **Chơi lại** (Khi Game Over) hoặc Quay về Menu |
| `1`, `2`, `3` | Chọn độ khó (**Dễ / Vừa / Khó**) tại màn hình Menu |**Chọn độ khó (Dễ / Vừa / Khó) tại Menu**

## 🔥 Tính năng nổi bật (Technical Highlights)

Dự án áp dụng các kỹ thuật lập trình sau để tối ưu hiệu năng và trải nghiệm:

* **♻️ Object Pooling (Tối ưu bộ nhớ):**
    * Thay vì xóa và tạo mới liên tục (gây lag), game **tái sử dụng** các bệ đỡ khi chúng trôi khỏi màn hình.
    * Giúp game chạy mượt mà, ổn định.

* **⚛️ Physics & Collision (Vật lý & Va chạm):**
    * Tự xây dựng hệ thống **Trọng lực (Gravity)** và gia tốc rơi tự do mà không dùng engine có sẵn.
    * Xử lý vùng va chạm (Hitbox) chính xác giữa người chơi và bệ đỡ.

* **📈 Dynamic Difficulty (Độ khó động):**
    * Tốc độ rơi của bệ đỡ **tăng dần** theo điểm số người chơi.
    * Hệ thống **Cooldown (Hồi chiêu)** cho kỹ năng Sonar, buộc người chơi phải tính toán chiến thuật thay vì bấm phím liên tục.
