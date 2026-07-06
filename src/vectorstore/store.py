import os
import shutil
import hashlib
import json
from pathlib import Path
from langchain_community.vectorstores import Chroma
from src.config import VECTOR_DB_DIR, RAW_DATA_DIR, CHUNK_SIZE, CHUNK_OVERLAP
from src.vectorstore.embedder import get_embedding_function

# Tính hash MD5 cho toàn bộ file .txt trong thư mục dữ liệu
def calculate_directory_hash(directory_path: str) -> dict[str, str]:
    hashes = {}
    dir_path = Path(directory_path)
    if dir_path.exists():
        for file_path in sorted(dir_path.glob("*.txt")):
            hasher = hashlib.md5()
            try:
                with open(file_path, "rb") as f:
                    buf = f.read()
                    hasher.update(buf)
                hashes[file_path.name] = hasher.hexdigest()
            except Exception as e:
                print(f"Lỗi khi đọc file {file_path.name} để tính hash: {e}")
    return hashes

# Lưu vector store

def save_to_vector_store(chunks, embedding_function=None):
    if embedding_function is None:
        embedding_function=get_embedding_function()

    metadata_path = Path(VECTOR_DB_DIR) / "build_metadata.json"
    current_hashes = calculate_directory_hash(RAW_DATA_DIR)
    
    current_metadata = {
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "hashes": current_hashes
    }

    # Kiểm tra xem vector store đã tồn tại và dữ liệu/cấu hình có giống cũ không
    if os.path.exists(VECTOR_DB_DIR) and metadata_path.exists():
        try:
            with open(metadata_path, "r", encoding="utf-8") as f:
                saved_metadata = json.load(f)
            if saved_metadata == current_metadata:
                print("Dữ liệu và cấu hình không thay đổi. Không cần tạo lại vector store.")
                return Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embedding_function)
        except Exception as e:
            print(f"Lỗi khi đọc metadata cũ ({e}). Tiến hành tạo mới...")

    # Nếu có thay đổi hoặc chưa tồn tại, tiến hành xóa và tạo mới
    if os.path.exists(VECTOR_DB_DIR):
        print(f'Đang xóa Vector store cũ tại: {VECTOR_DB_DIR}...')
        shutil.rmtree(VECTOR_DB_DIR)
        print('Xóa thành công Vector store cũ!')

    os.makedirs(VECTOR_DB_DIR, exist_ok=True)
    db=Chroma.from_documents(chunks,embedding_function,persist_directory=VECTOR_DB_DIR)
    print(f"Lưu thành công vector store tại: {VECTOR_DB_DIR}")

    # Ghi lại metadata mới để kiểm tra lần sau
    try:
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(current_metadata, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Không thể lưu metadata mới: {e}")

    return db

# Lấy vector từ cơ sở dữ liệu

def get_vector_store(embedding_function=None):
    if embedding_function is None:
        embedding_function=get_embedding_function()
    db=Chroma(persist_directory=VECTOR_DB_DIR,embedding_function=embedding_function)
    print("Đang tải vector store từ cơ sở dữ liệu....")
    return db

# Hàm tìm kiếm tương đồng trong vectorstore

def query_vector_store(query,k=3,embedding_function=None):
    if embedding_function is None:
        embedding_function=get_embedding_function()
    db=get_vector_store(embedding_function)
    print("Đang tìm kiếm tương đồng trong vectorstore....")
    results=db.similarity_search(query,k=k)
    return results

# Code chạy thử nghiệm

if __name__ == "__main__":
    from src.ingestion.chunker import chunk_documents
    from src.ingestion.loader import load_documents
    from src.config import RAW_DATA_DIR
    docs = load_documents(RAW_DATA_DIR)
    chunks = chunk_documents(docs)
    db=save_to_vector_store(chunks)
    query="Lãi suất ngân hàng có cao không"
    print(f"Đang tìm kiếm với query: {query}")
    results=query_vector_store(query,k=3)
    for i,result in enumerate(results):
        print(f"Kết quả {i+1}:\n{result.page_content}\n")


