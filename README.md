<![CDATA[<div align="center">

# 🏦 BankBot — Agentic AI

**Trợ lý ảo ngân hàng thông minh, xây dựng trên kiến trúc Agentic AI**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-1C3C3C?logo=langchain&logoColor=white)](https://langchain.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-ReAct_Agent-FF6F00)](https://langchain-ai.github.io/langgraph/)
[![Gemini](https://img.shields.io/badge/Google_Gemini-Flash-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-1.0-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://docker.com)

</div>

---

## 📖 Giới thiệu

**BankBot** là một chatbot hỗ trợ khách hàng ngân hàng, được xây dựng theo kiến trúc **Agentic AI** — nơi một Agent thông minh (LLM) có khả năng **tự suy luận** và **tự quyết định** sử dụng công cụ nào để trả lời câu hỏi của người dùng.

Thay vì chỉ đơn thuần tìm kiếm từ khoá, BankBot có thể:
- 🔍 **Tra cứu thông tin** sản phẩm ngân hàng từ cơ sở dữ liệu FAQ (bằng kỹ thuật RAG)
- 🧮 **Tính toán lãi vay** và **lãi tiết kiệm** chính xác bằng công thức tài chính
- 💱 **Tra cứu tỷ giá ngoại tệ** thời gian thực qua API

> **Đồ án môn học** — Trường Đại học Công nghiệp Hà Nội (HaUI)

---

## 🏗️ Kiến trúc hệ thống

```
┌──────────────────────────────────────────────────────────────────────┐
│                         NGƯỜI DÙNG (User)                            │
│                    Nhập câu hỏi bằng tiếng Việt                      │
└─────────────────────────────┬────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    🖥️ STREAMLIT FRONTEND                             │
│              Giao diện chat thân thiện (frontend/app.py)             │
└─────────────────────────────┬────────────────────────────────────────┘
                              │ HTTP POST /chat
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    ⚡ FASTAPI BACKEND                                │
│              REST API + Session Management (src/api/)                │
└─────────────────────────────┬────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│                  🧠 LANGGRAPH REACT AGENT                            │
│           Agent tự suy luận & chọn Tool (src/agent/)                 │
│                                                                      │
│    ┌─────────────┐    ┌────────────────┐    ┌──────────────────┐     │
│    │  🔍 RAG     │    │  🧮 Calculator │    │  💱 Exchange     │     │
│    │  Tool       │    │  Tool          │    │  Rate Tool       │     │
│    │             │    │                │    │                  │     │
│    │ Vector DB   │    │ Lãi vay &      │    │ API tỷ giá       │     │
│    │ ChromaDB    │    │ Lãi tiết kiệm  │    │ thời gian thực   │     │
│    └──────┬──────┘    └────────────────┘    └──────────────────┘     │
│           │                                                          │
│           ▼                                                          │
│    ┌─────────────┐                                                   │
│    │  📚 FAQ     │                                                   │
│    │  Data       │                                                   │
│    │  (data/raw) │                                                   │
│    └─────────────┘                                                   │
└──────────────────────────────────────────────────────────────────────┘
```

### Luồng xử lý (ReAct Loop)

1. **Người dùng** gửi câu hỏi qua giao diện Streamlit
2. **Frontend** gọi API `POST /chat` của FastAPI Backend
3. **Agent** (Gemini LLM + LangGraph) nhận câu hỏi, **suy luận** và quyết định gọi tool nào
4. **Tool** thực thi và trả kết quả cho Agent
5. **Agent** tổng hợp kết quả, **sinh câu trả lời** bằng tiếng Việt
6. **Kết quả** trả về Frontend hiển thị cho người dùng

---

## 🛠️ Công nghệ sử dụng

| Thành phần | Công nghệ | Mô tả |
|---|---|---|
| **LLM** | Google Gemini Flash | Mô hình ngôn ngữ lớn, miễn phí |
| **Agent Framework** | LangChain + LangGraph | Khung xây dựng Agent (ReAct pattern) |
| **Embedding** | Gemini Embedding | Vector hoá văn bản cho RAG |
| **Vector Database** | ChromaDB | Lưu trữ & truy vấn embedding vectors |
| **Backend API** | FastAPI + Uvicorn | REST API hiệu suất cao |
| **Frontend** | Streamlit | Giao diện chatbot tương tác |
| **Containerization** | Docker + Docker Compose | Đóng gói & triển khai ứng dụng |
| **Testing** | Pytest | Kiểm thử đơn vị (Unit Test) |
| **Ngôn ngữ** | Python 3.11 | Ngôn ngữ lập trình chính |

---

## ✨ Tính năng chính

### 🔍 Tra cứu FAQ ngân hàng (RAG)
Sử dụng kỹ thuật **Retrieval-Augmented Generation** để tìm kiếm thông tin chính xác từ cơ sở dữ liệu FAQ:
- Thẻ tín dụng (điều kiện mở, hạn mức, phí, lãi suất)
- Tiết kiệm (lãi suất, kỳ hạn, rút trước hạn)
- Vay vốn (vay mua nhà, tiêu dùng, điều kiện, hồ sơ)
- Thông tin chung (giờ làm việc, hotline, dịch vụ)

### 🧮 Tính toán lãi vay & tiết kiệm
- **Lãi vay trả góp:** Tính số tiền trả hàng tháng (gốc + lãi), tổng tiền trả và tổng lãi phải trả
- **Lãi tiết kiệm:** Tính tiền lãi nhận được cuối kỳ dựa trên số tiền gửi, lãi suất và kỳ hạn

### 💱 Tra cứu tỷ giá ngoại tệ
- Lấy tỷ giá thời gian thực từ API (USD, EUR, JPY, GBP, CNY, KRW...)
- Hiển thị giá mua vào và giá bán ra so với VND
- Có dữ liệu dự phòng khi không có kết nối mạng

---

## 🚀 Cài đặt & Chạy

### Yêu cầu hệ thống
- Python 3.11+
- Git
- (Tuỳ chọn) Docker & Docker Compose

### Cách 1: Chạy thủ công

```bash
# 1. Clone repository
git clone https://github.com/<your-username>/bankbot-agentic-ai.git
cd bankbot-agentic-ai

# 2. Tạo môi trường ảo
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

# 3. Cài đặt thư viện
pip install -r requirements.txt

# 4. Cấu hình biến môi trường
cp .env.example .env
# Mở file .env và điền GEMINI_API_KEY của bạn

# 5. Nạp dữ liệu FAQ vào Vector Database
python scripts/ingest.py

# 6. Khởi chạy Backend API (Terminal 1)
uvicorn src.api.main:app --reload --port 8000

# 7. Khởi chạy Frontend (Terminal 2)
streamlit run frontend/app.py
```

### Cách 2: Chạy bằng Docker

```bash
# 1. Cấu hình biến môi trường
cp .env.example .env
# Mở file .env và điền GEMINI_API_KEY

# 2. Build và chạy bằng Docker Compose
docker-compose up --build

# API sẽ chạy tại: http://localhost:8000
```

---

## 🧪 Demo & Ví dụ

### Test API bằng cURL

```bash
# Health check
curl http://localhost:8000/health

# Hỏi FAQ ngân hàng
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Điều kiện mở thẻ tín dụng là gì?"}'

# Tính lãi vay
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tôi vay 500 triệu, lãi suất 8.5%/năm, trong 10 năm. Tính tiền trả hàng tháng?"}'

# Tra cứu tỷ giá
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tỷ giá USD hôm nay bao nhiêu?"}'
```

### Ví dụ Response

```json
{
  "reply": "Dạ, theo thông tin từ ngân hàng, tỷ giá USD/VND hôm nay như sau:\n- Giá mua vào: 25,870.00 VNĐ\n- Giá bán ra: 26,130.00 VNĐ\nQuý khách có cần hỗ trợ thêm gì không ạ?",
  "session_id": "a1b2c3d4-...",
  "used_tools": ["get_exchange_rate"]
}
```

---

## 📁 Cấu trúc thư mục

```
bankbot-agentic-ai/
├── 📂 data/
│   ├── raw/                    # Dữ liệu FAQ gốc (.txt)
│   ├── processed/              # Dữ liệu đã xử lý
│   └── vector_db/              # ChromaDB vector store
│
├── 📂 src/                     # Source code chính
│   ├── __init__.py
│   ├── config.py               # Cấu hình & hằng số
│   │
│   ├── 📂 ingestion/           # Pipeline nạp dữ liệu
│   │   ├── loader.py           #   Đọc file .txt
│   │   └── chunker.py          #   Chia nhỏ văn bản
│   │
│   ├── 📂 vectorstore/         # Vector Database
│   │   ├── embedder.py         #   Khởi tạo Embedding model
│   │   └── store.py            #   CRUD ChromaDB
│   │
│   ├── 📂 tools/               # Công cụ cho Agent
│   │   ├── rag_tool.py         #   🔍 Tra cứu FAQ (RAG)
│   │   ├── loan_calculator_tool.py  # 🧮 Tính lãi vay/tiết kiệm
│   │   └── exchange_rate_tool.py    # 💱 Tỷ giá ngoại tệ
│   │
│   ├── 📂 agent/               # Agent thông minh
│   │   ├── prompts.py          #   System Prompt
│   │   └── agent_executor.py   #   LangGraph ReAct Agent
│   │
│   └── 📂 api/                 # REST API
│       ├── main.py             #   FastAPI endpoints
│       └── schemas.py          #   Pydantic models
│
├── 📂 frontend/
│   └── app.py                  # Giao diện Streamlit
│
├── 📂 scripts/
│   └── ingest.py               # Script nạp dữ liệu vào Vector DB
│
├── 📂 tests/                   # Kiểm thử
│   ├── test_tools.py           #   Test từng tool riêng lẻ
│   └── test_agent.py           #   Test agent routing
│
├── .env.example                # Mẫu biến môi trường
├── .gitignore
├── Dockerfile                  # Docker image
├── docker-compose.yml          # Docker Compose
├── requirements.txt            # Thư viện Python
└── README.md                   # ← Bạn đang đọc file này
```

---

## 🧪 Chạy kiểm thử (Testing)

```bash
# Chạy tất cả test
pytest tests/ -v

# Chạy test riêng cho tools
pytest tests/test_tools.py -v

# Chạy test riêng cho agent routing
pytest tests/test_agent.py -v
```

---

## 🔮 Hướng phát triển

- 🤖 **Multi-Agent:** Chia thành nhiều agent chuyên biệt (tư vấn vay, tư vấn tiết kiệm, hỗ trợ kỹ thuật)
- 📊 **Thêm công cụ:** Tra cứu lịch sử giao dịch, kiểm tra số dư, theo dõi biến động lãi suất
- ☁️ **Deploy Cloud:** Triển khai trên Google Cloud Run, AWS Lambda hoặc Azure
- 🗄️ **Database thật:** Tích hợp PostgreSQL/MongoDB thay cho in-memory session
- 🔐 **Xác thực:** Thêm JWT authentication cho API
- 📱 **Mobile:** Phát triển ứng dụng di động React Native / Flutter

---

## 📝 Giấy phép

Dự án phục vụ mục đích học tập và nghiên cứu.

---

<div align="center">

**Được xây dựng với ❤️ bởi sinh viên HaUI**

</div>
]]>
