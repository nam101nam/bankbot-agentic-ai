# Báo cáo đánh giá Agentic AI BankBot

## Tóm tắt kết quả (Summary Metrics)

- **Tổng số câu hỏi test:** 25
- **Độ chính xác chọn tool:** **96.00%**
- **Độ trễ API (Latency):**
  - Trung bình: **2708.81 ms**
  - Nhỏ nhất: **775.88 ms**
  - Lớn nhất: **19847.20 ms**

---

## Chi tiết kết quả kiểm thử (Test Cases Details)

| ID | Nhóm câu hỏi | Câu hỏi | Tool Kỳ vọng | Tool Thực tế | Kết quả | Latency (ms) |
|---|---|---|---|---|---|---|
| 1 | FAQ Tra cứu | Thời gian làm việc của ngân hàng thế nào? | `search_bank_faq` | `search_bank_faq` | ✅ Đúng | 2610.0 |
| 2 | FAQ Tra cứu | Địa chỉ chi nhánh chính của ngân hàng ở đâu? | `search_bank_faq` | `search_bank_faq` | ✅ Đúng | 2152.7 |
| 3 | FAQ Tra cứu | Tôi có thể liên hệ số điện thoại hotline nào để khóa thẻ khẩn cấp? | `search_bank_faq` | `search_bank_faq` | ✅ Đúng | 2148.7 |
| 4 | FAQ Tra cứu | Hạn mức chuyển tiền tối đa qua Mobile Banking là bao nhiêu? | `search_bank_faq` | `search_bank_faq` | ✅ Đúng | 2368.9 |
| 5 | FAQ Tra cứu | Phí phát hành thẻ ATM nội địa là bao nhiêu? | `search_bank_faq` | `search_bank_faq` | ✅ Đúng | 2007.9 |
| 6 | FAQ Tra cứu | Làm thế nào để kích hoạt thẻ tín dụng mới? | `search_bank_faq` | `search_bank_faq` | ✅ Đúng | 2520.8 |
| 7 | FAQ Tra cứu | Ngân hàng có hỗ trợ vay mua nhà trả góp không? | `search_bank_faq` | `search_bank_faq` | ✅ Đúng | 2421.7 |
| 8 | Tính lãi vay | Tôi muốn vay 100 triệu trả trong 12 tháng với lãi suất 8%/năm. Số tiền phải trả hàng tháng là bao nhiêu? | `calculate_loan` | `calculate_loan` | ✅ Đúng | 1605.2 |
| 9 | Tính lãi vay | Vay mua ô tô 500 triệu lãi suất 9% trong vòng 5 năm, tính giùm tôi tổng tiền lãi phải trả. | `calculate_loan` | `calculate_loan` | ✅ Đúng | 1883.1 |
| 10 | Tính lãi vay | Vay tiêu dùng 10.000.000 VNĐ trả góp trong 3 tháng lãi suất 12% một năm. | `calculate_loan` | `calculate_loan` | ✅ Đúng | 1596.8 |
| 11 | Tính lãi vay | Tính lịch trả nợ vay 2 tỷ thời hạn 120 tháng lãi suất 7.5%/năm. | `calculate_loan` | `calculate_loan` | ✅ Đúng | 1610.6 |
| 12 | Tính lãi vay | Vay tín chấp 30 triệu thời hạn 6 tháng, lãi suất 11%/năm. Cần trả bao nhiêu cả gốc lẫn lãi? | `calculate_loan` | `calculate_loan` | ✅ Đúng | 1509.5 |
| 13 | Tính lãi tiết kiệm | Nếu gửi tiết kiệm 50 triệu kỳ hạn 6 tháng với lãi suất 4.5%/năm thì tiền lãi nhận được là bao nhiêu? | `calculate_savings_interest` | `None` | ❌ Sai | 30005.6 |
| 14 | Tính lãi tiết kiệm | Tính tiền lãi khi gửi tiết kiệm 200 triệu với lãi suất 6.2% trong 1 năm. | `calculate_savings_interest` | `calculate_savings_interest` | ✅ Đúng | 4689.7 |
| 15 | Tính lãi tiết kiệm | Gửi 10.000.000 VNĐ vào ngân hàng lãi suất 3% một năm trong 1 tháng nhận được bao nhiêu tiền lãi? | `calculate_savings_interest` | `calculate_savings_interest` | ✅ Đúng | 1556.4 |
| 16 | Tính lãi tiết kiệm | Tính tiền lãi cuối kỳ khi gửi tiết kiệm 500 triệu kỳ hạn 24 tháng lãi suất 5.8%/năm. | `calculate_savings_interest` | `calculate_savings_interest` | ✅ Đúng | 1538.2 |
| 17 | Tính lãi tiết kiệm | Tôi muốn gửi 80 triệu đồng kỳ hạn 3 tháng với lãi suất 4% một năm, lãi nhận được bao nhiêu? | `calculate_savings_interest` | `calculate_savings_interest` | ✅ Đúng | 1459.1 |
| 18 | Tra cứu tỷ giá | Tỷ giá USD/VND hiện tại mua vào bán ra như thế nào? | `get_exchange_rate` | `get_exchange_rate` | ✅ Đúng | 2111.6 |
| 19 | Tra cứu tỷ giá | Cho tôi xin tỷ giá đồng Euro (EUR) mới nhất. | `get_exchange_rate` | `get_exchange_rate` | ✅ Đúng | 2139.9 |
| 20 | Tra cứu tỷ giá | Đồng Yên Nhật (JPY) hôm nay có giá bao nhiêu? | `get_exchange_rate` | `get_exchange_rate` | ✅ Đúng | 1976.5 |
| 21 | Tra cứu tỷ giá | Xem tỷ giá đồng Dollar Úc (AUD). | `get_exchange_rate` | `get_exchange_rate` | ✅ Đúng | 19847.2 |
| 22 | Tra cứu tỷ giá | Đổi đồng Nhân dân tệ (CNY) sang Việt Nam đồng hôm nay tỷ giá thế nào? | `get_exchange_rate` | `get_exchange_rate` | ✅ Đúng | 2010.1 |
| 23 | Chit-chat | Chào bạn, bạn là ai thế? | `None` | `None` | ✅ Đúng | 1079.8 |
| 24 | Chit-chat | Cảm ơn bạn rất nhiều vì sự giúp đỡ! | `None` | `None` | ✅ Đúng | 775.9 |
| 25 | Chit-chat | Bạn có thể làm được những việc gì? | `None` | `None` | ✅ Đúng | 1390.9 |

---

## Nhận xét & Đánh giá
1. **Độ chính xác định tuyến (Tool Selection Accuracy):** Phản ánh khả năng của mô hình ngôn ngữ trong việc nhận diện đúng ý định người dùng để kích hoạt chức năng RAG, tính toán vay, gửi tiết kiệm hoặc xem tỷ giá.
2. **Độ trễ (Latency):** Thời gian phản hồi của API bao gồm thời gian chạy suy luận của mô hình Gemini và gọi các tool tương ứng.
