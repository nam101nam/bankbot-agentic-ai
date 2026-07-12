import pytest
from langchain_core.documents import Document
from src.ingestion.chunker import chunk_documents
from src.ingestion.loader import load_documents

def test_chunk_documents():
    """
    Kiểm tra chức năng chia nhỏ tài liệu theo cặp Q&A.
    """
    doc = Document(
        page_content="Câu hỏi 1: A?\nCâu trả lời 1: B.\n\nCâu hỏi 2: C?\nCâu trả lời 2: D.",
        metadata={"source": "test.txt"}
    )
    chunks = chunk_documents([doc])
    assert len(chunks) == 2
    assert chunks[0].page_content == "Câu hỏi 1: A?\nCâu trả lời 1: B."
    assert chunks[1].page_content == "Câu hỏi 2: C?\nCâu trả lời 2: D."
    assert chunks[0].metadata["source"] == "test.txt"

def test_load_documents(tmp_path):
    """
    Kiểm tra chức năng đọc tài liệu từ thư mục.
    """
    # Tạo các file tạm thời
    file1 = tmp_path / "faq1.txt"
    file1.write_text("Nội dung file 1", encoding="utf-8")
    
    file2 = tmp_path / "faq2.txt"
    file2.write_text("Nội dung file 2", encoding="utf-8")
    
    docs = load_documents(str(tmp_path))
    assert len(docs) == 2
    
    # Sắp xếp file theo tên nên faq1 sẽ trước
    assert docs[0].page_content == "Nội dung file 1"
    assert docs[0].metadata["source"] == "faq1.txt"
    assert docs[1].page_content == "Nội dung file 2"
    assert docs[1].metadata["source"] == "faq2.txt"

def test_load_documents_non_existent():
    """
    Kiểm tra lỗi ném ra khi thư mục không tồn tại.
    """
    with pytest.raises(FileNotFoundError):
        load_documents("/non_existent_directory_12345")
