import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional
from utils import (
    format_text, format_number, format_date, format_money,
    formatar_texto, formatar_numero, formatar_data, formatar_dinheiro
)


class GeradorCNAB:
    
    def __init__(self):
        self.tamanho_registro = 444
        self.dados = None
    
    def gerar_header(self, nome_originador: str, cod_originador: str, 
                     seq_arquivo: int) -> str:
        
        linha = ""
        linha += "0"
        linha += "1"
        linha += "REMESSA"
        linha += "01"
        linha += formatar_texto("COBRANCA", 15)
        linha += formatar_numero(cod_originador, 20)
        linha += formatar_texto(nome_originador, 30)
        linha += "611"
        linha += formatar_texto("PAULISTA S.A.", 15)
        linha += formatar_data(datetime.now())
        linha += " " * 8
        linha += "MX"
        linha += formatar_numero(seq_arquivo, 7)
        linha += " " * 321
        linha += "000001"
        
        if len(linha) != self.tamanho_registro:
            raise ValueError(
                f"Header com tamanho incorreto: {len(linha)} "
                f"(esperado: {self.tamanho_registro})"
            )
        
        return linha
    
    def gerar_detalhe(self, linha: pd.Series, sequencial_registro: int) -> str:
        
        registro = [" "] * self.tamanho_registro
        
        registro[0] = "1"
        
        for i in range(1, 20):
            registro[i] = " "
        
        registro[20] = "0"
        registro[21] = "2"
        
        for i in range(22, 37):
            registro[i] = "0"
        
        seu_numero = ""
        if hasattr(linha, 'SEU_NUMERO') and pd.notna(linha.SEU_NUMERO):
            seu_numero = str(linha.SEU_NUMERO)
        elif hasattr(linha, 'ID_RECEBIVEL') and pd.notna(linha.ID_RECEBIVEL):
            seu_numero = str(linha.ID_RECEBIVEL)
        
        seu_numero_fmt = formatar_numero(seu_numero, 25)
        for i, char in enumerate(seu_numero_fmt):
            registro[37 + i] = char
        
        for i in range(62, 120):
            registro[i] = "0"
        
        data_vencimento = None
        if hasattr(linha, 'DATA_VENCIMENTO_AJUSTADA') and pd.notna(linha.DATA_VENCIMENTO_AJUSTADA):
            data_vencimento = linha.DATA_VENCIMENTO_AJUSTADA
        elif hasattr(linha, 'DATA_VENCIMENTO') and pd.notna(linha.DATA_VENCIMENTO):
            data_vencimento = linha.DATA_VENCIMENTO
        
        data_venc_fmt = formatar_data(data_vencimento)
        for i, char in enumerate(data_venc_fmt):
            registro[120 + i] = char
        
        valor_nominal = 0
        if hasattr(linha, 'VALOR_NOMINAL') and pd.notna(linha.VALOR_NOMINAL):
            valor_nominal = linha.VALOR_NOMINAL
        
        valor_fmt = formatar_dinheiro(valor_nominal, 13)
        for i, char in enumerate(valor_fmt):
            registro[126 + i] = char
        
        for i in range(139, 147):
            registro[i] = "0"
        
        registro[147] = "0"
        registro[148] = "4"
        
        registro[149] = " "
        
        data_emissao = None
        if hasattr(linha, 'DATA_EMISSAO') and pd.notna(linha.DATA_EMISSAO):
            data_emissao = linha.DATA_EMISSAO
        
        data_emis_fmt = formatar_data(data_emissao)
        for i, char in enumerate(data_emis_fmt):
            registro[150 + i] = char
        
        for i in range(156, 220):
            registro[i] = "0"
        
        doc_sacado = ""
        if hasattr(linha, 'DOC_SACADO') and pd.notna(linha.DOC_SACADO):
            doc_sacado = str(linha.DOC_SACADO)
        
        doc_fmt = formatar_numero(doc_sacado, 14)
        for i, char in enumerate(doc_fmt):
            registro[220 + i] = char
        
        nome_sacado = ""
        if hasattr(linha, 'NOME_SACADO') and pd.notna(linha.NOME_SACADO):
            nome_sacado = str(linha.NOME_SACADO)
        
        nome_fmt = formatar_texto(nome_sacado, 40)
        for i, char in enumerate(nome_fmt):
            registro[234 + i] = char
        
        endereco_fmt = formatar_texto("ENDERECO COMPLETO", 40)
        for i, char in enumerate(endereco_fmt):
            registro[274 + i] = char
        
        for i in range(314, 438):
            registro[i] = " "
        
        seq_fmt = formatar_numero(sequencial_registro, 6)
        for i, char in enumerate(seq_fmt):
            registro[438 + i] = char
        
        linha_final = "".join(registro)
        
        if len(linha_final) != self.tamanho_registro:
            raise ValueError(
                f"Detalhe com tamanho incorreto: {len(linha_final)} "
                f"(esperado: {self.tamanho_registro})"
            )
        
        return linha_final
    
    def gerar_trailer(self, total_registros: int) -> str:
        
        linha = ""
        linha += "9"
        linha += " " * 437
        linha += formatar_numero(total_registros, 6)
        
        if len(linha) != self.tamanho_registro:
            raise ValueError(
                f"Trailer com tamanho incorreto: {len(linha)} "
                f"(esperado: {self.tamanho_registro})"
            )
        
        return linha
    
    def gerar_arquivo_completo(self, df: pd.DataFrame, nome_originador: str,
                              cod_originador: str, seq_arquivo: int) -> str:
        
        linhas = []
        
        header = self.gerar_header(nome_originador, cod_originador, seq_arquivo)
        linhas.append(header)
        
        for idx, row in df.iterrows():
            sequencial = idx + 2
            detalhe = self.gerar_detalhe(row, sequencial)
            linhas.append(detalhe)
        
        total_registros = len(linhas) + 1
        trailer = self.gerar_trailer(total_registros)
        linhas.append(trailer)
        
        return "\r\n".join(linhas)


class CNABGenerator(GeradorCNAB):
    pass


class CNABEngine(GeradorCNAB):
    pass
