#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classe principal para tradução de arquivos XML
"""

import xml.etree.ElementTree as ET
import os
from typing import Dict, List, Optional
from pathlib import Path

from .auto_translator import AutoTranslator
from ..utils.logger import get_logger


class XMLTranslator:
    """Classe principal para tradução de arquivos XML"""
    
    def __init__(self, config_dir: str = "config"):
        """
        Inicializa o XMLTranslator
        
        Args:
            config_dir: Diretório de configurações
        """
        self.translator = AutoTranslator(config_dir)
        self.logger = get_logger(__name__)
    
    def load_xml(self, file_path: str) -> ET.ElementTree:
        """
        Carrega arquivo XML
        
        Args:
            file_path: Caminho para o arquivo XML
            
        Returns:
            Árvore XML carregada
        """
        try:
            tree = ET.parse(file_path)
            self.logger.info(f"XML carregado com sucesso: {file_path}")
            return tree
        except ET.ParseError as e:
            error_msg = f"Erro ao carregar XML '{file_path}': {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Erro inesperado ao carregar XML '{file_path}': {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
    
    def extract_strings(self, tree: ET.ElementTree) -> List[Dict]:
        """
        Extrai todas as strings para traduzir do XML
        
        Args:
            tree: Árvore XML
            
        Returns:
            Lista de dicionários com informações das strings
        """
        root = tree.getroot()
        strings = []
        
        def extract_recursive(element, path=""):
            for child in element:
                tag_name = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                current_path = f"{path}/{tag_name}" if path else tag_name
                
                if tag_name == 'string':
                    key = child.get('key')
                    text = child.text or ""
                    if text.strip():  
                        strings.append({
                            'key': key,
                            'text': text,
                            'path': current_path
                        })
                elif tag_name == 'group':
                    group_name = child.get('name', '')
                    new_path = f"{current_path}[{group_name}]" if group_name else current_path
                    extract_recursive(child, new_path)
                elif tag_name == 'localization':
                    extract_recursive(child, current_path)
        
        extract_recursive(root)
        self.logger.info(f"Extraídas {len(strings)} strings do XML")
        return strings
    
    def process_translations(self, strings: List[Dict]) -> Dict[str, str]:
        """
        Processa traduções automaticamente
        
        Args:
            strings: Lista de strings extraídas
            
        Returns:
            Dicionário com traduções
        """
        translations = {}
        
        print(f"Processando {len(strings)} strings...")
        
        override_count = 0
        google_count = 0
        original_count = 0
        
        for string_data in strings:
            key = string_data['key']
            text = string_data['text']
            
            # Obter tradução automática
            translation, source = self.translator.get_translation(text, key)
            
            # Contar por fonte
            if source == "override":
                override_count += 1
            elif source == "google":
                google_count += 1
            else:
                original_count += 1
            
            translations[key] = translation
            
            # Log apenas erros críticos
            if source == "original" and self.translator.translator:
                self.logger.warning(f"Mantido original para '{key}': '{text}'")
        
        # Relatório final
        print(f"✓ Processadas: {len(translations)} strings")
        if override_count > 0:
            print(f"  - Overrides: {override_count}")
        print(f"  - Google Translate: {google_count}")
        if original_count > 0:
            print(f"  - Mantidos originais: {original_count}")
        
        self.logger.info(f"Tradução concluída: {len(translations)} strings processadas "
                        f"(overrides: {override_count}, google: {google_count}, originais: {original_count})")
        return translations
    
    def apply_translations(self, tree: ET.ElementTree, translations: Dict[str, str]) -> ET.ElementTree:
        """
        Aplica as traduções ao XML
        
        Args:
            tree: Árvore XML original
            translations: Dicionário com traduções
            
        Returns:
            Árvore XML com traduções aplicadas
        """
        root = tree.getroot()
        
        # Alterar cultura para pt-BR
        if root.get('culture'):
            root.set('culture', 'pt-BR')
            self.logger.info("Cultura alterada para pt-BR")
        
        applied_count = 0
        
        def apply_recursive(element):
            nonlocal applied_count
            for child in element:
                # Remover namespace do tag para comparação
                tag_name = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                
                if tag_name == 'string':
                    key = child.get('key')
                    if key and key in translations:
                        child.text = translations[key]
                        applied_count += 1
                else:
                    apply_recursive(child)
        
        apply_recursive(root)
        self.logger.info(f"Aplicadas {applied_count} traduções ao XML")
        return tree
    
    def save_xml(self, tree: ET.ElementTree, output_path: str):
        """
        Salva XML traduzido
        
        Args:
            tree: Árvore XML traduzida
            output_path: Caminho de saída
        """
        try:
            # Criar diretório se necessário
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Adicionar encoding UTF-8 explicitamente
            tree.write(output_path, encoding='utf-8', xml_declaration=True)
            print(f"✓ Arquivo salvo: {output_path}")
            self.logger.info(f"XML traduzido salvo: {output_path}")
        except Exception as e:
            error_msg = f"Erro ao salvar XML '{output_path}': {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
    
    def translate_file(self, input_path: str, output_path: str = None) -> dict:
        """
        Traduz um arquivo XML completo automaticamente
        
        Args:
            input_path: Caminho do arquivo de entrada
            output_path: Caminho de saída (opcional)
            
        Returns:
            Dicionário com estatísticas da tradução
        """
        try:
            if not output_path:
                input_file = Path(input_path)
                output_path = input_file.parent / f"{input_file.stem}_pt-BR{input_file.suffix}"
            
            print(f"Carregando: {input_path}")
            tree = self.load_xml(input_path)
            
            print("Extraindo strings...")
            strings = self.extract_strings(tree)
            
            if not strings:
                self.logger.warning(f"Nenhuma string encontrada em '{input_path}'")
                print("⚠ Nenhuma string encontrada para traduzir")
                return {"status": "warning", "message": "Nenhuma string encontrada"}
            
            translations = self.process_translations(strings)
            
            if translations:
                print(f"Aplicando traduções...")
                translated_tree = self.apply_translations(tree, translations)
                self.save_xml(translated_tree, str(output_path))
                
                # Estatísticas
                stats = self.translator.get_stats()
                stats.update({
                    "status": "success",
                    "input_file": input_path,
                    "output_file": str(output_path),
                    "strings_processed": len(strings),
                    "translations_applied": len(translations)
                })
                return stats
            else:
                self.logger.warning("Nenhuma tradução foi realizada")
                print("Nenhuma tradução realizada")
                return {"status": "error", "message": "Nenhuma tradução realizada"}
                
        except Exception as e:
            self.logger.error(f"Erro durante tradução do arquivo '{input_path}': {e}")
            raise
    
    def get_translation_preview(self, input_path: str, max_items: int = 10) -> List[dict]:
        """
        Gera preview das traduções sem aplicar
        
        Args:
            input_path: Caminho do arquivo XML
            max_items: Máximo de itens no preview
            
        Returns:
            Lista com preview das traduções
        """
        tree = self.load_xml(input_path)
        strings = self.extract_strings(tree)
        
        preview = []
        for i, string_data in enumerate(strings[:max_items]):
            key = string_data['key']
            text = string_data['text']
            translation, source = self.translator.get_translation(text, key)
            
            preview.append({
                "key": key,
                "original": text,
                "translation": translation,
                "source": source
            })
        
        return preview
