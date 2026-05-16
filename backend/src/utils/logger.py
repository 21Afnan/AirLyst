import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

def get_logger(name: str):
    """
    Creates a standard logger that outputs to both console and a rotating file.
    Always saves logs in the 'backend/logs' directory.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        # 1. FIX THE PATH: Always use the backend/logs folder
        # This file is in backend/src/utils/logger.py -> backend/logs
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        log_dir = BASE_DIR / "logs"
        log_dir.mkdir(exist_ok=True)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # 2. CONSOLE HANDLER (For live debugging)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # 3. ROTATING FILE HANDLER (For permanent history)
        file_handler = RotatingFileHandler(
            log_dir / "pipeline.log", 
            maxBytes=5*1024*1024, 
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger
