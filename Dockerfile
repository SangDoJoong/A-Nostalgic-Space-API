FROM python:3.10

# 패키지 업데이트 및 PostgreSQL 및 PostGIS 설치
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql \
        postgresql-contrib \
        postgis \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# 애플리케이션 종속성 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스코드 복사
COPY . .

# 컨테이너 실행 명령 설정
CMD ["python", "app/main.py", "--APP_ENV=dev"]
