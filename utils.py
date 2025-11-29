import re
import unicodedata
from datetime import datetime
from typing import Optional, Union

try:
    from unidecode import unidecode
    UNIDECODE_AVAILABLE = True
except ImportError:
    UNIDECODE_AVAILABLE = False


def format_text(value: Union[str, None], length: int) -> str:
    if value is None or value == "":
        return " " * length
    
    texto = str(value)
    texto_sem_acento = unicodedata.normalize('NFD', texto)
    texto_sem_acento = ''.join(
        char for char in texto_sem_acento 
        if unicodedata.category(char) != 'Mn'
    )
    texto_limpo = re.sub(r'[^A-Za-z0-9 ]', '', texto_sem_acento)
    texto_upper = texto_limpo.upper()
    
    if len(texto_upper) > length:
        return texto_upper[:length]
    else:
        return texto_upper.ljust(length, ' ')


def format_number(value: Union[int, str, None], length: int) -> str:
    if value is None or value == "":
        return "0" * length
    
    texto = str(value)
    apenas_digitos = re.sub(r'\D', '', texto)
    
    if not apenas_digitos:
        return "0" * length
    
    return apenas_digitos.zfill(length)


def format_money(value: Union[float, int, str, None], length: int) -> str:
    if value is None or value == "":
        return "0" * length
    
    try:
        if isinstance(value, str):
            value = value.strip().replace(',', '.')
        
        valor_float = float(value)
        valor_centavos = int(round(valor_float * 100))
        return str(valor_centavos).zfill(length)
    
    except (ValueError, TypeError):
        return "0" * length


def format_date(value: Union[datetime, str, None]) -> str:
    if value is None or value == "":
        return "000000"
    
    try:
        if isinstance(value, str):
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d', '%d-%m-%Y']:
                try:
                    data = datetime.strptime(value, fmt)
                    break
                except ValueError:
                    continue
            else:
                return "000000"
        elif isinstance(value, datetime):
            data = value
        else:
            return "000000"
        
        dia = str(data.day).zfill(2)
        mes = str(data.month).zfill(2)
        ano = str(data.year)[-2:]
        
        return f"{dia}{mes}{ano}"
    
    except (ValueError, AttributeError, TypeError):
        return "000000"


def remover_acentos(texto: Union[str, None]) -> str:
    if texto is None or texto == "":
        return ""
    
    texto_str = str(texto)
    
    if UNIDECODE_AVAILABLE:
        texto_sem_acento = unidecode(texto_str)
    else:
        texto_normalizado = unicodedata.normalize('NFD', texto_str)
        texto_sem_acento = ''.join(
            char for char in texto_normalizado 
            if unicodedata.category(char) != 'Mn'
        )
    
    texto_limpo = re.sub(r'[^A-Za-z0-9 ]', '', texto_sem_acento)
    return texto_limpo.upper()


def formatar_texto(valor: Union[str, None], tamanho: int) -> str:
    if valor is None or valor == "":
        return " " * tamanho
    
    texto_limpo = remover_acentos(valor)
    
    if len(texto_limpo) > tamanho:
        return texto_limpo[:tamanho]
    
    return texto_limpo.ljust(tamanho, ' ')


def formatar_numero(valor: Union[int, str, None], tamanho: int) -> str:
    if valor is None or valor == "":
        return "0" * tamanho
    
    texto = str(valor)
    apenas_digitos = re.sub(r'\D', '', texto)
    
    if not apenas_digitos:
        return "0" * tamanho
    
    return apenas_digitos.zfill(tamanho)


def formatar_dinheiro(valor: Union[float, int, str, None], tamanho: int) -> str:
    if valor is None or valor == "":
        return "0" * tamanho
    
    try:
        if isinstance(valor, str):
            valor_limpo = valor.strip().replace('R$', '').replace(' ', '')
            valor_limpo = valor_limpo.replace(',', '.')
            valor_float = float(valor_limpo)
        else:
            valor_float = float(valor)
        
        valor_centavos = int(round(valor_float * 100))
        return str(valor_centavos).zfill(tamanho)
    
    except (ValueError, TypeError):
        return "0" * tamanho


def formatar_data(valor: Union[datetime, str, None]) -> str:
    if valor is None or valor == "":
        return "000000"
    
    try:
        if isinstance(valor, str):
            formatos = [
                '%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d',
                '%d-%m-%Y', '%Y%m%d', '%d%m%Y'
            ]
            
            for fmt in formatos:
                try:
                    data = datetime.strptime(valor, fmt)
                    break
                except ValueError:
                    continue
            else:
                return "000000"
        elif isinstance(valor, datetime):
            data = valor
        else:
            return "000000"
        
        dia = str(data.day).zfill(2)
        mes = str(data.month).zfill(2)
        ano = str(data.year)[-2:]
        
        return f"{dia}{mes}{ano}"
    
    except (ValueError, AttributeError, TypeError):
        return "000000"
