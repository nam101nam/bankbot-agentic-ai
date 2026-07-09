import pytest 
from src.tools.loan_calculator_tool import calculator_loan, calculator_savings_interest
from src.tools.exchange_rate_tool import get_exchange_rate
from src.tools.rag_tool import search_bank_faq

def test_calculator_loan():
    result = calculator_loan.invoke({
        "principal": 500000000,
        "rate": 8.5,
        "months": 120
    })
    # Kiểm tra tiêu đề bảng tính
    assert "BẢNG TÍNH TOÁN KHOẢN VAY" in result
    # Kiểm tra số tiền gốc
    assert "500.000.000 VNĐ" in result
    # Kiểm tra lãi suất và kỳ hạn vay
    assert "8.5%" in result
    assert "120 tháng" in result
    # Tiền trả hàng tháng dự kiến: ~6.199.291 VNĐ
    assert "6.199.284 VNĐ" in result

def test_get_exchange_rate_valid():
    """
    Kiểm thử công cụ tra cứu tỷ giá với mã tiền tệ hợp lệ (USD).
    """
    result = get_exchange_rate.invoke({"currency_code": "USD"})
    # Kiểm tra xem có chứa thông tin tỷ giá mua/bán hay không
    assert "TỶ GIÁ NGOẠI TỆ USD/VND" in result
    assert "Giá mua vào" in result
    assert "Giá bán ra" in result

def test_get_exchange_rate_invalid():
    """
    Kiểm thử công cụ tra cứu tỷ giá với mã tiền tệ không hỗ trợ.
    """
    result = get_exchange_rate.invoke({"currency_code": "XYZ"})
    # Kiểm tra thông báo lỗi/không tìm thấy
    assert "chưa có thông tin tỷ giá" in result or "XYZ" in result

def test_search_bank_faq():
    """
    Kiểm thử công cụ tìm kiếm RAG từ cơ sở dữ liệu Vector DB.
    Yêu cầu: Đã chạy scripts/ingest.py để tạo database trước khi chạy test.
    """
    result = search_bank_faq.invoke({"query": "thẻ tín dụng"})
    assert isinstance(result, str)
    assert len(result) > 0
    # Kết quả trả về phải là tài liệu tham khảo hoặc thông báo không tìm thấy (nếu db rỗng)
    assert "[Tài liệu tham khảo 1]" in result or "Không tìm thấy" in result