from flask import Flask

def create_app():
    """Flask 應用程式建立工廠"""
    app = Flask(__name__)
    
    # 註冊藍圖 (Blueprint) 以模組化管理路由
    from src.app import bp
    app.register_blueprint(bp)
    
    return app
