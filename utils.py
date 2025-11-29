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


# =============================================================================
# FUNÇÕES EM PORTUGUÊS (ALIASES E EXTRAS)
# =============================================================================

try:
    from unidecode import unidecode
    UNIDECODE_AVAILABLE = True
except ImportError:
    UNIDECODE_AVAILABLE = False


def remover_acentos(texto: Union[str, None]) -> str:
    """
    Remove acentos e caracteres especiais de um texto.
    Converte para maiúsculo.
    
    Args:
        texto: String a ser processada
        
    Returns:
        String sem acentos em maiúsculo
        
    Examples:
        >>> remover_acentos("José da Silva")
        "JOSE DA SILVA"
        >>> remover_acentos("Ação & Reação!")
        "ACAO  REACAO"
    """
    if texto is None or texto == "":
        return ""
    
    # Converte para string
    texto_str = str(texto)
    
    # Usa unidecode se disponível, senão usa unicodedata
    if UNIDECODE_AVAILABLE:
        texto_sem_acento = unidecode(texto_str)
    else:
        # Fallback usando unicodedata
        texto_normalizado = unicodedata.normalize('NFD', texto_str)
        texto_sem_acento = ''.join(
            char for char in texto_normalizado 
            if unicodedata.category(char) != 'Mn'
        )
    
    # Remove caracteres especiais (mantém apenas letras, números e espaços)
    texto_limpo = re.sub(r'[^A-Za-z0-9 ]', '', texto_sem_acento)
    
    # Converte para maiúsculo
    return texto_limpo.upper()


def formatar_texto(valor: Union[str, None], tamanho: int) -> str:
    """
    Formata texto para padrão CNAB (versão em português).
    Remove acentos, trunca se necessário, preenche com espaços à direita.
    
    Args:
        valor: Texto a ser formatado
        tamanho: Tamanho final da string
        
    Returns:
        String formatada com tamanho fixo
        
    Examples:
        >>> formatar_texto("José Silva", 15)
        "JOSE SILVA     "
        >>> formatar_texto("Texto muito longo para caber", 10)
        "TEXTO MUIT"
        >>> formatar_texto(None, 5)
        "     "
    """
    if valor is None or valor == "":
        return " " * tamanho
    
    # Remove acentos e converte para maiúsculo
    texto_limpo = remover_acentos(valor)
    
    # Trunca se for maior que o tamanho
    if len(texto_limpo) > tamanho:
        return texto_limpo[:tamanho]
    
    # Preenche com espaços à direita
    return texto_limpo.ljust(tamanho, ' ')


def formatar_numero(valor: Union[int, str, None], tamanho: int) -> str:
    """
    Formata número para padrão CNAB (versão em português).
    Remove tudo que não for dígito, preenche com zeros à esquerda.
    
    Args:
        valor: Número a ser formatado
        tamanho: Tamanho final da string
        
    Returns:
        String formatada com zeros à esquerda
        
    Examples:
        >>> formatar_numero(123, 8)
        "00000123"
        >>> formatar_numero("45.67", 6)
        "004567"
        >>> formatar_numero("ABC123DEF456", 10)
        "0000123456"
    """
    if valor is None or valor == "":
        return "0" * tamanho
    
    # Converte para string
    texto = str(valor)
    
    # Remove todos os caracteres não-dígitos
    apenas_digitos = re.sub(r'\D', '', texto)
    
    # Se não sobrou nada, retorna zeros
    if not apenas_digitos:
        return "0" * tamanho
    
    # Preenche com zeros à esquerda
    return apenas_digitos.zfill(tamanho)


def formatar_dinheiro(valor: Union[float, int, str, None], tamanho: int) -> str:
    """
    Formata valor monetário para padrão CNAB (versão em português).
    Multiplica por 100 para remover casas decimais.
    Remove pontos e vírgulas, preenche com zeros à esquerda.
    
    Args:
        valor: Valor monetário (float, int ou string)
        tamanho: Tamanho final da string
        
    Returns:
        String formatada com zeros à esquerda
        
    Examples:
        >>> formatar_dinheiro(100.50, 13)
        "0000000010050"
        >>> formatar_dinheiro("1234.56", 13)
        "0000000123456"
        >>> formatar_dinheiro(0.99, 10)
        "0000000099"
    """
    if valor is None or valor == "":
        return "0" * tamanho
    
    try:
        # Converte para float
        if isinstance(valor, str):
            # Remove espaços, "R$" e substitui vírgula por ponto
            valor_limpo = valor.strip().replace('R$', '').replace(' ', '')
            valor_limpo = valor_limpo.replace(',', '.')
            valor_float = float(valor_limpo)
        else:
            valor_float = float(valor)
        
        # Multiplica por 100 e arredonda para remover casas decimais
        valor_centavos = int(round(valor_float * 100))
        
        # Converte para string e preenche com zeros à esquerda
        return str(valor_centavos).zfill(tamanho)
    
    except (ValueError, TypeError):
        # Em caso de erro, retorna zeros
        return "0" * tamanho


def formatar_data(valor: Union[datetime, str, None]) -> str:
    """
    Formata data para padrão CNAB (versão em português).
    Recebe datetime ou string YYYY-MM-DD.
    Retorna string no formato DDMMAA.
    
    Args:
        valor: Data a ser formatada (datetime ou string)
        
    Returns:
        String no formato DDMMAA ou "000000" se nulo
        
    Examples:
        >>> formatar_data(datetime(2025, 11, 29))
        "291125"
        >>> formatar_data("2025-11-29")
        "291125"
        >>> formatar_data("29/11/2025")
        "291125"
        >>> formatar_data(None)
        "000000"
    """
    if valor is None or valor == "":
        return "000000"
    
    try:
        # Se é string, converte para datetime
        if isinstance(valor, str):
            # Tenta diferentes formatos comuns
            formatos = [
                '%Y-%m-%d',      # 2025-11-29
                '%d/%m/%Y',      # 29/11/2025
                '%Y/%m/%d',      # 2025/11/29
                '%d-%m-%Y',      # 29-11-2025
                '%Y%m%d',        # 20251129
                '%d%m%Y'         # 29112025
            ]
            
            for fmt in formatos:
                try:
                    data = datetime.strptime(valor, fmt)
                    break
                except ValueError:
                    continue
            else:
                # Se nenhum formato funcionou
                return "000000"
        elif isinstance(valor, datetime):
            data = valor
        else:
            return "000000"
        
        # Formata como DDMMAA
        dia = str(data.day).zfill(2)
        mes = str(data.month).zfill(2)
        ano = str(data.year)[-2:]  # Pega os 2 últimos dígitos do ano
        
        return f"{dia}{mes}{ano}"
    
    except (ValueError, AttributeError, TypeError):
        return "000000"


# =============================================================================
# FUNÇÕES AUXILIARES ADICIONAIS
# =============================================================================

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

