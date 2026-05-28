# ─── 基礎映像 ────────────────────────────────────────────────
FROM python:3.12-slim

# ─── 工作目錄 ────────────────────────────────────────────────
WORKDIR /app

# ─── 安裝相依套件（先複製 requirements 以利用 Docker 快取）───
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ─── 複製專案原始碼 ──────────────────────────────────────────
COPY src/ ./src/
COPY main.py .

# ─── 開放 Flask 使用的連接埠 ─────────────────────────────────
EXPOSE 19191

# ─── 啟動指令 ────────────────────────────────────────────────
CMD ["python", "main.py"]
