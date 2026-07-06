from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.config import GEMINI_API_KEY,EMBEDDING_MODEL_NAME

def get_embedding_function():
    embedding=GoogleGenerativeAIEmbeddings(api_key=GEMINI_API_KEY,model=EMBEDDING_MODEL_NAME)
    return embedding
if __name__ == "__main__":
    print("Đang khởi tạo thử Gemini Embedding... ")
    embed_tool = get_embedding_function()
    print("Khởi tạo thành công đối tượng:")
    print(embed_tool)