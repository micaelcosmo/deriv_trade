# Deriv Trading Bot - Git Commit Script v0.2.0 (Windows)
# Usage: .\commit.ps1

Write-Host "========================================" -ForegroundColor Yellow
Write-Host "🤖 Deriv Trading Bot - Git Commit" -ForegroundColor Yellow
Write-Host "Version 0.2.0" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "❌ Git not initialized in this directory" -ForegroundColor Red
    Write-Host "Run: git init" -ForegroundColor Yellow
    exit 1
}

# Add all files
Write-Host "✓ Adding all changes..." -ForegroundColor Green
git add -A

# Show what will be committed
Write-Host "✓ Files staged:" -ForegroundColor Green
git diff --cached --name-only

Write-Host ""
Write-Host "📝 Creating commit..." -ForegroundColor Yellow

$commitMessage = @"
feat(v0.2.0): Full-stack trading bot with real-time dashboard

## Features
- ✅ Complete WebSocket integration with Deriv API
- ✅ Real-time trading dashboard with Lightweight Charts
- ✅ Contrarian strategy for cryptocurrency market analysis
- ✅ Live logging and Socket.IO real-time updates
- ✅ Test mode for safe backtesting
- ✅ Dual account support (demo/real)
- ✅ Automated trade execution with P&L tracking

## Technical Improvements
- Fixed Flask template folder configuration
- Corrected SocketIO async_mode to 'threading'
- Improved chart library loading with version pinning
- Enhanced WebSocket error handling and reconnection
- Better logging with timestamps and module info
- Configuration system with environment-specific settings

## Architecture
- BotRunner: Main orchestrator
- TradingEngine: Market data collection and trade execution
- ContrarianStrategy: Signal generation algorithm
- DerivClient: WebSocket API connection
- Dashboard: Flask + Socket.IO web interface

## Configuration
- user.cfg: Token, symbol, stake, duration, test mode
- Support for test account (USE_TEST_ACCOUNT=True)
- Easy switching to real account (one config change)

## Security
- Token stored locally (git ignored)
- No credentials in code
- SSL/TLS API connections
- Token-based authentication only

## Testing
- Test mode (TEST_MODE=True) for analysis without trades
- Real mode (TEST_MODE=False) for live trading
- Live dashboard at http://127.0.0.1:5000

## Known Limitations
- Analyzes 5 most recent candles (1-minute)
- Fixed contract duration (configurable)
- Requires Deriv API token with Trade permission
- Test mode simulates without execution

## Files Changed
- dashboard.py: Flask app with Socket.IO
- main.py: BotRunner orchestration
- trader.py: TradingEngine implementation
- connection.py: WebSocket client
- config.py: Configuration loader
- index.html: Dashboard UI
- user.cfg: Configuration template
- requirements.txt: Dependencies

## Deployment Notes
1. Copy user.cfg.exemple to user.cfg
2. Update TOKEN with Deriv API token
3. Run: python dashboard.py
4. Visit: http://127.0.0.1:5000

---
Release: v0.2.0 | Date: 2026-04-18 | Status: Stable
"@

git commit -m $commitMessage

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Commit successful!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 Commit Details:" -ForegroundColor Yellow
    git log -1 --oneline
    Write-Host ""
    Write-Host "📌 Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Review commit: git log -1 -p"
    Write-Host "2. Push to remote: git push origin main"
    Write-Host "3. Create GitHub release with RELEASE_NOTES_v0.2.0.md"
    Write-Host "4. Tag version: git tag v0.2.0"
    Write-Host "5. Push tags: git push origin --tags"
} else {
    Write-Host "❌ Commit failed" -ForegroundColor Red
    exit 1
}
