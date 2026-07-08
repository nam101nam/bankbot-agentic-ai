import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from src.config import GEMINI_API_KEY, LLM_MODEL_NAME
from src.agent.prompts import SYSTEM_PROMPT
from src.tools.rag_tool import search_bank_faq
from src.tools.loan_calculator_tool import calculator_loan, calculator_savings_interest
from src.tools.exchange_rate_tool import get_exchange_rate

# Danh sách các công cụ cung cấp cho Agent
tools = [
    search_bank_faq,
    calculator_loan,
    calculator_savings_interest,
    get_exchange_rate
]

# Đối tượng Agent (Compiled State Graph) được khởi tạo dạng Lazy/Singleton
_agent = None

def get_agent_executor():
    """
    Khởi tạo và trả về đối tượng Agent (Compiled State Graph) (Singleton).
    """
    global _agent
    if _agent is None:
        # Khởi tạo mô hình LLM Gemini
        llm = ChatGoogleGenerativeAI(
            model=LLM_MODEL_NAME,
            google_api_key=GEMINI_API_KEY,
            temperature=0.0
        )
        
        # Tạo React Agent bằng LangGraph prebuilt
        # prompt ở đây đóng vai trò là System Message hướng dẫn hành vi cho Agent
        _agent = create_react_agent(
            model=llm,
            tools=tools,
            prompt=SYSTEM_PROMPT
        )
        
    return _agent

def convert_chat_history(chat_history: list) -> list:
    """
    Chuyển đổi lịch sử chat thô thành đối tượng Message của LangChain.
    Hỗ trợ định dạng:
    - [("human", "Hi"), ("ai", "Hello")]
    - [{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello"}]
    """
    converted = []
    for msg in chat_history:
        if isinstance(msg, dict):
            role = msg.get("role")
            content = msg.get("content", "")
            if role in ["user", "human"]:
                converted.append(HumanMessage(content=content))
            elif role in ["assistant", "ai"]:
                converted.append(AIMessage(content=content))
        elif isinstance(msg, tuple) and len(msg) == 2:
            role, content = msg
            if role in ["user", "human"]:
                converted.append(HumanMessage(content=content))
            elif role in ["assistant", "ai"]:
                converted.append(AIMessage(content=content))
        else:
            converted.append(msg)
    return converted

def chat(user_message: str, chat_history: list = None) -> str:
    """
    Hàm giao tiếp chính với BankBot Agent.
    
    Args:
        user_message: Câu hỏi/yêu cầu của người dùng.
        chat_history: Lịch sử cuộc trò chuyện (mặc định là None).
        
    Returns:
        Câu trả lời từ BankBot.
    """
    if chat_history is None:
        chat_history = []
        
    # Chuyển đổi lịch sử chat sang định dạng LangChain
    formatted_messages = convert_chat_history(chat_history)
    
    # Thêm câu hỏi mới của người dùng vào cuối danh sách tin nhắn
    formatted_messages.append(HumanMessage(content=user_message))
    
    # Lấy compiled agent graph
    agent = get_agent_executor()
    
    # Chạy agent và lấy kết quả đầu ra
    response = agent.invoke({
        "messages": formatted_messages
    })
    
    # Kết quả trả về chứa list các tin nhắn mới, phần tử cuối cùng là câu trả lời của AI
    messages = response.get("messages", [])
    if messages:
        content = messages[-1].content
        if isinstance(content, list):
            text_parts = []
            for part in content:
                if isinstance(part, dict) and part.get("type") == "text":
                    text_parts.append(part.get("text", ""))
                elif isinstance(part, str):
                    text_parts.append(part)
            return "".join(text_parts)
        return content
        
    return "Rất tiếc, đã xảy ra lỗi trong quá trình xử lý câu hỏi của bạn."

if __name__ == "__main__":
    print("=== CHẠY THỬ NGHIỆM AGENT (LANGGRAPH) ===")
    
    # Test RAG Tool
    print("\n[Test 1] Tra cứu FAQ ngân hàng:")
    response_rag = chat("Thời gian làm việc của ngân hàng thế nào?", [])
    print(f"Trả lời:\n{response_rag}\n")
    
    # Test Calculator Tool
    print("\n[Test 2] Tính toán lãi suất khoản vay:")
    response_loan = chat("Tôi muốn vay 100 triệu trong 12 tháng với lãi suất 10%/năm. Số tiền trả mỗi tháng là bao nhiêu?", [])
    print(f"Trả lời:\n{response_loan}\n")
    
    # Test Exchange Rate Tool
    print("\n[Test 3] Xem tỷ giá:")
    response_rate = chat("Tỷ giá USD hiện tại là bao nhiêu?", [])
    print(f"Trả lời:\n{response_rate}\n")
