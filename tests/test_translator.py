#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes para o XML Translator
"""

import pytest
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from xml_translator.core.auto_translator import AutoTranslator
from xml_translator.core.translator import XMLTranslator


class TestAutoTranslator:
    """Testes para AutoTranslator"""
    
    def test_init(self):
        """Testa inicialização do AutoTranslator"""
        translator = AutoTranslator("config")
        assert translator is not None
        assert hasattr(translator, 'overrides')
    
    def test_get_translation_without_override(self):
        """Testa tradução sem override"""
        translator = AutoTranslator("config")
        # Simular sem tradutor Google para testar fallback
        translator.translator = None
        translation, source = translator.get_translation("Hello", "test_key")
        assert translation == "Hello"
        assert source == "original"


class TestXMLTranslator:
    """Testes para XMLTranslator"""
    
    def test_init(self):
        """Testa inicialização do XMLTranslator"""
        translator = XMLTranslator("config")
        assert translator is not None
        assert hasattr(translator, 'translator')
        assert hasattr(translator, 'logger')


if __name__ == "__main__":
    pytest.main([__file__])
