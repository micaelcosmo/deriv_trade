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
    DURATION = _config.getint("DERIV", "DURATION", fallback=3)
    DURATION_UNIT = _config.get("DERIV", "DURATION_UNIT", fallback="m").strip(' "\'\n\r')

    API_URL = f"wss://ws.binaryws.com/websockets/v3?app_id={APP_ID}"