"""
Chunker module: Chia nhỏ văn bản thành các đoạn (chunks) phù hợp cho embedding.
Sử dụng RecursiveCharacterTextSplitter để giữ ngữ cảnh tốt nhất.
"""
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_documents(documents: list[Document]) -> list[Document]:
    """
    Chia nhỏ danh sách Document thành các chunks.

    Args:
        documents: Danh sách Document cần chia nhỏ.

    Returns:
        Danh sách Document đã được chia nhỏ, kế thừa metadata gốc.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\nQ: ", "\n", ". ", " ", ""],
    )

    chunks = text_splitter.split_documents(documents)
    print(f"✂️  Đã chia thành {len(chunks)} chunks (chunk_size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    return chunks


if __name__ == "__main__":
    from src.ingestion.loader import load_documents
    from src.config import RAW_DATA_DIR

    docs = load_documents(RAW_DATA_DIR)
    chunks = chunk_documents(docs)
    print(f"\n--- Ví dụ chunk đầu tiên ---")
    print(chunks[0].page_content)
    print(f"\nMetadata: {chunks[0].metadata}")
