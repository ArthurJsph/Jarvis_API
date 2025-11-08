"""
Sistema de logging simplificado para o Jarvis CLI
"""

import logging
import sys
from datetime import datetime
from typing import Optional

def setup_logger(name: str, verbose: bool = False) -> logging.Logger:
    """Configura e retorna um logger para o Jarvis"""
    
    # Criar logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    # Evitar duplicação de handlers
    if logger.handlers:
        return logger
    
    # Criar formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if verbose else logging.WARNING)
    console_handler.setFormatter(formatter)
    
    # Adicionar handler ao logger
    logger.addHandler(console_handler)
    
    return logger

class SimpleLogger:
    """Logger simplificado para casos onde logging padrão é muito pesado"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        
    def info(self, message: str):
        if self.verbose:
            self._log("INFO", message)
    
    def error(self, message: str):
        self._log("ERROR", message)
    
    def warning(self, message: str):
        self._log("WARNING", message)
    
    def debug(self, message: str):
        if self.verbose:
            self._log("DEBUG", message)
    
    def _log(self, level: str, message: str):
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {level}: {message}", file=sys.stderr)