"""
Script de teste para as funções utilitárias
"""

from datetime import datetime
from utils import (
    remover_acentos,
    formatar_texto,
    formatar_numero,
    formatar_dinheiro,
    formatar_data
)


def testar_funcoes():
    """
    Testa todas as funções utilitárias
    """
    print("=" * 80)
    print("TESTE DAS FUNÇÕES UTILITÁRIAS - utils.py")
    print("=" * 80)
    
    # Teste 1: remover_acentos
    print("\n1. TESTE: remover_acentos()")
    print("-" * 40)
    testes_acentos = [
        "José da Silva",
        "Ação & Reação!",
        "São Paulo - SP",
        "Côte d'Ivoire",
        "Crédito Fácil Ltda."
    ]
    for texto in testes_acentos:
        resultado = remover_acentos(texto)
        print(f"  '{texto}' → '{resultado}'")
    
    # Teste 2: formatar_texto
    print("\n2. TESTE: formatar_texto(valor, tamanho)")
    print("-" * 40)
    print(f"  formatar_texto('José Silva', 15):")
    print(f"    '{formatar_texto('José Silva', 15)}' (len={len(formatar_texto('José Silva', 15))})")
    print(f"  formatar_texto('Nome muito longo para caber', 10):")
    print(f"    '{formatar_texto('Nome muito longo para caber', 10)}' (len={len(formatar_texto('Nome muito longo para caber', 10))})")
    print(f"  formatar_texto('ABC', 10):")
    print(f"    '{formatar_texto('ABC', 10)}' (len={len(formatar_texto('ABC', 10))})")
    print(f"  formatar_texto(None, 5):")
    print(f"    '{formatar_texto(None, 5)}' (len={len(formatar_texto(None, 5))})")
    
    # Teste 3: formatar_numero
    print("\n3. TESTE: formatar_numero(valor, tamanho)")
    print("-" * 40)
    testes_numeros = [
        (123, 8),
        ("456", 10),
        ("12-34.56", 6),
        ("ABC123DEF456", 10),
        ("", 5)
    ]
    for valor, tamanho in testes_numeros:
        resultado = formatar_numero(valor, tamanho)
        print(f"  formatar_numero({repr(valor)}, {tamanho}) → '{resultado}' (len={len(resultado)})")
    
    # Teste 4: formatar_dinheiro
    print("\n4. TESTE: formatar_dinheiro(valor, tamanho)")
    print("-" * 40)
    testes_dinheiro = [
        (100.50, 13),
        (1234.56, 13),
        ("99.99", 10),
        (0.01, 10),
        ("R$ 1.500,00", 15),
        (10000.00, 13)
    ]
    for valor, tamanho in testes_dinheiro:
        resultado = formatar_dinheiro(valor, tamanho)
        print(f"  formatar_dinheiro({repr(valor)}, {tamanho}) → '{resultado}' (len={len(resultado)})")
    
    # Teste 5: formatar_data
    print("\n5. TESTE: formatar_data(valor)")
    print("-" * 40)
    testes_datas = [
        datetime(2025, 11, 29),
        "2025-11-29",
        "29/11/2025",
        "2025/11/29",
        "20251129",
        None,
        ""
    ]
    for data in testes_datas:
        resultado = formatar_data(data)
        print(f"  formatar_data({repr(data)}) → '{resultado}'")
    
    # Teste Completo: Simulação de linha CNAB
    print("\n" + "=" * 80)
    print("SIMULAÇÃO: Linha CNAB com dados formatados")
    print("=" * 80)
    
    nome_sacado = "José da Silva Ação"
    valor_titulo = 1234.56
    doc_sacado = "123.456.789-00"
    data_vencimento = "2025-12-31"
    seu_numero = "ABC12345"
    
    print(f"\nDados de entrada:")
    print(f"  Nome Sacado: {nome_sacado}")
    print(f"  Valor Título: {valor_titulo}")
    print(f"  Documento: {doc_sacado}")
    print(f"  Vencimento: {data_vencimento}")
    print(f"  Seu Número: {seu_numero}")
    
    print(f"\nDados formatados para CNAB:")
    print(f"  Nome (40 pos): '{formatar_texto(nome_sacado, 40)}'")
    print(f"  Valor (13 pos): '{formatar_dinheiro(valor_titulo, 13)}'")
    print(f"  Documento (14 pos): '{formatar_numero(doc_sacado, 14)}'")
    print(f"  Vencimento (6 pos): '{formatar_data(data_vencimento)}'")
    print(f"  Seu Número (25 pos): '{formatar_numero(seu_numero, 25)}'")
    
    print("\n" + "=" * 80)
    print("TODOS OS TESTES CONCLUÍDOS!")
    print("=" * 80)


if __name__ == "__main__":
    testar_funcoes()

