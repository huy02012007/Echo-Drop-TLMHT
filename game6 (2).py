"""
ECHO DROP - GAME SINH TỒN SỬ DỤNG SONAR
----------------------------------------
Nhóm thực hiện: TTLMHT

Mô tả:
    Người chơi điều khiển nhân vật rơi tự do trong hang động tối tăm.
    Sử dụng Sonar (Sóng âm) để phát hiện các bệ đỡ vô hình.
    Mục tiêu là sống sót càng lâu càng tốt để đạt điểm cao.
"""

import turtle
import random
import time

# =============================================================================
# 1. CẤU HÌNH HẰNG SỐ (CONSTANTS)
# =============================================================================

# --- Cấu hình Màn hình & Màu sắc ---
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
COLOR_BG = "black"
COLOR_PLAYER = "white"
COLOR_PLATFORM_VISIBLE = "white"
COLOR_PLATFORM_HIDDEN = "black"
COLOR_TEXT = "white"
COLOR_GAME_OVER = "red"
COLOR_SONAR_READY = "#00FF00"  # Màu xanh lá (Sẵn sàng)
COLOR_SONAR_WAIT = "#FF4500"  # Màu cam đỏ (Đang hồi chiêu)

# --- Cấu hình Vật lý & Hiệu năng ---
GRAVITY = 0.06  # Lực hút trái đất (Gia tốc rơi)
FPS_LIMIT = 0.017  # Giới hạn thời gian mỗi khung hình (~60 FPS)

# --- Cấu hình Độ khó (Game Balance) ---
# base_speed: Tốc độ ban đầu của bệ đỡ
# acceleration: Tốc độ game tăng thêm sau mỗi điểm ghi được
# sonar_visible_time: Thời gian hiển thị sóng âm
# sonar_cooldown: Thời gian hồi chiêu giữa 2 lần sử dụng
# platform_width: Độ dài thanh ngang (Hệ số stretch_len của Turtle)
# platform_count: Số lượng thanh ngang xuất hiện cùng lúc
DIFFICULTY_CONFIG = {
    "EASY": {
        "name": "DỄ",
        "base_speed": 1.0,
        "acceleration": 0.02,
        "sonar_visible_time": 3.0,
        "sonar_cooldown": 3.0,
        "platform_width": 6,
        "platform_count": 6,
    },
    "NORMAL": {
        "name": "VỪA",
        "base_speed": 1.5,
        "acceleration": 0.05,
        "sonar_visible_time": 2.0,
        "sonar_cooldown": 4.0,
        "platform_width": 5,
        "platform_count": 5,
    },
    "HARD": {
        "name": "KHÓ",
        "base_speed": 2.5,
        "acceleration": 0.1,
        "sonar_visible_time": 1.0,
        "sonar_cooldown": 5.0,
        "platform_width": 4,
        "platform_count": 4,
    },
}

# =============================================================================
# 2. KHỞI TẠO MÀN HÌNH (SETUP)
# =============================================================================
wn = turtle.Screen()
wn.title("ECHO DROP - SONAR SURVIVAL")
wn.bgcolor(COLOR_BG)
wn.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
# Tắt chế độ vẽ tự động (tracer) để tối ưu hiệu năng và tự quản lý frame
wn.tracer(0)

# =============================================================================
# 3. KHỞI TẠO ĐỐI TƯỢNG (OBJECTS)
# =============================================================================

# --- Nhân vật (Player) ---
player = turtle.Turtle()
player.speed(0)
player.shape("square")
player.color(COLOR_PLAYER)
player.penup()
player.hideturtle()  # Chỉ hiện khi bắt đầu chơi
player.goto(0, 100)
player.dy = 0  # Vận tốc theo trục Y

# --- Sóng âm (Sonar) ---
sonar = turtle.Turtle()
sonar.speed(0)
sonar.shape("circle")
sonar.color(COLOR_PLAYER)
sonar.penup()
sonar.hideturtle()

# --- Bút vẽ UI (Giao diện chính) ---
pen_main = turtle.Turtle()
pen_main.speed(0)
pen_main.color(COLOR_TEXT)
pen_main.penup()
pen_main.hideturtle()

# --- Bút vẽ HUD (Thông số trong game) ---
pen_hud = turtle.Turtle()
pen_hud.speed(0)
pen_hud.color(COLOR_TEXT)
pen_hud.penup()
pen_hud.hideturtle()

# --- Danh sách Bệ đỡ ---
# Sẽ được khởi tạo động trong hàm setup_platforms()
platforms = []

# =============================================================================
# 4. QUẢN LÝ TRẠNG THÁI GAME (STATE MANAGEMENT)
# =============================================================================

game_state = "MENU"  # Các trạng thái: "MENU", "PLAYING", "GAME_OVER"

# Biến toàn cục lưu trữ thông số game hiện tại
score = 0
sonar_radius = 0
sonar_active = False
last_sonar_time = -100  # Đặt giá trị âm để có thể dùng Sonar ngay khi vào game
current_difficulty = DIFFICULTY_CONFIG["EASY"]

# =============================================================================
# 5. CÁC HÀM XỬ LÝ LOGIC (FUNCTIONS)
# =============================================================================


def draw_menu():
    """Vẽ màn hình Menu chính: Tiêu đề, Hướng dẫn và Chọn độ khó."""
    pen_main.clear()

    # 1. Header (Tiêu đề & Tác giả)
    pen_main.goto(0, 160)
    pen_main.write("ECHO DROP", align="center", font=("Arial", 40, "bold"))

    pen_main.goto(0, 120)
    pen_main.write("Created by TTLMHT", align="center", font=("Arial", 20, "bold"))

    # 2. Hướng dẫn chơi
    pen_main.goto(0, 60)
    pen_main.write("HƯỚNG DẪN", align="center", font=("Arial", 18, "bold"))

    pen_main.goto(0, 20)
    pen_main.write(
        "←  → : Di chuyển Trái / Phải", align="center", font=("Arial", 16, "normal")
    )

    pen_main.goto(0, -10)
    pen_main.write(
        "Space : Kích hoạt Sonar", align="center", font=("Arial", 16, "normal")
    )

    pen_main.goto(0, -40)
    pen_main.write(
        "R : Quay về Menu / Chơi lại", align="center", font=("Arial", 16, "normal")
    )

    # 3. Menu chọn độ khó
    pen_main.goto(0, -90)
    pen_main.write(
        "CHỌN CHẾ ĐỘ ĐỂ BẮT ĐẦU:", align="center", font=("Arial", 16, "bold")
    )

    pen_main.goto(0, -130)
    pen_main.write("1. DỄ", align="center", font=("Arial", 14, "bold"))

    pen_main.goto(0, -160)
    pen_main.write("2. VỪA", align="center", font=("Arial", 14, "bold"))

    pen_main.goto(0, -190)
    pen_main.write("3. KHÓ", align="center", font=("Arial", 14, "bold"))


def setup_platforms(difficulty_config):
    """
    Khởi tạo lại danh sách bệ đỡ dựa trên cấu hình độ khó.
    Args:
        difficulty_config (dict): Dictionary chứa thông số độ khó.
    """
    global platforms

    # Xóa các đối tượng cũ để tránh rò rỉ bộ nhớ hoặc lỗi hiển thị
    for p in platforms:
        p.hideturtle()
        p.clear()
    platforms.clear()

    count = difficulty_config["platform_count"]
    width = difficulty_config["platform_width"]

    # Tạo các đối tượng bệ đỡ mới (Object Pooling)
    for i in range(count):
        plat = turtle.Turtle()
        plat.speed(0)
        plat.shape("square")
        plat.color(COLOR_PLATFORM_HIDDEN)
        plat.shapesize(stretch_wid=0.5, stretch_len=width)
        plat.penup()
        plat.is_visible = False
        plat.fade_timer = 0
        plat.hideturtle()
        platforms.append(plat)


def start_game(difficulty_key):
    """Thiết lập thông số và bắt đầu vòng chơi mới."""
    global game_state, score, sonar_active, last_sonar_time, current_difficulty, player

    if game_state == "PLAYING":
        return

    # Cập nhật độ khó và tạo lại màn chơi
    current_difficulty = DIFFICULTY_CONFIG[difficulty_key]
    setup_platforms(current_difficulty)

    # Reset trạng thái Game
    game_state = "PLAYING"
    score = 0
    sonar_active = False
    last_sonar_time = time.time() - current_difficulty["sonar_cooldown"]

    pen_main.clear()

    # Reset vị trí Nhân vật
    player.showturtle()
    player.goto(0, 100)
    player.dy = 0
    player.color(COLOR_PLAYER)

    # Rải bệ đỡ ngẫu nhiên
    vertical_gap = int(700 / current_difficulty["platform_count"])
    for i, p in enumerate(platforms):
        p.showturtle()
        y_pos = -250 + i * vertical_gap
        x_pos = random.randint(-200, 200)
        p.goto(x_pos, y_pos)
        p.is_visible = False
        p.color(COLOR_PLATFORM_HIDDEN)

    update_hud()


def update_hud():
    """Cập nhật hiển thị Điểm số và Trạng thái hồi chiêu Sonar."""
    pen_hud.clear()

    # Hiển thị Điểm
    pen_hud.goto(-230, 260)
    pen_hud.color(COLOR_TEXT)
    pen_hud.write(f"ĐIỂM: {score}", align="left", font=("Arial", 12, "bold"))

    # Hiển thị Sonar
    pen_hud.goto(230, 260)
    current_time = time.time()
    time_passed = current_time - last_sonar_time
    cooldown = current_difficulty["sonar_cooldown"]

    if sonar_active:
        pen_hud.color(COLOR_SONAR_WAIT)
        pen_hud.write("SONAR: ĐANG QUÉT...", align="right", font=("Arial", 12, "bold"))
    elif time_passed < cooldown:
        time_left = cooldown - time_passed
        pen_hud.color(COLOR_SONAR_WAIT)
        pen_hud.write(
            f"HỒI CHIÊU: {time_left:.1f}s", align="right", font=("Arial", 12, "bold")
        )
    else:
        pen_hud.color(COLOR_SONAR_READY)
        pen_hud.write(
            "SONAR SẴN SÀNG (SPACE)", align="right", font=("Arial", 12, "bold")
        )


def move_left():
    """Di chuyển nhân vật sang trái (có kiểm tra biên)."""
    if game_state == "PLAYING":
        x = player.xcor()
        if x > -230:
            player.setx(x - 20)


def move_right():
    """Di chuyển nhân vật sang phải (có kiểm tra biên)."""
    if game_state == "PLAYING":
        x = player.xcor()
        if x < 230:
            player.setx(x + 20)


def trigger_sonar():
    """Kích hoạt kỹ năng Sonar nếu đã hồi chiêu xong."""
    global sonar_active, sonar_radius, last_sonar_time

    if game_state != "PLAYING":
        return

    current_time = time.time()
    cooldown = current_difficulty["sonar_cooldown"]
    visible_time = current_difficulty["sonar_visible_time"]

    # Kiểm tra điều kiện kích hoạt
    if not sonar_active and (current_time - last_sonar_time > cooldown):
        sonar.goto(player.xcor(), player.ycor())
        sonar.showturtle()
        sonar_radius = 1
        sonar_active = True
        last_sonar_time = current_time

        # Tính toán thời gian bệ đỡ hiện hình (quy đổi ra số frame)
        fade_frames = int(visible_time / FPS_LIMIT)

        for p in platforms:
            p.is_visible = True
            p.fade_timer = fade_frames


def update_physics():
    """Xử lý vật lý: Trọng lực và Va chạm."""
    global game_state

    # Áp dụng trọng lực (Rơi tự do)
    player.dy -= GRAVITY
    player.sety(player.ycor() + player.dy)

    # Tính toán vùng va chạm (Hitbox) dựa trên độ rộng bệ đỡ
    current_width_len = current_difficulty["platform_width"]
    hitbox_x = current_width_len * 10  # Hệ số 10px cho mỗi đơn vị width

    # Kiểm tra va chạm với từng bệ đỡ
    for p in platforms:
        if (
            player.dy < 0  # Chỉ va chạm khi đang rơi xuống
            and p.ycor() + 10
            <= player.ycor()
            <= p.ycor() + 30  # Va chạm theo chiều dọc
            and p.xcor() - hitbox_x
            < player.xcor()
            < p.xcor() + hitbox_x  # Va chạm theo chiều ngang
        ):
            player.dy = 0
            player.sety(p.ycor() + 20)

    # Điều kiện thua: Rơi khỏi màn hình
    if player.ycor() < -300:
        game_over_process()


def get_current_platform_speed():
    """Tính toán tốc độ trôi của bệ đỡ (Tăng dần theo điểm số)."""
    base = current_difficulty["base_speed"]
    accel = current_difficulty["acceleration"]
    return base + (score * accel)


def update_platforms():
    """Cập nhật vị trí và trạng thái hiển thị của các bệ đỡ."""
    global score
    speed = get_current_platform_speed()

    for p in platforms:
        p.sety(p.ycor() + speed)

        # Xử lý hiệu ứng tàng hình/hiện hình
        if p.is_visible:
            p.color(COLOR_PLATFORM_VISIBLE)
            p.fade_timer -= 1
            if p.fade_timer <= 0:
                p.is_visible = False
        else:
            p.color(COLOR_PLATFORM_HIDDEN)

        # Tái tạo bệ đỡ khi trôi lên quá cao
        if p.ycor() > 320:
            p.goto(random.randint(-200, 200), -320)
            p.is_visible = False
            score += 1


def update_sonar_effect():
    """Xử lý hiệu ứng hình ảnh sóng âm lan tỏa."""
    global sonar_active, sonar_radius
    if sonar_active:
        sonar_radius += 10
        sonar.shapesize(stretch_wid=sonar_radius, stretch_len=sonar_radius)
        if sonar_radius > 100:  # Giới hạn kích thước tối đa
            sonar.hideturtle()
            sonar_active = False


def game_over_process():
    """Xử lý khi người chơi thua cuộc."""
    global game_state
    game_state = "GAME_OVER"
    player.color(COLOR_GAME_OVER)

    # Ẩn bệ đỡ để làm sạch màn hình
    for p in platforms:
        p.hideturtle()

    pen_main.goto(0, 0)
    pen_main.color(COLOR_GAME_OVER)
    pen_main.write("GAME OVER", align="center", font=("Arial", 30, "bold"))

    pen_main.goto(0, -40)
    pen_main.color("white")
    pen_main.write(f"Điểm số: {score}", align="center", font=("Arial", 20, "bold"))

    pen_main.goto(0, -80)
    pen_main.write("Nhấn 'R' để về Menu", align="center", font=("Arial", 16, "normal"))


def return_to_menu():
    """Quay về màn hình chính."""
    global game_state
    if game_state == "GAME_OVER" or game_state == "PLAYING":
        game_state = "MENU"

        # Dọn dẹp màn hình
        player.hideturtle()
        for p in platforms:
            p.hideturtle()
        sonar.hideturtle()
        pen_hud.clear()

        draw_menu()


# Các hàm wrapper để gán phím tắt
def select_easy():
    if game_state == "MENU":
        start_game("EASY")


def select_normal():
    if game_state == "MENU":
        start_game("NORMAL")


def select_hard():
    if game_state == "MENU":
        start_game("HARD")


# =============================================================================
# 6. THIẾT LẬP PHÍM BẤM & VÒNG LẶP CHÍNH (MAIN LOOP)
# =============================================================================

wn.listen()
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")
wn.onkeypress(trigger_sonar, "space")

wn.onkeypress(select_easy, "1")
wn.onkeypress(select_normal, "2")
wn.onkeypress(select_hard, "3")

wn.onkeypress(return_to_menu, "r")
wn.onkeypress(return_to_menu, "R")

# Khởi chạy Menu lần đầu
draw_menu()

# Vòng lặp game chính
while True:
    wn.update()

    if game_state == "PLAYING":
        update_physics()
        update_platforms()
        update_sonar_effect()
        update_hud()

    # Giới hạn FPS để game chạy ổn định
    time.sleep(FPS_LIMIT)
