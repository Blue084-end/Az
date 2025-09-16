import streamlit as st
import matplotlib.pyplot as plt

# Khởi tạo session state để lưu kết quả
if "results" not in st.session_state:
    st.session_state.results = []

# Giao diện nhập dữ liệu
st.title("🃏 Baccarat Tracker")
st.markdown("Nhập kết quả từng ván: `B` = Banker, `P` = Player, `T` = Tie")

with st.form("input_form"):
    user_input = st.text_input("Nhập kết quả (B, P, T):", max_chars=1)
    submitted = st.form_submit_button("Thêm kết quả")
    if submitted:
        if user_input.upper() in ["B", "P", "T"]:
            st.session_state.results.append(user_input.upper())
        else:
            st.warning("Chỉ nhập B, P hoặc T thôi nhé!")

# Nút xóa kết quả
if st.button("🗑️ Xóa toàn bộ kết quả"):
    st.session_state.results = []

# Hiển thị danh sách kết quả đã nhập
st.subheader("📋 Kết quả đã nhập:")
if st.session_state.results:
    grid = [["" for _ in range((len(st.session_state.results) + 5) // 6)] for _ in range(6)]
    for i, r in enumerate(st.session_state.results):
        col = i // 6
        row = i % 6
        grid[row][col] = r
    for row in grid:
        st.write(" | ".join([r if r else " " for r in row]))
else:
    st.write("Chưa có kết quả nào.")

# Vẽ Bead Plate
def draw_bead_road(results):
    fig, ax = plt.subplots(figsize=(4.5, 4))
    colors = {"B": "red", "P": "blue", "T": "green"}
    for i, r in enumerate(results):
        x = (i // 6) * 0.6
        y = - (i % 6) * 0.6
        ax.scatter(x, y, color=colors[r], s=220)
        ax.text(x, y, r, ha='center', va='center', color='white', fontsize=12)
    ax.axis('off')
    st.subheader("📊 Bead Plate (Đường hạt)")
    st.pyplot(fig)

# Tạo Big Road từ kết quả
def generate_big_road(results):
    grid = []
    col = []
    last = None
    for r in results:
        if r == "T":
            continue
        if r == last:
            col.append(r)
        else:
            if col:
                grid.append(col)
            col = [r]
            last = r
    if col:
        grid.append(col)
    return grid

# Vẽ Big Road với khoảng cách hàng thu hẹp
def draw_big_road(big_road):
    fig, ax = plt.subplots(figsize=(6, 4))
    for x, col in enumerate(big_road):
        for y, r in enumerate(col):
            color = "red" if r == "B" else "blue"
            ax.scatter(x * 0.6, -y * 0.6, color=color, s=220)
            ax.text(x * 0.6, -y * 0.6, r, ha='center', va='center', color='white', fontsize=12)
    ax.axis('off')
    st.subheader("🔴 Big Road")
    st.pyplot(fig)

# Biểu đồ phụ: Big Eye Boy
def generate_big_eye_boy(big_road):
    result = []
    for col in range(1, len(big_road)):
        if len(big_road[col]) == len(big_road[col - 1]):
            result.append("red")
        else:
            result.append("blue")
    return result

# Biểu đồ phụ: Small Road
def generate_small_road(big_road):
    result = []
    for col in range(2, len(big_road)):
        if len(big_road[col]) == len(big_road[col - 2]):
            result.append("red")
        else:
            result.append("blue")
    return result

# Biểu đồ phụ: Cockroach Pig
def generate_cockroach_pig(big_road):
    result = []
    for col in range(3, len(big_road)):
        diff = abs(len(big_road[col]) - len(big_road[col - 3]))
        if diff == 0:
            result.append("red")
        elif diff == 1:
            result.append("blue")
        else:
            result.append("yellow")
    return result

# Vẽ biểu đồ phụ dạng lưới từ trên xuống dưới rồi sang phải
def draw_pattern_grid(title, colors, max_rows=6):
    fig, ax = plt.subplots(figsize=(4.5, 3.5))
    x, y = 0, 0
    for c in colors:
        ax.scatter(x * 0.5, -y * 0.6, color=c, s=220)
        y += 1
        if y >= max_rows:
            y = 0
            x += 1
    ax.axis('off')
    st.subheader(title)
    st.pyplot(fig)

# Hiển thị tất cả biểu đồ nếu có dữ liệu
if st.session_state.results:
    draw_bead_road(st.session_state.results)

    big_road = generate_big_road(st.session_state.results)
    draw_big_road(big_road)

    eye_boy = generate_big_eye_boy(big_road)
    small_road = generate_small_road(big_road)
    cockroach = generate_cockroach_pig(big_road)

    draw_pattern_grid("👁️ Big Eye Boy", eye_boy)
    draw_pattern_grid("🟥 Small Road", small_road)
    draw_pattern_grid("🪳 Cockroach Pig", cockroach)
