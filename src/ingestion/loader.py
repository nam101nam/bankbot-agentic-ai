"""
Loader module: Đọc các file tài liệu từ thư mục data/raw.
Hỗ trợ file .txt, trả về danh sách Document (LangChain format).
"""
import os
from pathlib import Path
from langchain_core.documents import Document


def load_documents(directory: str) -> list[Document]:
    """
    Đọc tất cả file .txt trong thư mục chỉ định.

    Args:
        directory: Đường dẫn đến thư mục chứa file dữ liệu.

    Returns:
        Danh sách Document với page_content và metadata (source filename).
    """
    documents = []
    dir_path = Path(directory)

    if not dir_path.exists():
        raise FileNotFoundError(f"Thư mục không tồn tại: {directory}")

    for file_path in sorted(dir_path.glob("*.txt")):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if content:
            doc = Document(
                page_content=content,
                metadata={"source": file_path.name}
            )
            documents.append(doc)
            print(f"  ✅ Đã đọc: {file_path.name} ({len(content)} ký tự)")

    print(f"\n📄 Tổng cộng đã đọc {len(documents)} file.")
    return documents


if __name__ == "__main__":
    from src.config import RAW_DATA_DIR
    docs = load_documents(RAW_DATA_DIR)
    for doc in docs:
        print(f"\n--- {doc.metadata['source']} ---")
        print(doc.page_content[:200] + "...")
