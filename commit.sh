#!/bin/bash
# Deriv Trading Bot - Git Commit Script v0.2.0
# Usage: ./commit.sh or bash commit.sh

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🤖 Deriv Trading Bot - Git Commit${NC}"
echo -e "${YELLOW}Version 0.2.0${NC}"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo -e "${RED}❌ Git not initialized in this directory${NC}"
    echo "Run: git init"
    exit 1
fi

# Add all files
echo -e "${GREEN}✓ Adding all changes...${NC}"
git add -A

# Show what will be committed
echo -e "${GREEN}✓ Files staged:${NC}"
git diff --cached --name-only

# Commit with detailed message
echo ""
echo -e "${YELLOW}📝 Creating commit...${NC}"

git commit -m "feat(v0.2.0): Full-stack trading bot with real-time dashboard

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

## Breaking Changes
- None (first functional release)

## Dependencies
- websockets>=12.0
- pytest>=7.0.0
- flask
- flask-socketio
- python-socketio
- python-engineio

## Files Changed
- dashboard.py: Flask app with Socket.IO
- main.py: BotRunner orchestration
- trader.py: TradingEngine implementation
- connection.py: WebSocket client
- config.py: Configuration loader
- index.html: Dashboard UI
- user.cfg: Configuration template
- requirements.txt: Dependencies

## Next Steps (v0.3.0)
- Multiple strategies
- Risk management (stop-loss, take-profit)
- Trade history database
- Advanced analytics
- Notifications (Telegram/Email)

## Contributors
- Initial development and testing

## Related Issues
- Resolves: Full trading bot implementation
- Fixes: API authentication, dashboard rendering, real-time updates

## Deployment Notes
1. Copy user.cfg.exemple to user.cfg
2. Update TOKEN with Deriv API token
3. Run: python dashboard.py
4. Visit: http://127.0.0.1:5000

---
Release: v0.2.0
Date: 2026-04-18
Status: Stable
"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Commit successful!${NC}"
    echo ""
    echo -e "${YELLOW}📊 Commit Details:${NC}"
    git log -1 --oneline
    echo ""
    echo -e "${YELLOW}📌 Next Steps:${NC}"
    echo "1. Review commit: git log -1 -p"
    echo "2. Push to remote: git push origin main"
    echo "3. Create GitHub release with RELEASE_NOTES_v0.2.0.md"
    echo "4. Tag version: git tag v0.2.0"
    echo "5. Push tags: git push origin --tags"
else
    echo -e "${RED}❌ Commit failed${NC}"
    exit 1
fi
