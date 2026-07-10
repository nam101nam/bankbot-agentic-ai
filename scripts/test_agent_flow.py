import os
from dotenv import load_dotenv
load_dotenv()

from src.agent.agent_executor import chat

history = [
    {"role": "user", "content": "30tr, mua điện thoại, khoảng 4-5 tháng , chưa"},
    {"role": "assistant", "content": "Chào bạn, tôi là BankBot. Rất vui được hỗ trợ bạn về kế hoạch vay 30 triệu đồng để mua điện thoại...\n[Giả định vay tiêu dùng tín chấp lãi suất 12%/năm]:\n- Số tiền gốc vay: 30.000.000 VNĐ\n- Lãi suất: 12%/năm\n- Kỳ hạn vay: 5 tháng\n- Số tiền trả hàng tháng: 6.125.500 VNĐ"},
    {"role": "user", "content": "lãi suất hàng năm như nào"},
    {"role": "assistant", "content": "Chào bạn, tôi là BankBot. Lãi suất vay tiêu dùng tín chấp thường dao động từ 12% đến 20%/năm..."}
]

print("=== RUNNING CHAT TEST ===")
reply, used_tools = chat("Vay 30 triệu mua điện thoại trong 5 tháng", history)
print(f"Reply:\n{reply}")
print(f"Used Tools: {used_tools}")
