import pandas as pd
from cnab_engine import GeradorCNAB
from datetime import datetime
import os


def validar_arquivo_cnab(arquivo_gerado: str, arquivo_exemplo: str = "CNAB_Consignado2811.txt"):
    print("=" * 80)
    print("VALIDAÇÃO DO ARQUIVO CNAB GERADO")
    print("=" * 80)
    
    with open(arquivo_gerado, 'r', encoding='latin-1') as f:
        linhas_geradas = f.read().split('\r\n')
    
    with open(arquivo_exemplo, 'r', encoding='latin-1') as f:
        linhas_exemplo = f.read().split('\r\n')
    
    print(f"\nArquivo gerado: {arquivo_gerado}")
    print(f"Total de linhas: {len(linhas_geradas)}")
    print(f"\nArquivo exemplo: {arquivo_exemplo}")
    print(f"Total de linhas: {len(linhas_exemplo)}")
    
    print("\n" + "-" * 80)
    print("VALIDAÇÕES:")
    print("-" * 80)
    
    todas_validas = True
    
    for i, linha in enumerate(linhas_geradas, 1):
        if len(linha) != 444:
            print(f"❌ Linha {i}: Tamanho incorreto ({len(linha)} chars)")
            todas_validas = False
    
    if todas_validas:
        print("✅ Todas as linhas têm 444 caracteres")
    
    if linhas_geradas[0][0] == '0':
        print("✅ Primeira linha é Header (Tipo 0)")
    else:
        print("❌ Primeira linha deveria ser Header")
        todas_validas = False
    
    if linhas_geradas[-1][0] == '9':
        print("✅ Última linha é Trailer (Tipo 9)")
    else:
        print("❌ Última linha deveria ser Trailer")
        todas_validas = False
    
    detalhes_ok = True
    for linha in linhas_geradas[1:-1]:
        if linha[0] != '1':
            detalhes_ok = False
            break
    
    if detalhes_ok:
        print(f"✅ Todas as linhas intermediárias são Detalhes (Tipo 1)")
    else:
        print("❌ Algumas linhas intermediárias não são Detalhes")
        todas_validas = False
    
    header_exemplo = linhas_exemplo[0]
    header_gerado = linhas_geradas[0]
    
    if header_gerado[0:2] == header_exemplo[0:2]:
        print("✅ Header: Tipo de registro correto (01)")
    if header_gerado[2:9] == "REMESSA":
        print("✅ Header: REMESSA presente")
    if header_gerado[76:79] == "611":
        print("✅ Header: Código banco correto (611)")
    
    print("\n" + "-" * 80)
    print("AMOSTRA DO ARQUIVO GERADO:")
    print("-" * 80)
    
    for i in range(min(3, len(linhas_geradas))):
        tipo = "Header" if linhas_geradas[i][0] == '0' else "Detalhe" if linhas_geradas[i][0] == '1' else "Trailer"
        print(f"\nLinha {i+1} ({tipo}):")
        print(f"Primeiros 80 chars: {linhas_geradas[i][:80]}")
        print(f"Últimos 20 chars: ...{linhas_geradas[i][-20:]}")
    
    print("\n" + "=" * 80)
    if todas_validas:
        print("✅ VALIDAÇÃO CONCLUÍDA COM SUCESSO!")
    else:
        print("⚠️  VALIDAÇÃO CONCLUÍDA COM AVISOS")
    print("=" * 80)
    
    return todas_validas


def testar_com_excel(arquivo_excel: str = "BAIXA TOTAL 271125.xlsx"):
    print("=" * 80)
    print("TESTE DE GERAÇÃO CNAB COM ARQUIVO EXCEL")
    print("=" * 80)
    
    if not os.path.exists(arquivo_excel):
        print(f"\n❌ Arquivo não encontrado: {arquivo_excel}")
        return False
    
    print(f"\n1. Carregando arquivo: {arquivo_excel}")
    df = pd.read_excel(arquivo_excel)
    print(f"   ✅ {len(df)} registros carregados")
    print(f"   ✅ {len(df.columns)} colunas encontradas")
    
    print("\n2. Colunas disponíveis:")
    for col in df.columns:
        print(f"   - {col}")
    
    print("\n3. Gerando arquivo CNAB...")
    gerador = GeradorCNAB()
    
    arquivo_cnab = gerador.gerar_arquivo_completo(
        df=df,
        nome_originador="BANCO PAULISTA",
        cod_originador="20250158479927000136",
        seq_arquivo=1
    )
    
    print("   ✅ Arquivo gerado na memória")
    
    nome_saida = f"REMESSA_TESTE_{datetime.now().strftime('%Y%m%d_%H%M%S')}.REM"
    
    print(f"\n4. Salvando arquivo: {nome_saida}")
    with open(nome_saida, 'w', encoding='latin-1') as f:
        f.write(arquivo_cnab)
    
    tamanho = os.path.getsize(nome_saida)
    print(f"   ✅ Arquivo salvo ({tamanho:,} bytes)")
    
    print("\n5. Validando arquivo gerado...")
    validar_arquivo_cnab(nome_saida)
    
    return True


def comparar_estrutura():
    print("\n" + "=" * 80)
    print("COMPARAÇÃO DE ESTRUTURA COM ARQUIVO DE EXEMPLO")
    print("=" * 80)
    
    arquivo_exemplo = "CNAB_Consignado2811.txt"
    
    if not os.path.exists(arquivo_exemplo):
        print(f"\n❌ Arquivo exemplo não encontrado: {arquivo_exemplo}")
        return
    
    with open(arquivo_exemplo, 'r', encoding='latin-1') as f:
        linhas = f.read().split('\r\n')
    
    print(f"\nArquivo de exemplo: {arquivo_exemplo}")
    print(f"Total de linhas: {len(linhas)}")
    
    if len(linhas) > 0:
        header = linhas[0]
        print(f"\nHEADER (primeira linha):")
        print(f"  Tamanho: {len(header)} caracteres")
        print(f"  Tipo: {header[0]}")
        print(f"  Literal: {header[2:9]}")
        print(f"  Banco: {header[76:79]}")
    
    if len(linhas) > 1:
        detalhe = linhas[1]
        print(f"\nDETALHE (segunda linha):")
        print(f"  Tamanho: {len(detalhe)} caracteres")
        print(f"  Tipo: {detalhe[0]}")
        print(f"  Primeiros 50 chars: {detalhe[:50]}")
    
    if len(linhas) > 0:
        trailer = linhas[-1]
        print(f"\nTRAILER (última linha):")
        print(f"  Tamanho: {len(trailer)} caracteres")
        print(f"  Tipo: {trailer[0]}")
        print(f"  Sequencial: {trailer[-6:]}")


if __name__ == "__main__":
    try:
        comparar_estrutura()
        print("\n")
        testar_com_excel()
        
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()

