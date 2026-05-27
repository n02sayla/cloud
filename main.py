import sys
from src import create_app

app = create_app()

if __name__ == "__main__":
    print("=" * 50)
    print(" Flask Server starting up...")
    print("  - Address: http://127.0.0.1:19191")
    print("  - Structure: src/ (App logic) | test/ (Test suite)")
    print("=" * 50)
    
    try:
        # 啟動 Flask 伺服器，設定連接埠為 19191
        app.run(host="0.0.0.0", port=19191, debug=True)
    except KeyboardInterrupt:
        print("\n Server stopped by user.")
        sys.exit(0)
