# Changelog

## [0.2.0] - 2026-04-18

### Added
- ✅ Real WebSocket integration with Deriv API
- ✅ Contrarian strategy implementation for cryptocurrency trading
- ✅ Live trading dashboard with candlestick chart (Lightweight Charts)
- ✅ Real-time Socket.IO communication between bot and frontend
- ✅ Test mode for safe analysis without executing trades
- ✅ Dual account support (test/demo and real accounts)
- ✅ Enhanced logging with time-stamped events
- ✅ Contract result monitoring with profit/loss tracking
- ✅ API token authentication with permission handling
- ✅ Error handling and recovery mechanisms

### Features
- **Dashboard (`dashboard.py`)**: Flask + Socket.IO web interface with live updates
- **Trading Engine (`main.py`, `trader.py`)**: Orchestrates market analysis and trade execution
- **Contrarian Strategy (`strategy.py`)**: Analyzes candlestick patterns for buy/sell signals
- **WebSocket Connection (`connection.py`)**: Manages Deriv API communication
- **Configuration (`config.py`)**: Centralized settings from `user.cfg`
- **Logging (`logger.py`)**: Real-time log streaming to frontend

### Configuration
- `user.cfg`: Main configuration file (token, symbol, stake, duration, test mode)
- `user.cfg.exemple`: Configuration template for new users
- Test Mode: `TEST_MODE = True` for analysis only, `False` for live trading
- Account Type: `USE_TEST_ACCOUNT = True` for demo, `False` for real account

### Fixed
- SocketIO async_mode now uses 'threading' instead of eventlet
- Template folder correctly configured in Flask
- Lightweight Charts library version fixed and error handling improved
- API URL correctly routes to test/demo or real accounts
- Token authentication improved with better error messages

### Technical Details
- Python 3.10+
- WebSocket via `websockets` library
- Web framework: Flask + flask-socketio
- Frontend: HTML5 + JavaScript with Lightweight Charts
- Async/await pattern throughout for non-blocking operations
- Real-time event streaming via Socket.IO

### Known Limitations
- Test mode: Simulates trades without executing (for safe testing)
- Requires valid Deriv API token with Trade permissions
- Bot analyzes only 5 most recent candles (1-minute intervals)
- Fixed contract duration (configurable)

### Next Steps (v0.3.0)
- Multiple strategy implementations
- Risk management (stop-loss, take-profit)
- Performance metrics and backtesting
- Database for trade history
- Notifications (email, Telegram)
- Advanced analytics dashboard

---

## [0.1.0] - 2026-04-18

### Initial Release
- Project setup and structure
- Basic configuration system
- Logger implementation
- Documentation
