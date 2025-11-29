"""
GeraCNAB-FIDC - Aplicação Web para Geração de Arquivos CNAB
Ponto de entrada principal da aplicação Streamlit
"""

import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from cnab_engine import CNABGenerator


def carregar_arquivo(arquivo):
    """
    Carrega arquivo Excel ou CSV
    
    Args:
        arquivo: Arquivo carregado pelo Streamlit
        
    Returns:
        DataFrame ou None em caso de erro
    """
    try:
        nome_arquivo = arquivo.name.lower()
        
        if nome_arquivo.endswith('.csv'):
            df = pd.read_csv(arquivo)
        elif nome_arquivo.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(arquivo)
        else:
            st.error("❌ Formato de arquivo não suportado!")
            return None
        
        return df
    
    except Exception as e:
        st.error(f"❌ Erro ao carregar arquivo: {str(e)}")
        return None


def main():
    """
    Função principal da aplicação Streamlit
    Pode ser chamada diretamente ou importada por app.py
    """
    # Apenas configura a página se estiver sendo executado diretamente
    # (não quando importado por app.py que já configura)
    try:
        st.set_page_config(
            page_title="Gerador CNAB 444",
            page_icon="🏦",
            layout="wide"
        )
    except st.errors.StreamlitAPIException:
        # Página já foi configurada (importado por app.py)
        pass
    
    # Título principal
    st.title("🏦 Gerador de Remessa CNAB 444 - CONCRETO")
    st.markdown("### Sistema de Geração de Arquivos CNAB no Padrão 444 caracteres")
    st.markdown("---")
    
    # Seção de configuração
    st.header("⚙️ Configurações do Originador")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        codigo_originador = st.text_input(
            "Código do Originador",
            value="20250158479927000136",
            help="Código numérico do originador (até 20 dígitos)",
            max_chars=20
        )
    
    with col2:
        nome_originador = st.text_input(
            "Nome do Originador",
            value="BANCO PAULISTA",
            help="Nome do originador (até 30 caracteres)",
            max_chars=30
        )
    
    with col3:
        numero_sequencial = st.number_input(
            "Número Sequencial do Arquivo",
            min_value=1,
            max_value=9999999,
            value=1,
            step=1,
            help="Número sequencial do arquivo de remessa"
        )
    
    st.markdown("---")
    
    # Seção de upload
    st.header("📁 Upload do Arquivo de Dados")
    
    arquivo_upload = st.file_uploader(
        "Selecione o arquivo com os dados para geração do CNAB",
        type=['xlsx', 'xls', 'csv'],
        help="Formatos aceitos: Excel (.xlsx, .xls) ou CSV (.csv)"
    )
    
    # Verifica se arquivo foi carregado
    if arquivo_upload is not None:
        st.success(f"✅ Arquivo carregado: **{arquivo_upload.name}**")
        
        # Carrega os dados
        with st.spinner("⏳ Carregando dados..."):
            df = carregar_arquivo(arquivo_upload)
        
        if df is not None:
            # Mostra informações do arquivo
            st.markdown("---")
            st.header("📊 Prévia dos Dados")
            
            col_info1, col_info2, col_info3 = st.columns(3)
            with col_info1:
                st.metric("Total de Registros", len(df))
            with col_info2:
                st.metric("Total de Colunas", len(df.columns))
            with col_info3:
                st.metric("Registros para CNAB", len(df))
            
            # Mostra prévia das primeiras 5 linhas
            st.subheader("🔍 Primeiras 5 linhas")
            st.dataframe(df.head(5), use_container_width=True)
            
            # Mostra colunas disponíveis
            with st.expander("📋 Colunas disponíveis no arquivo"):
                st.write(list(df.columns))
            
            st.markdown("---")
            
            # Botão para gerar CNAB
            st.header("🚀 Geração do Arquivo CNAB")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            
            with col_btn2:
                gerar_cnab = st.button(
                    "🎯 Gerar CNAB",
                    type="primary",
                    use_container_width=True
                )
            
            # Processa geração do CNAB
            if gerar_cnab:
                # Validações
                if not codigo_originador:
                    st.error("❌ Por favor, informe o Código do Originador!")
                    return
                
                if not nome_originador:
                    st.error("❌ Por favor, informe o Nome do Originador!")
                    return
                
                try:
                    with st.spinner("⏳ Gerando arquivo CNAB..."):
                        # Instancia o gerador
                        gerador = CNABGenerator()
                        
                        # Prepara dados do originador
                        originador_data = {
                            'codigo': codigo_originador,
                            'nome': nome_originador
                        }
                        
                        # Gera o arquivo CNAB completo
                        linhas = []
                        
                        # 1. Gera Header
                        header = gerador.generate_header(numero_sequencial, originador_data)
                        linhas.append(header)
                        
                        # 2. Gera Detalhes
                        total_detalhes = 0
                        erros = []
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for idx, row in df.iterrows():
                            try:
                                numero_sequencial_registro = idx + 2  # +2 porque header é 1
                                detalhe = gerador.generate_detail(row, numero_sequencial_registro)
                                linhas.append(detalhe)
                                total_detalhes += 1
                                
                                # Atualiza barra de progresso
                                progress = (idx + 1) / len(df)
                                progress_bar.progress(progress)
                                status_text.text(f"Processando registro {idx + 1} de {len(df)}...")
                                
                            except Exception as e:
                                erros.append(f"Linha {idx + 2}: {str(e)}")
                        
                        progress_bar.empty()
                        status_text.empty()
                        
                        # 3. Gera Trailer
                        total_registros = len(linhas) + 1  # +1 para o trailer
                        trailer = gerador.generate_trailer(total_registros)
                        linhas.append(trailer)
                        
                        # Concatena tudo com \r\n (padrão CNAB)
                        conteudo_cnab = "\r\n".join(linhas)
                        
                        # Mostra resultado
                        st.success("✅ Arquivo CNAB gerado com sucesso!")
                        
                        # Estatísticas
                        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                        with col_stat1:
                            st.metric("📝 Header", "1 registro")
                        with col_stat2:
                            st.metric("📋 Detalhes", f"{total_detalhes} registros")
                        with col_stat3:
                            st.metric("📊 Trailer", "1 registro")
                        with col_stat4:
                            st.metric("📦 Total", f"{total_registros} registros")
                        
                        # Mostra erros se houver
                        if erros:
                            with st.expander(f"⚠️ Avisos/Erros ({len(erros)} encontrados)"):
                                for erro in erros:
                                    st.warning(erro)
                        
                        # Preparar arquivo para download
                        nome_arquivo_saida = f"REMESSA_{datetime.now().strftime('%Y%m%d_%H%M%S')}.REM"
                        
                        # Converte para bytes
                        conteudo_bytes = conteudo_cnab.encode('latin-1')
                        
                        # Botão de download
                        st.markdown("---")
                        st.subheader("💾 Download do Arquivo")
                        
                        col_down1, col_down2, col_down3 = st.columns([1, 2, 1])
                        with col_down2:
                            st.download_button(
                                label="⬇️ Baixar Arquivo CNAB (.REM)",
                                data=conteudo_bytes,
                                file_name=nome_arquivo_saida,
                                mime="text/plain",
                                use_container_width=True
                            )
                        
                        # Prévia do arquivo
                        with st.expander("👁️ Prévia do Arquivo CNAB (primeiras 10 linhas)"):
                            linhas_preview = linhas[:10]
                            for i, linha in enumerate(linhas_preview, 1):
                                st.text(f"{i:02d}: {linha}")
                        
                        # Informações adicionais
                        with st.expander("ℹ️ Informações do Arquivo"):
                            st.write(f"**Nome do arquivo:** {nome_arquivo_saida}")
                            st.write(f"**Tamanho:** {len(conteudo_bytes):,} bytes")
                            st.write(f"**Encoding:** latin-1")
                            st.write(f"**Caracteres por linha:** 444")
                            st.write(f"**Data de geração:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                            st.write(f"**Código Originador:** {codigo_originador}")
                            st.write(f"**Nome Originador:** {nome_originador}")
                            st.write(f"**Sequencial:** {numero_sequencial}")
                
                except Exception as e:
                    st.error(f"❌ Erro ao gerar arquivo CNAB: {str(e)}")
                    st.exception(e)
    
    else:
        st.info("👆 Faça upload de um arquivo para começar")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
            <small>Gerador de Remessa CNAB 444 - CONCRETO | Desenvolvido com Streamlit</small>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()

