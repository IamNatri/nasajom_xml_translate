#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XML Localization Translator - Main Entry Point
Traduz arquivos XML de localização do inglês para português (pt-BR)
"""

import os
import sys
from pathlib import Path

# Adicionar src ao path para imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from xml_translator.core.translator import XMLTranslator
from xml_translator.utils.logger import setup_logging


def detect_xml_files(directory: str = ".") -> list:
    """
    Detecta arquivos XML no diretório
    
    Args:
        directory: Diretório para buscar
        
    Returns:
        Lista de arquivos XML encontrados
    """
    xml_files = []
    for file in Path(directory).glob("*.xml"):
        # Ignorar arquivos já traduzidos
        if not file.name.endswith("_pt-BR.xml"):
            xml_files.append(str(file))
    return sorted(xml_files)


def get_user_choice(xml_files: list) -> str:
    """
    Obtém escolha do usuário para arquivo XML
    
    Args:
        xml_files: Lista de arquivos disponíveis
        
    Returns:
        Caminho do arquivo escolhido
    """
    if xml_files:
        print(f"Arquivos XML encontrados: {', '.join(xml_files)}")
        choice = input(f"Arquivo [ENTER={xml_files[0]}]: ").strip()
        return choice if choice else xml_files[0]
    else:
        return input("Caminho do XML: ").strip()


def main():
    """Função principal - tradução automática"""
    logger = setup_logging()
    
    try:
        translator = XMLTranslator()
        
        xml_files = detect_xml_files()
        input_file = get_user_choice(xml_files)
        
        if not os.path.exists(input_file):
            error_msg = f"Arquivo não encontrado: {input_file}"
            logger.error(error_msg)
            print(f"{error_msg}")
            return 1
        
        print(f"\n Iniciando tradução de: {input_file}")
        result = translator.translate_file(input_file)
        
        if result.get("status") == "success":
            print("\n Tradução concluída com sucesso!")
            print(f"Arquivo gerado: {result['output_file']}")
            print(f"Strings processadas: {result['strings_processed']}")
            print(f"Traduções aplicadas: {result['translations_applied']}")
            
            if result.get('overrides_count', 0) > 0:
                print(f"Overrides utilizados: {result['overrides_count']}")

            return 0
        else:
            print(f"\n{result.get('message', 'Erro na tradução')}")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n Operação cancelada pelo usuário")
        return 130
    except Exception as e:
        logger.error(f"Erro na execução principal: {e}")
        print(f"\n Erro: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
