import streamlit as st
import matplotlib.pyplot as plt

# Khởi tạo session state
if "results" not in st.session_state:
    st.session_state.results = []
if "predictions" not in st.session_state:
    st.session_state.predictions = []

# Giao diện nhập dữ liệu
st.title("🃏 Baccarat Tracker")
st.markdown("Nhập kết quả từng ván: `B` = Banker, `P` = Player, `T` = Tie")

with st.form("input_form"):
    user_input = st.text_input("Nhập kết quả (B, P, T):", max_chars=1)
    submitted = st.form_submit_button("Thêm kết quả")
    if submitted:
        if user_input.upper() in ["B", "P", "T"]:
            # Dự đoán trước khi thêm kết quả mới
            if st.session_state.results:
                pred, conf = predict_next(st.session_state.results)
                actual = user_input.upper()
                verdict = "D" if pred == actual else "S"
                st.session_state.predictions.append((pred, f"{conf}%", verdict))
            st.session_state.results.append(user_input.upper())
        else:
            st.warning("Chỉ nhập B, P hoặc T thôi nhé!")

# Nút xóa kết quả
if st.button("🗑️ Xóa toàn bộ kết quả"):
    st.session_state.results = []
    st.session_state.predictions = []

# Hàm dự đoán kết quả tiếp theo
def predict_next(results):
    b = results.count("B")
    p = results.count("P")
    t = results.count("T")
    total = b + p + t
    if total == 0:
        return "B", 50
    counts = {"B": b, "P": p, "T": t}
    prediction = max(counts, key=counts.get)
    confidence = int((counts[prediction] / total) * 100)
    return prediction, confidence

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

# Tạo Big Road
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

# Vẽ Big Road
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

# Biểu đồ phụ
def generate_big_eye_boy(big_road):
    return ["red" if len(big_road[i]) == len(big_road[i - 1]) else "blue" for i in range(1, len(big_road))]

def generate_small_road(big_road):
    return ["red" if len(big_road[i]) == len(big_road[i - 2]) else "blue" for i in range(2, len(big_road))]

def generate_cockroach_pig(big_road):
    result = []
    for i in range(3, len(big_road)):
        diff = abs(len(big_road[i]) - len(big_road[i - 3]))
        if diff == 0:
            result.append("red")
        elif diff == 1:
            result.append("blue")
        else:
            result.append("yellow")
    return result

# Vẽ biểu đồ dạng lưới
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

# Vẽ biểu đồ dự đoán
def draw_prediction_grid(predictions, max_rows=6):
    fig, ax = plt.subplots(figsize=(6, 4))
    x, y = 0, 0
    for pred, conf, verdict in predictions:
        for val in [pred, conf, verdict]:
            ax.text(x * 0.5, -y * 0.6, val, ha='center', va='center',
                    bbox=dict(boxstyle="circle", facecolor="lightgray"), fontsize=10)
            x += 1
        if x >= max_rows * 3:
            x = 0
            y += 1
    ax.axis('off')
    st.subheader("🔮 Dự đoán tiếp theo")
    st.pyplot(fig)

# Hiển thị tất cả biểu đồ
if st.session_state.results:
    draw_bead_road(st.session_state.results)

    big_road = generate_big_road(st.session_state.results)
    draw_big_road(big_road)

    draw_pattern_grid("👁️ Big Eye Boy", generate_big_eye_boy(big_road))
    draw_pattern_grid("🟥 Small Road", generate_small_road(big_road))
    draw_pattern_grid("🪳 Cockroach Pig", generate_cockroach_pig(big_road))

    if st.session_state.predictions:
        draw_prediction_grid(st.session_state.predictions)
