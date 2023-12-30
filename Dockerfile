# Sử dụng image Python 3.8.2
FROM python:3.8.2

# Đặt biến môi trường không yêu cầu khi chạy trong môi trường sản xuất
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Tạo và di chuyển vào thư mục /app
WORKDIR /app

# Sao chép file requirements.txt vào thư mục /app/
COPY requirements.txt /app/

# Cài đặt các dependencies từ file requirements.txt
RUN pip install -r requirements.txt

# Sao chép toàn bộ nội dung của thư mục hiện tại vào thư mục /app/ trên container
COPY . /app/

# Chạy lệnh migrate khi container khởi chạy
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
