import logging
import os
from datetime import datetime


class BotLogger:
    """Configuração centralizada de logging para a automação."""

    @staticmethod
    def get_logger(module_name: str) -> logging.Logger:
        logger = logging.getLogger(module_name)
        
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            
            log_dir = "logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            date_str = datetime.now().strftime("%Y-%m-%d")
            log_file = os.path.join(log_dir, f"bot_deriv_{date_str}.log")
            
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            console_handler = logging.StreamHandler()
            
            formatter = logging.Formatter(
                fmt="%(asctime)s %(filename)s %(levelname)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
            
        return logger