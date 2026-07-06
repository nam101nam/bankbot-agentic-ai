"""
Chunker module: Chia nhỏ văn bản thành các đoạn (chunks) phù hợp cho embedding.
"""
from langchain_core.documents import Document


def chunk_documents(documents: list[Document]) -> list[Document]:
    """
    Chia nhỏ danh sách Document thành các chunks theo từng cặp Q&A (phân tách bởi 2 dòng xuống dòng \n\n).

    Args:
        documents: Danh sách Document cần chia nhỏ.

    Returns:
        Danh sách Document đã được chia nhỏ theo từng cặp Q&A, kế thừa metadata gốc.
    """
    chunks = []
    for doc in documents:
        # Tách nội dung theo hai dấu xuống dòng liên tiếp
        raw_chunks = doc.page_content.split("\n\n")
        for chunk in raw_chunks:
            cleaned_content = chunk.strip()
            if cleaned_content:
                chunks.append(
                    Document(
                        page_content=cleaned_content,
                        metadata=doc.metadata.copy()
                    )
                )
    print(f"Đã chia thành {len(chunks)} chunks (Mỗi chunk là 1 cặp Q&A)")
    return chunks


if __name__ == "__main__":
    from src.ingestion.loader import load_documents
    from src.config import RAW_DATA_DIR

    docs = load_documents(RAW_DATA_DIR)
    chunks = chunk_documents(docs)
    print(f"\n--- Ví dụ chunk đầu tiên ---")
    print(chunks[0].page_content)
    print(f"\nMetadata: {chunks[0].metadata}")
