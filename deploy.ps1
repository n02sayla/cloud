# ============================================================
#  Cloud Dashboard - AWS EC2 One-Click Deploy Script
#  Usage: .\deploy.ps1 -KeyPath "C:\path\to\your-key.pem"
# ============================================================

param(
    [Parameter(Mandatory=$true, HelpMessage="Path to your EC2 .pem private key file")]
    [string]$KeyPath
)

# ─── 目標設定 ────────────────────────────────────────────────
$EC2_HOST = "54.250.228.196"
$EC2_USER = "ec2-user"
$REMOTE_DIR = "/home/ec2-user/cloud-dashboard"
$SSH_OPTS = "-o StrictHostKeyChecking=no -o ConnectTimeout=15"

# ─── 確認金鑰檔案存在 ────────────────────────────────────────
if (-not (Test-Path $KeyPath)) {
    Write-Host "[ERROR] .pem 金鑰檔案不存在: $KeyPath" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Cloud Dashboard - EC2 Deploy Script" -ForegroundColor Cyan
Write-Host "  Target: $EC2_USER@$EC2_HOST" -ForegroundColor Cyan
Write-Host "  Remote: $REMOTE_DIR" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ─── 步驟 1: 在遠端建立目錄 ────────────────────────────────
Write-Host "[1/4] 正在遠端建立部署目錄..." -ForegroundColor Yellow
$mkdirCmd = "mkdir -p $REMOTE_DIR/src/templates"
ssh $SSH_OPTS.Split(" ") -i $KeyPath "$EC2_USER@$EC2_HOST" $mkdirCmd
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] 無法連線到 EC2 主機，請確認金鑰與安全群組設定。" -ForegroundColor Red
    exit 1
}
Write-Host "[1/4] 目錄建立完成。" -ForegroundColor Green

# ─── 步驟 2: 複製專案檔案 ───────────────────────────────────
Write-Host ""
Write-Host "[2/4] 正在將專案檔案同步到 EC2 主機..." -ForegroundColor Yellow

# 取得腳本所在目錄（即專案根目錄）
$ProjectRoot = $PSScriptRoot

# 複製各項目
$filesToCopy = @(
    @{ Local = "$ProjectRoot\main.py"; Remote = "$REMOTE_DIR/main.py" },
    @{ Local = "$ProjectRoot\requirements.txt"; Remote = "$REMOTE_DIR/requirements.txt" },
    @{ Local = "$ProjectRoot\Dockerfile"; Remote = "$REMOTE_DIR/Dockerfile" },
    @{ Local = "$ProjectRoot\docker-compose.yml"; Remote = "$REMOTE_DIR/docker-compose.yml" }
)

foreach ($file in $filesToCopy) {
    scp $SSH_OPTS.Split(" ") -i $KeyPath $file.Local "$EC2_USER@$EC2_HOST`:$($file.Remote)"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] 無法複製 $($file.Local)" -ForegroundColor Red
        exit 1
    }
}

# 複製 src 資料夾
scp $SSH_OPTS.Split(" ") -i $KeyPath -r "$ProjectRoot\src\__init__.py" "$EC2_USER@$EC2_HOST`:$REMOTE_DIR/src/__init__.py"
scp $SSH_OPTS.Split(" ") -i $KeyPath -r "$ProjectRoot\src\app.py" "$EC2_USER@$EC2_HOST`:$REMOTE_DIR/src/app.py"
scp $SSH_OPTS.Split(" ") -i $KeyPath -r "$ProjectRoot\src\templates\index.html" "$EC2_USER@$EC2_HOST`:$REMOTE_DIR/src/templates/index.html"

Write-Host "[2/4] 檔案同步完成。" -ForegroundColor Green

# ─── 步驟 3: 在 EC2 上建置並啟動 Docker 容器 ─────────────────
Write-Host ""
Write-Host "[3/4] 正在 EC2 遠端建置 Docker 映像並啟動容器..." -ForegroundColor Yellow

$remoteCmd = @"
cd $REMOTE_DIR
docker compose down 2>/dev/null || true
docker compose up -d --build
"@

ssh $SSH_OPTS.Split(" ") -i $KeyPath "$EC2_USER@$EC2_HOST" $remoteCmd
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Docker Compose 在遠端執行失敗。" -ForegroundColor Red
    Write-Host "請確認 EC2 上已安裝 Docker，並且安全群組已開放 Port 19191。" -ForegroundColor Yellow
    exit 1
}
Write-Host "[3/4] 容器啟動完成。" -ForegroundColor Green

# ─── 步驟 4: 顯示結果 ────────────────────────────────────────
Write-Host ""
Write-Host "[4/4] 驗證容器狀態..." -ForegroundColor Yellow
ssh $SSH_OPTS.Split(" ") -i $KeyPath "$EC2_USER@$EC2_HOST" "docker compose -f $REMOTE_DIR/docker-compose.yml ps"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  部署成功！" -ForegroundColor Green
Write-Host ""
Write-Host "  請透過瀏覽器開啟以下網址：" -ForegroundColor White
Write-Host "  http://$EC2_HOST`:19191" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
