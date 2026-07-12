import os
import time
import uuid
import httpx
import json
from dotenv import load_dotenv

load_dotenv()

# List of 25 test cases with queries and expected tools
# Expected tools: "search_bank_faq", "calculate_loan", "calculate_savings_interest", "get_exchange_rate", None
TEST_CASES = [
    # 1. search_bank_faq (FAQ RAG Tool)
    {
        "query": "Thời gian làm việc của ngân hàng thế nào?",
        "expected_tool": "search_bank_faq",
        "category": "FAQ Tra cứu"
    },
    {
        "query": "Địa chỉ chi nhánh chính của ngân hàng ở đâu?",
        "expected_tool": "search_bank_faq",
        "category": "FAQ Tra cứu"
    },
    {
        "query": "Tôi có thể liên hệ số điện thoại hotline nào để khóa thẻ khẩn cấp?",
        "expected_tool": "search_bank_faq",
        "category": "FAQ Tra cứu"
    },
    {
        "query": "Hạn mức chuyển tiền tối đa qua Mobile Banking là bao nhiêu?",
        "expected_tool": "search_bank_faq",
        "category": "FAQ Tra cứu"
    },
    {
        "query": "Phí phát hành thẻ ATM nội địa là bao nhiêu?",
        "expected_tool": "search_bank_faq",
        "category": "FAQ Tra cứu"
    },
    {
        "query": "Làm thế nào để kích hoạt thẻ tín dụng mới?",
        "expected_tool": "search_bank_faq",
        "category": "FAQ Tra cứu"
    },
    {
        "query": "Ngân hàng có hỗ trợ vay mua nhà trả góp không?",
        "expected_tool": "search_bank_faq",
        "category": "FAQ Tra cứu"
    },
    # 2. calculate_loan (Loan Calculator Tool)
    {
        "query": "Tôi muốn vay 100 triệu trả trong 12 tháng với lãi suất 8%/năm. Số tiền phải trả hàng tháng là bao nhiêu?",
        "expected_tool": "calculate_loan",
        "category": "Tính lãi vay"
    },
    {
        "query": "Vay mua ô tô 500 triệu lãi suất 9% trong vòng 5 năm, tính giùm tôi tổng tiền lãi phải trả.",
        "expected_tool": "calculate_loan",
        "category": "Tính lãi vay"
    },
    {
        "query": "Vay tiêu dùng 10.000.000 VNĐ trả góp trong 3 tháng lãi suất 12% một năm.",
        "expected_tool": "calculate_loan",
        "category": "Tính lãi vay"
    },
    {
        "query": "Tính lịch trả nợ vay 2 tỷ thời hạn 120 tháng lãi suất 7.5%/năm.",
        "expected_tool": "calculate_loan",
        "category": "Tính lãi vay"
    },
    {
        "query": "Vay tín chấp 30 triệu thời hạn 6 tháng, lãi suất 11%/năm. Cần trả bao nhiêu cả gốc lẫn lãi?",
        "expected_tool": "calculate_loan",
        "category": "Tính lãi vay"
    },
    # 3. calculate_savings_interest (Savings Calculator Tool)
    {
        "query": "Nếu gửi tiết kiệm 50 triệu kỳ hạn 6 tháng với lãi suất 4.5%/năm thì tiền lãi nhận được là bao nhiêu?",
        "expected_tool": "calculate_savings_interest",
        "category": "Tính lãi tiết kiệm"
    },
    {
        "query": "Tính tiền lãi khi gửi tiết kiệm 200 triệu với lãi suất 6.2% trong 1 năm.",
        "expected_tool": "calculate_savings_interest",
        "category": "Tính lãi tiết kiệm"
    },
    {
        "query": "Gửi 10.000.000 VNĐ vào ngân hàng lãi suất 3% một năm trong 1 tháng nhận được bao nhiêu tiền lãi?",
        "expected_tool": "calculate_savings_interest",
        "category": "Tính lãi tiết kiệm"
    },
    {
        "query": "Tính tiền lãi cuối kỳ khi gửi tiết kiệm 500 triệu kỳ hạn 24 tháng lãi suất 5.8%/năm.",
        "expected_tool": "calculate_savings_interest",
        "category": "Tính lãi tiết kiệm"
    },
    {
        "query": "Tôi muốn gửi 80 triệu đồng kỳ hạn 3 tháng với lãi suất 4% một năm, lãi nhận được bao nhiêu?",
        "expected_tool": "calculate_savings_interest",
        "category": "Tính lãi tiết kiệm"
    },
    # 4. get_exchange_rate (Exchange Rate Tool)
    {
        "query": "Tỷ giá USD/VND hiện tại mua vào bán ra như thế nào?",
        "expected_tool": "get_exchange_rate",
        "category": "Tra cứu tỷ giá"
    },
    {
        "query": "Cho tôi xin tỷ giá đồng Euro (EUR) mới nhất.",
        "expected_tool": "get_exchange_rate",
        "category": "Tra cứu tỷ giá"
    },
    {
        "query": "Đồng Yên Nhật (JPY) hôm nay có giá bao nhiêu?",
        "expected_tool": "get_exchange_rate",
        "category": "Tra cứu tỷ giá"
    },
    {
        "query": "Xem tỷ giá đồng Dollar Úc (AUD).",
        "expected_tool": "get_exchange_rate",
        "category": "Tra cứu tỷ giá"
    },
    {
        "query": "Đổi đồng Nhân dân tệ (CNY) sang Việt Nam đồng hôm nay tỷ giá thế nào?",
        "expected_tool": "get_exchange_rate",
        "category": "Tra cứu tỷ giá"
    },
    # 5. None (Chit-chat / General inquiries)
    {
        "query": "Chào bạn, bạn là ai thế?",
        "expected_tool": None,
        "category": "Chit-chat"
    },
    {
        "query": "Cảm ơn bạn rất nhiều vì sự giúp đỡ!",
        "expected_tool": None,
        "category": "Chit-chat"
    },
    {
        "query": "Bạn có thể làm được những việc gì?",
        "expected_tool": None,
        "category": "Chit-chat"
    }
]

API_URL = "http://127.0.0.1:8000/chat"

def evaluate():
    print("=== BẮT ĐẦU ĐÁNH GIÁ CHẤT LƯỢNG AGENT (25 CÂU HỎI) ===")
    print(f"Gọi FastAPI endpoint: {API_URL}")
    print("Độ trễ (delay) giữa mỗi câu hỏi: 2.5s (tránh rate limit Gemini API)\n")
    
    results = []
    correct_count = 0
    total_latency = 0.0
    latencies = []
    
    client = httpx.Client(timeout=30.0)
    
    # Check health first
    try:
        health_resp = client.get("http://127.0.0.1:8000/health")
        if health_resp.status_code != 200:
            print("Cảnh báo: Health check FastAPI không thành công!")
    except Exception as e:
        print(f"Lỗi: Không thể kết nối tới FastAPI server tại {API_URL}. Vui lòng đảm bảo server đang chạy.")
        print(e)
        return
        
    for i, tc in enumerate(TEST_CASES, 1):
        query = tc["query"]
        expected = tc["expected_tool"]
        category = tc["category"]
        
        # Prepare request
        payload = {
            "message": query,
            "session_id": str(uuid.uuid4()) # Unique session per query for independent evaluation
        }
        
        print(f"[{i}/{len(TEST_CASES)}] [{category}] Hỏi: {query}")
        
        start_time = time.time()
        try:
            response = client.post(API_URL, json=payload)
            latency = (time.time() - start_time) * 1000 # in ms
            
            if response.status_code == 200:
                data = response.json()
                used_tools = data.get("used_tools", [])
                reply = data.get("reply", "")
                
                # Check correctness
                # If expected is None, no tools should be called
                # If expected is a tool name, it must be in used_tools
                if expected is None:
                    is_correct = len(used_tools) == 0
                else:
                    is_correct = expected in used_tools
                    
                status = "ĐÚNG" if is_correct else "SAI"
                if is_correct:
                    correct_count += 1
                
                print(f"   -> Dùng tool: {used_tools} (Kỳ vọng: {expected}) - Kết quả: {status}")
                print(f"   -> Latency: {latency:.2f} ms")
                
                results.append({
                    "index": i,
                    "query": query,
                    "category": category,
                    "expected": expected,
                    "actual": used_tools,
                    "correct": is_correct,
                    "latency_ms": latency,
                    "reply_preview": reply[:100] + "..." if len(reply) > 100 else reply,
                    "error": None
                })
                
                latencies.append(latency)
                total_latency += latency
            else:
                print(f"   -> Lỗi API: HTTP {response.status_code}")
                results.append({
                    "index": i,
                    "query": query,
                    "category": category,
                    "expected": expected,
                    "actual": [],
                    "correct": False,
                    "latency_ms": latency,
                    "reply_preview": "",
                    "error": f"HTTP {response.status_code}: {response.text}"
                })
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            print(f"   -> Lỗi kết nối: {str(e)}")
            results.append({
                "index": i,
                "query": query,
                "category": category,
                "expected": expected,
                "actual": [],
                "correct": False,
                "latency_ms": latency,
                "reply_preview": "",
                "error": str(e)
            })
            
        # Wait to avoid Gemini API rate limits
        if i < len(TEST_CASES):
            time.sleep(2.5)

    client.close()
    
    # Calculate statistics
    total_tests = len(TEST_CASES)
    accuracy = (correct_count / total_tests) * 100 if total_tests > 0 else 0
    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    min_latency = min(latencies) if latencies else 0
    max_latency = max(latencies) if latencies else 0
    
    print("\n" + "="*50)
    print("=== KẾT QUẢ ĐÁNH GIÁ (SUMMARY) ===")
    print(f"- Tổng số câu hỏi: {total_tests}")
    print(f"- Số câu chọn đúng tool: {correct_count}")
    print(f"- Độ chính xác chọn tool: {accuracy:.2f}%")
    print(f"- Latency trung bình: {avg_latency:.2f} ms")
    print(f"- Latency nhỏ nhất: {min_latency:.2f} ms")
    print(f"- Latency lớn nhất: {max_latency:.2f} ms")
    print("="*50)
    
    # Generate markdown report
    generate_markdown_report(results, accuracy, avg_latency, min_latency, max_latency)

def generate_markdown_report(results, accuracy, avg_latency, min_latency, max_latency):
    report_path = "evaluation_report.md"
    
    markdown_content = f"""# Báo cáo đánh giá Agentic AI BankBot

## Tóm tắt kết quả (Summary Metrics)

- **Tổng số câu hỏi test:** {len(results)}
- **Độ chính xác chọn tool:** **{accuracy:.2f}%**
- **Độ trễ API (Latency):**
  - Trung bình: **{avg_latency:.2f} ms**
  - Nhỏ nhất: **{min_latency:.2f} ms**
  - Lớn nhất: **{max_latency:.2f} ms**

---

## Chi tiết kết quả kiểm thử (Test Cases Details)

| ID | Nhóm câu hỏi | Câu hỏi | Tool Kỳ vọng | Tool Thực tế | Kết quả | Latency (ms) |
|---|---|---|---|---|---|---|
"""
    
    for r in results:
        status_emoji = "✅ Đúng" if r["correct"] else "❌ Sai"
        expected_str = r["expected"] if r["expected"] else "None"
        actual_str = ", ".join(r["actual"]) if r["actual"] else "None"
        
        # Escape markdown table characters
        query_cleaned = r["query"].replace("|", "\\|")
        
        markdown_content += f"| {r['index']} | {r['category']} | {query_cleaned} | `{expected_str}` | `{actual_str}` | {status_emoji} | {r['latency_ms']:.1f} |\n"
        
    markdown_content += """
---

## Nhận xét & Đánh giá
1. **Độ chính xác định tuyến (Tool Selection Accuracy):** Phản ánh khả năng của mô hình ngôn ngữ trong việc nhận diện đúng ý định người dùng để kích hoạt chức năng RAG, tính toán vay, gửi tiết kiệm hoặc xem tỷ giá.
2. **Độ trễ (Latency):** Thời gian phản hồi của API bao gồm thời gian chạy suy luận của mô hình Gemini và gọi các tool tương ứng.
"""

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
        
    print(f"\nĐã lưu báo cáo chi tiết vào file: {report_path}")

if __name__ == "__main__":
    evaluate()
