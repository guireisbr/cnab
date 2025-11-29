"""
Módulo responsável pela lógica de geração de arquivos CNAB
"""

import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional
from utils import (
    format_text, format_number, format_date, format_money,
    formatar_texto, formatar_numero, formatar_data, formatar_dinheiro
)


class CNABGenerator:
    """
    Classe principal para geração de arquivos CNAB no padrão 444 caracteres
    Baseado no Layout Fromtis - 444
    """
    
    def __init__(self):
        """
        Inicializa o gerador CNAB
        """
        self.dados = None
        self.cnab_gerado = None
        self.registro_length = 444
    
    def generate_header(self, sequence_number: int, originador_data: dict) -> str:
        """
        Gera o registro header do arquivo CNAB (Tipo 0)
        
        Args:
            sequence_number: Número sequencial do arquivo
            originador_data: Dicionário contendo:
                - codigo: Código do originador
                - nome: Nome do originador
        
        Returns:
            String formatada do header com 444 caracteres
            
        Layout:
            001-001: '0' (ID Registro Header)
            002-002: '1' (ID Arquivo Remessa)
            003-009: 'REMESSA' (Literal)
            010-011: '01' (Código do Serviço)
            012-026: 'COBRANCA' (Literal com espaços - 15 pos)
            027-046: Código Originador (20 pos numérico)
            047-076: Nome Originador (30 pos texto)
            077-079: '611' (Código Banco Paulista)
            080-094: 'PAULISTA S.A.' (Nome do Banco - 15 pos)
            095-100: Data de Gravação DDMMAA (6 pos)
            101-108: Brancos (8 pos)
            109-110: 'MX' (Identificação)
            111-117: Sequencial do Arquivo (7 pos numérico)
            118-438: Brancos (321 pos)
            439-444: Sequencial do Registro '000001' (6 pos)
        """
        # Monta o header posição por posição
        linha = ""
        
        # Pos 001-001: ID Registro
        linha += "0"
        
        # Pos 002-002: ID Arquivo
        linha += "1"
        
        # Pos 003-009: REMESSA (7 caracteres)
        linha += "REMESSA"
        
        # Pos 010-011: Código do Serviço
        linha += "01"
        
        # Pos 012-026: COBRANCA (15 caracteres com espaços à direita)
        linha += format_text("COBRANCA", 15)
        
        # Pos 027-046: Código Originador (20 posições numéricas)
        codigo_originador = originador_data.get('codigo', '')
        linha += format_number(codigo_originador, 20)
        
        # Pos 047-076: Nome Originador (30 posições texto)
        nome_originador = originador_data.get('nome', '')
        linha += format_text(nome_originador, 30)
        
        # Pos 077-079: Código do Banco Paulista
        linha += "611"
        
        # Pos 080-094: Nome do Banco (15 caracteres)
        linha += format_text("PAULISTA S.A.", 15)
        
        # Pos 095-100: Data de Gravação (DDMMAA)
        data_hoje = datetime.now()
        linha += format_date(data_hoje)
        
        # Pos 101-108: Brancos (8 posições)
        linha += " " * 8
        
        # Pos 109-110: Identificação MX
        linha += "MX"
        
        # Pos 111-117: Sequencial do Arquivo (7 posições)
        linha += format_number(sequence_number, 7)
        
        # Pos 118-438: Brancos (321 posições)
        linha += " " * 321
        
        # Pos 439-444: Sequencial do Registro (sempre 000001 para header)
        linha += "000001"
        
        # Valida o tamanho final
        if len(linha) != self.registro_length:
            raise ValueError(
                f"Header gerado com tamanho incorreto: {len(linha)} "
                f"(esperado: {self.registro_length})"
            )
        
        return linha
    
    def generate_trailer(self, record_count: int) -> str:
        """
        Gera o registro trailer do arquivo CNAB (Tipo 9)
        
        Args:
            record_count: Número total de registros no arquivo (incluindo header e trailer)
        
        Returns:
            String formatada do trailer com 444 caracteres
            
        Layout:
            001-001: '9' (ID Registro Trailer)
            002-007: Quantidade total de registros (6 pos numérico)
            008-438: Brancos (431 pos)
            439-444: Sequencial do Registro (6 pos numérico)
        """
        linha = ""
        
        # Pos 001-001: ID Registro Trailer
        linha += "9"
        
        # Pos 002-007: Quantidade total de registros (6 posições)
        linha += format_number(record_count, 6)
        
        # Pos 008-438: Brancos (431 posições)
        linha += " " * 431
        
        # Pos 439-444: Sequencial do Registro (número do registro trailer)
        linha += format_number(record_count, 6)
        
        # Valida o tamanho final
        if len(linha) != self.registro_length:
            raise ValueError(
                f"Trailer gerado com tamanho incorreto: {len(linha)} "
                f"(esperado: {self.registro_length})"
            )
        
        return linha
    
    def carregar_dados(self, arquivo) -> pd.DataFrame:
        """
        Carrega dados de um arquivo Excel ou CSV
        
        Args:
            arquivo: Arquivo carregado pelo Streamlit
            
        Returns:
            DataFrame com os dados carregados
        """
        # TODO: Implementar carregamento de dados
        pass
    
    def validar_dados(self, df: pd.DataFrame) -> tuple[bool, List[str]]:
        """
        Valida os dados carregados
        
        Args:
            df: DataFrame com os dados
            
        Returns:
            Tuple (válido, lista de erros)
        """
        # TODO: Implementar validação
        pass
    
    def generate_detail(self, row, sequence_number: int) -> str:
        """
        Gera um registro de detalhe do arquivo CNAB (Tipo 1)
        
        Args:
            row: Linha do DataFrame pandas com os dados
            sequence_number: Número sequencial do registro
            
        Returns:
            String formatada do detalhe com 444 caracteres
            
        Layout baseado no arquivo de exemplo e colunas do Excel:
            001-001: '1' (ID Registro Detalhe)
            002-020: Brancos (19 pos - Débito Automático)
            021-022: '02' (Coobrigação)
            023-037: Brancos/Campos diversos
            038-062: Seu Número (25 pos)
            063-068: Data Vencimento DDMMAA (6 pos)
            069-081: Valor Título (13 pos monetário)
            082-084: Código Banco (3 pos)
            085-089: Brancos (5 pos)
            090-091: Espécie Título '04' (2 pos)
            092-093: Aceite
            094-099: Data Emissão DDMMAA (6 pos)
            100-138: Campos diversos
            139-140: Tipo Inscrição Sacado (01=CPF, 02=CNPJ)
            141-154: Documento Sacado (14 pos)
            155-194: Nome Sacado (40 pos)
            195-234: Endereço Sacado (40 pos)
            235-247: Campos adicionais
            248-257: Nosso Número (10 pos)
            258-438: Campos diversos e brancos
            439-444: Sequencial do Registro (6 pos)
        """
        linha = ""
        
        # Pos 001-001: ID Registro Detalhe
        linha += "1"
        
        # Pos 002-020: Brancos (Débito Automático - 19 posições)
        linha += " " * 19
        
        # Pos 021-022: Coobrigação
        linha += "02"
        
        # Pos 023-037: Brancos e campos não utilizados (15 posições)
        linha += "0" * 14  # zeros
        linha += "AA"  # 2 caracteres fixos (visto no exemplo)
        
        # Pos 039-044: Campos numéricos (6 posições) - visto no exemplo
        linha += "0" * 6
        
        # Pos 045-047: Carteira/Agência (3 posições)
        linha += "400"  # fixo conforme exemplo
        
        # Pos 048-052: Campos diversos (5 posições)
        linha += "50000"  # fixo conforme exemplo
        
        # Pos 053-062: SEU NÚMERO (10 posições) - parte inicial
        # Usa SEU_NUMERO ou ID_RECEBIVEL
        seu_numero = ""
        if hasattr(row, 'SEU_NUMERO') and row.SEU_NUMERO:
            seu_numero = str(row.SEU_NUMERO)
        elif hasattr(row, 'ID_RECEBIVEL') and row.ID_RECEBIVEL:
            seu_numero = str(row.ID_RECEBIVEL)
        linha += format_number(seu_numero, 10)
        
        # Pos 063-068: DATA VENCIMENTO (DDMMAA - 6 posições)
        data_vencimento = None
        if hasattr(row, 'DATA_VENCIMENTO_AJUSTADA'):
            data_vencimento = row.DATA_VENCIMENTO_AJUSTADA
        elif hasattr(row, 'DATA_VENCIMENTO'):
            data_vencimento = row.DATA_VENCIMENTO
        linha += format_date(data_vencimento)
        
        # Pos 069-081: VALOR TÍTULO (13 posições monetárias)
        valor_nominal = 0
        if hasattr(row, 'VALOR_NOMINAL') and row.VALOR_NOMINAL:
            valor_nominal = row.VALOR_NOMINAL
        linha += format_money(valor_nominal, 13)
        
        # Pos 082-084: Código Banco
        linha += "000"
        
        # Pos 085-089: Agência (5 posições)
        linha += "00000"
        
        # Pos 090-091: ESPÉCIE TÍTULO (2 posições)
        linha += "04"  # DS - Duplicata de Serviço
        
        # Pos 092-093: Aceite (2 posições)
        linha += "  "  # brancos
        
        # Pos 094-099: DATA EMISSÃO (DDMMAA - 6 posições)
        data_emissao = None
        if hasattr(row, 'DATA_EMISSAO'):
            data_emissao = row.DATA_EMISSAO
        linha += format_date(data_emissao)
        
        # Pos 100-109: Instruções (10 posições)
        linha += "0000200000"  # conforme exemplo
        
        # Pos 110-138: Juros, multa e outros campos (29 posições)
        linha += "0" * 29
        
        # Pos 139-140: TIPO INSCRIÇÃO SACADO (01=CPF, 02=CNPJ)
        doc_sacado = ""
        if hasattr(row, 'DOC_SACADO') and row.DOC_SACADO:
            doc_sacado = str(row.DOC_SACADO)
        
        # Remove caracteres não numéricos
        doc_sacado_limpo = format_number(doc_sacado, 14)
        
        # Determina tipo: CPF (11 dígitos) ou CNPJ (14 dígitos)
        doc_apenas_digitos = doc_sacado_limpo.lstrip('0')
        if len(doc_apenas_digitos) > 11:
            tipo_inscricao = "02"  # CNPJ
        else:
            tipo_inscricao = "01"  # CPF
        linha += tipo_inscricao
        
        # Pos 141-154: DOCUMENTO SACADO (14 posições)
        linha += doc_sacado_limpo
        
        # Pos 155-194: NOME SACADO (40 posições)
        nome_sacado = ""
        if hasattr(row, 'NOME_SACADO') and row.NOME_SACADO:
            nome_sacado = str(row.NOME_SACADO)
        linha += format_text(nome_sacado, 40)
        
        # Pos 195-234: ENDEREÇO SACADO (40 posições)
        # Usando valor fixo conforme exemplo e instrução do usuário
        linha += format_text("ENDERECO COMPLETO", 40)
        
        # Pos 235-247: Campos diversos (13 posições)
        linha += " " * 3
        linha += format_number(seu_numero, 10)  # Repete seu número
        
        # Pos 248-250: Brancos (3 posições)
        linha += " " * 3
        
        # Pos 251-258: Zeros (8 posições)
        linha += "0" * 8
        
        # Pos 259-298: NOME EMPRESA/CEDENTE (40 posições)
        linha += format_text("CAPITAL CONSIG SOCIEDADE DE CREDITO DIRE", 40)
        
        # Pos 299-304: Brancos (6 posições)
        linha += " " * 6
        
        # Pos 305-314: NOSSO NÚMERO (10 posições)
        nosso_numero = ""
        if hasattr(row, 'DS_NOSSO_NUMERO') and row.DS_NOSSO_NUMERO:
            nosso_numero = str(row.DS_NOSSO_NUMERO)
        elif hasattr(row, 'NOSSO_NUMERO') and row.NOSSO_NUMERO:
            nosso_numero = str(row.NOSSO_NUMERO)
        linha += format_number(nosso_numero, 10)
        
        # Pos 315-438: Brancos e zeros diversos (124 posições)
        linha += "0" * 124
        
        # Pos 439-444: SEQUENCIAL DO REGISTRO (6 posições)
        linha += format_number(sequence_number, 6)
        
        # Valida o tamanho final
        if len(linha) != self.registro_length:
            raise ValueError(
                f"Detalhe gerado com tamanho incorreto: {len(linha)} "
                f"(esperado: {self.registro_length})"
            )
        
        return linha
    
    def gerar_detalhe(self, registro: pd.Series, numero_sequencial: int) -> str:
        """
        Alias para generate_detail (compatibilidade)
        
        Args:
            registro: Série do pandas com dados de um registro
            numero_sequencial: Número sequencial do registro
            
        Returns:
            String formatada do detalhe
        """
        return self.generate_detail(registro, numero_sequencial)
    
    def gerar_cnab(self, df: pd.DataFrame, sequence_number: int, 
                   originador_data: dict) -> str:
        """
        Gera o arquivo CNAB completo
        
        Args:
            df: DataFrame com os dados
            sequence_number: Número sequencial do arquivo
            originador_data: Dados do originador
            
        Returns:
            String com o conteúdo completo do arquivo CNAB
        """
        linhas = []
        
        # 1. Gera Header
        header = self.generate_header(sequence_number, originador_data)
        linhas.append(header)
        
        # 2. Gera Detalhes
        for idx, row in df.iterrows():
            numero_sequencial = idx + 2  # +2 porque header é 1
            detalhe = self.generate_detail(row, numero_sequencial)
            linhas.append(detalhe)
        
        # 3. Gera Trailer
        total_registros = len(linhas) + 1  # +1 para o trailer
        trailer = self.generate_trailer(total_registros)
        linhas.append(trailer)
        
        # Junta todas as linhas com quebra de linha
        return "\n".join(linhas)


# Mantém compatibilidade com código existente
class CNABEngine(CNABGenerator):
    """
    Alias para CNABGenerator (compatibilidade retroativa)
    """
    pass


# =============================================================================
# CLASSE EM PORTUGUÊS - GeradorCNAB
# =============================================================================

class GeradorCNAB:
    """
    Classe para geração de arquivos CNAB 444 caracteres (versão em português)
    Baseada no layout CNAB 444 posições e arquivo de exemplo
    """
    
    def __init__(self):
        """
        Inicializa o gerador CNAB
        """
        self.tamanho_registro = 444
        self.dados = None
    
    def gerar_header(self, nome_originador: str, cod_originador: str, 
                     seq_arquivo: int) -> str:
        """
        Gera o registro header (Tipo 0) do arquivo CNAB 444 posições
        
        Args:
            nome_originador: Nome do originador/empresa
            cod_originador: Código do originador
            seq_arquivo: Número sequencial do arquivo
            
        Returns:
            String com 444 caracteres do header
            
        Layout CNAB 444:
            001-001: '0' (Tipo Registro Header)
            002-002: '1' (Tipo Arquivo - Remessa)
            003-009: 'REMESSA' (7 pos)
            010-011: '01' (Código Serviço)
            012-026: 'COBRANCA' (15 pos com espaços)
            027-046: Código Originador (20 pos numérico)
            047-076: Nome Originador (30 pos texto)
            077-079: '611' (Código Banco Paulista)
            080-094: 'PAULISTA S.A.' (15 pos)
            095-100: Data Gravação DDMMAA (6 pos)
            101-108: Brancos (8 pos)
            109-110: 'MX' (2 pos)
            111-117: Sequencial Arquivo (7 pos numérico)
            118-438: Brancos (321 pos)
            439-444: '000001' (Sequencial Registro - sempre 1 para header)
        """
        linha = ""
        
        # Pos 001: Tipo Registro
        linha += "0"
        
        # Pos 002: Tipo Arquivo
        linha += "1"
        
        # Pos 003-009: REMESSA (7 caracteres)
        linha += "REMESSA"
        
        # Pos 010-011: Código Serviço
        linha += "01"
        
        # Pos 012-026: COBRANCA (15 caracteres com espaços à direita)
        linha += formatar_texto("COBRANCA", 15)
        
        # Pos 027-046: Código Originador (20 posições numéricas)
        linha += formatar_numero(cod_originador, 20)
        
        # Pos 047-076: Nome Originador (30 posições texto)
        linha += formatar_texto(nome_originador, 30)
        
        # Pos 077-079: Código Banco
        linha += "611"
        
        # Pos 080-094: Nome Banco (15 posições)
        linha += formatar_texto("PAULISTA S.A.", 15)
        
        # Pos 095-100: Data Gravação (DDMMAA)
        linha += formatar_data(datetime.now())
        
        # Pos 101-108: Brancos (8 posições)
        linha += " " * 8
        
        # Pos 109-110: Identificação MX
        linha += "MX"
        
        # Pos 111-117: Sequencial do Arquivo (7 posições)
        linha += formatar_numero(seq_arquivo, 7)
        
        # Pos 118-438: Brancos (321 posições)
        linha += " " * 321
        
        # Pos 439-444: Sequencial do Registro (sempre 000001 para header)
        linha += "000001"
        
        # Valida tamanho
        if len(linha) != self.tamanho_registro:
            raise ValueError(
                f"Header com tamanho incorreto: {len(linha)} "
                f"(esperado: {self.tamanho_registro})"
            )
        
        return linha
    
    def gerar_detalhe(self, linha: pd.Series, sequencial_registro: int) -> str:
        """
        Gera um registro de detalhe (Tipo 1) do arquivo CNAB 444 posições
        
        Args:
            linha: Linha do DataFrame com os dados do registro
            sequencial_registro: Número sequencial do registro
            
        Returns:
            String com 444 caracteres do detalhe
            
        Mapeamento de colunas:
            - SEU_NUMERO → Pos 038-062 (25 pos texto)
            - DATA_VENCIMENTO_AJUSTADA → Pos 121-126 (6 pos DDMMAA)
            - VALOR_NOMINAL → Pos 127-139 (13 pos monetário)
            - DATA_EMISSAO → Pos 151-156 (6 pos DDMMAA)
            - DOC_SACADO → Pos 221-234 (14 pos numérico)
            - NOME_SACADO → Pos 235-274 (40 pos texto)
            - Endereço fixo → Pos 275-314 (40 pos texto)
        """
        # Inicializa linha com brancos (será preenchida posição por posição)
        registro = [" "] * self.tamanho_registro
        
        # Pos 001: Tipo Registro Detalhe
        registro[0] = "1"
        
        # Pos 002-037: Preencher com brancos ou conforme padrão (36 pos)
        # Baseado no exemplo CNAB_Consignado2811.txt
        for i in range(1, 20):  # Pos 2-20: brancos (19 pos)
            registro[i] = " "
        
        # Pos 021-022: '02' (Coobrigação - conforme exemplo)
        registro[20] = "0"
        registro[21] = "2"
        
        # Pos 023-037: Zeros e campos fixos (15 pos) - baseado no exemplo
        for i in range(22, 37):
            registro[i] = "0"
        
        # Pos 038-062: SEU_NUMERO (25 posições texto)
        seu_numero = ""
        if hasattr(linha, 'SEU_NUMERO') and pd.notna(linha.SEU_NUMERO):
            seu_numero = str(linha.SEU_NUMERO)
        elif hasattr(linha, 'ID_RECEBIVEL') and pd.notna(linha.ID_RECEBIVEL):
            seu_numero = str(linha.ID_RECEBIVEL)
        
        seu_numero_fmt = formatar_numero(seu_numero, 25)
        for i, char in enumerate(seu_numero_fmt):
            registro[37 + i] = char  # Pos 38-62
        
        # Pos 063-120: Campos diversos conforme exemplo (58 pos)
        # Preenchimento baseado no arquivo exemplo
        for i in range(62, 120):
            registro[i] = "0"
        
        # Pos 121-126: DATA_VENCIMENTO_AJUSTADA (6 posições DDMMAA)
        data_vencimento = None
        if hasattr(linha, 'DATA_VENCIMENTO_AJUSTADA') and pd.notna(linha.DATA_VENCIMENTO_AJUSTADA):
            data_vencimento = linha.DATA_VENCIMENTO_AJUSTADA
        elif hasattr(linha, 'DATA_VENCIMENTO') and pd.notna(linha.DATA_VENCIMENTO):
            data_vencimento = linha.DATA_VENCIMENTO
        
        data_venc_fmt = formatar_data(data_vencimento)
        for i, char in enumerate(data_venc_fmt):
            registro[120 + i] = char  # Pos 121-126
        
        # Pos 127-139: VALOR_NOMINAL (13 posições monetário)
        valor_nominal = 0
        if hasattr(linha, 'VALOR_NOMINAL') and pd.notna(linha.VALOR_NOMINAL):
            valor_nominal = linha.VALOR_NOMINAL
        
        valor_fmt = formatar_dinheiro(valor_nominal, 13)
        for i, char in enumerate(valor_fmt):
            registro[126 + i] = char  # Pos 127-139
        
        # Pos 140-147: Campos diversos (8 pos)
        for i in range(139, 147):
            registro[i] = "0"
        
        # Pos 148-149: Espécie Título '04' (DS)
        registro[147] = "0"
        registro[148] = "4"
        
        # Pos 150: Campo adicional
        registro[149] = " "
        
        # Pos 151-156: DATA_EMISSAO (6 posições DDMMAA)
        data_emissao = None
        if hasattr(linha, 'DATA_EMISSAO') and pd.notna(linha.DATA_EMISSAO):
            data_emissao = linha.DATA_EMISSAO
        
        data_emis_fmt = formatar_data(data_emissao)
        for i, char in enumerate(data_emis_fmt):
            registro[150 + i] = char  # Pos 151-156
        
        # Pos 157-220: Campos diversos (64 pos)
        for i in range(156, 220):
            registro[i] = "0"
        
        # Pos 221-234: DOC_SACADO (14 posições numérico - CPF/CNPJ)
        doc_sacado = ""
        if hasattr(linha, 'DOC_SACADO') and pd.notna(linha.DOC_SACADO):
            doc_sacado = str(linha.DOC_SACADO)
        
        doc_fmt = formatar_numero(doc_sacado, 14)
        for i, char in enumerate(doc_fmt):
            registro[220 + i] = char  # Pos 221-234
        
        # Pos 235-274: NOME_SACADO (40 posições texto)
        nome_sacado = ""
        if hasattr(linha, 'NOME_SACADO') and pd.notna(linha.NOME_SACADO):
            nome_sacado = str(linha.NOME_SACADO)
        
        nome_fmt = formatar_texto(nome_sacado, 40)
        for i, char in enumerate(nome_fmt):
            registro[234 + i] = char  # Pos 235-274
        
        # Pos 275-314: ENDERECO (40 posições texto - fixo por enquanto)
        endereco_fmt = formatar_texto("ENDERECO COMPLETO", 40)
        for i, char in enumerate(endereco_fmt):
            registro[274 + i] = char  # Pos 275-314
        
        # Pos 315-438: Campos diversos e brancos (124 pos)
        for i in range(314, 438):
            registro[i] = " "
        
        # Pos 439-444: Sequencial do Registro (6 posições)
        seq_fmt = formatar_numero(sequencial_registro, 6)
        for i, char in enumerate(seq_fmt):
            registro[438 + i] = char  # Pos 439-444
        
        # Converte lista em string
        linha_final = "".join(registro)
        
        # Valida tamanho
        if len(linha_final) != self.tamanho_registro:
            raise ValueError(
                f"Detalhe com tamanho incorreto: {len(linha_final)} "
                f"(esperado: {self.tamanho_registro})"
            )
        
        return linha_final
    
    def gerar_trailer(self, total_registros: int) -> str:
        """
        Gera o registro trailer (Tipo 9) do arquivo CNAB 444 posições
        
        Args:
            total_registros: Número total de registros no arquivo
                            (incluindo header e trailer)
            
        Returns:
            String com 444 caracteres do trailer
            
        Layout:
            001-001: '9' (Tipo Registro Trailer)
            002-007: Total de registros (6 pos numérico)
            008-438: Brancos (431 pos)
            439-444: Sequencial do Registro (6 pos numérico)
        """
        linha = ""
        
        # Pos 001: Tipo Registro
        linha += "9"
        
        # Pos 002-007: Total de registros (6 posições)
        linha += formatar_numero(total_registros, 6)
        
        # Pos 008-438: Brancos (431 posições)
        linha += " " * 431
        
        # Pos 439-444: Sequencial do Registro (mesmo valor que total_registros)
        linha += formatar_numero(total_registros, 6)
        
        # Valida tamanho
        if len(linha) != self.tamanho_registro:
            raise ValueError(
                f"Trailer com tamanho incorreto: {len(linha)} "
                f"(esperado: {self.tamanho_registro})"
            )
        
        return linha
    
    def gerar_arquivo_completo(self, df: pd.DataFrame, nome_originador: str,
                              cod_originador: str, seq_arquivo: int) -> str:
        """
        Gera o arquivo CNAB completo (Header + Detalhes + Trailer)
        
        Args:
            df: DataFrame com os dados dos registros
            nome_originador: Nome do originador
            cod_originador: Código do originador
            seq_arquivo: Número sequencial do arquivo
            
        Returns:
            String com o conteúdo completo do arquivo CNAB
        """
        linhas = []
        
        # 1. Header
        header = self.gerar_header(nome_originador, cod_originador, seq_arquivo)
        linhas.append(header)
        
        # 2. Detalhes
        for idx, row in df.iterrows():
            sequencial = idx + 2  # +2 porque header é 1
            detalhe = self.gerar_detalhe(row, sequencial)
            linhas.append(detalhe)
        
        # 3. Trailer
        total_registros = len(linhas) + 1  # +1 para o trailer
        trailer = self.gerar_trailer(total_registros)
        linhas.append(trailer)
        
        # Junta com quebra de linha padrão CNAB (\r\n)
        return "\r\n".join(linhas)

