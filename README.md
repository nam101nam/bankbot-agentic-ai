# BankBot — Agentic AI

**Trợ lý ảo ngân hàng thông minh sử dụng kiến trúc Agentic AI.** Agent (LLM) tự suy luận và chọn công cụ phù hợp để trả lời câu hỏi khách hàng — thay vì trả lời theo kịch bản cố định.

> Đồ án môn học — Trường Đại học Công nghiệp Hà Nội (HaUI)

---

## Tính năng chính

- **Tra cứu FAQ ngân hàng** bằng RAG (Retrieval-Augmented Generation) — tìm kiếm ngữ nghĩa trên dữ liệu thẻ tín dụng, tiết kiệm, vay vốn, thông tin chung
- **Tính lãi vay trả góp & lãi tiết kiệm** — áp dụng công thức tài chính chuẩn (PMT, lãi đơn)
- **Tra cứu tỷ giá ngoại tệ** thời gian thực — hỗ trợ USD, EUR, JPY, GBP, CNY, KRW...
- **Agent tự động chọn tool** — LangGraph ReAct Agent tự suy luận, không cần cấu hình rule thủ công

**Tech stack:** Python 3.11 · Google Gemini · LangChain + LangGraph · ChromaDB · FastAPI · Streamlit · Docker

---

## Cài đặt & Chạy

### Yêu cầu

- Python 3.11+, Git
- Google Gemini API Key (miễn phí tại [ai.google.dev](https://ai.google.dev/))

### Quick Start

```bash
# Clone dự án
git clone https://github.com/nam101nam/bankbot-agentic-ai.git
cd bankbot-agentic-ai

# Tạo môi trường ảo & cài thư viện
python -m venv venv
source venv/bin/activate          # Linux/Mac (Windows: venv\Scripts\activate)
pip install -r requirements.txt

# Cấu hình API Key
cp .env.example .env
# → Mở file .env, điền GEMINI_API_KEY của bạn

# Nạp dữ liệu FAQ vào Vector Database
python scripts/ingest.py

# Chạy Backend (Terminal 1)
uvicorn src.api.main:app --reload --port 8000

# Chạy Frontend (Terminal 2)
streamlit run frontend/app.py
```

Truy cập: **Frontend** → http://localhost:8501 | **API Docs** → http://localhost:8000/docs

### Chạy bằng Docker (tuỳ chọn)

```bash
cp .env.example .env              # Điền GEMINI_API_KEY
docker-compose up --build         # Backend chạy tại http://localhost:8000
```

---

## Cách sử dụng

Mở giao diện Streamlit tại `http://localhost:8501`, nhập câu hỏi bằng tiếng Việt. Agent sẽ tự chọn tool phù hợp.

**Ví dụ câu hỏi & kết quả:**

| Input (câu hỏi) | Tool được gọi | Output |
|---|---|---|
| "Điều kiện mở thẻ tín dụng là gì?" | RAG | Trả lời dựa trên dữ liệu FAQ ngân hàng |
| "Vay 500 triệu, lãi 8.5%/năm, 10 năm?" | Calculator | Số tiền trả hàng tháng, tổng lãi |
| "Tỷ giá USD hôm nay?" | Exchange Rate | Giá mua vào / bán ra so với VND |

**Test bằng cURL:**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tỷ giá USD hôm nay bao nhiêu?"}'
```

---

## Cấu trúc thư mục

```
bankbot-agentic-ai/
├── data/                        # Dữ liệu FAQ (.txt) + ChromaDB vector store
├── src/
│   ├── ingestion/               # Pipeline nạp dữ liệu (loader, chunker)
│   ├── vectorstore/             # Embedding + ChromaDB (store, embedder)
│   ├── tools/                   # 3 Tools: RAG, Loan Calculator, Exchange Rate
│   ├── agent/                   # LangGraph ReAct Agent + System Prompt
│   └── api/                     # FastAPI endpoints + Pydantic schemas
├── frontend/app.py              # Giao diện Streamlit
├── scripts/ingest.py            # Script nạp FAQ → Vector DB
├── tests/                       # Unit tests (pytest)
├── Dockerfile                   # Docker image
├── docker-compose.yml           # Docker Compose
├── requirements.txt             # Thư viện Python
└── .env.example                 # Mẫu biến môi trường
```

---

<div align="center">

**Được xây dựng bởi sinh viên HaUI**

</div>
