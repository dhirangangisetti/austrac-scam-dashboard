import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Australian Scam Intelligence Dashboard",
    page_icon="🔍",
    layout="wide"
)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    yearly = pd.read_csv('yearly_totals.csv')
    scams = pd.read_csv('scam_types_all_years.csv')
    orgs = pd.read_csv('org_summary_2024.csv')
    return yearly, scams, orgs

yearly, scams, orgs = load_data()

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🔍 Australian Scam Intelligence Dashboard")
st.markdown("**Data source:** ACCC National Anti-Scam Centre — Targeting Scams Reports 2022–2025")
st.divider()

# ── KPI Cards ─────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

latest = yearly[yearly['year'] == 2025].iloc[0]
prev = yearly[yearly['year'] == 2024].iloc[0]

with col1:
    st.metric(
        label="2025 Combined Losses",
        value=f"${latest['total_losses_b']:.2f}B",
        delta=f"{((latest['total_losses_b'] - prev['total_losses_b']) / prev['total_losses_b'] * 100):.1f}% vs 2024",
        delta_color="inverse"
    )

with col2:
    st.metric(
        label="2025 Total Reports",
        value=f"{latest['total_reports']:,}",
        delta=f"{((latest['total_reports'] - prev['total_reports']) / prev['total_reports'] * 100):.1f}% vs 2024",
        delta_color="inverse"
    )

with col3:
    st.metric(
        label="Peak Losses (2022)",
        value="$3.10B",
        delta="Highest recorded year"
    )

with col4:
    reduction = ((3.1 - latest['total_losses_b']) / 3.1 * 100)
    st.metric(
        label="Reduction Since Peak",
        value=f"{reduction:.1f}%",
        delta="Since 2022 peak"
    )

st.divider()

# ── Row 1: Yearly trend + Scam type filter ────────────────────────────────────
col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.subheader("Combined Scam Losses by Year")
    fig_yearly = px.bar(
        yearly,
        x='year',
        y='total_losses_b',
        color='total_losses_b',
        color_continuous_scale='Reds',
        labels={'total_losses_b': 'Total Losses ($B)', 'year': 'Year'},
        text='total_losses_b'
    )
    fig_yearly.update_traces(texttemplate='$%{text:.2f}B', textposition='outside')
    fig_yearly.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis_title='Losses ($B)',
        xaxis=dict(tickmode='linear')
    )
    st.plotly_chart(fig_yearly, use_container_width=True)

with col_right:
    st.subheader("Reports vs Losses Trend")
    fig_dual = go.Figure()
    fig_dual.add_trace(go.Scatter(
        x=yearly['year'], y=yearly['total_reports'],
        name='Total Reports', mode='lines+markers',
        line=dict(color='steelblue', width=2)
    ))
    fig_dual.add_trace(go.Scatter(
        x=yearly['year'], y=yearly['scamwatch_losses_m'],
        name='Scamwatch Losses ($M)', mode='lines+markers',
        line=dict(color='crimson', width=2),
        yaxis='y2'
    ))
    fig_dual.update_layout(
        yaxis=dict(title='Total Reports'),
        yaxis2=dict(title='Scamwatch Losses ($M)', overlaying='y', side='right'),
        legend=dict(x=0, y=1),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig_dual, use_container_width=True)

st.divider()

# ── Row 2: Scam type analysis ─────────────────────────────────────────────────
st.subheader("Scam Type Analysis")

col_filter, _ = st.columns([1, 3])
with col_filter:
    selected_years = st.multiselect(
        "Filter by year",
        options=[2022, 2023, 2024, 2025],
        default=[2022, 2023, 2024, 2025]
    )

filtered_scams = scams[scams['year'].isin(selected_years)]

col_l, col_r = st.columns(2)

with col_l:
    fig_scam_total = px.bar(
        filtered_scams,
        x='scam_type',
        y='total_m',
        color='year',
        barmode='group',
        labels={'total_m': 'Total Losses ($M)', 'scam_type': 'Scam Type', 'year': 'Year'},
        color_discrete_sequence=px.colors.sequential.Reds_r
    )
    fig_scam_total.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_tickangle=-20
    )
    st.plotly_chart(fig_scam_total, use_container_width=True)

with col_r:
    # Scam type share for most recent selected year
    latest_year = max(selected_years) if selected_years else 2025
    pie_data = scams[scams['year'] == latest_year]
    fig_pie = px.pie(
        pie_data,
        values='total_m',
        names='scam_type',
        title=f'Scam Type Share — {latest_year}',
        color_discrete_sequence=px.colors.sequential.Reds_r
    )
    fig_pie.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# ── Row 3: Organisation breakdown 2024 ───────────────────────────────────────
st.subheader("Losses by Reporting Organisation — 2023 vs 2024")

orgs_filtered = orgs[orgs['organisation'] != 'Adjustments']

fig_orgs = go.Figure()
fig_orgs.add_trace(go.Bar(
    name='2023 Losses ($M)',
    x=orgs_filtered['organisation'],
    y=orgs_filtered['losses_2023_m'],
    marker_color='lightcoral'
))
fig_orgs.add_trace(go.Bar(
    name='2024 Losses ($M)',
    x=orgs_filtered['organisation'],
    y=orgs_filtered['losses_2024_m'],
    marker_color='crimson'
))
fig_orgs.update_layout(
    barmode='group',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    yaxis_title='Losses ($M)'
)
st.plotly_chart(fig_orgs, use_container_width=True)

st.divider()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
**Methodology:** Data extracted and cleaned from ACCC National Anti-Scam Centre 
Targeting Scams Reports (2022–2025) using Python and pdfplumber. 
Combined losses include data from Scamwatch, ReportCyber, AFCX, IDCARE and ASIC.
Adjustments applied to account for cross-reporting duplication.
""")