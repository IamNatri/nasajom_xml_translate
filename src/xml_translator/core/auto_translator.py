#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classe para tradução automática com Google Translate e overrides manuais
"""

import json
import os
import time
from typing import Optional, Tuple
from pathlib import Path

from ..utils.logger import get_logger


class AutoTranslator:
    """Classe para tradução automática com Google Translate e overrides manuais"""
    
    def __init__(self, config_dir: str = "config"):
        """
        Inicializa o AutoTranslator
        
        Args:
            config_dir: Diretório onde buscar arquivos de configuração
        """
        self.config_dir = Path(config_dir)
        self.overrides_file = self.config_dir / "overrides.json"
        self.translator = None
        self.logger = get_logger(__name__)
        self.load_overrides()
        self.init_translator()
    
    def init_translator(self):
        """Inicializa o tradutor automático"""
        try:
            from googletrans import Translator
            self.translator = Translator()
            self.logger.info("Google Translate inicializado com sucesso")
        except ImportError:
            self.logger.error("googletrans não instalado. Execute: poetry install")
            self.translator = None
        except Exception as e:
            self.logger.error(f"Erro ao inicializar tradutor: {e}")
            self.translator = None
    
    def load_overrides(self):
        """Carrega arquivo de overrides manuais"""
        try:
            if self.overrides_file.exists():
                with open(self.overrides_file, 'r', encoding='utf-8') as f:
                    self.overrides = json.load(f)
                self.logger.info(f"Carregados {len(self.overrides)} overrides de {self.overrides_file}")
            else:
                # Se não existe, inicializar vazio (sem criar arquivo de exemplo)
                self.overrides = {}
                self.logger.info("Nenhum arquivo de overrides encontrado. Usando apenas Google Translate.")
        except Exception as e:
            self.logger.error(f"Erro ao carregar overrides: {e}")
            self.overrides = {}
    
    def save_overrides(self):
        """Salva arquivo de overrides"""
        try:
            # Criar diretório se não existir
            self.config_dir.mkdir(exist_ok=True)
            
            with open(self.overrides_file, 'w', encoding='utf-8') as f:
                json.dump(self.overrides, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"Erro ao salvar overrides: {e}")
    
    def translate_text(self, text: str) -> Optional[str]:
        """
        Traduz texto usando Google Translate
        
        Args:
            text: Texto a ser traduzido
            
        Returns:
            Texto traduzido ou None se falhar
        """
        if not self.translator:
            return None
        
        try:
            # Skip muito curtos ou códigos
            if len(text.strip()) < 2 or (text.isupper() and len(text) < 8):
                return None
            
            result = self.translator.translate(text, src='en', dest='pt')
            translation = result.text.strip()
            
            # Rate limiting
            time.sleep(0.1)
            
            return translation if translation.lower() != text.lower() else None
            
        except Exception as e:
            self.logger.warning(f"Erro na tradução de '{text}': {e}")
            return None
    
    def get_translation(self, text: str, key: str = None) -> Tuple[str, str]:
        """
        Retorna melhor tradução disponível com fonte
        
        Args:
            text: Texto original (usado como chave para overrides)
            key: Chave do elemento XML (para log apenas)
            
        Returns:
            Tupla (tradução, fonte)
        """
        
        # 1. Override manual baseado no texto original (prioridade máxima)
        text_clean = text.strip()
        if text_clean in self.overrides:
            return self.overrides[text_clean], "override"
        
        # 2. Tradução automática do Google
        auto_translation = self.translate_text(text)
        if auto_translation:
            return auto_translation, "google"
        
        # 3. Manter original se nada funcionar
        return text, "original"
    
    def add_override(self, original_text: str, translation: str):
        """
        Adiciona override manual permanente baseado no texto original
        
        Args:
            original_text: Texto original em inglês
            translation: Tradução manual
        """
        try:
            text_clean = original_text.strip()
            self.overrides[text_clean] = translation
            self.save_overrides()
            self.logger.info(f"Override salvo: '{text_clean}' → '{translation}'")
        except Exception as e:
            self.logger.error(f"Erro ao adicionar override: {e}")
    
    def get_stats(self) -> dict:
        """
        Retorna estatísticas do tradutor
        
        Returns:
            Dicionário com estatísticas
        """
        return {
            "overrides_count": len(self.overrides),
            "translator_available": self.translator is not None,
            "config_file": str(self.overrides_file),
            "override_type": "text_based"
        }
    
    def list_overrides(self) -> dict:
        """
        Lista todos os overrides configurados
        
        Returns:
            Dicionário com overrides (texto original → tradução)
        """
        return self.overrides.copy()
