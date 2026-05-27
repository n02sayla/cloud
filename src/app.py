import os
import sys
import platform
import time
from flask import Blueprint, render_template, jsonify

# 建立 Blueprint 路由模組
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """首頁路由 - 渲染儀表板頁面"""
    return render_template('index.html')

@bp.route('/api/info')
def api_info():
    """API 路由 - 獲取系統資訊與伺服器遙測數據"""
    # 稍微模擬一些隨機系統負載資訊，使儀表板看起来是活的
    import random
    
    # 獲取基礎平台資訊
    platform_info = {
        "python_version": platform.python_version(),
        "os_name": platform.system(),
        "os_version": platform.release(),
        "machine": platform.machine(),
        "cwd": os.getcwd(),
        "python_exe": sys.executable
    }
    
    # 模擬硬體負載資料
    telemetry = {
        "cpu_usage": random.randint(15, 65),
        "ram_usage": random.randint(40, 85),
        "disk_usage": random.randint(25, 45),
        "uptime_seconds": int(time.time()) % 86400, # 虛擬的今日運行秒數
        "port": 19191,
        "status": "Healthy"
    }
    
    return jsonify({
        "status": "success",
        "timestamp": int(time.time()),
        "platform": platform_info,
        "telemetry": telemetry
    })

@bp.route('/feature1')
def feature1():
    """功能一 - 早上看股票"""
    return "早上要看股票"

@bp.route('/feature2')
def feature2():
    """功能二 - 找下午上班的公司"""
    return "要找下午上班的公司"

@bp.route('/api/restart', methods=['POST'])
def api_restart():
    """API 路由 - 觸發伺服器重啟"""
    from flask import current_app
    import threading
    
    if current_app.config.get("TESTING"):
        return jsonify({
            "status": "restarting_skipped",
            "message": "Testing mode: Restart skipped."
        })
        
    def perform_restart():
        time.sleep(1.0)
        # 執行程式重啟，用新行程取代目前行程
        os.execv(sys.executable, [sys.executable] + sys.argv)
        
    threading.Thread(target=perform_restart).start()
    return jsonify({
        "status": "restarting",
        "message": "Server is restarting..."
    })
