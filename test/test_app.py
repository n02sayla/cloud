import pytest
from src import create_app

@pytest.fixture
def app():
    """定義測試用的 Flask App 實例"""
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture
def client(app):
    """定義 Flask 測試客戶端"""
    return app.test_client()

def test_index_route(client):
    """驗證首頁路由 (/) 是否能正常回傳 200 且包含預期標題"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Flask Server" in response.data

def test_api_info_route(client):
    """驗證 API 路由 (/api/info) 的回傳狀態與結構"""
    response = client.get('/api/info')
    assert response.status_code == 200
    
    json_data = response.get_json()
    assert json_data["status"] == "success"
    assert "platform" in json_data
    assert "telemetry" in json_data
    
    # 驗證部署 Port 號符合要求的 19191
    assert json_data["telemetry"]["port"] == 19191
    assert "cpu_usage" in json_data["telemetry"]
    assert "ram_usage" in json_data["telemetry"]

def test_feature1_route(client):
    """驗證 feature1 路由是否正確回傳中文"""
    response = client.get('/feature1')
    assert response.status_code == 200
    assert "早上要看股票" in response.data.decode('utf-8')

def test_feature2_route(client):
    """驗證 feature2 路由是否正確回傳中文"""
    response = client.get('/feature2')
    assert response.status_code == 200
    assert "要找下午上班的公司" in response.data.decode('utf-8')

def test_stress_api_flow(client):
    """驗證壓力測試 API 的完整工作流程 (狀態查詢、啟動、停止)"""
    # 1. 檢查初始狀態
    response = client.get('/api/stress/status')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "success"
    assert "stress_status" in json_data
    assert json_data["stress_status"]["active"] is False

    # 2. 啟動壓力測試 (啟動 1 核心，持續 10 秒)
    response = client.post('/api/stress/start', json={"cores": 1, "duration": 10})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "success"
    assert json_data["stress_status"]["active"] is True
    assert json_data["stress_status"]["cores"] == 1
    assert json_data["stress_status"]["duration"] == 10

    # 3. 再一次檢查狀態，確保維持 active
    response = client.get('/api/stress/status')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["stress_status"]["active"] is True

    # 4. 停止壓力測試
    response = client.post('/api/stress/stop')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "success"
    assert json_data["stress_status"]["active"] is False

    # 5. 最後驗證狀態已重置為 inactive
    response = client.get('/api/stress/status')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["stress_status"]["active"] is False

