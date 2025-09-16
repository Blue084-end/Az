import streamlit as st
import matplotlib.pyplot as plt

# Khởi tạo session state để lưu kết quả
if "results" not in st.session_state:
    st.session_state.results = []

# Giao diện nhập dữ liệu
st.title("🃏 Nhập kết quả Baccarat")
user_input = st.text_input("Nhập kết quả (B, P, T):", max_chars=1)

# Xử lý khi người dùng nhấn Enter
if user_input.upper() in ["B", "P", "T"]:
    st.session_state.results.append(user_input.upper())
    st.experimental_rerun()

# Hiển thị kết quả đã nhập
st.subheader("📋 Danh sách kết quả đã nhập:")
st.write(", ".join(st.session_state.results))

# Vẽ biểu đồ Bead Plate
def draw_bead_road(results):
    fig, ax = plt.subplots(figsize=(6, 4))
    colors = {"B": "red", "P": "blue", "T": "green"}
    for i, r in enumerate(results):
        x = i % 6
        y = -i // 6
        ax.scatter(x, y, color=colors[r], s=300)
        ax.text(x, y, r, ha='center', va='center', color='white', fontsize=12)
    ax.axis('off')
    st.pyplot(fig)

st.subheader("📊 Bead Plate (Đường hạt)")
draw_bead_road(st.session_state.results)
