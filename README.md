# Sistema CNAB 444 - CONCRETO

Sistema web para geração de arquivos CNAB no padrão 444 caracteres com autenticação.

## Funcionalidades

- Sistema de login com senha
- Upload de arquivos Excel (.xlsx, .xls) ou CSV
- Geração de arquivos CNAB 444 caracteres
- Preview dos dados carregados
- Barra de progresso durante processamento
- Download do arquivo .REM gerado
- Interface moderna e intuitiva

## Como Executar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Executar a Aplicação

```bash
streamlit run app.py
```

### 3. Acessar

Abra o navegador em: `http://localhost:8501`

**Senha padrão:** `admin123`

## Estrutura de Arquivos

```
cnab/
├── app.py                      
├── cnab_engine.py              
├── utils.py                    
├── test_final.py               
├── requirements.txt            
├── INSTRUCOES.md              
├── .streamlit/
│   ├── secrets.toml            
│   └── config.toml            
└── .gitignore                  
```

## Formato do Arquivo de Entrada

O arquivo Excel/CSV deve conter as seguintes colunas:

- `SEU_NUMERO` ou `ID_RECEBIVEL`
- `DATA_VENCIMENTO_AJUSTADA` ou `DATA_VENCIMENTO`
- `VALOR_NOMINAL`
- `DATA_EMISSAO`
- `DOC_SACADO`
- `NOME_SACADO`

## Arquivo Gerado

- **Formato:** `.REM`
- **Encoding:** latin-1
- **Caracteres por linha:** 444
- **Estrutura:**
  - 1 registro Header (Tipo 0)
  - N registros de Detalhe (Tipo 1)
  - 1 registro Trailer (Tipo 9)

## Tecnologias

- **Python 3.13+**
- **Streamlit** - Interface web
- **Pandas** - Processamento de dados
- **openpyxl** - Leitura de arquivos Excel
- **unidecode** - Remoção de acentos

## Testes

```bash
python test_final.py
```

## Configuração de Senha

Para alterar a senha de acesso, edite o arquivo `.streamlit/secrets.toml`:

```toml
access_password = "sua_senha_aqui"
```

**⚠️ IMPORTANTE:** O arquivo `.streamlit/secrets.toml` não deve ser commitado no Git!

## Uso via Código Python

```python
import pandas as pd
from cnab_engine import GeradorCNAB

gerador = GeradorCNAB()
df = pd.read_excel('arquivo.xlsx')

arquivo_cnab = gerador.gerar_arquivo_completo(
    df=df,
    nome_originador="BANCO PAULISTA",
    cod_originador="20250158479927000136",
    seq_arquivo=1
)

with open('remessa.REM', 'w', encoding='latin-1') as f:
    f.write(arquivo_cnab)
```

## Licença

CONCRETO © 2025 - Todos os direitos reservados
