import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from cnab_engine import GeradorCNAB


def check_password():
    
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if st.session_state.authenticated:
        return True
    
    st.markdown(
        """
        <div style='text-align: center; padding: 50px 0;'>
            <h1>🔐 Sistema CNAB - CONCRETO</h1>
            <h3>Acesso Restrito</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("---")
        
        password = st.text_input(
            "🔑 Senha de Acesso",
            type="password",
            placeholder="Digite a senha...",
            key="password_input"
        )
        
        login_button = st.button(
            "🚪 Entrar",
            type="primary",
            use_container_width=True
        )
        
        if login_button:
            if password:
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
    
    st.markdown(
        """
        <div style='text-align: center; color: gray; padding-top: 100px;'>
            <small>Entre em contato com o administrador para obter acesso</small>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.stop()


def main():
    
    st.set_page_config(
        page_title="Sistema CNAB - CONCRETO",
        page_icon="🔐",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    check_password()
    
    with st.sidebar:
        st.markdown("### 👤 Usuário")
        st.success("✅ Autenticado")
        
        st.markdown("---")
        
        if st.button("🚪 Sair", type="secondary", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
        
        st.markdown("---")
        st.markdown("### ⚙️ Configurações da Remessa")
        
        cod_originador = st.text_input(
            "🔢 Código Originador",
            value="",
            help="Código numérico do originador (até 20 dígitos)",
            max_chars=20,
            placeholder="Ex: 202501"
        )
        
        razao_social = st.text_input(
            "📝 Razão Social",
            value="",
            help="CNPJ + Nome (até 30 caracteres). Ex: 58479927000136BANCO PAULISTA",
            max_chars=30,
            placeholder="Ex: 58479927000136BANCO PAULISTA"
        )
        
        numero_banco = st.text_input(
            "🏦 Número do Banco",
            value="",
            help="Código numérico do banco (3 dígitos). Ex: 611",
            max_chars=3,
            placeholder="Ex: 611"
        )
        
        nome_banco = st.text_input(
            "🏛️ Nome do Banco",
            value="",
            help="Nome do banco (até 15 caracteres)",
            max_chars=15,
            placeholder="Ex: PAULISTA S.A."
        )
        
        seq_arquivo = st.number_input(
            "📋 Sequencial do Arquivo",
            min_value=1,
            max_value=9999999,
            value=1,
            step=1,
            help="Número sequencial do arquivo de remessa"
        )
        
        coobrigacao = st.selectbox(
            "🤝 Coobrigação",
            options=["02", "01"],
            format_func=lambda x: "02 - Sem Coobrigação" if x == "02" else "01 - Com Coobrigação",
            help="Indicador de coobrigação para todos os registros"
        )
        
        tipo_baixa = st.selectbox(
            "📋 Tipo de Baixa",
            options=["TOTAL", "PARCIAL"],
            format_func=lambda x: "Baixa Total" if x == "TOTAL" else "Baixa Parcial",
            help="Tipo de baixa: Total (7/7) ou Parcial (1/4)"
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
    
    st.title("🏦 Gerador de Remessa CNAB 444 - CONCRETO FIDC")
    st.markdown("### Sistema de Geração de Arquivos CNAB")
    st.markdown("---")
    
    st.header("📁 Upload do Arquivo de Dados")
    
    arquivo_upload = st.file_uploader(
        "Selecione o arquivo com os dados (Excel ou CSV)",
        type=['xlsx', 'xls', 'csv'],
        help="Formatos aceitos: Excel (.xlsx, .xls) ou CSV (.csv)"
    )
    
    if arquivo_upload is not None:
        st.success(f"✅ Arquivo carregado: **{arquivo_upload.name}**")
        
        try:
            with st.spinner("⏳ Carregando dados..."):
                nome_arquivo = arquivo_upload.name.lower()
                
                if nome_arquivo.endswith('.csv'):
                    df = pd.read_csv(arquivo_upload)
                elif nome_arquivo.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(arquivo_upload)
                else:
                    st.error("❌ Formato de arquivo não suportado!")
                    st.stop()
            
            st.markdown("---")
            st.header("📊 Prévia dos Dados")
            
            col_info1, col_info2, col_info3 = st.columns(3)
            with col_info1:
                st.metric("Total de Registros", len(df))
            with col_info2:
                st.metric("Total de Colunas", len(df.columns))
            with col_info3:
                st.metric("Tamanho", f"{arquivo_upload.size:,} bytes")
            
            st.subheader("🔍 Primeiras 5 linhas")
            st.dataframe(df.head(5), use_container_width=True)
            
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
            
            st.header("🚀 Geração do Arquivo CNAB")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            
            with col_btn2:
                gerar_cnab = st.button(
                    "🎯 Gerar Arquivo .REM",
                    type="primary",
                    use_container_width=True
                )
            
            if gerar_cnab:
                if not cod_originador or not cod_originador.strip():
                    st.error("❌ Por favor, informe o Código do Originador na sidebar!")
                    st.stop()
                
                if not razao_social or not razao_social.strip():
                    st.error("❌ Por favor, informe a Razão Social na sidebar!")
                    st.stop()
                
                if not numero_banco or not numero_banco.strip():
                    st.error("❌ Por favor, informe o Número do Banco na sidebar!")
                    st.stop()
                
                if not nome_banco or not nome_banco.strip():
                    st.error("❌ Por favor, informe o Nome do Banco na sidebar!")
                    st.stop()
                
                try:
                    with st.spinner("⏳ Gerando arquivo CNAB..."):
                        gerador = GeradorCNAB()
                        
                        header = gerador.gerar_header(
                            cod_originador=cod_originador,
                            razao_social=razao_social,
                            numero_banco=numero_banco,
                            nome_banco=nome_banco,
                            seq_arquivo=seq_arquivo
                        )
                        
                        linhas = [header]
                        
                        total_detalhes = 0
                        erros = []
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for idx, row in df.iterrows():
                            try:
                                sequencial_registro = idx + 2
                                detalhe = gerador.gerar_detalhe(row, sequencial_registro, coobrigacao, tipo_baixa)
                                linhas.append(detalhe)
                                total_detalhes += 1
                                
                                progress = (idx + 1) / len(df)
                                progress_bar.progress(progress)
                                status_text.text(f"Processando registro {idx + 1} de {len(df)}...")
                                
                            except Exception as e:
                                erros.append(f"Linha {idx + 2}: {str(e)}")
                        
                        progress_bar.empty()
                        status_text.empty()
                        
                        total_registros = len(linhas) + 1
                        trailer = gerador.gerar_trailer(total_registros)
                        linhas.append(trailer)
                        
                        conteudo_cnab = "\r\n".join(linhas)
                        
                        st.success("✅ Arquivo CNAB gerado com sucesso!")
                        
                        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                        with col_stat1:
                            st.metric("📝 Header", "1 registro")
                        with col_stat2:
                            st.metric("📋 Detalhes", f"{total_detalhes} registros")
                        with col_stat3:
                            st.metric("📊 Trailer", "1 registro")
                        with col_stat4:
                            st.metric("📦 Total", f"{total_registros} registros")
                        
                        if erros:
                            with st.expander(f"⚠️ Avisos/Erros ({len(erros)} encontrados)"):
                                for erro in erros:
                                    st.warning(erro)
                        
                        nome_arquivo_saida = f"REMESSA_{datetime.now().strftime('%Y%m%d_%H%M%S')}.REM"
                        
                        conteudo_bytes = conteudo_cnab.encode('latin-1')
                        
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
                        
                        with st.expander("👁️ Prévia do Arquivo CNAB (primeiras 10 linhas)"):
                            linhas_preview = linhas[:10]
                            for i, linha in enumerate(linhas_preview, 1):
                                tipo = "Header" if linha[0] == "0" else "Detalhe" if linha[0] == "1" else "Trailer"
                                st.text(f"{i:02d} ({tipo}): {linha}")
                        
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
                                st.write(f"**Razão Social:** {razao_social}")
                                st.write(f"**Banco:** {numero_banco} - {nome_banco}")
                                st.write(f"**Sequencial:** {seq_arquivo}")
                                st.write(f"**Coobrigação:** {coobrigacao}")
                                st.write(f"**Tipo de Baixa:** {'Baixa Total' if tipo_baixa == 'TOTAL' else 'Baixa Parcial'}")
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
    
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
            <small>Gerador de Remessa CNAB 444 - CONCRETO FIDC | Desenvolvido com Streamlit</small>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
