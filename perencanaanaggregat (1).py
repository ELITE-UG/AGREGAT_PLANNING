import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import io
import base64
import requests

# ==============================================================================
# 1. PAGE CONFIGURATION & PREMIUM MINIMALIST DESIGN STYLE
# ==============================================================================
st.set_page_config(
    page_title="Interactive Aggregate Planning Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS: Professional Academic Theme + FIXED SOLID STICKY TABS
st.markdown("""
<style>
    :root {
        color-scheme: light !important;
        --st-background: #ffffff !important;
        --st-color: #0f172a !important;
    }
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #f8fafc !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #0f172a !important;
        font-weight: 600 !important;
    }

    /* Clean Dataframes and Tables */
    div[data-testid="stDataFrame"], div[data-testid="stDataEditor"], [data-testid="stTable"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 6px !important;
    }

    div[data-baseweb="table"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
    }
    
    /* Form Inputs & Sidebar Controls */
    div[data-baseweb="input"], div[data-baseweb="select"], select, input {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 4px !important;
    }
    
    button[title="Increment"], button[title="Decrement"], 
    [data-testid="stNumberInputStepDown"], [data-testid="stNumberInputStepUp"] {
        background-color: #f1f5f9 !important;
        color: #475569 !important;
        border: 1px solid #cbd5e1 !important;
    }

    /* KPI Component Cards with Soft Border Highlights */
    .kpi-card {
        background-color: #ffffff !important;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #e2e8f0;
        position: relative;
        overflow: hidden;
    }
    .kpi-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; bottom: 0;
        width: 4px;
        background: #2563eb;
    }
    .kpi-title { font-size: 12px; color: #64748b !important; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .kpi-value { font-size: 22px; color: #0f172a !important; font-weight: 700; margin-top: 4px; }
    .kpi-card small { color: #475569 !important; font-weight: 500; }
    
    /* Academic Recommendation Box */
    .recommendation-box {
        background-color: #f8fafc !important;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 20px;
        position: relative;
    }
    .recommendation-box::before {
        content: "";
        position: absolute;
        top: 0; left: 0; bottom: 0;
        width: 4px;
        background: #10b981;
    }
    .recommendation-box h4 { color: #0f172a !important; font-weight: 700; margin-top: 0; }
    .recommendation-box li, .recommendation-box p { color: #334155 !important; font-weight: 500; line-height: 1.6; }

    hr {
        border: 0;
        height: 1px;
        background: #e2e8f0 !important;
        margin: 20px 0;
    }

    /* Template File Guide Panel */
    .upload-box {
        background-color: #f8fafc !important;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 20px;
        position: relative;
        margin-bottom: 20px;
    }
    .upload-box::before {
        content: "";
        position: absolute;
        top: 0; left: 0; bottom: 0;
        width: 4px;
        background: #2563eb;
    }
    .upload-box h4 { color: #0f172a !important; font-weight: 700; margin-top: 0; margin-bottom: 8px;}
    .upload-box p { color: #475569 !important; font-size: 14px; margin-bottom: 12px; line-height: 1.5; }
    .table-template { width: 100%; border-collapse: collapse; margin: 10px 0; background-color: #ffffff; }
    .table-template th { background-color: #f1f5f9; color: #0f172a; padding: 6px 12px; border: 1px solid #cbd5e1; font-size: 13px; font-weight: 600; text-align: left; }
    .table-template td { padding: 6px 12px; border: 1px solid #cbd5e1; color: #475569; font-size: 13px; font-family: monospace; }

    /* =========================================================================
       FIXED CRITICAL ELEMENT: STICKY/FREEZE TABS VIEWPORTS SETUP
       ========================================================================= */
    [data-testid="stMainBlockContainer"] {
        position: relative !important;
    }
    
    div[data-testid="stTabs"] [data-baseweb="tab-list"] { 
        gap: 4px; 
        border-bottom: 2px solid #e2e8f0 !important;
        position: -webkit-sticky !important;
        position: sticky !important;
        top: 2.85rem !important; 
        background-color: #ffffff !important;
        z-index: 99999 !important;
        padding-top: 12px !important;
        padding-bottom: 12px !important;
        box-shadow: 0 8px 16px -8px rgba(0,0,0,0.08) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: #64748b !important;
        padding: 10px 16px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        color: #2563eb !important;
        border-bottom: 2px solid #2563eb !important;
        font-weight: 600 !important;
    }

    /* Minimalist Academic Authors Profiles */
    .author-profile-container {
        border-left: 3px solid #2563eb; 
        padding-left: 12px;
        margin: 10px 0;
    }
    .author-profile-name {
        font-size: 14px;
        color: #0f172a !important;
        font-weight: 600;
        letter-spacing: 0.3px;
        line-height: 1.4;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# LOGO & HEADLINE STRUCTURE (FIXED: RESPONSIVE SIDE-BY-SIDE NO COLLISION)
# ==============================================================================
def load_gdrive_image_base64(file_id):
    try:
        url = f"https://drive.google.com/uc?export=view&id={file_id}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return base64.b64encode(response.content).decode()
    except Exception:
        pass
    return ""

# Memuat Gambar menggunakan ID dari Google Drive mentah Anda
logo_1_b64 = load_gdrive_image_base64("1wMCJi6pWtYuqsWJC7m2lbjtqNXFYWDP7")
# Logo pendukung Laboratorium
logo_2_b64 = load_gdrive_image_base64("1V3x3dfHlsHP-LLbkxVGt4Z9NmfdoR8XH") 

if logo_1_b64:
    st.markdown(f"""
    <div style="display: flex; align-items: center; flex-wrap: wrap; gap: 20px; margin-top: -45px; margin-bottom: 10px; width: 100%;">
        <div style="display: flex; gap: 12px; flex-shrink: 0; align-items: center;">
            <img src="data:image/png;base64,{logo_1_b64}" style="height: 60px; width: auto; object-fit: contain;">
            {"<img src='data:image/png;base64," + logo_2_b64 + "' style='height: 60px; width: auto; object-fit: contain;'>" if logo_2_b64 else ""}
        </div>
        <div style="flex: 1; min-width: 320px;">
            <h1 style="margin: 0; padding: 0; font-size: 28px; font-weight: 700; color: #0f172a; line-height: 1.2;">
                Decision Support System: Interactive Aggregate Production Planning (12 Periods)
            </h1>
            <p style="margin: 4px 0 0 0; color: #475569; font-size: 14px; line-height: 1.4;">
                Comprehensive operational capacity analysis utilizing robust scenario-based optimization techniques.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<style>div[data-testid='stVerticalBlock'] > div:first-child {margin-top: -30px;}</style>", unsafe_allow_html=True)
    st.title("Decision Support System: Interactive Aggregate Production Planning (12 Periods)")
    st.markdown("Comprehensive operational capacity analysis utilizing robust scenario-based optimization techniques.")

st.markdown("---")

# ==============================================================================
# DATA STATE MANAGEMENT & MULTI-PARAMETER EXCEL SPREADSHEET INTEGRATION
# ==============================================================================
num_periods = 12
default_demand = [1200, 1300, 1500, 1700, 1800, 1600, 1400, 1300, 1100, 1400, 1600, 1900]

if "base_demand" not in st.session_state:
    st.session_state.base_demand = default_demand.copy()
if "editor_trigger" not in st.session_state:
    st.session_state.editor_trigger = 0

st.markdown("""
<div class="upload-box">
    <h4>Data Integration via Excel Template (Multi-Parameter)</h4>
    <p>Upload operational targets and system configurations simultaneously. To ensure precise mapping, files must strictly match the following header column template:</p>
    <table class="table-template">
        <tr>
            <th>Period</th>
            <th>Demand</th>
            <th>Workforce</th>
            <th>Worker Capacity</th>
            <th>Initial Inventory</th>
            <th>Safety Stock</th>
        </tr>
        <tr>
            <td>Month 1</td>
            <td>1200</td>
            <td>20</td>
            <td>70</td>
            <td>200</td>
            <td>100</td>
        </tr>
        <tr>
            <td>Month 2</td>
            <td>1300</td>
            <td>20</td>
            <td>70</td>
            <td>0</td>
            <td>100</td>
        </tr>
    </table>
    <small style="color: #64748b; font-weight: 500;">*Note: The 'Initial Inventory' is retrieved from the first data row (Month 1) as the planning horizon threshold.</small>
</div>
""", unsafe_allow_html=True)

# Generate Template Sheet
template_df = pd.DataFrame({
    "Period": [f"Month {i+1}" for i in range(num_periods)],
    "Demand": st.session_state.base_demand,
    "Workforce": [20] * num_periods,
    "Worker Capacity": [70] * num_periods,
    "Initial Inventory": [200] + [0] * (num_periods - 1),
    "Safety Stock": [100] * num_periods
})

template_io = io.BytesIO()
with pd.ExcelWriter(template_io, engine='openpyxl') as writer:
    template_df.to_excel(writer, index=False, sheet_name='Planning_Template')
template_io.seek(0)

col_dl, col_up = st.columns([1, 2])

with col_dl:
    st.write("") 
    st.write("") 
    st.download_button(
        label="Download Official Excel Template",
        data=template_io,
        file_name="aggregate_planning_template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

with col_up:
    uploaded_file = st.file_uploader("Upload system files here:", type=["xlsx", "xls"], label_visibility="collapsed")

if uploaded_file is not None:
    try:
        excel_data = pd.read_excel(uploaded_file)
        if "Period" in excel_data.columns and "Demand" in excel_data.columns:
            parsed_df = excel_data.head(num_periods).copy()
            st.session_state.base_demand = pd.to_numeric(parsed_df["Demand"], errors='coerce').fillna(0).astype(int).tolist()
            st.session_state.editor_trigger += 1
            st.success("Excel data verified successfully! Operational attributes synchronized.")
        else:
            st.error("Invalid column headers! Check if 'Period' and 'Demand' keys exist.")
    except Exception as e:
        st.error(f"Failed to read file: {str(e)}")

st.markdown("---")

# ==============================================================================
# 2. SIDEBAR - PROFESSIONAL SYSTEM CONTROL PANEL
# ==============================================================================
st.sidebar.header("Operational Parameters")

# Masukkan ke dalam data_editor dan langsung simpan perubahannya ke session_state
sidebar_input_df = pd.DataFrame({
    "Period": [f"Month {i+1}" for i in range(num_periods)],
    "Demand": st.session_state.base_demand
})

master_editor_df = st.sidebar.data_editor(
    sidebar_input_df,
    hide_index=True,
    key=f"master_editor_{st.session_state.editor_trigger}"
)

st.session_state.base_demand = master_editor_df["Demand"].astype(int).tolist()
base_demand = st.session_state.base_demand

st.sidebar.subheader("Capacity & Workforce")
init_workforce = st.sidebar.number_input("Initial Workforce (Workers)", value=20, min_value=0)
worker_cap = st.sidebar.number_input("Worker Capacity (Units/Month)", value=70, min_value=1)
init_inv = st.sidebar.number_input("Initial Inventory (Units)", value=200, min_value=0)
safety_stock = st.sidebar.number_input("Safety Stock Threshold (Units)", value=100, min_value=0)

workforce_list = [init_workforce] * num_periods
capacity_list = [worker_cap] * num_periods
inventory_initial_list = [init_inv] + [0] * (num_periods - 1)
safety_stock_list = [safety_stock] * num_periods

st.sidebar.subheader("Additional Capacity Limits")
max_ot_cap = st.sidebar.number_input("Maximum Overtime Limit (Units/Month)", value=300, min_value=0)
min_sub_cap = st.sidebar.number_input("Minimum Subcontracting Limit (Units/Month)", value=50, min_value=0)
max_sub_cap = st.sidebar.number_input("Maximum Subcontracting Limit (Units/Month)", value=500, min_value=0)

if min_sub_cap > max_sub_cap:
    st.sidebar.error("Minimum subcontract limit cannot exceed maximum capacity limits!")

st.sidebar.header("Cost Structure (IDR)")
c_material = st.sidebar.number_input("Raw Material Cost (/Unit)", value=150000, step=5000, min_value=0)
c_regular = st.sidebar.number_input("Regular Production Cost (/Unit)", value=50000, step=1000, min_value=0)
c_overtime = st.sidebar.number_input("Overtime Production Cost (/Unit)", value=75000, step=1000, min_value=0)
c_subcontract = st.sidebar.number_input("Subcontracting Cost (/Unit)", value=90000, step=1000, min_value=0)
c_inventory = st.sidebar.number_input("Holding Cost (/Unit/Month)", value=10000, step=500, min_value=0)
c_stockout = st.sidebar.number_input("Stockout Cost (/Unit/Month)", value=15000, step=500, min_value=0)
c_hiring = st.sidebar.number_input("Hiring Cost (/Worker)", value=2000000, step=50000, min_value=0)
c_firing = st.sidebar.number_input("Firing Cost (/Worker)", value=3500000, step=50000, min_value=0)

# KUNCI PERBAIKAN 2: Proteksi Probabilitas Kontrol Dinamis agar Tidak Minus
st.sidebar.header("Demand Uncertainty Scenarios")
p_normal = st.sidebar.slider("Normal Probability", 0.0, 1.0, 0.6, step=0.05)

# Sisa slot maksimal yang tersedia untuk optimis setelah dipotong nilai normal
max_p_optimistic = round(1.0 - p_normal, 2)
p_optimistic = st.sidebar.slider("Optimistic Probability (Demand)", 0.0, float(max_p_optimistic), min(0.2, max_p_optimistic), step=0.05)

# Pesimis otomatis dikunci dari sisa mutlak (pasti >= 0 dan total selalu tepat 1.0)
p_pessimistic = round(1.0 - p_normal - p_optimistic, 2)
st.sidebar.info(f"Pessimistic Probability (Demand): {p_pessimistic}")

selected_scenario = st.selectbox("Dashboard Target Scenario View:", ["Normal", "Optimis", "Pesimis"])

# ==============================================================================
# 3. CORE PROCESSING MATHEMATICAL ALGORITHM ENGINE
# ==============================================================================
def calculate_aggregate_planning(strategy, base_demand_list, demand_list, wf_inp, cap_inp, sf_inp, initial_inventory_val):
    inv_prev = initial_inventory_val
    wf_prev = wf_inp[0]
    records = []
    
    if strategy == "Level":
        total_demand = sum(demand_list)
        avg_cap = np.mean(cap_inp) if np.mean(cap_inp) > 0 else 1
        total_production_needed = max(0, total_demand + sf_inp[-1] - initial_inventory_val)
        avg_production_needed = total_production_needed / num_periods
        constant_wf = int(np.ceil(avg_production_needed / avg_cap))
    else:
        constant_wf = wf_inp[0]

    for t in range(num_periods):
        b_d = base_demand_list[t]
        d_t = demand_list[t]
        c_cap = cap_inp[t]
        c_safety = sf_inp[t]
        net_demand = d_t + c_safety
        
        if strategy == "Chase":
            prod_needed = max(0, d_t + c_safety - inv_prev)
            wf_needed = int(np.ceil(prod_needed / c_cap)) if c_cap > 0 else 0
            hiring = max(0, wf_needed - wf_prev)
            firing = max(0, wf_prev - wf_needed)
            wf_current = wf_needed
            rt_prod = wf_current * c_cap
        elif strategy == "Level":
            wf_current = constant_wf
            hiring = max(0, wf_current - wf_prev) if t == 0 else 0
            firing = max(0, wf_prev - wf_current) if t == 0 else 0
            rt_prod = wf_current * c_cap
        elif strategy == "Mixed":
            wf_current = wf_inp[t]
            hiring = max(0, wf_current - wf_prev)
            firing = max(0, wf_prev - wf_current)
            rt_prod = wf_current * c_cap

        deficit = max(0, net_demand - rt_prod - inv_prev)
        ot_prod = 0
        sub_prod = 0
        
        if strategy == "Mixed" and deficit > 0:
            ot_prod = min(max_ot_cap, deficit)
            deficit -= ot_prod
            if deficit > 0:
                sub_needed = max(min_sub_cap, deficit)
                sub_prod = min(max_sub_cap, sub_needed)
                deficit = max(0, deficit - sub_prod)

        total_supply = inv_prev + rt_prod + ot_prod + sub_prod
        if total_supply >= d_t:
            inv_end = total_supply - d_t
            stockout = 0
        else:
            inv_end = 0
            stockout = d_t - total_supply
            
        cost_mat = (rt_prod + ot_prod) * c_material 
        cost_rep = rt_prod * c_regular
        cost_labor = wf_current * 3000000
        cost_hire = hiring * c_hiring
        cost_fire = firing * c_firing
        cost_hold = inv_end * c_inventory
        cost_ot = ot_prod * c_overtime
        cost_sub = sub_prod * c_subcontract
        cost_short = stockout * c_stockout
        total_cost = cost_mat + cost_rep + cost_labor + cost_hire + cost_fire + cost_hold + cost_ot + cost_sub + cost_short

        records.append({
            "Period": f"Month {t+1}",
            "Base Demand": b_d,
            "Demand": d_t,
            "Net Demand": net_demand,
            "Workforce": wf_current,
            "Hiring": hiring,
            "Firing": firing,
            "RT Production": rt_prod,
            "OT Production": ot_prod,
            "Subcontracting": sub_prod,
            "Inventory": inv_end,
            "Stockout": stockout,
            "Total Supply": total_supply,
            "Material Cost": cost_mat,
            "Production Cost": cost_rep,
            "Labor Cost": cost_labor,
            "Hiring Cost": cost_hire,
            "Firing Cost": cost_fire,
            "Inventory Holding Cost": cost_hold,
            "Overtime Cost": cost_ot,
            "Subcontract Cost": cost_sub,
            "Shortage Cost": cost_short,
            "Total Cost": total_cost
        })
        inv_prev = inv_end
        wf_prev = wf_current
        
    return pd.DataFrame(records)

demand_scenarios = {
    "Normal": base_demand,
    "Optimis": [int(d * 1.25) for d in base_demand],
    "Pesimis": [int(d * 0.75) for d in base_demand]
}

results = {}
for strat in ["Chase", "Level", "Mixed"]:
    results[strat] = {}
    for scen, d_list in demand_scenarios.items():
        results[strat][scen] = calculate_aggregate_planning(strat, base_demand, d_list, workforce_list, capacity_list, safety_stock_list, init_inv)

# ==============================================================================
# 4. EXPECTED FINANCIAL METRICS COMPUTATION ENGINE
# ==============================================================================
summary_metrics = []
for strat in ["Chase", "Level", "Mixed"]:
    c_norm = results[strat]["Normal"]["Total Cost"].sum()
    c_opt = results[strat]["Optimis"]["Total Cost"].sum()
    c_pess = results[strat]["Pesimis"]["Total Cost"].sum()
    expected_cost = (c_norm * p_normal) + (c_opt * p_optimistic) + (c_pess * p_pessimistic)
    
    df_active = results[strat][selected_scenario]
    total_demand = df_active["Demand"].sum()
    total_shortage = df_active["Stockout"].sum()
    
    service_level = max(0.0, ((total_demand - total_shortage) / total_demand) * 100) if total_demand > 0 else 100
    actual_production = df_active["RT Production"].sum() + df_active["OT Production"].sum()
    max_capacity = (df_active["Workforce"] * capacity_list).sum() + (max_ot_cap * num_periods)
    capacity_util = (actual_production / max_capacity) * 100 if max_capacity > 0 else 0
    
    summary_metrics.append({
        "Strategy": strat,
        "Total Cost (Active)": df_active["Total Cost"].sum(),
        "Expected Cost": expected_cost,
        "Service Level": service_level,
        "Capacity Utilization": capacity_util
    })

summary_df = pd.DataFrame(summary_metrics)

def apply_forced_light_theme(fig, is_cost_chart=False):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor='#ffffff',
        plot_bgcolor='#f8fafc',  
        font=dict(color="#0f172a", size=11, family="'Inter', sans-serif"),
        title_font=dict(color="#0f172a", size=14, family="'Inter', sans-serif"),
        xaxis=dict(gridcolor="#ffffff", linecolor="#cbd5e1", tickfont=dict(color="#475569")),
        yaxis=dict(gridcolor="#e2e8f0", linecolor="#cbd5e1", tickfont=dict(color="#475569")),
        legend=dict(font=dict(color="#475569"), bordercolor="#e2e8f0", borderwidth=1, bgcolor="rgba(255,255,255,0.9)"),
        bargap=0.25
    )
    if is_cost_chart:
        fig.update_layout(yaxis=dict(tickprefix="Rp "))
        fig.update_traces(texttemplate='Rp %{y:,.0f}', textposition='outside', selector=dict(type='bar'))
    return fig

# ==============================================================================
# 6. DASHBOARD INTERFACE LAYOUT (ORDER REVERSED PER USER SCREENSHOT RULES)
# ==============================================================================
tab1, tab2, tab3 = st.tabs([
    "🔍 Detailed Operational", 
    "📈 Executive Summary & Strategy Formulation", 
    "🎲 Robust Scenario & Risk Analysis"
])

# ------------------------------------------------------------------------------
# TAB 1: EXECUTIVE SUMMARY & STRATEGY FORMULATION
# ------------------------------------------------------------------------------
with tab2:
    st.subheader(f"Key Performance Indicator (KPI) — Scenario: {selected_scenario}")
    
    cols = st.columns(3)
    for idx, row in summary_df.iterrows():
        with cols[idx]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">{row['Strategy']} Strategy Profile</div>
                <div class="kpi-value">Rp {row['Total Cost (Active)']:,.0f}</div>
                <small>Expected Cost: Rp {row['Expected Cost']:,.0f}</small><br>
                <small>Service Level Target: {row['Service Level']:.2f}%</small><br>
                <small>Capacity Utilization: {row['Capacity Utilization']:.1f}%</small>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        fig_cost = px.bar(summary_df, x="Strategy", y="Total Cost (Active)", 
                          title=f"Total Cumulative Expenditure Comparison ({selected_scenario})",
                          color="Strategy", color_discrete_sequence=px.colors.qualitative.Safe)
        fig_cost = apply_forced_light_theme(fig_cost, is_cost_chart=True)
        st.plotly_chart(fig_cost, use_container_width=True)
    with c2:
        fig_sl = px.bar(summary_df, x="Strategy", y="Service Level", 
                          title="Demand Fulfillment Integrity Metrics (Service Level %)",
                          color="Strategy", text_auto='.2f', range_y=[0, 105], color_discrete_sequence=px.colors.qualitative.Safe)
        fig_sl = apply_forced_light_theme(fig_sl)
        fig_sl.update_traces(textposition='outside', selector=dict(type='bar'))
        st.plotly_chart(fig_sl, use_container_width=True)

    st.markdown("### Strategic Recommendation Model")
    best_cost_strat = summary_df.loc[summary_df["Expected Cost"].idxmin()]["Strategy"]
    best_sl_strat = summary_df.loc[summary_df["Service Level"].idxmax()]["Strategy"]
    best_util_strat = summary_df.loc[summary_df["Capacity Utilization"].idxmax()]["Strategy"]
    
    st.markdown(f"""
    <div class="recommendation-box">
        <h4>System Analysis Summary for Policy Formulation:</h4>
        <ul>
            <li><b>Financial Optimization Vector (Robustness Criteria):</b> The <b>{best_cost_strat}</b> model manages risk with the minimum expected cost distribution across probability nodes.</li>
            <li><b>Supply Chain Safety Vector (Market Reliability):</b> The <b>{best_sl_strat}</b> configuration minimizes stockout constraints under volatile demand conditions.</li>
            <li><b>Asset Utilization Vector (Fixed Infrastructure Efficiency):</b> The <b>{best_util_strat}</b> model records maximum workforce deployment efficiency.</li>
        </ul>
        <p><b>Conclusion Matrix:</b> The empirical evidence suggests implementing the <b>{best_cost_strat} Strategy</b> to protect the operating margins against structural demand distribution shifts within long-term planning bounds.</p>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 2: DETAILED OPERATIONAL DEEP-DIVE
# ------------------------------------------------------------------------------
with tab1:
    selected_strategy = st.radio("Target Operational Strategy:", ["Chase", "Level", "Mixed"], horizontal=True)
    df_selected = results[selected_strategy][selected_scenario]
    
    st.subheader(f"Master Operational Planning Horizon: {selected_strategy} Strategy ({selected_scenario} View)")
    master_display = df_selected[["Period", "Base Demand", "Demand", "Net Demand", "RT Production", "OT Production", "Subcontracting", "Total Supply", "Inventory", "Stockout"]].copy()
    master_display.index = range(1, len(master_display) + 1)
    st.dataframe(master_display.style.format(precision=0), use_container_width=True)
    
    if selected_strategy == "Chase":
        st.subheader("Workforce Capacity & Allocation Schedule")
        chase_display = df_selected[["Period", "Workforce", "Hiring", "Firing", "RT Production"]].copy()
        chase_display.index = range(1, len(chase_display) + 1)
        st.dataframe(chase_display.style.format(precision=0), use_container_width=True)
        
    elif selected_strategy == "Level":
        st.subheader("Inventory Buffers & Capacity Utilization Variances")
        df_level_spec = df_selected[["Period", "Inventory", "Stockout", "RT Production"]].copy()
        df_level_spec["Capacity Efficiency (%)"] = np.where((df_selected["Workforce"] * capacity_list) > 0, (df_level_spec["RT Production"] / (df_selected["Workforce"] * capacity_list)) * 100, 0)
        df_level_spec.index = range(1, len(df_level_spec) + 1)
        st.dataframe(df_level_spec.style.format(precision=1), use_container_width=True)
        
    elif selected_strategy == "Mixed":
        st.subheader("Sourcing Profiles & Make-or-Buy Allocation Parameters")
        mob_df = df_selected[["Period", "RT Production", "OT Production", "Subcontracting"]].copy()
        total_p = mob_df["RT Production"] + mob_df["OT Production"] + mob_df["Subcontracting"]
        mob_df["Internal Content (%)"] = np.where(total_p > 0, ((mob_df["RT Production"] + mob_df["OT Production"]) / total_p) * 100, 0)
        mob_df.index = range(1, len(mob_df) + 1)
        st.dataframe(mob_df.style.format(precision=1), use_container_width=True)

    st.subheader("Comprehensive Variance Financial Accounts")
    cost_cols = ["Period", "Material Cost", "Production Cost", "Labor Cost", "Hiring Cost", "Firing Cost", "Inventory Holding Cost", "Overtime Cost", "Subcontract Cost", "Shortage Cost", "Total Cost"]
    cost_display = df_selected[cost_cols].copy()
    cost_display.index = range(1, len(cost_display) + 1)
    st.dataframe(cost_display.style.format(precision=0), use_container_width=True)
    
    st.markdown("### High-Contrast System Performance Trends")
    v1, v2 = st.columns(2)
    with v1:
        fig_dp = go.Figure()
        fig_dp.add_trace(go.Scatter(x=df_selected["Period"], y=df_selected["Demand"], name="Market Demand Curve", line=dict(color='#dc2626', width=3, dash='dash')))
        fig_dp.add_trace(go.Bar(x=df_selected["Period"], y=df_selected["RT Production"] + df_selected["OT Production"] + df_selected["Subcontracting"], name="Aggregated Output Yield", marker_color='#2563eb'))
        fig_dp.update_layout(title="Demand Alignment vs. Output Realization Volumetrics", barmode='group')
        fig_dp = apply_forced_light_theme(fig_dp)
        st.plotly_chart(fig_dp, use_container_width=True)
    with v2:
        # Perbaikan Struktur Stacked Bar Chart agar Angka Tidak Saling Menabrak
        fig_cb = px.bar(
            df_selected, 
            x="Period", 
            y=["Material Cost", "Production Cost", "Inventory Holding Cost", "Overtime Cost", "Subcontract Cost", "Shortage Cost"],
            title="Periodic Operating Expenditure Breakdown", 
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        
        # Terapkan basis tema putih akademis yang sudah dibuat sebelumnya
        fig_cb = apply_forced_light_theme(fig_cb, is_cost_chart=True)
        
        # KUNCI PERBAIKAN GRAFIK NABRAK: 
        # 1. Bersihkan texttemplate bawaan agar segmen kecil/nol tidak memaksa menulis teks di grafik.
        # 2. Rapikan format hover/tooltip saat kursor mendekat dengan separator mata uang yang rapi.
        fig_cb.update_traces(
            texttemplate=None,  # Menghapus angka statis yang saling bertabrakan
            hovertemplate="<b>%{x}</b><br>%{layer}: Rp %{y:,.0f}<extra></extra>"
        )
        
        # Menambahkan interaktivitas total kumulatif saat hover di atas satu pilar bulan
        fig_cb.update_layout(
            hovermode="x unified",
            legend_traceorder="normal"
        )
        
        st.plotly_chart(fig_cb, use_container_width=True)

    v3, v4 = st.columns(2)
    with v3:
        fig_inv = px.line(df_selected, x="Period", y="Inventory", title="End-of-Period Inventory Levels (Safety Buffers)", markers=True)
        fig_inv.update_traces(line=dict(color='#059669', width=3))
        fig_inv = apply_forced_light_theme(fig_inv)
        st.plotly_chart(fig_inv, use_container_width=True)
    with v4:
        fig_os = go.Figure()
        fig_os.add_trace(go.Bar(x=df_selected["Period"], y=df_selected["OT Production"], name="Overtime Allotment", marker_color='#d97706'))
        fig_os.add_trace(go.Bar(x=df_selected["Period"], y=df_selected["Subcontracting"], name="Subcontracted Allotment", marker_color='#7c3aed'))
        fig_os.update_layout(title="Supplementary Capacity Utilization Profiles", barmode='stack')
        fig_os = apply_forced_light_theme(fig_os)
        st.plotly_chart(fig_os, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 3: ROBUST SCENARIO & RISK ANALYSIS
# ------------------------------------------------------------------------------
with tab3:
    st.subheader("Robust Financial Performance Metrics Across Scenarios")
    robust_records = []
    for strat in ["Chase", "Level", "Mixed"]:
        c_norm = results[strat]["Normal"]["Total Cost"].sum()
        c_opt = results[strat]["Optimis"]["Total Cost"].sum()
        c_pess = results[strat]["Pesimis"]["Total Cost"].sum()
        expected_cost = (c_norm * p_normal) + (c_opt * p_optimistic) + (c_pess * p_pessimistic)
        robust_records.append({
            "Planning Strategy": strat,
            "Pessimistic Scenario": c_pess,
            "Normal Scenario (Base)": c_norm,
            "Optimistic Scenario": c_opt,
            "Expected System Value (Robust Cost)": expected_cost
        })
    robust_df = pd.DataFrame(robust_records)
    st.dataframe(robust_df.style.format(precision=0), use_container_width=True)

    st.markdown("### Multi-Scenario Contingency Trajectories")
    plot_data = []
    for strat in ["Chase", "Level", "Mixed"]:
        for scen in ["Normal", "Optimis", "Pesimis"]:
            total_scen_cost = results[strat][scen]["Total Cost"].sum()
            plot_data.append({"Strategy": strat, "Scenario": scen, "Total Cost": total_scen_cost})
    plot_df = pd.DataFrame(plot_data)
    
    fig_robust = px.line(plot_df, x="Scenario", y="Total Cost", color="Strategy", markers=True,
                         title="Operational System Costs Variations Across Boundary Risk Nodes")
    fig_robust = apply_forced_light_theme(fig_robust, is_cost_chart=True)
    fig_robust.update_traces(line=dict(width=3.5), selector=dict(type='scatter'))
    st.plotly_chart(fig_robust, use_container_width=True)

# ==============================================================================
# 7. PROFESSIONAL DEVELOPMENT TEAM / AUTHORS SECTION
# ==============================================================================
st.markdown("---")
st.subheader("Development Team & Authors")

auth_cols = st.columns(4)
authors_list = ["Azka Ibrah Mayditama", "Maulida Boru Butar Butar", "Muhammad Kamandafif", "Syehan"]

for idx, name in enumerate(authors_list):
    with auth_cols[idx]:
        st.markdown(f"""
        <div class="author-profile-container">
            <div class="author-profile-name">{name}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# FOOTER SYSTEM METADATA & COPYRIGHT INFO
# ==============================================================================
st.markdown("""
<div class="sticky-copyright" style="text-align: center; color: #64748b; font-size: 12px; font-weight: 500; padding: 20px 0; border-top: 1px solid #e2e8f0;">
    &copy; 2026 Elementary Laboratory of Industrial Engineering
</div>
""", unsafe_allow_html=True)
