"""
Página de Modelagem Preditiva.

Treina modelos de regressão para estimar necessidade/volume de irrigação.
Prioriza a view Oracle VW_DADOS_AGRICOLAS_ML e usa o CSV como fallback.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_loader import load_csv
from src.database import get_connection
from src.models import train_and_evaluate
from src.preprocessing import prepare_features
from src.ui import render_info_card, render_metric_card, render_section_divider

st.set_page_config(page_title="Modelagem Preditiva", layout="wide")
st.title("02 - Modelagem Preditiva")


@st.cache_data(show_spinner=False)
def load_ml_dataset() -> tuple[pd.DataFrame, str]:
    """Load ML dataset from Oracle view or fallback CSV."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM VW_DADOS_AGRICOLAS_ML WHERE ROWNUM <= 20000")
        cols = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        cur.close()
        conn.close()

        df_oracle = pd.DataFrame(rows, columns=cols)

        if not df_oracle.empty:
            return df_oracle, "Oracle - VW_DADOS_AGRICOLAS_ML"

    except Exception:
        pass

    df_csv = load_csv()
    return df_csv, "CSV local - sensores_data.csv"


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize DataFrame column names to uppercase."""
    df = df.copy()
    df.columns = [str(col).upper() for col in df.columns]
    return df


def add_fallback_targets(df: pd.DataFrame) -> pd.DataFrame:
    """Create regression targets when using the legacy CSV fallback."""
    df = df.copy()

    if "UMIDADE_SOLO" not in df.columns and "UMIDADE_SOLO".lower() in [c.lower() for c in df.columns]:
        pass

    if "VOLUME_IRRIGACAO_ESTIMADO" not in df.columns:
        required = {"UMIDADE_SOLO", "TEMPERATURA", "ACAO_IRRIGACAO"}
        if required.issubset(df.columns):
            df["VOLUME_IRRIGACAO_ESTIMADO"] = df.apply(
                lambda r: max(
                    0,
                    (60 - float(r["UMIDADE_SOLO"])) * 0.8
                    + max(0, float(r["TEMPERATURA"]) - 28) * 1.5
                    + int(r["ACAO_IRRIGACAO"]) * 10,
                ),
                axis=1,
            )

    if "SCORE_NECESSIDADE_IRRIGACAO" not in df.columns:
        required = {"UMIDADE_SOLO", "TEMPERATURA", "NUTRIENTES_N"}
        if required.issubset(df.columns):
            df["SCORE_NECESSIDADE_IRRIGACAO"] = df.apply(
                lambda r: min(
                    100,
                    max(
                        0,
                        max(0, 60 - float(r["UMIDADE_SOLO"])) * 1.2
                        + max(0, float(r["TEMPERATURA"]) - 28) * 2.0
                        + max(0, 15 - float(r["NUTRIENTES_N"]) / 10),
                    ),
                ),
                axis=1,
            )

    return df


def get_available_targets(df: pd.DataFrame) -> list[str]:
    """Return valid numeric regression targets."""
    candidates = [
        "VOLUME_IRRIGACAO_ESTIMADO",
        "SCORE_NECESSIDADE_IRRIGACAO",
    ]

    return [
        col
        for col in candidates
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col])
    ]


def select_features(df: pd.DataFrame, target: str) -> pd.DataFrame:
    """Select relevant numeric features and avoid target leakage."""
    preferred_features = [
        "UMIDADE_SOLO",
        "TEMPERATURA_SOLO",
        "TEMPERATURA",
        "TEMPERATURA_AR",
        "UMIDADE_AR",
        "VELOCIDADE_VENTO",
        "NUTRIENTES_N",
        "AREA_HECTARES",
        "QTD_EVENTOS_CLIMATICOS",
        "QTD_EVENTOS_RECONHECIDOS",
        "VALOR_PREJUIZO_TOTAL",
    ]

    leakage_columns = {
        target,
        "ID_SENSOR",
        "ID_FAZENDA",
        "ANO",
        "MES",
        "ACAO_IRRIGACAO",
        "VOLUME_IRRIGACAO_ESTIMADO",
        "SCORE_NECESSIDADE_IRRIGACAO",
    }

    available = [
        col
        for col in preferred_features
        if col in df.columns
        and col not in leakage_columns
        and pd.api.types.is_numeric_dtype(df[col])
    ]

    if available:
        return df[available]

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    fallback = [col for col in numeric_cols if col not in leakage_columns]
    return df[fallback]


df, source = load_ml_dataset()
df = normalize_columns(df)
df = add_fallback_targets(df)

st.caption(f"Fonte de dados utilizada: **{source}**")

if df.empty:
    st.error("Nenhum dado disponível para modelagem.")
    st.stop()

targets = get_available_targets(df)

if not targets:
    st.error(
        "Nenhum target regressivo encontrado. Verifique se existem as colunas "
        "VOLUME_IRRIGACAO_ESTIMADO ou SCORE_NECESSIDADE_IRRIGACAO."
    )
    st.stop()

with st.expander("Visualizar amostra dos dados usados no modelo"):
    st.dataframe(df.head(100), use_container_width=True, hide_index=True)

target = st.selectbox(
    "Selecione o target para regressão",
    options=targets,
    index=0,
)

X = select_features(df, target)
y = pd.to_numeric(df[target], errors="coerce")

valid_rows = X.notna().all(axis=1) & y.notna()
X = X.loc[valid_rows]
y = y.loc[valid_rows]

if X.empty or y.empty:
    st.error("Após limpeza dos dados, não restaram linhas válidas para treinamento.")
    st.stop()

render_section_divider("Configuração do Modelo")

col1, col2, col3 = st.columns(3)

with col1:
    model_choice = st.selectbox(
        "Modelo",
        ["LinearRegression", "RandomForest", "GradientBoosting"],
    )

with col2:
    st.metric("Linhas válidas", len(X))

with col3:
    st.metric("Features usadas", len(X.columns))

with st.expander("Features utilizadas"):
    st.write(list(X.columns))

if st.button("Treinar e Avaliar", type="primary"):
    try:
        result = train_and_evaluate(X, y, model_name=model_choice)

        render_section_divider("Métricas de Avaliação")

        mcols = st.columns(4)

        with mcols[0]:
            render_metric_card("MAE", round(result.metrics.mae, 3))
        with mcols[1]:
            render_metric_card("MSE", round(result.metrics.mse, 3))
        with mcols[2]:
            render_metric_card("RMSE", round(result.metrics.rmse, 3))
        with mcols[3]:
            render_metric_card("R²", round(result.metrics.r2, 3))

        r2 = result.metrics.r2
        if r2 >= 0.8:
            interp = "Excelente capacidade preditiva."
        elif r2 >= 0.6:
            interp = "Bom desempenho preditivo."
        elif r2 >= 0.3:
            interp = "Desempenho moderado. O modelo ainda pode ser melhorado."
        else:
            interp = "Baixo desempenho. É recomendável revisar features e dados."

        render_info_card("Interpretação", interp, icon="💡")

        render_section_divider("Real vs Previsto")

        df_cmp = pd.DataFrame(
            {
                "Real": result.y_true,
                "Previsto": result.y_pred,
            }
        )

        fig = px.scatter(
            df_cmp,
            x="Real",
            y="Previsto",
            title="Comparação entre valores reais e previstos",
            labels={
                "Real": "Valor real",
                "Previsto": "Valor previsto",
            },
        )

        min_value = min(df_cmp["Real"].min(), df_cmp["Previsto"].min())
        max_value = max(df_cmp["Real"].max(), df_cmp["Previsto"].max())

        fig.add_shape(
            type="line",
            x0=min_value,
            x1=max_value,
            y0=min_value,
            y1=max_value,
            line=dict(dash="dash"),
        )

        st.plotly_chart(fig, use_container_width=True)

        if target == "SCORE_NECESSIDADE_IRRIGACAO":
            render_section_divider("Impacto Econômico e Sustentabilidade")
            st.write("Preço aproximado do m³ de Água: 21.00$")
            st.link_button(
                label="Valores m³ - CAESB", 
                url="https://www.caesb.df.gov.br/tarifas-e-precos/",
                type="secondary"  
)
            volume_original: float = df_cmp["Real"].sum()
            volume_otimizado: float = df_cmp["Previsto"].sum()
            agua_economizada: float = volume_original - volume_otimizado
            valor_metro_agua: int = 30

            if agua_economizada > 0:
                custo_original: float = volume_original * valor_metro_agua
                custo_otimizado: float = volume_otimizado * valor_metro_agua
                reais_economizados: float = custo_original - custo_otimizado

                porcentagem_ecoAgua = (agua_economizada / volume_original) * 100
                porcentagem_ecoReais = (reais_economizados / custo_original) * 100

                colAntigaAgua, colOtimizadaAgua, colEcoAgua = st.columns(3)

                with colAntigaAgua:
                    render_metric_card("🔴 Consumo Antigo",  round(volume_original,2))
                with colOtimizadaAgua:
                    render_metric_card("🔵 Consumo Otimizado",  round(volume_otimizado,2))
                with colEcoAgua:
                    render_metric_card("🟢 Recurso Salvo (m³)",  round(agua_economizada,2), delta=f"+{round(porcentagem_ecoAgua, 1)}% de Eficiência")
                
                colAntigaReais, colOtimizadaReais, colEcoReais = st.columns(3)

                with colAntigaReais:
                    render_metric_card("🔴 Gasto Antigo",  round(custo_original,2))
                with colOtimizadaReais:
                    render_metric_card("🔵 Gasto Otimizado",  round(custo_otimizado,2))
                with colEcoReais:
                    render_metric_card("🟢 Recurso Salvo ($)",  round(reais_economizados,2), delta=f"+{round(porcentagem_ecoReais, 1)}% de Eficiência")
                
                
            else: 
                st.warning("O modelo não foi capaz de otimizar o custo de água")



        render_section_divider("Leitura para o gestor")

        
        if target == "VOLUME_IRRIGACAO_ESTIMADO":
            texto = (
                "O modelo estima o volume de irrigação necessário a partir das "
                "condições do solo, clima, nutrientes e contexto da fazenda."
            )
        else:
            texto = (
                "O modelo estima um score de necessidade de irrigação. Quanto maior "
                "o score, maior a urgência para irrigar ou monitorar o talhão."
            )

        render_info_card("Resumo", texto, icon="🚜")

    except Exception as exc:
        st.error(f"Erro ao treinar modelo: {exc}")

