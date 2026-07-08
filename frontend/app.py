import streamlit as st
import httpx
import uuid

# Cấu hình hiển thị trang Streamlit
st.set_page_config(
    page_title="BankBot - Trợ lý tài chính thông minh",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS nâng cấp giao diện thành Premium
st.markdown("""
<style>
    /* Nhúng và cài đặt Font chữ Outfit */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Hiệu ứng màu Gradient cho Tiêu đề */
    .gradient-text {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 50%, #60A5FA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2.8rem;
        margin-bottom: 0.2rem;
    }
    
    /* Phông phụ đề */
    .subtitle-text {
        color: #4B5563;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Thiết kế thẻ Card cho sidebar */
    .feature-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #E2E8F0;
        margin-bottom: 0.8rem;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
    }
    
    /* Trạng thái kết nối API */
    .api-status-online {
        display: inline-block;
        background-color: #DEF7EC;
        color: #03543F;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .api-status-offline {
        display: inline-block;
        background-color: #FDE8E8;
        color: #9B1C1C;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Cổng mặc định của API Backend
API_URL = "http://localhost:8000"

# Bản đồ ánh xạ tên công cụ sang tên thân thiện trực quan
TOOL_NAMES_MAP = {
    "search_bank_faq": "🔍 Tra cứu FAQ",
    "calculator_loan": "🧮 Tính lãi vay",
    "calculator_savings_interest": "💰 Tính lãi tiết kiệm",
    "get_exchange_rate": "💱 Tra cứu tỷ giá"
}

def display_used_tools(tools: list[str]):
    if not tools:
        return
    # Chuyển đổi sang tên tiếng Việt dễ hiểu
    friendly_names = [TOOL_NAMES_MAP.get(t, f"🛠️ {t}") for t in tools]
    tools_html = "".join([
        f'<span style="background-color: #EFF6FF; color: #1E40AF; border: 1px solid #BFDBFE; padding: 0.2rem 0.5rem; border-radius: 6px; font-size: 0.8rem; font-weight: 500; margin-right: 0.5rem;">{name}</span>'
        for name in friendly_names
    ])
    st.markdown(f"<div style='margin-top: 0.5rem; display: flex; align-items: center;'><span style='font-size: 0.85rem; color: #6B7280; margin-right: 0.5rem;'>🛠️ Công cụ đã dùng:</span>{tools_html}</div>", unsafe_allow_html=True)

# Khởi tạo các giá trị mặc định cho Session State
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

# Kiểm tra tình trạng kết nối tới API Backend
api_online = False
try:
    response = httpx.get(f"{API_URL}/health", timeout=2.0)
    if response.status_code == 200:
        api_online = True
except Exception:
    pass

# === SIDEBAR ===
with st.sidebar:
    st.markdown("<div style='text-align: center; margin-top: 1rem;'><span style='font-size: 4rem;'>🏦</span></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #1E3A8A; margin-top: 0px;'>BankBot System</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6B7280; font-size: 0.9rem;'>Hệ thống Trợ lý Tài chính Agentic AI</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Kết nối hệ thống")
    if api_online:
        st.markdown('<span class="api-status-online">● Backend Online (Port 8000)</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="api-status-offline">● Backend Offline</span>', unsafe_allow_html=True)
        st.warning("Vui lòng khởi động API Backend ở cổng 8000 trước khi gửi tin nhắn.")

    st.markdown("---")
    st.markdown("### Công cụ của Agent")
    st.markdown("""
    <div class="feature-card">
        <strong>🔍 Tra cứu FAQ</strong><br>
        <span style="font-size: 0.85rem; color: #4B5563;">Truy vấn thông tin thẻ, tiết kiệm, vay từ Vector DB.</span>
    </div>
    <div class="feature-card">
        <strong>🧮 Tính lãi vay</strong><br>
        <span style="font-size: 0.85rem; color: #4B5563;">Tính toán gốc và lãi hàng tháng theo dư nợ giảm dần hoặc trả đều.</span>
    </div>
    <div class="feature-card">
        <strong>💱 Tỷ giá ngoại tệ</strong><br>
        <span style="font-size: 0.85rem; color: #4B5563;">Tra cứu tỷ giá hối đoái ngoại tệ thời gian thực.</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🔄 Làm mới cuộc trò chuyện", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

# === CHƯƠNG TRÌNH CHÍNH ===
st.markdown('<h1 class="gradient-text">BankBot 🏦</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Trợ lý ảo ngân hàng thông minh hỗ trợ giải đáp FAQ, tính lãi vay và cập nhật tỷ giá.</p>', unsafe_allow_html=True)

# Hiển thị lịch sử chat đã có
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("used_tools"):
            display_used_tools(msg["used_tools"])

# Danh sách gợi ý câu hỏi nhanh cho người dùng mới
suggested_questions = [
    "Điều kiện mở thẻ tín dụng là gì?",
    "Tính lãi vay 500 triệu lãi suất 8.5% trong 10 năm",
    "Tỷ giá USD hôm nay thế nào?"
]

# Hiển thị gợi ý nếu lịch sử chat trống
if len(st.session_state.messages) == 0:
    st.markdown("### 💡 Câu hỏi gợi ý:")
    cols = st.columns(len(suggested_questions))
    for idx, question in enumerate(suggested_questions):
        with cols[idx]:
            if st.button(question, key=f"sugg_{idx}", use_container_width=True):
                # Thêm vào UI
                st.session_state.messages.append({"role": "user", "content": question})
                
                # Gọi API backend
                with st.spinner("BankBot đang suy nghĩ..."):
                    try:
                        res = httpx.post(
                            f"{API_URL}/chat",
                            json={"message": question, "session_id": st.session_state.session_id},
                            timeout=30.0
                        )
                        if res.status_code == 200:
                            reply = res.json().get("reply", "Không có phản hồi.")
                            used_tools = res.json().get("used_tools", [])
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": reply,
                                "used_tools": used_tools
                            })
                        else:
                            st.session_state.messages.append({"role": "assistant", "content": "❌ Đã xảy ra lỗi từ phía máy chủ."})
                    except Exception as e:
                        st.session_state.messages.append({"role": "assistant", "content": f"❌ Không thể kết nối với Backend API. Chi tiết: {str(e)}"})
                st.rerun()

# Nhập tin nhắn từ khung chat chính
user_input = st.chat_input("Nhập câu hỏi của bạn tại đây...")

if user_input:
    # Hiển thị tin nhắn người dùng ngay lập tức
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
        
    # Gọi API và hiển thị câu trả lời của AI
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("BankBot đang suy nghĩ..."):
            try:
                res = httpx.post(
                    f"{API_URL}/chat",
                    json={"message": user_input, "session_id": st.session_state.session_id},
                    timeout=30.0
                )
                if res.status_code == 200:
                    reply = res.json().get("reply", "Không có phản hồi.")
                    used_tools = res.json().get("used_tools", [])
                    message_placeholder.write(reply)
                    display_used_tools(used_tools)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": reply,
                        "used_tools": used_tools
                    })
                else:
                    err_msg = "❌ Đã xảy ra lỗi kết nối hoặc xử lý từ server."
                    message_placeholder.write(err_msg)
                    st.session_state.messages.append({"role": "assistant", "content": err_msg})
            except Exception as e:
                err_msg = f"❌ Không thể kết nối tới Backend API. Lỗi: {str(e)}"
                message_placeholder.write(err_msg)
                st.session_state.messages.append({"role": "assistant", "content": err_msg})
