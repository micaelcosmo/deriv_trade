import configparser
import os

from logger import BotLogger


logger = BotLogger.get_logger(__name__)


class Config:
    """Configurações centrais do bot lidas do arquivo user.cfg."""

    _config = configparser.ConfigParser()
    _config_file = "user.cfg"

    if not os.path.exists(_config_file):
        logger.critical(f"Arquivo '{_config_file}' não encontrado.")
        raise FileNotFoundError(f"Arquivo '{_config_file}' não encontrado.")

    _config.read(_config_file)

    TOKEN = _config.get("DERIV", "TOKEN", fallback="").strip(' "\'\n\r')
    APP_ID = _config.get("DERIV", "APP_ID", fallback="1089").strip(' "\'\n\r')
    SYMBOL = _config.get("DERIV", "SYMBOL", fallback="cryBTCUSD").strip(' "\'\n\r')
    STAKE = _config.getfloat("DERIV", "STAKE", fallback=1.0)
    DURATION = _config.getint("DERIV", "DURATION", fallback=1)
    DURATION_UNIT = _config.get("DERIV", "DURATION_UNIT", fallback="m").strip(' "\'\n\r')
    MIN_AVG_CANDLE_BODY_SIZE = _config.getfloat("DERIV", "MIN_AVG_CANDLE_BODY_SIZE", fallback=0.5)
    TEST_MODE = _config.getboolean("DERIV", "TEST_MODE", fallback=True)
    USE_TEST_ACCOUNT = _config.getboolean("DERIV", "USE_TEST_ACCOUNT", fallback=True)

    # Use a standard app_id for API connection (token handles authentication)
    # For test/demo account: ws.derivws.com
    # For real account: ws.binaryws.com
    # Personal tokens usually need a generic app_id, not the custom one
    _ws_url = "wss://ws.derivws.com/websockets/v3" if USE_TEST_ACCOUNT else "wss://ws.binaryws.com/websockets/v3"
    API_URL = f"{_ws_url}?app_id=1089"
    
    # Log configuration on startup
    logger.info(f"Configuração: TEST_MODE={TEST_MODE}, USE_TEST_ACCOUNT={USE_TEST_ACCOUNT}")