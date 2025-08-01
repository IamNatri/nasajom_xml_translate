#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de logging para o tradutor XML
"""

import logging
import os
from datetime import datetime
from pathlib import Path


def setup_logging(log_dir: str = "logs") -> logging.Logger:
    """
    Configura sistema de logging
    
    Args:
        log_dir: Diretório onde salvar os logs
        
    Returns:
        Logger configurado
    """
    # Criar diretório de logs se não existir
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    # Nome do arquivo com data
    log_filename = log_path / f"xml_translator_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)


def get_logger(name: str = None) -> logging.Logger:
    """
    Obtém logger para módulo específico
    
    Args:
        name: Nome do módulo
        
    Returns:
        Logger configurado
    """
    return logging.getLogger(name or __name__)
