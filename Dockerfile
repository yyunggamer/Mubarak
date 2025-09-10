# 1) Use Alpine-based Python image
FROM python:3.11-alpine

#  2) Environment variables (no pyc files, unbuffered logs)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3) Create a non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# 4) Set working directory
WORKDIR /app

# 5) Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6) Copy app code
COPY . .

# 7) Use non-root user
USER appuser

# 8) Expose Flask port
EXPOSE 8000

# 9) Run the app
CMD ["python", "app.py"]
