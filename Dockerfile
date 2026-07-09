# Sử dụng Python phiên bản 3.11 slim để giảm kích thước image
FROM python:3.11-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Đặt biến môi trường ngăn Python ghi file pyc và đảm bảo stdout/stderr hiển thị trực tiếp
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy file requirements.txt vào trước để tối ưu hóa cache lớp của Docker
COPY requirements.txt .

# Cập nhật pip và cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn của dự án vào thư mục làm việc
COPY . .

# Chạy script nạp dữ liệu FAQ vào Vector DB ngay trong lúc build image
RUN python scripts/ingest.py

# Mở cổng 8000 (cổng chạy backend FastAPI)
EXPOSE 8000

# Lệnh chạy ứng dụng khi container khởi động
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
