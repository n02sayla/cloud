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
