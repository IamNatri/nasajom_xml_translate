# XML Translator - Estrutura Profissional

Tradutor automatizado de arquivos XML de localização do inglês para português (pt-BR) utilizando Google Translate com sistema de overrides manuais.

## Estrutura do Projeto

```
xml_translator/
├── src/                           # Código fonte
│   └── xml_translator/            # Pacote principal
│       ├── __init__.py            # Inicialização do pacote
│       ├── core/                  # Módulos centrais
│       │   ├── __init__.py
│       │   ├── auto_translator.py # Tradutor automático Google
│       │   └── translator.py      # Processador XML principal
│       └── utils/                 # Utilitários
│           ├── __init__.py
│           └── logger.py          # Sistema de logging
├── tests/                         # Testes automatizados
│   ├── __init__.py
│   └── test_translator.py         # Testes principais
├── examples/                      # Arquivos de exemplo
│   └── sample_en.xml              # XML exemplo
├── config/                        # Configurações
│   ├── overrides.json             # Traduções manuais
│   └── overrides.example.json     # Exemplo de overrides
├── logs/                          # Logs da aplicação
├── main.py                        # Ponto de entrada
├── pyproject.toml                 # Configuração Poetry
└── README.md                      # Esta documentação
```

## Instalação

### Pré-requisitos
- Python 3.8+
- Poetry (recomendado)

### Com Poetry (recomendado)
```bash
# Instalar dependências
poetry install

# Executar tradutor
poetry run xml-translator
```

## Uso

### Uso Básico
```bash
poetry run xml-translator
```

O sistema irá:
1. Detectar arquivos XML no diretório atual
2. Permitir escolha do arquivo
3. Processar traduções automaticamente
4. Gerar arquivo `*_pt-BR.xml`

### Estrutura XML Suportada
```xml
<?xml version="1.0" encoding="utf-8"?>
<localization culture="en-US">
  <group name="Common">
    <string key="Title">Title</string>
    <string key="Cancel">Cancel</string>
  </group>
</localization>
```

## Configuração

### Overrides Manuais
Arquivo: `config/overrides.json`
```json
{
  "GS_LogOn_Title": "Entrar no Sistema BI",
  "GS_Dashboard_Title": "Painel de Controle",
  "GS_Button_Cancel": "Cancelar"
}
```

### Logs
- Logs salvos em: `logs/xml_translator_YYYYMMDD.log`
- Níveis: INFO, WARNING, ERROR
- Console + arquivo simultaneamente

## Desenvolvimento

### Executar Testes
```bash
poetry run pytest tests/
```

### Formatação de Código
```bash
# Black (formatador)
poetry run black src/ tests/

# isort (organizar imports)
poetry run isort src/ tests/

# Linting
poetry run flake8 src/ tests/
```

### Estrutura de Desenvolvimento
```bash
# Instalar dependências de desenvolvimento
poetry install --with dev

# Adicionar nova dependência
poetry add nova-biblioteca

# Adicionar dependência de desenvolvimento
poetry add --group dev pytest-mock
```

## Funcionalidades

### Implementadas
- Tradução automática via Google Translate
- Logging estruturado
- Estrutura de projeto profissional
- Gerenciamento com Poetry
- Testes 
- Detecção automática de arquivos

## Arquitetura

### Módulos Principais

#### `core/auto_translator.py`
- Integração com Google Translate
- Gerenciamento de overrides
- Rate limiting
- Cache de traduções

#### `core/translator.py`
- Processamento de arquivos XML
- Extração de strings
- Aplicação de traduções
- Geração de relatórios

#### `utils/logger.py`
- Configuração centralizada de logs
- Rotação automática
- Múltiplos handlers

### Fluxo de Processamento
1. **Inicialização** → Configurar logging + tradutor
2. **Detecção** → Buscar arquivos XML disponíveis
3. **Carregamento** → Parser XML com validação
4. **Extração** → Identificar strings traduzíveis
5. **Tradução** → Overrides → Google → Original
6. **Aplicação** → Atualizar XML com traduções
7. **Salvamento** → Gerar arquivo pt-BR
8. **Relatório** → Estatísticas e logs

## 🔧 Troubleshooting

### Problemas Comuns

**Erro: "googletrans não instalado"**
```bash
poetry install
```

**Erro: "Arquivo não encontrado"**
- Verificar se arquivo XML existe
- Usar caminho absoluto se necessário

**Traduções inconsistentes**
- Adicionar overrides em `config/overrides.json`
- Verificar conectividade com Google

### Logs e Debug
- Verificar `logs/xml_translator_YYYYMMDD.log`
- Usar nível DEBUG para mais detalhes
- Conferir estatísticas no final da execução