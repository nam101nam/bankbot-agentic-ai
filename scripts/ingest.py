import os
import sys

from src.config import RAW_DATA_DIR
from src.ingestion.loader import load_documents
from src.ingestion.chunker import chunk_documents
from src.vectorstore.store import save_to_vector_store

def main():
    print(f"\n1. Đang đọc tài liệu từ: {RAW_DATA_DIR}...")
    documents = load_documents(RAW_DATA_DIR)
    if not documents:
        print("Không tìm thấy tài liệu nào trong thư mục dữ liệu nguồn.")
        return
    # 2. Chia nhỏ tài liệu thành từng cặp Q&A
    print("\n2. Đang chia nhỏ tài liệu theo từng cặp Q&A...")
    chunks = chunk_documents(documents)
    # 3. Lưu dữ liệu đã chia nhỏ vào Vector Database (Chroma)
    print("\n3. Đang tiến hành lưu trữ vào Vector Store...")
    db = save_to_vector_store(chunks)
    print("\n Quá trình Ingestion dữ liệu hoàn thành thành công!")

if __name__ == "__main__":
    main()