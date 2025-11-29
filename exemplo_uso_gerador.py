"""
Exemplo de uso da classe GeradorCNAB
Demonstra como gerar um arquivo CNAB a partir de um Excel
"""

import pandas as pd
from datetime import datetime
from cnab_engine import GeradorCNAB


def exemplo_simples():
    """
    Exemplo simples de geração de CNAB
    """
    print("=" * 80)
    print("EXEMPLO DE USO - GeradorCNAB")
    print("=" * 80)
    
    # 1. Cria instância do gerador
    print("\n1. Criando gerador...")
    gerador = GeradorCNAB()
    
    # 2. Carrega dados (pode ser de Excel ou CSV)
    print("\n2. Carregando dados...")
    
    # Opção A: Carregar de arquivo Excel
    # df = pd.read_excel('BAIXA TOTAL 271125.xlsx')
    
    # Opção B: Criar dados de exemplo
    dados = [
        {
            'SEU_NUMERO': '100001',
            'DATA_VENCIMENTO_AJUSTADA': '2025-12-31',
            'VALOR_NOMINAL': 1500.00,
            'DATA_EMISSAO': '2025-11-29',
            'DOC_SACADO': '12345678901234',  # CNPJ
            'NOME_SACADO': 'EMPRESA EXEMPLO LTDA'
        },
        {
            'SEU_NUMERO': '100002',
            'DATA_VENCIMENTO_AJUSTADA': '2026-01-31',
            'VALOR_NOMINAL': 2500.00,
            'DATA_EMISSAO': '2025-11-29',
            'DOC_SACADO': '98765432100',  # CPF
            'NOME_SACADO': 'João da Silva'
        }
    ]
    
    df = pd.DataFrame(dados)
    print(f"   Total de registros: {len(df)}")
    
    # 3. Define informações do originador
    print("\n3. Configurando originador...")
    nome_originador = "BANCO PAULISTA"
    cod_originador = "20250158479927000136"
    seq_arquivo = 1
    
    print(f"   Nome: {nome_originador}")
    print(f"   Código: {cod_originador}")
    print(f"   Sequencial: {seq_arquivo}")
    
    # 4. Gera o arquivo CNAB completo
    print("\n4. Gerando arquivo CNAB...")
    arquivo_cnab = gerador.gerar_arquivo_completo(
        df=df,
        nome_originador=nome_originador,
        cod_originador=cod_originador,
        seq_arquivo=seq_arquivo
    )
    
    # 5. Salva o arquivo
    nome_arquivo = f"REMESSA_{datetime.now().strftime('%Y%m%d_%H%M%S')}.REM"
    print(f"\n5. Salvando arquivo: {nome_arquivo}")
    
    with open(nome_arquivo, 'w', encoding='latin-1') as f:
        f.write(arquivo_cnab)
    
    # 6. Mostra estatísticas
    linhas = arquivo_cnab.split("\r\n")
    print(f"\n6. Estatísticas do arquivo:")
    print(f"   Total de linhas: {len(linhas)}")
    print(f"   Header: 1")
    print(f"   Detalhes: {len(linhas) - 2}")
    print(f"   Trailer: 1")
    print(f"   Tamanho: {len(arquivo_cnab)} bytes")
    
    # 7. Preview
    print(f"\n7. Preview das primeiras linhas:")
    for i, linha in enumerate(linhas[:3], 1):
        tipo = "Header" if linha[0] == "0" else "Detalhe" if linha[0] == "1" else "Trailer"
        print(f"\n   Linha {i} ({tipo}):")
        print(f"   {linha[:80]}...")
    
    print("\n" + "=" * 80)
    print(f"✅ Arquivo CNAB gerado com sucesso: {nome_arquivo}")
    print("=" * 80)


def exemplo_com_excel():
    """
    Exemplo usando arquivo Excel real
    """
    print("\n" + "=" * 80)
    print("EXEMPLO COM ARQUIVO EXCEL")
    print("=" * 80)
    
    try:
        # 1. Carrega Excel
        print("\n1. Carregando arquivo Excel...")
        df = pd.read_excel('BAIXA TOTAL 271125.xlsx')
        print(f"   ✅ Carregado: {len(df)} registros")
        
        # 2. Mostra colunas disponíveis
        print("\n2. Colunas disponíveis:")
        for col in df.columns:
            print(f"   - {col}")
        
        # 3. Gera CNAB
        print("\n3. Gerando CNAB...")
        gerador = GeradorCNAB()
        
        arquivo_cnab = gerador.gerar_arquivo_completo(
            df=df,
            nome_originador="BANCO PAULISTA",
            cod_originador="20250158479927000136",
            seq_arquivo=1
        )
        
        # 4. Salva
        nome_arquivo = f"REMESSA_REAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}.REM"
        with open(nome_arquivo, 'w', encoding='latin-1') as f:
            f.write(arquivo_cnab)
        
        print(f"\n✅ Arquivo gerado: {nome_arquivo}")
        print(f"   Total de registros: {len(df)}")
        print(f"   Tamanho: {len(arquivo_cnab):,} bytes")
        
    except FileNotFoundError:
        print("\n❌ Arquivo 'BAIXA TOTAL 271125.xlsx' não encontrado")
        print("   Use exemplo_simples() para teste com dados fictícios")
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Executa exemplo simples
    exemplo_simples()
    
    # Descomente para testar com Excel real
    # exemplo_com_excel()

