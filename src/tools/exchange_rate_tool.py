import httpx
from langchain_core.tools import tool

# Data dự phòng khi không có kết nối internet
MOCK_EXCHANGE_RATES = {
    "USD": 26000.0,
    "EUR": 27000.0,
    "JPY": 160.0,
    "GBP": 32000.0,
    "AUD": 17000.0,
    "SGD": 19000.0,
    "CNY": 3510.0,
    "KRW": 18.4,
    "CAD": 18560.0
}

# Lấy tỷ giá ngoại tệ
@tool("get_exchange_rate",description="Lấy tỷ giá ngoại tệ của các ngân hàng"  )
def get_exchange_rate(currency_code:str)->str:
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = httpx.get(url, timeout=5.0)
    
    if response.status_code == 200:
        data = response.json()
        rates = data.get("rates", {})
        
        # API v4 lấy USD làm gốc (USD = 1)
        # Tỷ giá chéo của currency_code so với VND = rates["VND"] / rates[currency_code]
        if "VND" in rates and currency_code in rates:
            vnd_rate = rates["VND"]
            curr_rate = rates[currency_code]
            mid_rate = vnd_rate / curr_rate
            
            # Tính giá mua/bán giả lập cho thực tế ngân hàng (biên độ +- 0.5%)
            buy_rate = mid_rate * 0.995
            sell_rate = mid_rate * 1.005
            
            return (
                f"=== TỶ GIÁ NGOẠI TỆ {currency_code}/VND (Trực tuyến) ===\n"
                f"- Giá mua vào (chuyển khoản): {buy_rate:,.2f} VNĐ\n"
                    f"- Giá bán ra: {sell_rate:,.2f} VNĐ\n"
                    f"*(Dữ liệu cập nhật mới nhất từ API)*"
                )
    if currency_code in MOCK_EXCHANGE_RATES:
        mid_rate = MOCK_EXCHANGE_RATES[currency_code]
        buy_rate = mid_rate * 0.995
        sell_rate = mid_rate * 1.005
        return (
            f"=== TỶ GIÁ NGOẠI TỆ {currency_code}/VND (Offline) ===\n"
            f"- Giá mua vào (chuyển khoản): {buy_rate:,.2f} VNĐ\n"
            f"- Giá bán ra: {sell_rate:,.2f} VNĐ\n"
            f"*(Hệ thống hiện ngoại tuyến, đang hiển thị tỷ giá cố định dự phòng)*"
        )
    else:
        return (
            f"Rất tiếc, ngân hàng hiện chưa có thông tin tỷ giá cho đồng tiền: {currency_code}.\n"
            f"Vui lòng thử lại với các mã ngoại tệ phổ biến như: USD, EUR, JPY, GBP, CNY."
        )
if __name__ == "__main__":
    # Chạy thử nghiệm độc lập
    print("--- Thử nghiệm trực tiếp ---")
    print(get_exchange_rate.invoke({"currency_code": "USD"}))
    print()
    print(get_exchange_rate.invoke({"currency_code": "EUR"}))
    print()
    print(get_exchange_rate.invoke({"currency_code": "CNY"}))