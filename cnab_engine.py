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
    
    def gerar_header(self, cod_originador: str, razao_social: str, 
                     numero_banco: str, nome_banco: str, seq_arquivo: int) -> str:
        
        registro = [" "] * self.tamanho_registro
        
        registro[0] = "0"
        
        registro[1] = "1"
        
        remessa = "REMESSA"
        for i, char in enumerate(remessa):
            registro[2 + i] = char
        
        registro[9] = "0"
        registro[10] = "1"
        
        cobranca_limpa = formatar_texto("COBRANCA", 15)
        for i, char in enumerate(cobranca_limpa):
            registro[11 + i] = char
        
        cod_orig_limpo = formatar_numero(cod_originador, 20)
        for i, char in enumerate(cod_orig_limpo):
            registro[26 + i] = char
        
        razao_limpa = formatar_texto(razao_social, 30)
        for i, char in enumerate(razao_limpa):
            registro[46 + i] = char
        
        num_banco_limpo = formatar_numero(numero_banco, 3)
        for i, char in enumerate(num_banco_limpo):
            registro[76 + i] = char
        
        nome_banco_limpo = formatar_texto(nome_banco, 15)
        for i, char in enumerate(nome_banco_limpo):
            registro[79 + i] = char
        
        data_fmt = formatar_data(datetime.now())
        for i, char in enumerate(data_fmt):
            registro[94 + i] = char
        
        for i in range(100, 108):
            registro[i] = " "
        
        registro[108] = "M"
        registro[109] = "X"
        
        seq_header = "000001"
        for i, char in enumerate(seq_header):
            registro[110 + i] = char
        
        for i in range(117, 438):
            registro[i] = " "
        
        seq_final = "000001"
        for i, char in enumerate(seq_final):
            registro[438 + i] = char
        
        linha_final = "".join(registro)
        
        if len(linha_final) != self.tamanho_registro:
            raise ValueError(
                f"Header com tamanho incorreto: {len(linha_final)} "
                f"(esperado: {self.tamanho_registro})"
            )
        
        return linha_final
    
    def gerar_detalhe(self, linha: pd.Series, sequencial_registro: int, 
                     coobrigacao: str = "02") -> str:
        
        registro = [" "] * self.tamanho_registro
        
        registro[0] = "1"
        
        for i in range(1, 20):
            registro[i] = " "
        
        coobrig_fmt = formatar_numero(coobrigacao, 2)
        registro[20] = coobrig_fmt[0]
        registro[21] = coobrig_fmt[1]
        
        for i in range(22, 34):
            registro[i] = "0"
        
        registro[34] = "A"
        registro[35] = "A"
        
        registro[36] = "0"
        
        seu_numero_raw = ""
        if hasattr(linha, 'SEU_NUMERO') and pd.notna(linha.SEU_NUMERO):
            try:
                seu_numero_raw = str(int(float(linha.SEU_NUMERO)))
            except:
                seu_numero_raw = str(linha.SEU_NUMERO)
        
        seu_numero_fmt = formatar_numero(seu_numero_raw, 25)
        for i, char in enumerate(seu_numero_fmt):
            registro[37 + i] = char
        
        for i in range(62, 70):
            registro[i] = "0"
        
        id_recebivel = ""
        if hasattr(linha, 'ID_RECEBIVEL') and pd.notna(linha.ID_RECEBIVEL):
            id_recebivel = str(int(linha.ID_RECEBIVEL))
        
        id_fmt = formatar_numero(id_recebivel, 11)
        for i, char in enumerate(id_fmt):
            registro[70 + i] = char
        
        registro[81] = " "
        
        valor_presente = 0
        if hasattr(linha, 'VALOR_PRESENTE') and pd.notna(linha.VALOR_PRESENTE):
            valor_presente = linha.VALOR_PRESENTE
        
        valor_pres_fmt = formatar_dinheiro(valor_presente, 10)
        for i, char in enumerate(valor_pres_fmt):
            registro[82 + i] = char
        
        registro[92] = "0"
        
        registro[93] = " "
        
        data_referencia = None
        if hasattr(linha, 'DATA_REFERENCIA') and pd.notna(linha.DATA_REFERENCIA):
            data_referencia = linha.DATA_REFERENCIA
        
        data_ref_fmt = formatar_data(data_referencia)
        for i, char in enumerate(data_ref_fmt):
            registro[94 + i] = char
        
        for i in range(100, 105):
            registro[i] = " "
        
        registro[105] = "0"
        
        for i in range(106, 108):
            registro[i] = " "
        
        registro[108] = "7"
        registro[109] = "7"
        
        nu_documento = ""
        if hasattr(linha, 'NU_DOCUMENTO') and pd.notna(linha.NU_DOCUMENTO):
            nu_documento = str(linha.NU_DOCUMENTO)
        
        nu_doc_clean = formatar_texto(nu_documento, 10)
        for i, char in enumerate(nu_doc_clean):
            registro[110 + i] = char
        
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
        
        valor_nom_fmt = formatar_dinheiro(valor_nominal, 13)
        for i, char in enumerate(valor_nom_fmt):
            registro[126 + i] = char
        
        for i in range(139, 147):
            registro[i] = "0"
        
        registro[147] = "7"
        registro[148] = "1"
        
        registro[149] = " "
        
        data_emissao = None
        if hasattr(linha, 'DATA_EMISSAO') and pd.notna(linha.DATA_EMISSAO):
            data_emissao = linha.DATA_EMISSAO
        
        data_emis_fmt = formatar_data(data_emissao)
        for i, char in enumerate(data_emis_fmt):
            registro[150 + i] = char
        
        for i in range(156, 159):
            registro[i] = "0"
        
        doc_cedente = ""
        if hasattr(linha, 'DOC_CEDENTE') and pd.notna(linha.DOC_CEDENTE):
            doc_cedente = str(linha.DOC_CEDENTE).replace(".", "").replace("/", "").replace("-", "")
        
        tipo_pessoa_cedente = "02" if len(doc_cedente) == 14 else "01"
        registro[159] = tipo_pessoa_cedente[0]
        registro[160] = tipo_pessoa_cedente[1]
        
        for i in range(161, 192):
            registro[i] = "0"
        
        valor_aquisicao = 0
        if hasattr(linha, 'VALOR_AQUISICAO') and pd.notna(linha.VALOR_AQUISICAO):
            valor_aquisicao = linha.VALOR_AQUISICAO
        
        valor_aquis_fmt = formatar_dinheiro(valor_aquisicao, 13)
        for i, char in enumerate(valor_aquis_fmt):
            registro[192 + i] = char
        
        for i in range(205, 218):
            registro[i] = "0"
        
        doc_sacado = ""
        if hasattr(linha, 'DOC_SACADO') and pd.notna(linha.DOC_SACADO):
            doc_sacado = str(linha.DOC_SACADO).replace(".", "").replace("/", "").replace("-", "")
        
        tipo_pessoa_sacado = "02" if len(doc_sacado) == 14 else "01"
        registro[218] = tipo_pessoa_sacado[0]
        registro[219] = tipo_pessoa_sacado[1]
        
        doc_sacado_fmt = formatar_numero(doc_sacado, 14)
        for i, char in enumerate(doc_sacado_fmt):
            registro[220 + i] = char
        
        nome_sacado_raw = ""
        if hasattr(linha, 'NOME_SACADO') and pd.notna(linha.NOME_SACADO):
            nome_sacado_raw = str(linha.NOME_SACADO)
        
        nome_sac_fmt = formatar_texto(nome_sacado_raw, 40)
        for i, char in enumerate(nome_sac_fmt):
            registro[234 + i] = char
        
        endereco_fmt = formatar_texto("ENDERECO COMPLETO", 40)
        for i, char in enumerate(endereco_fmt):
            registro[274 + i] = char
        
        chave_nfe = ""
        if hasattr(linha, 'CHAVE_NFE') and pd.notna(linha.CHAVE_NFE):
            chave_nfe = str(linha.CHAVE_NFE)
        
        chave_nfe_fmt = formatar_numero(chave_nfe, 9)
        for i, char in enumerate(chave_nfe_fmt):
            registro[314 + i] = char
        
        for i in range(323, 326):
            registro[i] = " "
        
        for i in range(326, 334):
            registro[i] = "0"
        
        nome_cedente_raw = ""
        if hasattr(linha, 'NOME_CEDENTE') and pd.notna(linha.NOME_CEDENTE):
            nome_cedente_raw = str(linha.NOME_CEDENTE)
        
        nome_cedente = formatar_texto(nome_cedente_raw, 200)
        doc_cedente_clean = doc_cedente
        
        espaco_disponivel = 60
        tamanho_doc = len(doc_cedente_clean)
        tamanho_nome_disponivel = espaco_disponivel - tamanho_doc - 1
        
        if tamanho_nome_disponivel > 0:
            nome_cedente_truncado = nome_cedente[:tamanho_nome_disponivel]
        else:
            nome_cedente_truncado = ""
        
        campo_completo = nome_cedente_truncado
        if nome_cedente_truncado and doc_cedente_clean:
            campo_completo = nome_cedente_truncado + " " + doc_cedente_clean
        elif doc_cedente_clean:
            campo_completo = doc_cedente_clean
        
        posicao_inicial = 394 - len(campo_completo)
        if posicao_inicial < 334:
            posicao_inicial = 334
            campo_completo = campo_completo[-(394-334):]
        
        for i in range(334, posicao_inicial):
            registro[i] = " "
        
        for i, char in enumerate(campo_completo):
            if 334 + i < 394:
                registro[posicao_inicial + i] = char
        
        for i in range(394, 438):
            registro[i] = "0"
        
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
    
    def gerar_arquivo_completo(self, df: pd.DataFrame, cod_originador: str,
                              razao_social: str, numero_banco: str, 
                              nome_banco: str, seq_arquivo: int,
                              coobrigacao: str = "02") -> str:
        
        linhas = []
        
        header = self.gerar_header(cod_originador, razao_social, numero_banco, 
                                   nome_banco, seq_arquivo)
        linhas.append(header)
        
        for idx, row in df.iterrows():
            sequencial = idx + 2
            detalhe = self.gerar_detalhe(row, sequencial, coobrigacao)
            linhas.append(detalhe)
        
        total_registros = len(linhas) + 1
        trailer = self.gerar_trailer(total_registros)
        linhas.append(trailer)
        
        return "\r\n".join(linhas)


class CNABGenerator(GeradorCNAB):
    pass


class CNABEngine(GeradorCNAB):
    pass
