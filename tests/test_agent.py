import pytest
from src.agent.agent_executor import chat

def test_agent_routing_faq():
    """
    Kiểm tra Agent có tự gọi tool 'search_bank_faq' khi hỏi về dịch vụ ngân hàng.
    """
    reply, used_tools = chat("Điều kiện mở thẻ tín dụng của ngân hàng là gì?", [])
    # Agent bắt buộc phải gọi tool tra cứu FAQ
    assert "search_bank_faq" in used_tools
    assert len(reply) > 0

def test_agent_routing_loan():
    """
    Kiểm tra Agent có tự gọi tool 'calculate_loan' khi hỏi tính toán khoản vay.
    """
    reply, used_tools = chat(
        "Tôi muốn vay 100 triệu, lãi suất 10%/năm trong 12 tháng. Tính tiền phải trả hàng tháng?", 
        []
    )
    # Agent bắt buộc phải gọi tool tính lãi vay
    assert "calculate_loan" in used_tools
    assert len(reply) > 0

def test_agent_routing_exchange_rate():
    """
    Kiểm tra Agent có tự gọi tool 'get_exchange_rate' khi hỏi tỷ giá.
    """
    reply, used_tools = chat("Tỷ giá USD hôm nay bao nhiêu?", [])
    # Agent bắt buộc phải gọi tool lấy tỷ giá ngoại tệ
    assert "get_exchange_rate" in used_tools
    assert len(reply) > 0
