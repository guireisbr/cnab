# 🏦 Gerador de Remessa CNAB 444 - CONCRETO

Sistema web para geração de arquivos CNAB no padrão 444 caracteres com autenticação.

## 📋 Funcionalidades

- ✅ Sistema de login com senha
- ✅ Upload de arquivos Excel (.xlsx, .xls) ou CSV
- ✅ Geração de arquivos CNAB 444 caracteres
- ✅ Preview dos dados carregados
- ✅ Barra de progresso durante processamento
- ✅ Download do arquivo .REM gerado
- ✅ Interface moderna e intuitiva

## 🚀 Como Executar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Executar a Aplicação

#### Com Autenticação (Recomendado):
```bash
streamlit run app.py
```

#### Sem Autenticação (Apenas desenvolvimento):
```bash
streamlit run main.py
```

### 3. Acessar

Abra o navegador em: `http://localhost:8501`

**Senha padrão:** `admin123`

## 📁 Estrutura de Arquivos

```
cnab/
├── app.py                      # Aplicação principal com autenticação
├── main.py                     # Interface Streamlit (gerador CNAB)
├── cnab_engine.py              # Lógica de geração CNAB
│   ├── CNABGenerator           # Classe em inglês
│   └── GeradorCNAB            # Classe em português ⭐
├── utils.py                    # Funções utilitárias de formatação
├── test_utils.py               # Testes das funções utilitárias
├── test_gerador_cnab.py        # Testes da classe GeradorCNAB ⭐
├── exemplo_uso_gerador.py      # Exemplos de uso ⭐
├── requirements.txt            # Dependências do projeto
├── .streamlit/
│   └── secrets.toml            # Configurações de senha (não commitado)
└── .gitignore                  # Arquivos ignorados pelo Git
```

## 🔐 Configuração de Senha

Para alterar a senha de acesso, edite o arquivo `.streamlit/secrets.toml`:

```toml
access_password = "sua_senha_aqui"
```

**⚠️ IMPORTANTE:** O arquivo `.streamlit/secrets.toml` não deve ser commitado no Git!

## 📊 Formato do Arquivo de Entrada

O arquivo Excel/CSV deve conter as seguintes colunas:

- `SEU_NUMERO` ou `ID_RECEBIVEL`
- `DATA_VENCIMENTO_AJUSTADA` ou `DATA_VENCIMENTO`
- `VALOR_NOMINAL`
- `DATA_EMISSAO`
- `DOC_SACADO`
- `NOME_SACADO`
- `DS_NOSSO_NUMERO` ou `NOSSO_NUMERO`

## 📤 Arquivo Gerado

- **Formato:** `.REM`
- **Encoding:** latin-1
- **Caracteres por linha:** 444
- **Estrutura:**
  - 1 registro Header (Tipo 0)
  - N registros de Detalhe (Tipo 1)
  - 1 registro Trailer (Tipo 9)

## 🔧 Funções Utilitárias (utils.py)

O módulo `utils.py` oferece funções robustas para formatação de dados CNAB:

### Funções em Português:

- **`remover_acentos(texto)`** - Remove acentos usando biblioteca `unidecode`
- **`formatar_texto(valor, tamanho)`** - Formata texto (remove acentos, trunca, preenche)
- **`formatar_numero(valor, tamanho)`** - Formata número (remove não-dígitos, preenche com zeros)
- **`formatar_dinheiro(valor, tamanho)`** - Formata valor monetário (x100, sem decimais)
- **`formatar_data(valor)`** - Formata data para DDMMAA

### Funções em Inglês (aliases):

- `format_text()`, `format_number()`, `format_money()`, `format_date()`

**Exemplo de uso:**
```python
from utils import formatar_texto, formatar_dinheiro, formatar_data

nome = formatar_texto("José da Silva", 40)  # "JOSE DA SILVA                           "
valor = formatar_dinheiro(100.50, 13)       # "0000000010050"
data = formatar_data("2025-11-29")          # "291125"
```

**Teste as funções:**
```bash
python test_utils.py
```

## 🏗️ Classes Disponíveis (cnab_engine.py)

O módulo oferece duas classes para geração de CNAB:

### **GeradorCNAB** (Recomendada - Em Português) ⭐

Classe com nomes de métodos em português:

```python
from cnab_engine import GeradorCNAB

gerador = GeradorCNAB()

# Gerar header
header = gerador.gerar_header(
    nome_originador="BANCO PAULISTA",
    cod_originador="20250158479927000136",
    seq_arquivo=1
)

# Gerar detalhe
detalhe = gerador.gerar_detalhe(linha_df, sequencial_registro=2)

# Gerar trailer
trailer = gerador.gerar_trailer(total_registros=10)

# Gerar arquivo completo
arquivo = gerador.gerar_arquivo_completo(
    df=df,
    nome_originador="BANCO PAULISTA",
    cod_originador="20250158479927000136",
    seq_arquivo=1
)
```

### **CNABGenerator** (Em Inglês)

Classe com nomes de métodos em inglês (mantida para compatibilidade):
- `generate_header()`, `generate_detail()`, `generate_trailer()`

**Testar o gerador:**
```bash
python test_gerador_cnab.py
```

**Exemplos de uso:**
```bash
python exemplo_uso_gerador.py
```

## 🛠️ Tecnologias

- **Python 3.13+**
- **Streamlit** - Interface web
- **Pandas** - Processamento de dados
- **openpyxl** - Leitura de arquivos Excel
- **unidecode** - Remoção de acentos e caracteres especiais

## 📝 Licença

CONCRETO © 2025 - Todos os direitos reservados

