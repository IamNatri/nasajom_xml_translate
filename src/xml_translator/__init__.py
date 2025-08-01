"""
XML Translator - Tradutor de arquivos XML de localização
Traduz arquivos XML de localização do inglês para português (pt-BR)
"""

__version__ = "1.0.0"
__author__ = "Nasajon Systems"
__description__ = "Tradutor automatizado de arquivos XML de localização"

from .core.translator import XMLTranslator
from .core.auto_translator import AutoTranslator

__all__ = ['XMLTranslator', 'AutoTranslator']
