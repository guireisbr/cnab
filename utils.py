"""
Funções utilitárias para formatação de texto e data
"""

import re
import unicodedata
from datetime import datetime
from typing import Optional, Union


def format_text(value: Union[str, None], length: int) -> str:
    """
    Formata texto para padrão CNAB:
    - Remove acentos e caracteres especiais
    - Converte para maiúsculo
    - Trunca se maior que length
    - Preenche com espaços à direita
    
    Args:
        value: Texto a ser formatado (pode ser None)
        length: Tamanho final da string
        
    Returns:
        String formatada com tamanho fixo
        
    Examples:
        >>> format_text("José Silva", 10)
        "JOSE SILVA"
        >>> format_text("Texto muito longo", 5)
        "TEXTO"
        >>> format_text(None, 10)
        "          "
    """
    if value is None or value == "":
        return " " * length
    
    # Converte para string caso não seja
    texto = str(value)
    
    # Remove acentos usando NFD (Normalization Form Decomposed)
    texto_sem_acento = unicodedata.normalize('NFD', texto)
    texto_sem_acento = ''.join(
        char for char in texto_sem_acento 
        if unicodedata.category(char) != 'Mn'
    )
    
    # Remove caracteres especiais (mantém apenas letras, números e espaços)
    texto_limpo = re.sub(r'[^A-Za-z0-9 ]', '', texto_sem_acento)
    
    # Converte para maiúsculo
    texto_upper = texto_limpo.upper()
    
    # Trunca ou preenche com espaços à direita
    if len(texto_upper) > length:
        return texto_upper[:length]
    else:
        return texto_upper.ljust(length, ' ')


def format_number(value: Union[int, str, None], length: int) -> str:
    """
    Formata número para padrão CNAB:
    - Remove todos os caracteres não-dígitos
    - Preenche com zeros à esquerda
    
    Args:
        value: Número a ser formatado (int ou string numérica)
        length: Tamanho final da string
        
    Returns:
        String formatada com zeros à esquerda
        
    Examples:
        >>> format_number(123, 6)
        "000123"
        >>> format_number("456", 8)
        "00000456"
        >>> format_number("12-34.56", 6)
        "123456"
    """
    if value is None or value == "":
        return "0" * length
    
    # Converte para string
    texto = str(value)
    
    # Remove todos os caracteres não-dígitos
    apenas_digitos = re.sub(r'\D', '', texto)
    
    # Se não sobrou nada, retorna zeros
    if not apenas_digitos:
        return "0" * length
    
    # Preenche com zeros à esquerda
    return apenas_digitos.zfill(length)


def format_money(value: Union[float, int, str, None], length: int) -> str:
    """
    Formata valor monetário para padrão CNAB:
    - Multiplica por 100 para remover casas decimais
    - Remove pontos e vírgulas
    - Preenche com zeros à esquerda
    
    Args:
        value: Valor monetário (float, int ou string)
        length: Tamanho final da string
        
    Returns:
        String formatada com zeros à esquerda
        
    Examples:
        >>> format_money(100.50, 10)
        "0000010050"
        >>> format_money(1234.56, 10)
        "0000123456"
        >>> format_money("99.99", 8)
        "00009999"
    """
    if value is None or value == "":
        return "0" * length
    
    try:
        # Converte para float
        if isinstance(value, str):
            # Remove espaços e substitui vírgula por ponto
            value = value.strip().replace(',', '.')
        
        valor_float = float(value)
        
        # Multiplica por 100 e arredonda para remover casas decimais
        valor_centavos = int(round(valor_float * 100))
        
        # Converte para string e preenche com zeros à esquerda
        return str(valor_centavos).zfill(length)
    
    except (ValueError, TypeError):
        # Em caso de erro, retorna zeros
        return "0" * length


def format_date(value: Union[datetime, str, None]) -> str:
    """
    Formata data para padrão CNAB (DDMMAA):
    - Recebe datetime ou string no formato YYYY-MM-DD
    - Retorna string no formato DDMMAA
    - Se nulo, retorna "000000"
    
    Args:
        value: Data a ser formatada (datetime ou string YYYY-MM-DD)
        
    Returns:
        String formatada no formato DDMMAA
        
    Examples:
        >>> format_date(datetime(2025, 11, 29))
        "291125"
        >>> format_date("2025-11-29")
        "291125"
        >>> format_date(None)
        "000000"
    """
    if value is None or value == "":
        return "000000"
    
    try:
        # Se é string, converte para datetime
        if isinstance(value, str):
            # Tenta diferentes formatos comuns
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d', '%d-%m-%Y']:
                try:
                    data = datetime.strptime(value, fmt)
                    break
                except ValueError:
                    continue
            else:
                # Se nenhum formato funcionou
                return "000000"
        elif isinstance(value, datetime):
            data = value
        else:
            return "000000"
        
        # Formata como DDMMAA
        dia = str(data.day).zfill(2)
        mes = str(data.month).zfill(2)
        ano = str(data.year)[-2:]  # Pega os 2 últimos dígitos do ano
        
        return f"{dia}{mes}{ano}"
    
    except (ValueError, AttributeError, TypeError):
        return "000000"


# Funções auxiliares adicionais

def validar_cpf_cnpj(documento: str) -> bool:
    """
    Valida CPF ou CNPJ
    
    Args:
        documento: String com CPF ou CNPJ
        
    Returns:
        True se válido, False caso contrário
    """
    # TODO: Implementar validação de CPF/CNPJ
    pass


def validar_arquivo(arquivo) -> tuple[bool, Optional[str]]:
    """
    Valida se o arquivo carregado é válido
    
    Args:
        arquivo: Arquivo carregado
        
    Returns:
        Tuple (válido, mensagem de erro)
    """
    # TODO: Implementar validação de arquivo
    pass

