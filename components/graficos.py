"""
Componente de Graficos v2 - Dashboard Mapaton 2026
Con descripciones para cualquier persona.
"""
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def renderizar_graficos(df_serie, df_correlacion, ano=None, cuenca=None):
    st.subheader("📈 Evolucion Temporal 2019-2025")

    if not df_serie.empty and "ano" in df_serie.columns:
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        if "arena_ha" in df_serie.columns:
            fig.add_trace(
                go.Scatter(
                    x=df_serie["ano"], y=df_serie["arena_ha"],
                    name="Bancos de Arena (ha)", mode="lines+markers",
                    line=dict(color="#FFD700", width=3),
                    marker=dict(size=12),
                ), secondary_y=False,
            )
        if "mineria_ha" in df_serie.columns:
            fig.add_trace(
                go.Scatter(
                    x=df_serie["ano"], y=df_serie["mineria_ha"],
                    name="Mineria (ha)", mode="lines+markers",
                    line=dict(color="#FF0000", width=3, dash="dash"),
                    marker=dict(size=12),
                ), secondary_y=True,
            )

        fig.update_layout(
            template="plotly_white", height=420,
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            hovermode="x unified",
        )
        fig.update_xaxes(title_text="Año", dtick=1)
        fig.update_yaxes(title_text="Bancos de Arena (ha)", secondary_y=False)
        fig.update_yaxes(title_text="Mineria (ha)", secondary_y=True)

        st.plotly_chart(fig, use_container_width=True)

        st.caption("💡 **Como leer este grafico:** La linea dorada muestra los bancos de arena (eje izquierdo). "
                   "La linea roja punteada muestra la mineria (eje derecho). Cuando la mineria sube y la arena "
                   "baja al mismo tiempo, hay evidencia de impacto directo.")

    st.subheader("📊 Proximidad Mineria -> Perdida de Arena")
    if not df_correlacion.empty:
        valores = list(df_correlacion.get("arena_perdida_ha", [0]))
        todos_ceros = all(v == 0.0 for v in valores)

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=df_correlacion["buffer_m"].astype(str) + " m",
            y=valores,
            marker_color=["#FFD700", "#FFA500", "#FF4500", "#FF0000"][:len(valores)],
            text=[f"{v:.1f}" for v in valores],
            textposition="outside",
        ))
        fig2.update_layout(
            template="plotly_white", height=350,
            xaxis_title="Distancia desde zona minera",
            yaxis_title="Arena perdida (ha)",
        )
        st.plotly_chart(fig2, use_container_width=True)

        if todos_ceros:
            st.info(
                "🔍 **Resultado:** No se detecto perdida de arena en buffers de 20m a 100m "
                "alrededor de zonas mineras. La mineria y los bancos de arena ocupan espacios "
                "diferentes: mineria en tierra firme, arena en el cauce. El impacto podria "
                "ser indirecto (sedimentos, mercurio en el agua)."
            )
        else:
            st.caption("💡 Muestra cuanta arena se perdio cerca de zonas mineras. "
                       "Valores altos en buffers pequenos indican impacto directo.")
