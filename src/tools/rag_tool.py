from langchain_core.tools import tool
from src.vectorstore.store import query_vector_store

@tool(
    "search_bank_faq",  
    description="Tìm kiếm thông tin chính thức của ngân hàng về các sản phẩm như: gửi tiết kiệm, lãi suất, thẻ tín dụng, các sản phẩm vay vốn (vay mua nhà, mua xe, tiêu dùng), giờ làm việc, hotline, phí chuyển tiền và dịch vụ...",
)
def search_bank_faq(query:str)-> str:
    """
    Tìm kiếm thông tin chính thức của ngân hàng về các sản phẩm như:
    gửi tiết kiệm, lãi suất, thẻ tín dụng, các sản phẩm vay vốn (vay mua nhà, mua xe, tiêu dùng),
    giờ làm việc, hotline, phí chuyển tiền và dịch vụ...
    
    Args:
        query: Câu hỏi hoặc từ khóa cần tìm kiếm liên quan đến thông tin ngân hàng.
        
    Returns:
        Một chuỗi văn bản chứa thông tin tìm được từ cơ sở dữ liệu FAQ của ngân hàng.
    """
    results = query_vector_store(query, k=3)
    if not results:
        return "Không tìm thấy thông tin phù hợp trong tài liệu của ngân hàng."
    # Format lại các tài liệu tìm được thành chuỗi văn bản rõ ràng
    formatted_results = []
    for i, doc in enumerate(results):
        formatted_results.append(f"[Tài liệu tham khảo {i+1}]:\n{doc.page_content}")
        
    return "\n\n".join(formatted_results)

if __name__ == "__main__":
    # Chạy thử nghiệm độc lập tool
    print("=== CHẠY THỬ NGHIỆM RAG TOOL ===")
    test_query = "Lãi suất tiết kiệm hiện tại"
    print(f"Query: {test_query}\n")
    res = search_bank_faq.invoke({"query": test_query})
    print(res)