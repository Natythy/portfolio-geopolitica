import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Laboratório Geopolítico", page_icon="🌍", layout="wide")

st.title("🌍 Diplomacia de Dados: Uma Análise da Riqueza Global")
st.markdown("""
Este projeto nasceu da intersecção entre a **Ciência de Dados** e as **Relações Internacionais**. 
Mais do que um portfólio técnico, esta é uma ferramenta de estudo para compreender como 
blocos econômicos e eventos históricos moldam o desenvolvimento humano.
""")


# --- CARREGAMENTO E TRATAMENTO DE DADOS ---
@st.cache_data
def carregar_dados():
    """
    Carrega o dataset Gapminder e realiza a engenharia de atributos
    para classificar os países em blocos econômicos específicos.

    Returns:
        pd.DataFrame: DataFrame processado com a coluna 'Bloco_Economico'.
    """
    df = px.data.gapminder()

    g7 = [
        "United States",
        "Canada",
        "United Kingdom",
        "Germany",
        "France",
        "Italy",
        "Japan",
    ]
    brics = ["Brazil", "Russia", "India", "China", "South Africa"]
    mercosul = ["Argentina", "Uruguay", "Paraguay", "Venezuela"]
    tigres = ["Hong Kong, China", "Singapore", "Korea, Rep.", "Taiwan"]

    def classificar_bloco(pais, continente):
        """
        Lógica de categorização de países baseada em alianças políticas e econômicas.

        Args:
            pais (str): Nome do país.
            continente (str): Continente do país.

        Returns:
            str: O nome do bloco econômico ou 'Outros'.
        """
        if pais in g7:
            return "G7"
        elif pais in brics:
            return "BRICS"
        elif pais in mercosul:
            return "Mercosul"
        elif pais in tigres:
            return " Tigres Asiáticos"
        elif continente == "Africa":
            return "União Africana (Média)"
        else:
            return "Outros"

    df["Bloco_Economico"] = df.apply(
        lambda row: classificar_bloco(row["country"], row["continent"]), axis=1
    )
    return df


df = carregar_dados()

# --- SIDEBAR (FILTROS E ABOUT) ---
st.sidebar.header("⚙️ Painel de Controlo Geopolítico")

lista_blocos = [b for b in df["Bloco_Economico"].unique() if b != "Outros"]
blocos_selecionados = st.sidebar.multiselect(
    "Selecione os Blocos para comparar:",
    options=lista_blocos,
    default=["G7", "BRICS", "Mercosul"],
)

# Filtro de dados baseado na seleção
df_filtrado = df[df["Bloco_Economico"].isin(blocos_selecionados)]

if not df_filtrado.empty:
    st.markdown("---")

    col_esquerda, col_direita = st.columns([0.6, 0.4], gap="large")

    with col_esquerda:
        st.subheader("📈 A Corrida da Riqueza (PIB per capita)")

        fig = px.scatter(
            df_filtrado,
            x="gdpPercap",
            y="lifeExp",
            animation_frame="year",
            animation_group="country",
            size="pop",
            color="Bloco_Economico",
            hover_name="country",
            log_x=True,
            size_max=55,
            range_x=[200, 100000],
            range_y=[25, 90],
            template="plotly_white",
            labels={
                "gdpPercap": "PIB per capita (USD - Escala Log)",
                "lifeExp": "Expectativa de Vida (Anos)",
                "year": "Ano",
                "pop": "População",
                "Bloco_Economico": "Bloco",
            },
        )

        # Ajuste da velocidade da animação
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 800
        
        st.plotly_chart(fig, use_container_width=True)

    with col_direita:
        st.subheader("📚 Notas Geopolíticas")
        st.write("Entenda o impacto histórico nas curvas de crescimento:")

        # with st.expander("🔍 1973: O Choque do Petróleo e a Vulnerabilidade do G7"):
        #     st.write("""
        #             **Contexto Geopolítico:** A crise ocorreu no contexto da Guerra do Yom Kippur. Com os EUA apoiando militarmente Israel, 
        #                 e a URSS apoiando Egito e Síria na dinâmica da Guerra Fria, os países árabes exportadores de petróleo (liderados pela Arábia Saudita) 
        #                 impuseram um embargo aos aliados de Israel. Eles perceberam que o petróleo era uma vantagem estratégica e uma ferramenta de pressão, 
        #                 inclusive para a libertação do povo palestino.
             
        #             **Análise de Dados:** O embargo causou um choque brutal, aumentando o valor do barril de cerca de 2,90 para 11 dólares. 
        #                 Ao analisar a evolução do **G7** no gráfico, compreendemos o tamanho desse impacto: o evento expôs a vulnerabilidade extrema 
        #                 das maiores potências ocidentais, cuja riqueza era altamente dependente dessa matriz energética. 
        #                 E influênciando o fortalecimento da Agência Internacional de Energia (AIE)
        # """)

        with st.expander(
            "🤝 1991: Redemocratização e a Integração Regional (Mercosul)"
        ):
            st.write("""
                    **Contexto Geopolítico:** A integração na América Latina ganhou força com a redemocratização de Brasil e Argentina após suas ditaduras militares. 
                        O que começou com a Declaração do Iguaçu (1985) mostrou-se uma aliança promissora. Inspirados pelo sucesso do 
                        Mercado Comum Europeu — que uniu antigos rivais como França e Alemanha para reconstruir a Europa — os países sul-americanos 
                        buscaram uma união similar.
                    
                    **Análise de Dados:** O Tratado de Assunção em 1991 formalizou o Mercosul entre Brasil, Argentina, Paraguai e Uruguai. No gráfico, 
                        este período marca uma tentativa de fortalecimento econômico regional para enfrentar a nova ordem globalizada e competitiva 
                        que surgiu após o fim da Guerra Fria, buscando escala e proteção mútua no mercado internacional.
                """)

        with st.expander("🐉 2001: China na OMC e a Consolidação dos BRICS"):
            st.write("""
                    **Contexto Geopolítico:** A ingressão da China na Organização Mundial do Comércio (OMC) em 2001 foi um marco global.
                        Ela permitiu a circulação de produtos chineses a preços altamente competitivos e a abertura de novos mercados de exportação 
                        para diversos países, aumentando exponencialmente o poder de barganha chinês. 
            
                    **Análise de Dados:** No gráfico, esse período marca a "decolagem" da curva de riqueza das nações emergentes. 
                        O impacto desse crescimento refletiu-se diretamente na diplomacia: diante dessa nova força econômica, e especialmente após a 
                        crise global de 2008, os países fundadores do bloco buscaram estabelecer posições coordenadas em instituições financeiras 
                        como o FMI, desafiando a hegemonia histórica do G7.
                """)

else:
    st.warning(
        "⚠️ Por favor, selecione pelo menos um bloco económico no painel lateral."
    )

st.markdown("---")
st.subheader("🗺️ Visão Geográfica: Riqueza no Ano Mais Recente")

ano_recente = df_filtrado["year"].max()
df_atual = df_filtrado[df_filtrado["year"] == ano_recente]

fig_mapa = px.choropleth(
    df_atual,
    locations="iso_alpha",
    color="gdpPercap",
    hover_name="country",
    hover_data=["lifeExp", "pop"],
    color_continuous_scale=px.colors.sequential.Plasma,
    title=f"Distribuição de Riqueza em {ano_recente}",
)

fig_mapa.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})

st.plotly_chart(fig_mapa, use_container_width=True)


st.sidebar.divider()
st.sidebar.subheader("Sobre o Projeto")
st.sidebar.info("""
Este Laboratório foi desenvolvido como um projeto de portfólio que une 
**Ciência de Dados** e **Análise de Relações Internacionais**.

**Autora:** Nathaly Eduarda
**Objetivo:** Estudo prático de como eventos geopolíticos impactam indicadores macroeconômicos globais.
""")

st.sidebar.caption("Dados fornecidos pela Fundação Gapminder.")
