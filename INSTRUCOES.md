# Sistema CNAB 444 - CONCRETO

## Instruções de Uso

### Instalação

```bash
pip install -r requirements.txt
```

### Executar Aplicação

```bash
streamlit run app.py
```

Acesso: http://localhost:8501
Senha padrão: **admin123**

### Uso da Aplicação

1. Faça login com a senha
2. Configure na sidebar:
   - Nome Originador
   - Código Originador
   - Sequencial do Arquivo
3. Faça upload do arquivo Excel ou CSV
4. Clique em "Gerar Arquivo .REM"
5. Baixe o arquivo CNAB gerado

### Colunas Necessárias no Arquivo

O arquivo Excel/CSV deve conter as seguintes colunas:

- `SEU_NUMERO` ou `ID_RECEBIVEL`
- `DATA_VENCIMENTO_AJUSTADA` ou `DATA_VENCIMENTO`
- `VALOR_NOMINAL`
- `DATA_EMISSAO`
- `DOC_SACADO`
- `NOME_SACADO`

### Arquivo Gerado

- **Formato:** .REM ou .TXT
- **Encoding:** latin-1 (padrão bancário)
- **Tamanho da linha:** 444 caracteres
- **Quebra de linha:** \r\n
- **Estrutura:**
  - 1 linha Header (Tipo 0)
  - N linhas Detalhe (Tipo 1)
  - 1 linha Trailer (Tipo 9)

### Testes

```bash
python test_final.py
```

### Estrutura dos Arquivos

- `app.py` - Aplicação Streamlit com autenticação
- `cnab_engine.py` - Lógica de geração CNAB
- `utils.py` - Funções utilitárias de formatação
- `.streamlit/secrets.toml` - Configuração de senha

### Suporte

Para dúvidas ou problemas, entre em contato com o administrador do sistema.

