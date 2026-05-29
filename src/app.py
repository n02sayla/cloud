import os
import sys
import platform
import time
import random
import multiprocessing
import threading
from flask import Blueprint, render_template, jsonify, request

# Graceful import of psutil
try:
    import psutil
except ImportError:
    psutil = None

# 建立 Blueprint 路由模組
bp = Blueprint('main', __name__)

def cpu_stress_worker():
    """CPU 壓力測試工作元 - 跑一個緊密迴圈消耗 CPU"""
    while True:
        # 緊密迴圈
        pass

class StressManager:
    def __init__(self):
        self.active_processes = []
        self.lock = threading.Lock()
        self.start_time = 0
        self.duration = 0
        self.num_cores = 0
        self.timer_thread = None

    def start_stress(self, cores, duration_sec):
        with self.lock:
            # 停止現有測試
            self._stop_stress_no_lock()

            self.num_cores = cores
            self.duration = duration_sec
            self.start_time = time.time()

            # 啟動 CPU 密集多處理程序
            for _ in range(cores):
                p = multiprocessing.Process(target=cpu_stress_worker)
                p.daemon = True
                p.start()
                self.active_processes.append(p)

            # 設定自動停止計時器
            if duration_sec > 0:
                self.timer_thread = threading.Thread(
                    target=self._wait_and_stop,
                    args=(duration_sec, self.active_processes.copy())
                )
                self.timer_thread.daemon = True
                self.timer_thread.start()

    def stop_stress(self):
        with self.lock:
            self._stop_stress_no_lock()

    def _stop_stress_no_lock(self):
        for p in self.active_processes:
            try:
                if p.is_alive():
                    p.terminate()
                    p.join(timeout=0.5)
            except Exception:
                pass
        self.active_processes = []
        self.num_cores = 0
        self.duration = 0
        self.start_time = 0

    def _wait_and_stop(self, duration_sec, processes):
        time.sleep(duration_sec)
        with self.lock:
            # 只有在目前程序與剛啟動的程序一致時才停止 (避免重疊)
            is_current = all(p in self.active_processes for p in processes)
            if is_current:
                self._stop_stress_no_lock()

    def get_status(self):
        with self.lock:
            # 清理已結束的程序
            alive_count = sum(1 for p in self.active_processes if p.is_alive())
            if alive_count == 0 and len(self.active_processes) > 0:
                self.active_processes = []
                self.num_cores = 0
                self.duration = 0
                self.start_time = 0
            
            is_active = len(self.active_processes) > 0
            elapsed = int(time.time() - self.start_time) if is_active else 0
            remaining = max(0, self.duration - elapsed) if (is_active and self.duration > 0) else 0

            max_cores = multiprocessing.cpu_count()

            return {
                "active": is_active,
                "cores": self.num_cores,
                "duration": self.duration,
                "elapsed": elapsed,
                "remaining": remaining,
                "max_system_cores": max_cores
            }

# 全域壓力測試管理器
stress_manager = StressManager()

@bp.route('/')
def index():
    """首頁路由 - 渲染儀表板頁面"""
    return render_template('index.html')

@bp.route('/api/info')
def api_info():
    """API 路由 - 獲取系統資訊與伺服器遙測數據"""
    # 獲取基礎平台資訊
    platform_info = {
        "python_version": platform.python_version(),
        "os_name": platform.system(),
        "os_version": platform.release(),
        "machine": platform.machine(),
        "cwd": os.getcwd(),
        "python_exe": sys.executable
    }
    
    # 嘗試取得真實系統硬體負載資料
    if psutil is not None:
        try:
            cpu_usage = int(psutil.cpu_percent(interval=None))
            ram_usage = int(psutil.virtual_memory().percent)
            cwd = os.getcwd()
            drive = os.path.splitdrive(cwd)[0] or '/'
            disk_usage = int(psutil.disk_usage(drive).percent)
        except Exception:
            cpu_usage = random.randint(15, 65)
            ram_usage = random.randint(40, 85)
            disk_usage = random.randint(25, 45)
    else:
        cpu_usage = random.randint(15, 65)
        ram_usage = random.randint(40, 85)
        disk_usage = random.randint(25, 45)
        
    telemetry = {
        "cpu_usage": cpu_usage,
        "ram_usage": ram_usage,
        "disk_usage": disk_usage,
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

@bp.route('/api/stress/start', methods=['POST'])
def api_stress_start():
    """API 路由 - 啟動伺服器端 CPU 壓力測試"""
    data = request.get_json() or {}
    
    # 支援 JSON 或者是 query 參數
    cores = data.get('cores') or request.args.get('cores', 1, type=int)
    duration = data.get('duration') or request.args.get('duration', 30, type=int)
    
    try:
        cores = int(cores)
        duration = int(duration)
    except (ValueError, TypeError):
        cores = 1
        duration = 30
        
    max_cores = multiprocessing.cpu_count()
    if cores < 1:
        cores = 1
    elif cores > max_cores:
        cores = max_cores
        
    if duration < 0:
        duration = 0 # 0 代表無限期
        
    stress_manager.start_stress(cores, duration)
    return jsonify({
        "status": "success",
        "message": f"Successfully started CPU stress test with {cores} cores for {duration} seconds.",
        "stress_status": stress_manager.get_status()
    })

@bp.route('/api/stress/stop', methods=['POST'])
def api_stress_stop():
    """API 路由 - 停止伺服器端 CPU 壓力測試"""
    stress_manager.stop_stress()
    return jsonify({
        "status": "success",
        "message": "Stopped CPU stress test.",
        "stress_status": stress_manager.get_status()
    })

@bp.route('/api/stress/status', methods=['GET'])
def api_stress_status():
    """API 路由 - 獲取伺服器端 CPU 壓力測試狀態"""
    return jsonify({
        "status": "success",
        "stress_status": stress_manager.get_status()
    })

@bp.route('/api/restart', methods=['POST'])
def api_restart():
    """API 路由 - 觸發伺服器重啟"""
    from flask import current_app
    
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
