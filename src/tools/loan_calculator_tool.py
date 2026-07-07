from langchain_core.tools import tool

# Hàm định dạng tiền việt nam
def format_vnd(amount:float)->str:
    return f'{amount:,.0f} VNĐ'.replace(',', '.')

# Tính toán khoản vay

@tool("calculate_loan",description="Tính toán số tiền phải trả góp hàng tháng (gốc + lãi), tổng số tiền lãi và tổng số tiền phải trả cho một khoản vay ngân hàng dựa trên số tiền gốc, lãi suất năm (%) và số tháng vay."  )
def calculator_loan(principal:float, rate:float, months:int)->str:
    monthly_rate = (rate / 100) / 12
        
    if monthly_rate == 0:
        monthly_payment = principal / months
    else:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / (((1 + monthly_rate) ** months) - 1)
            
    total_payment = monthly_payment * months
    total_interest = total_payment - principal
    return (
            f"=== BẢNG TÍNH TOÁN KHOẢN VAY ===\n"
            f"- Số tiền gốc vay: {format_vnd(principal)}\n"
            f"- Lãi suất: {rate}%/năm\n"
            f"- Kỳ hạn vay: {months} tháng (~{months/12:.1f} năm)\n"
            f"---------------------------------\n"
            f"- Số tiền trả hàng tháng (gốc + lãi): {format_vnd(monthly_payment)}\n"
            f"- Tổng số tiền phải trả: {format_vnd(total_payment)}\n"
            f"- Tổng số tiền lãi phải trả: {format_vnd(total_interest)}\n"
            f"================================="
        )

# Tính tiền lãi tiết kiệm

@tool("calculate_savings_interest",description="Tính lãi suất tiền gửi tiết kiệm dựa trên số tiền gửi, lãi suất năm và số tháng gửi."  )
def calculator_savings_interest(principal:float, rate:float, months:int)->str:
    interest = principal * (rate / 100) * (months / 12)
    total = principal + interest       
    return (
            f"=== BẢNG TÍNH TOÁN LÃI TIẾT KIỆM ===\n"
            f"- Số tiền gửi gốc: {format_vnd(principal)}\n"
            f"- Lãi suất áp dụng: {rate}%/năm\n"
            f"- Kỳ hạn gửi: {months} tháng\n"
            f"-------------------------------------\n"
            f"- Tiền lãi nhận được cuối kỳ: {format_vnd(interest)}\n"
            f"- Tổng tiền nhận được (gốc + lãi): {format_vnd(total)}\n"
            f"====================================="
        )

if __name__ == "__main__":
    # Test thử nghiệm độc lập
    print("--- Test Khoản vay ---")
    print(calculator_loan.invoke({"principal": 500000000, "rate": 8.5, "months": 120}))
    
    print("\n--- Test Gửi tiết kiệm ---")
    print(calculator_savings_interest.invoke({"principal": 100000000, "rate": 6.0, "months": 12}))