"""
Script de teste para a classe GeradorCNAB
"""

import pandas as pd
from datetime import datetime
from cnab_engine import GeradorCNAB


def testar_gerador_cnab():
    """
    Testa a classe GeradorCNAB
    """
    print("=" * 80)
    print("TESTE DA CLASSE GeradorCNAB")
    print("=" * 80)
    
    # Cria instância do gerador
    gerador = GeradorCNAB()
    
    # Teste 1: Header
    print("\n1. TESTE: gerar_header()")
    print("-" * 80)
    
    header = gerador.gerar_header(
        nome_originador="BANCO PAULISTA",
        cod_originador="20250158479927000136",
        seq_arquivo=1
    )
    
    print(f"Tamanho: {len(header)} caracteres")
    print(f"\nPrimeiros 100 caracteres:")
    print(header[:100])
    print(f"\nÚltimos 50 caracteres:")
    print(header[-50:])
    
    # Validações do header
    assert len(header) == 444, f"Header deve ter 444 caracteres, tem {len(header)}"
    assert header[0] == "0", "Pos 1 deve ser '0'"
    assert header[1] == "1", "Pos 2 deve ser '1'"
    assert header[2:9] == "REMESSA", "Pos 3-9 deve ser 'REMESSA'"
    assert header[9:11] == "01", "Pos 10-11 deve ser '01'"
    assert header[76:79] == "611", "Pos 77-79 deve ser '611'"
    assert header[438:444] == "000001", "Pos 439-444 deve ser '000001'"
    print("\n✅ Header validado com sucesso!")
    
    # Teste 2: Detalhe
    print("\n2. TESTE: gerar_detalhe()")
    print("-" * 80)
    
    # Cria um registro de exemplo
    dados_exemplo = {
        'SEU_NUMERO': '12345',
        'DATA_VENCIMENTO_AJUSTADA': '2025-12-31',
        'VALOR_NOMINAL': 1234.56,
        'DATA_EMISSAO': '2025-11-29',
        'DOC_SACADO': '12345678900',
        'NOME_SACADO': 'João da Silva'
    }
    
    linha_df = pd.Series(dados_exemplo)
    detalhe = gerador.gerar_detalhe(linha_df, sequencial_registro=2)
    
    print(f"Tamanho: {len(detalhe)} caracteres")
    print(f"\nPrimeiros 100 caracteres:")
    print(detalhe[:100])
    print(f"\nCaracteres 120-160 (data vencimento e valor):")
    print(detalhe[120:160])
    print(f"\nCaracteres 220-280 (doc e nome sacado):")
    print(detalhe[220:280])
    print(f"\nÚltimos 50 caracteres:")
    print(detalhe[-50:])
    
    # Validações do detalhe
    assert len(detalhe) == 444, f"Detalhe deve ter 444 caracteres, tem {len(detalhe)}"
    assert detalhe[0] == "1", "Pos 1 deve ser '1'"
    assert detalhe[438:444] == "000002", "Pos 439-444 deve ser '000002'"
    print("\n✅ Detalhe validado com sucesso!")
    
    # Teste 3: Trailer
    print("\n3. TESTE: gerar_trailer()")
    print("-" * 80)
    
    trailer = gerador.gerar_trailer(total_registros=10)
    
    print(f"Tamanho: {len(trailer)} caracteres")
    print(f"\nPrimeiros 50 caracteres:")
    print(trailer[:50])
    print(f"\nÚltimos 50 caracteres:")
    print(trailer[-50:])
    
    # Validações do trailer
    assert len(trailer) == 444, f"Trailer deve ter 444 caracteres, tem {len(trailer)}"
    assert trailer[0] == "9", "Pos 1 deve ser '9'"
    assert trailer[1:7] == "000010", "Pos 2-7 deve ser '000010'"
    assert trailer[438:444] == "000010", "Pos 439-444 deve ser '000010'"
    print("\n✅ Trailer validado com sucesso!")
    
    # Teste 4: Arquivo Completo
    print("\n4. TESTE: gerar_arquivo_completo()")
    print("-" * 80)
    
    # Cria DataFrame com múltiplos registros
    dados = [
        {
            'SEU_NUMERO': '100001',
            'DATA_VENCIMENTO_AJUSTADA': '2025-12-31',
            'VALOR_NOMINAL': 1000.00,
            'DATA_EMISSAO': '2025-11-29',
            'DOC_SACADO': '12345678901',
            'NOME_SACADO': 'Maria Santos'
        },
        {
            'SEU_NUMERO': '100002',
            'DATA_VENCIMENTO_AJUSTADA': '2026-01-15',
            'VALOR_NOMINAL': 2500.50,
            'DATA_EMISSAO': '2025-11-29',
            'DOC_SACADO': '98765432100',
            'NOME_SACADO': 'Pedro Oliveira'
        },
        {
            'SEU_NUMERO': '100003',
            'DATA_VENCIMENTO_AJUSTADA': '2026-02-28',
            'VALOR_NOMINAL': 750.25,
            'DATA_EMISSAO': '2025-11-29',
            'DOC_SACADO': '11122233344',
            'NOME_SACADO': 'Ana Costa'
        }
    ]
    
    df = pd.DataFrame(dados)
    
    arquivo_completo = gerador.gerar_arquivo_completo(
        df=df,
        nome_originador="BANCO PAULISTA",
        cod_originador="20250158479927000136",
        seq_arquivo=1
    )
    
    linhas = arquivo_completo.split("\r\n")
    print(f"\nTotal de linhas no arquivo: {len(linhas)}")
    print(f"Esperado: {len(df) + 2} (Header + {len(df)} Detalhes + Trailer)")
    
    # Validações do arquivo completo
    assert len(linhas) == len(df) + 2, "Deve ter header + detalhes + trailer"
    assert linhas[0][0] == "0", "Primeira linha deve ser header (tipo 0)"
    assert linhas[-1][0] == "9", "Última linha deve ser trailer (tipo 9)"
    
    for i, linha in enumerate(linhas):
        assert len(linha) == 444, f"Linha {i+1} deve ter 444 caracteres, tem {len(linha)}"
    
    print("\n✅ Arquivo completo validado com sucesso!")
    
    # Mostra preview das linhas
    print("\n" + "=" * 80)
    print("PREVIEW DO ARQUIVO GERADO")
    print("=" * 80)
    for i, linha in enumerate(linhas, 1):
        print(f"\nLinha {i} (Tipo {linha[0]}):")
        print(f"  Primeiros 80 chars: {linha[:80]}")
        print(f"  Últimos 20 chars: ...{linha[-20:]}")
    
    # Salva arquivo de exemplo
    nome_arquivo = f"teste_remessa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.REM"
    with open(nome_arquivo, 'w', encoding='latin-1') as f:
        f.write(arquivo_completo)
    
    print(f"\n✅ Arquivo salvo: {nome_arquivo}")
    
    print("\n" + "=" * 80)
    print("TODOS OS TESTES CONCLUÍDOS COM SUCESSO! ✅")
    print("=" * 80)


if __name__ == "__main__":
    try:
        testar_gerador_cnab()
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()

