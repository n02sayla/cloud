# Flask Server Dashboard (Port 19191)

本專案是一個遵循 `src/` 與 `test/` 目錄結構分離設計的 Flask 網頁應用程式。

- **`src/`**：存放應用程式核心邏輯與前端模板。
- **`test/`**：存放單元測試案例。

---

## 📂 目錄結構

```
雲端/
├── src/
│   ├── __init__.py      # Flask App 工廠 (create_app)
│   ├── app.py           # 路由邏輯 (Blueprint)
│   └── templates/
│       └── index.html   # 精美網頁控制台首頁
├── test/
│   ├── __init__.py
│   └── test_app.py      # pytest 測試案例
├── venv/                # Python 虛擬環境
├── main.py              # 服務啟動入口 (執行在 Port 19191)
├── requirements.txt     # 相依套件清單 (Flask, pytest)
└── README.md            # 專案說明文件
```

---

## 🛠️ 安裝與設置

1. **啟用虛擬環境** (PowerShell)：
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
2. **安裝所需套件**：
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 啟動 Flask 網頁服務

在專案根目錄下，執行：
```bash
python main.py
```
啟動後，請在瀏覽器中開啟以下網址查看儀表板：
👉 **[http://127.0.0.1:19191](http://127.0.0.1:19191)**

此網頁會自動向後端的 `/api/info` 獲取系統效能數據，並動態呈現在網頁儀表板上。

---

## 🧪 執行單元測試

我們使用 `pytest` 框架進行測試。請確保在**啟用虛擬環境**的狀態下，於根目錄執行：
```bash
pytest
```
測試程式會模擬 HTTP 請求，驗證首頁路由（`/`）以及資料 API（`/api/info`）是否功能正常。

---

## 🐳 Docker / Docker Compose 部署

本專案支援使用 Docker 進行容器化部署。請確保您的系統已安裝並啟動 **Docker Desktop**。

### 1. 啟動 Docker 服務
在 Windows 上，請先點選圖示開啟 **Docker Desktop**，並確認左下角狀態列顯示為綠色的 "Engine Running"（引擎運行中）。

### 2. 使用 Docker Compose 啟動服務
在專案根目錄下，開啟 PowerShell 執行：
```powershell
docker compose up -d --build
```
- `-d`：在背景（Daemon）模式下執行。
- `--build`：每次啟動前重新建置映像檔，確保程式碼為最新版本。

啟動完成後，即可直接在瀏覽器瀏覽儀表板：
👉 **[http://127.0.0.1:19191](http://127.0.0.1:19191)**

### 3. 查看容器狀態與日誌
- **查看目前運行的容器**：
  ```powershell
  docker compose ps
  ```
- **查看容器即時日誌**：
  ```powershell
  docker compose logs -f
  ```

### 4. 停止並移除容器
若要停止服務，執行：
```powershell
docker compose down
```

---

## ☁️ AWS EC2 雲端部署指引

本專案提供一鍵部署腳本 `deploy.ps1`，可直接將程式碼同步到 AWS EC2 並自動啟動容器。

### 前置需求
1. **EC2 主機**：請確認目標 EC2 執行個體已在運作中（`running` 狀態）。
2. **Docker 已安裝**：EC2 主機上已安裝 Docker 與 Docker Compose。
3. **.pem 金鑰**：您持有連線到 EC2 的 SSH 私有金鑰檔案。
4. **安全群組**：EC2 的安全群組（Security Group）需開放以下 **入站規則（Inbound Rule）**：
   - Type: `Custom TCP`
   - Port: `19191`
   - Source: `0.0.0.0/0`（或您指定的 IP 範圍）

### 執行部署腳本
在本機 PowerShell 中執行：
```powershell
.\deploy.ps1 -KeyPath "C:\path\to\your-key.pem"
```
腳本會自動完成以下步驟：
1. SSH 連線至 EC2 並建立部署目錄
2. 將最新的程式碼檔案上傳至遠端主機
3. 在 EC2 上執行 `docker compose up -d --build` 建置並啟動容器

### 部署完成後
即可透過以下網址存取雲端上的儀表板：
👉 **http://54.250.228.196:19191**


