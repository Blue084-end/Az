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
    st.write(", ".join(st.session_state.results))
else:
    st.write("Chưa có kết quả nào.")

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

if st.session_state.results:
    st.subheader("📊 Bead Plate (Đường hạt)")
    draw_bead_road(st.session_state.results)
