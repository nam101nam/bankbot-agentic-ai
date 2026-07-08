import uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.schemas import ChatRequest, ChatResponse
from src.agent.agent_executor import chat

app = FastAPI(
    title="BankBot API",
    description="Backend API phục vụ cho Trợ lý tài chính BankBot Agentic AI",
    version="1.0.0"
)

# Cấu hình CORS để Frontend (Streamlit) có thể gọi API mà không bị chặn
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong thực tế nên cấu hình cụ thể domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database để lưu trữ lịch sử chat tạm thời: session_id -> list of message dicts
sessions_db = {}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    session_id = request.session_id
    
    # Nếu chưa có session_id hoặc session chưa tồn tại trong bộ nhớ, tạo mới
    if not session_id or session_id not in sessions_db:
        session_id = session_id or str(uuid.uuid4())
        sessions_db[session_id] = []
        
    chat_history = sessions_db[session_id]
    
    # Gọi hàm xử lý của Agent với tin nhắn hiện tại và lịch sử cuộc gọi trước đó
    reply, used_tools = chat(user_message=request.message, chat_history=chat_history)
    
    # Cập nhật lịch sử chat của session này
    chat_history.append({"role": "user", "content": request.message})
    chat_history.append({"role": "assistant", "content": reply, "used_tools": used_tools})
    
    return ChatResponse(reply=reply, session_id=session_id, used_tools=used_tools)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
