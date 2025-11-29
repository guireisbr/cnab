"""
Sistema CNAB - Aplicação com Autenticação
Desenvolvido com Streamlit
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from cnab_engine import GeradorCNAB


def check_password():
    """
    Verifica a senha de acesso usando st.secrets
    
    Returns:
        True se autenticado, False caso contrário
    """
    # Inicializa o estado de autenticação se não existir
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    # Se já está autenticado, retorna True
    if st.session_state.authenticated:
        return True
    
    # Mostra tela de login
    st.markdown(
        """
        <div style='text-align: center; padding: 50px 0;'>
            <h1>🔐 Sistema CNAB - CONCRETO</h1>
            <h3>Acesso Restrito</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Centraliza o formulário de login
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("---")
        
        # Input de senha
        password = st.text_input(
            "🔑 Senha de Acesso",
            type="password",
            placeholder="Digite a senha...",
            key="password_input"
        )
        
        # Botão de login
        login_button = st.button(
            "🚪 Entrar",
            type="primary",
            use_container_width=True
        )
        
        # Verifica a senha quando o botão é clicado
        if login_button:
            if password:
                # Obtém a senha dos secrets
                try:
                    senha_correta = st.secrets["access_password"]
                    
                    if password == senha_correta:
                        st.session_state.authenticated = True
                        st.success("✅ Login bem-sucedido!")
                        st.rerun()
                    else:
                        st.error("❌ Senha incorreta! Tente novamente.")
                        st.session_state.authenticated = False
                
                except Exception as e:
                    st.error(f"❌ Erro ao verificar senha: {str(e)}")
                    st.info("💡 Verifique se o arquivo .streamlit/secrets.toml existe.")
            else:
                st.warning("⚠️ Por favor, digite uma senha.")
        
        st.markdown("---")
    
    # Informação de contato
    st.markdown(
        """
        <div style='text-align: center; color: gray; padding-top: 100px;'>
            <small>Entre em contato com o administrador para obter acesso</small>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Para a execução se não estiver autenticado
    st.stop()


def main():
    """
    Função principal da aplicação
    """
    # Configura a página
    st.set_page_config(
        page_title="Sistema CNAB - CONCRETO",
        page_icon="🔐",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Verifica autenticação
    check_password()
    
    # Se chegou aqui, está autenticado
    # ==========================================================================
    # SIDEBAR - CONFIGURAÇÕES DA REMESSA
    # ==========================================================================
    with st.sidebar:
        st.markdown("### 👤 Usuário")
        st.success("✅ Autenticado")
        
        st.markdown("---")
        
        # Botão de logout
        if st.button("🚪 Sair", type="secondary", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
        
        st.markdown("---")
        st.markdown("### ⚙️ Configurações da Remessa")
        
        # Input: Nome Originador
        nome_originador = st.text_input(
            "📝 Nome Originador",
            value="BANCO PAULISTA",
            help="Nome da empresa/banco originador (até 30 caracteres)",
            max_chars=30
        )
        
        # Input: Código Originador
        cod_originador = st.text_input(
            "🔢 Código Originador",
            value="20250158479927000136",
            help="Código numérico do originador (até 20 dígitos)",
            max_chars=20
        )
        
        # Input: Sequencial do Arquivo
        seq_arquivo = st.number_input(
            "📋 Sequencial do Arquivo",
            min_value=1,
            max_value=9999999,
            value=1,
            step=1,
            help="Número sequencial do arquivo de remessa"
        )
        
        st.markdown("---")
        st.markdown(
            """
            <div style='text-align: center; color: gray; padding-top: 20px;'>
                <small>Sistema CNAB v1.0</small><br>
                <small>CONCRETO © 2025</small>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # ==========================================================================
    # ÁREA PRINCIPAL - UPLOAD E GERAÇÃO
    # ==========================================================================
    
    # Título
    st.title("🏦 Gerador de Remessa CNAB 444 - CONCRETO")
    st.markdown("### Sistema de Geração de Arquivos CNAB")
    st.markdown("---")
    
    # Seção de Upload
    st.header("📁 Upload do Arquivo de Dados")
    
    arquivo_upload = st.file_uploader(
        "Selecione o arquivo com os dados (Excel ou CSV)",
        type=['xlsx', 'xls', 'csv'],
        help="Formatos aceitos: Excel (.xlsx, .xls) ou CSV (.csv)"
    )
    
    # Verifica se arquivo foi carregado
    if arquivo_upload is not None:
        st.success(f"✅ Arquivo carregado: **{arquivo_upload.name}**")
        
        try:
            # Carrega o arquivo
            with st.spinner("⏳ Carregando dados..."):
                nome_arquivo = arquivo_upload.name.lower()
                
                if nome_arquivo.endswith('.csv'):
                    df = pd.read_csv(arquivo_upload)
                elif nome_arquivo.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(arquivo_upload)
                else:
                    st.error("❌ Formato de arquivo não suportado!")
                    st.stop()
            
            # Mostra informações do arquivo
            st.markdown("---")
            st.header("📊 Prévia dos Dados")
            
            col_info1, col_info2, col_info3 = st.columns(3)
            with col_info1:
                st.metric("Total de Registros", len(df))
            with col_info2:
                st.metric("Total de Colunas", len(df.columns))
            with col_info3:
                st.metric("Tamanho", f"{arquivo_upload.size:,} bytes")
            
            # Mostra prévia das primeiras 5 linhas
            st.subheader("🔍 Primeiras 5 linhas")
            st.dataframe(df.head(5), use_container_width=True)
            
            # Mostra colunas disponíveis
            with st.expander("📋 Colunas disponíveis no arquivo"):
                colunas_necessarias = [
                    'SEU_NUMERO', 'ID_RECEBIVEL',
                    'DATA_VENCIMENTO_AJUSTADA', 'DATA_VENCIMENTO',
                    'VALOR_NOMINAL', 'DATA_EMISSAO',
                    'DOC_SACADO', 'NOME_SACADO'
                ]
                
                st.write("**Colunas no arquivo:**")
                for col in df.columns:
                    st.write(f"  ✓ {col}")
                
                st.markdown("---")
                st.write("**Colunas esperadas pelo sistema:**")
                for col in colunas_necessarias:
                    if col in df.columns:
                        st.write(f"  ✅ {col}")
                    else:
                        st.write(f"  ⚠️ {col} (opcional)")
            
            st.markdown("---")
            
            # Seção de Geração
            st.header("🚀 Geração do Arquivo CNAB")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            
            with col_btn2:
                gerar_cnab = st.button(
                    "🎯 Gerar Arquivo .REM",
                    type="primary",
                    use_container_width=True
                )
            
            # Processa geração do CNAB
            if gerar_cnab:
                # Validações
                if not nome_originador or not nome_originador.strip():
                    st.error("❌ Por favor, informe o Nome do Originador na sidebar!")
                    st.stop()
                
                if not cod_originador or not cod_originador.strip():
                    st.error("❌ Por favor, informe o Código do Originador na sidebar!")
                    st.stop()
                
                try:
                    with st.spinner("⏳ Gerando arquivo CNAB..."):
                        # Instancia o gerador
                        gerador = GeradorCNAB()
                        
                        # Gera o Header
                        header = gerador.gerar_header(
                            nome_originador=nome_originador,
                            cod_originador=cod_originador,
                            seq_arquivo=seq_arquivo
                        )
                        
                        # Lista para armazenar todas as linhas
                        linhas = [header]
                        
                        # Gera Detalhes com barra de progresso
                        total_detalhes = 0
                        erros = []
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for idx, row in df.iterrows():
                            try:
                                sequencial_registro = idx + 2  # +2 porque header é 1
                                detalhe = gerador.gerar_detalhe(row, sequencial_registro)
                                linhas.append(detalhe)
                                total_detalhes += 1
                                
                                # Atualiza progresso
                                progress = (idx + 1) / len(df)
                                progress_bar.progress(progress)
                                status_text.text(f"Processando registro {idx + 1} de {len(df)}...")
                                
                            except Exception as e:
                                erros.append(f"Linha {idx + 2}: {str(e)}")
                        
                        progress_bar.empty()
                        status_text.empty()
                        
                        # Gera o Trailer
                        total_registros = len(linhas) + 1  # +1 para o trailer
                        trailer = gerador.gerar_trailer(total_registros)
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
                        
                        # Converte para bytes com encoding latin-1 (padrão bancário)
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
                                tipo = "Header" if linha[0] == "0" else "Detalhe" if linha[0] == "1" else "Trailer"
                                st.text(f"{i:02d} ({tipo}): {linha}")
                        
                        # Informações adicionais
                        with st.expander("ℹ️ Informações do Arquivo"):
                            info_col1, info_col2 = st.columns(2)
                            
                            with info_col1:
                                st.write(f"**Nome do arquivo:** {nome_arquivo_saida}")
                                st.write(f"**Tamanho:** {len(conteudo_bytes):,} bytes")
                                st.write(f"**Encoding:** latin-1 (padrão bancário)")
                                st.write(f"**Caracteres por linha:** 444")
                                st.write(f"**Quebra de linha:** \\r\\n")
                            
                            with info_col2:
                                st.write(f"**Data de geração:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                                st.write(f"**Código Originador:** {cod_originador}")
                                st.write(f"**Nome Originador:** {nome_originador}")
                                st.write(f"**Sequencial:** {seq_arquivo}")
                                st.write(f"**Total de registros:** {total_registros}")
                
                except Exception as e:
                    st.error(f"❌ Erro ao gerar arquivo CNAB: {str(e)}")
                    with st.expander("🔍 Detalhes do erro"):
                        import traceback
                        st.code(traceback.format_exc())
        
        except Exception as e:
            st.error(f"❌ Erro ao carregar arquivo: {str(e)}")
            with st.expander("🔍 Detalhes do erro"):
                import traceback
                st.code(traceback.format_exc())
    
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

