from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_check():
    """
    Kiểm tra endpoint /health của FastAPI.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_chat_endpoint_faq():
    """
    Kiểm tra endpoint /chat gọi đến Agent tra cứu câu hỏi FAQ.
    """
    response = client.post("/chat", json={
        "message": "Thời gian làm việc của ngân hàng thế nào?"
    })
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert "session_id" in data
    assert "search_bank_faq" in data.get("used_tools", [])
