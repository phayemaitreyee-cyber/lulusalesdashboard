import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Inventory & Waste Reduction System",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Pastel Colour Palette ─────────────────────────────────────────────────────
PASTEL_PINK       = "#FFB3C6"   # soft pink
PASTEL_LAVENDER   = "#C9B8E8"   # soft purple
PASTEL_MINT       = "#B5EAD7"   # soft green
PASTEL_PEACH      = "#FFDAB9"   # soft peach/orange
PASTEL_SKY        = "#AED6F1"   # soft blue
PASTEL_YELLOW     = "#FFF5BA"   # soft yellow
PASTEL_CORAL      = "#FFB5A7"   # soft coral
PASTEL_LILAC      = "#E8D5F5"   # soft lilac
PASTEL_SAGE       = "#D4EDDA"   # soft sage green
PASTEL_CREAM      = "#FFF8F0"   # warm cream (background)
PASTEL_TEXT       = "#5A5A7A"   # muted dark text
PASTEL_CARD_BG    = "#FFFFFF"   # white card background
PASTEL_BORDER     = "#E0D7F0"   # light lavender border

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base & Background ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #FFF8F0 !important;
    color: #5A5A7A !important;
    font-family: 'Segoe UI', sans-serif;
}

[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #E8D5F5 0%, #AED6F1 100%) !important;
    border-right: 2px solid #E0D7F0;
}

[data-testid="stSidebar"] * {
    color: #5A5A7A !important;
}

/* ── Metric Cards ── */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1.5px solid #E0D7F0;
    border-radius: 14px;
    padding: 16px 20px;
    box-shadow: 0 2px 8px rgba(180,160,220,0.10);
}

[data-testid="stMetricLabel"] { color: #9B8EC4 !important; font-weight: 600; }
[data-testid="stMetricValue"] { color: #5A5A7A !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #C9B8E8, #AED6F1) !important;
    color: #5A5A7A !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #FFB3C6, #C9B8E8) !important;
    box-shadow: 0 4px 14px rgba(200,150,200,0.25) !important;
    transform: translateY(-1px);
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background-color: #F5EEFF;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    color: #9B8EC4 !important;
    border-radius: 10px;
    font-weight: 500;
    padding: 8px 20px;
}
.stTabs [aria-selected="true"] {
    background-color: #C9B8E8 !important;
    color: #5A5A7A !important;
    font-weight: 700 !important;
}

/* ── DataFrames / Tables ── */
[data-testid="stDataFrame"] {
    border: 1.5px solid #E0D7F0;
    border-radius: 12px;
    overflow: hidden;
}

/* ── Select / Input widgets ── */
.stSelectbox > div > div,
.stMultiSelect > div > div,
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background-color: #FFFFFF !important;
    border: 1.5px solid #C9B8E8 !important;
    border-radius: 10px !important;
    color: #5A5A7A !important;
}

/* ── Sliders ── */
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background-color: #C9B8E8 !important;
    border-color: #9B8EC4 !important;
}

/* ── Progress bars ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #B5EAD7, #AED6F1) !important;
    border-radius: 10px;
}

/* ── Alerts / Info boxes ── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border-left: 5px solid #C9B8E8 !important;
    background-color: #F5EEFF !important;
    color: #5A5A7A !important;
}

/* ── Expanders ── */
.streamlit-expanderHeader {
    background-color: #F5EEFF !important;
    border-radius: 10px !important;
    color: #5A5A7A !important;
    border: 1px solid #E0D7F0 !important;
}

/* ── Section headers (h1–h3) ── */
h1 { color: #9B8EC4 !important; letter-spacing: 0.5px; }
h2 { color: #7BA7CC !important; }
h3 { color: #7BBF9E !important; }

/* ── Dividers ── */
hr { border-color: #E0D7F0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 7px; }
::-webkit-scrollbar-track { background: #F5EEFF; }
::-webkit-scrollbar-thumb { background: #C9B8E8; border-radius: 6px; }
::-webkit-scrollbar-thumb:hover { background: #9B8EC4; }
</style>
""", unsafe_allow_html=True)

# ── Pastel chart colour sequence (used in all Plotly charts) ──────────────────
PASTEL_CHART_COLORS = [
    PASTEL_LAVENDER, PASTEL_SKY, PASTEL_MINT,
    PASTEL_PINK, PASTEL_PEACH, PASTEL_CORAL,
    PASTEL_YELLOW, PASTEL_LILAC, PASTEL_SAGE
]

# ── Helper: apply pastel template to any Plotly figure ───────────────────────
def apply_pastel_theme(fig, title=""):
    fig.update_layout(
        paper_bgcolor=PASTEL_CREAM,
        plot_bgcolor="#F5EEFF",
        font=dict(color=PASTEL_TEXT, family="Segoe UI"),
        title=dict(text=title, font=dict(color="#9B8EC4", size=16)),
        legend=dict(
            bgcolor=PASTEL_CREAM,
            bordercolor=PASTEL_BORDER,
            borderwidth=1,
            font=dict(color=PASTEL_TEXT)
        ),
        xaxis=dict(
            gridcolor=PASTEL_BORDER,
            zerolinecolor=PASTEL_BORDER,
            tickfont=dict(color=PASTEL_TEXT)
        ),
        yaxis=dict(
            gridcolor=PASTEL_BORDER,
            zerolinecolor=PASTEL_BORDER,
            tickfont=dict(color=PASTEL_TEXT)
        ),
        colorway=PASTEL_CHART_COLORS,
    )
    return fig

# ── Data generation (unchanged logic, colours injected via theme) ─────────────
@st.cache_data
def generate_inventory_data():
    categories = ['Produce', 'Dairy', 'Meat', 'Bakery', 'Beverages', 'Frozen', 'Snacks', 'Condiments']
    items = []
    for cat in categories:
        for i in range(random.randint(8, 15)):
            expiry_days = random.randint(-2, 30)
            quantity    = random.randint(0, 200)
            reorder_pt  = random.randint(20, 50)
            items.append({
                'Item ID'         : f"{cat[:3].upper()}-{i+1:03d}",
                'Product Name'    : f"{cat} Item {i+1}",
                'Category'        : cat,
                'Quantity'        : quantity,
                'Unit'            : random.choice(['kg', 'units', 'liters', 'boxes']),
                'Expiry Date'     : (datetime.now() + timedelta(days=expiry_days)).strftime('%Y-%m-%d'),
                'Days Until Expiry': expiry_days,
                'Reorder Point'   : reorder_pt,
                'Cost per Unit'   : round(random.uniform(0.5, 50.0), 2),
                'Supplier'        : f"Supplier {random.randint(1, 5)}",
                'Status'          : (
                    'Critical' if expiry_days < 0
                    else 'Expiring Soon' if expiry_days <= 3
                    else 'Low Stock' if quantity < reorder_pt
                    else 'Good'
                ),
                'Waste Risk'      : (
                    'High' if expiry_days < 0 or (expiry_days <= 3 and quantity > 30)
                    else 'Medium' if expiry_days <= 7
                    else 'Low'
                )
            })
    return pd.DataFrame(items)

@st.cache_data
def generate_sales_data():
    dates      = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    categories = ['Produce', 'Dairy', 'Meat', 'Bakery', 'Beverages', 'Frozen', 'Snacks', 'Condiments']
    records    = []
    for date in dates:
        for cat in categories:
            base     = random.randint(50, 500)
            seasonal = 1.2 if date.month in [6, 7, 8] else 0.8 if date.month in [12, 1, 2] else 1.0
            records.append({
                'Date'    : date,
                'Category': cat,
                'Sales'   : int(base * seasonal * random.uniform(0.8, 1.2)),
                'Revenue' : round(base * seasonal * random.uniform(2.0, 8.0), 2),
                'Waste'   : int(base * random.uniform(0.02, 0.15))
            })
    return pd.DataFrame(records)

@st.cache_data
def generate_waste_data():
    categories = ['Produce', 'Dairy', 'Meat', 'Bakery', 'Beverages', 'Frozen', 'Snacks', 'Condiments']
    reasons    = ['Expired', 'Damaged', 'Over-ordered', 'Quality Issues', 'Spoilage']
    records    = []
    for _ in range(200):
        cat = random.choice(categories)
        records.append({
            'Category'    : cat,
            'Reason'      : random.choice(reasons),
            'Quantity'    : random.randint(1, 50),
            'Cost'        : round(random.uniform(5, 500), 2),
            'Date'        : (datetime.now() - timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d'),
            'Preventable' : random.choice([True, False])
        })
    return pd.DataFrame(records)

# ── Load data ─────────────────────────────────────────────────────────────────
inventory_df = generate_inventory_data()
sales_df     = generate_sales_data()
waste_df     = generate_waste_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<h2 style='color:#9B8EC4; margin-bottom:4px;'>🌿 Smart Inventory</h2>"
        "<p style='color:#7BA7CC; font-size:13px; margin-top:0;'>Waste Reduction System</p>",
        unsafe_allow_html=True
    )
    st.divider()

    page = st.selectbox(
        "Navigate",
        ["📊 Dashboard", "📦 Inventory", "⚠️ Waste Alerts",
         "📈 Analytics", "🔮 Predictions", "⚙️ Settings"]
    )

    st.divider()
    st.markdown("<p style='color:#9B8EC4; font-weight:600; font-size:13px;'>Quick Filters</p>",
                unsafe_allow_html=True)
    selected_cats = st.multiselect(
        "Categories",
        options=inventory_df['Category'].unique(),
        default=inventory_df['Category'].unique()
    )
    risk_filter = st.selectbox("Waste Risk Level", ["All", "High", "Medium", "Low"])

    st.divider()
    now = datetime.now()
    st.markdown(
        f"<p style='color:#AED6F1; font-size:12px;'>"
        f"Last updated:<br><b>{now.strftime('%d %b %Y, %H:%M')}</b></p>",
        unsafe_allow_html=True
    )

# ── Filter data ───────────────────────────────────────────────────────────────
filtered_inv = inventory_df[inventory_df['Category'].isin(selected_cats)]
if risk_filter != "All":
    filtered_inv = filtered_inv[filtered_inv['Waste Risk'] == risk_filter]

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Dashboard
# ══════════════════════════════════════════════════════════════════════════════
if page == "📊 Dashboard":
    st.markdown(
        "<h1 style='color:#9B8EC4;'>📊 Inventory Dashboard</h1>",
        unsafe_allow_html=True
    )

    # ── KPI row ──────────────────────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    total_items    = len(inventory_df)
    critical_items = len(inventory_df[inventory_df['Status'] == 'Critical'])
    expiring_soon  = len(inventory_df[inventory_df['Status'] == 'Expiring Soon'])
    low_stock      = len(inventory_df[inventory_df['Status'] == 'Low Stock'])
    waste_value    = waste_df['Cost'].sum()

    c1.metric("Total Items",       total_items)
    c2.metric("Critical Items",    critical_items,  delta=f"-{critical_items} need action", delta_color="inverse")
    c3.metric("Expiring Soon",     expiring_soon,   delta="Next 3 days")
    c4.metric("Low Stock",         low_stock,       delta="Below reorder point")
    c5.metric("Total Waste Value", f"\\({waste_value:,.0f}", delta="-12% vs last month", delta_color="inverse")

    st.divider()

    # ── Charts row 1 ─────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        status_counts = inventory_df['Status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        fig_status = px.pie(
            status_counts, values='Count', names='Status',
            color_discrete_sequence=PASTEL_CHART_COLORS,
            hole=0.45
        )
        fig_status = apply_pastel_theme(fig_status, "Inventory Status Distribution")
        st.plotly_chart(fig_status, use_container_width=True)

    with col2:
        cat_waste = waste_df.groupby('Category')['Cost'].sum().reset_index()
        fig_waste = px.bar(
            cat_waste, x='Category', y='Cost',
            color='Category',
            color_discrete_sequence=PASTEL_CHART_COLORS
        )
        fig_waste = apply_pastel_theme(fig_waste, "Waste Cost by Category (\\))")
        st.plotly_chart(fig_waste, use_container_width=True)

    # ── Charts row 2 ─────────────────────────────────────────────────────────
    col3, col4 = st.columns(2)

    with col3:
        monthly = sales_df.groupby(sales_df['Date'].dt.month)['Waste'].sum().reset_index()
        monthly.columns = ['Month', 'Waste']
        month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        monthly['Month'] = monthly['Month'].apply(lambda x: month_names[x-1])
        fig_trend = px.line(
            monthly, x='Month', y='Waste',
            markers=True,
            color_discrete_sequence=[PASTEL_LAVENDER]
        )
        fig_trend.update_traces(
            line=dict(width=3, color=PASTEL_LAVENDER),
            marker=dict(size=8, color=PASTEL_PINK, line=dict(color=PASTEL_LAVENDER, width=2))
        )
        fig_trend = apply_pastel_theme(fig_trend, "Monthly Waste Trend")
        st.plotly_chart(fig_trend, use_container_width=True)

    with col4:
        risk_counts = inventory_df['Waste Risk'].value_counts().reset_index()
        risk_counts.columns = ['Risk', 'Count']
        fig_risk = px.bar(
            risk_counts, x='Risk', y='Count',
            color='Risk',
            color_discrete_map={
                'High'  : PASTEL_CORAL,
                'Medium': PASTEL_PEACH,
                'Low'   : PASTEL_MINT
            }
        )
        fig_risk = apply_pastel_theme(fig_risk, "Items by Waste Risk Level")
        st.plotly_chart(fig_risk, use_container_width=True)

    # ── Recent alerts ─────────────────────────────────────────────────────────
    st.divider()
    st.markdown("<h3 style='color:#7BBF9E;'>⚡ Recent Alerts</h3>", unsafe_allow_html=True)
    alerts = inventory_df[inventory_df['Status'].isin(['Critical', 'Expiring Soon'])].head(5)
    for _, row in alerts.iterrows():
        colour = PASTEL_CORAL if row['Status'] == 'Critical' else PASTEL_PEACH
        st.markdown(
            f"<div style='background:{colour}; border-radius:10px; padding:10px 16px; "
            f"margin-bottom:8px; color:#5A5A7A; font-weight:500;'>"
            f"⚠️ <b>{row['Product Name']}</b> ({row['Category']}) — "
            f"{row['Status']} | Qty: {row['Quantity']} | "
            f"Expires: {row['Expiry Date']}</div>",
            unsafe_allow_html=True
        )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Inventory
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📦 Inventory":
    st.markdown("<h1 style='color:#9B8EC4;'>📦 Inventory Management</h1>", unsafe_allow_html=True)

    # ── Search & column selector ──────────────────────────────────────────────
    s1, s2 = st.columns([2, 1])
    with s1:
        search = st.text_input("🔍 Search products", placeholder="Type product name or ID...")
    with s2:
        cols_to_show = st.multiselect(
            "Columns",
            options=inventory_df.columns.tolist(),
            default=['Item ID','Product Name','Category','Quantity','Status','Waste Risk','Expiry Date']
        )

    display_df = filtered_inv.copy()
    if search:
        mask = (
            display_df['Product Name'].str.contains(search, case=False) |
            display_df['Item ID'].str.contains(search, case=False)
        )
        display_df = display_df[mask]

    # ── Status badges via colour map ──────────────────────────────────────────
    def style_status(val):
        colour_map = {
            'Critical'     : f'background-color:{PASTEL_CORAL}; color:#5A5A7A; border-radius:6px; padding:2px 8px',
            'Expiring Soon': f'background-color:{PASTEL_PEACH}; color:#5A5A7A; border-radius:6px; padding:2px 8px',
            'Low Stock'    : f'background-color:{PASTEL_YELLOW}; color:#5A5A7A; border-radius:6px; padding:2px 8px',
            'Good'         : f'background-color:{PASTEL_MINT};  color:#5A5A7A; border-radius:6px; padding:2px 8px',
        }
        return colour_map.get(val, '')

    styled = display_df[cols_to_show].style.applymap(style_status, subset=['Status'] if 'Status' in cols_to_show else [])
    st.dataframe(styled, use_container_width=True, height=420)

    # ── Summary stats ─────────────────────────────────────────────────────────
    st.divider()
    st.markdown("<h3 style='color:#7BBF9E;'>Category Summary</h3>", unsafe_allow_html=True)
    cat_summary = (
        filtered_inv.groupby('Category')
        .agg(Items=('Item ID','count'), Avg_Qty=('Quantity','mean'), Avg_Days=('Days Until Expiry','mean'))
        .round(1).reset_index()
    )
    st.dataframe(cat_summary, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Waste Alerts
# ══════════════════════════════════════════════════════════════════════════════
elif page == "⚠️ Waste Alerts":
    st.markdown("<h1 style='color:#9B8EC4;'>⚠️ Waste Alerts</h1>", unsafe_allow_html=True)

    tabs = st.tabs(["🔴 Critical", "🟡 Expiring Soon", "📉 Low Stock", "📋 All Waste Data"])

    # ── Critical ──────────────────────────────────────────────────────────────
    with tabs[0]:
        critical_df = inventory_df[inventory_df['Status'] == 'Critical']
        st.markdown(
            f"<div style='background:{PASTEL_CORAL}; border-radius:12px; padding:14px 20px; "
            f"color:#5A5A7A; font-weight:600; margin-bottom:12px;'>"
            f"🚨 {len(critical_df)} items are past expiry date and require immediate action!</div>",
            unsafe_allow_html=True
        )
        if not critical_df.empty:
            st.dataframe(
                critical_df[['Item ID','Product Name','Category','Quantity','Expiry Date','Cost per Unit']],
                use_container_width=True
            )
            total_cost = (critical_df['Quantity'] * critical_df['Cost per Unit']).sum()
            st.markdown(
                f"<div style='background:{PASTEL_PINK}; border-radius:10px; padding:12px 18px; "
                f"color:#5A5A7A; margin-top:8px;'>"
                f"💰 Estimated waste value: <b>\\({total_cost:,.2f}</b></div>",
                unsafe_allow_html=True
            )

    # ── Expiring Soon ─────────────────────────────────────────────────────────
    with tabs[1]:
        exp_df = inventory_df[inventory_df['Status'] == 'Expiring Soon']
        st.markdown(
            f"<div style='background:{PASTEL_PEACH}; border-radius:12px; padding:14px 20px; "
            f"color:#5A5A7A; font-weight:600; margin-bottom:12px;'>"
            f"⚡ {len(exp_df)} items expiring within 3 days — consider discounting or donating.</div>",
            unsafe_allow_html=True
        )
        if not exp_df.empty:
            st.dataframe(
                exp_df[['Item ID','Product Name','Category','Quantity','Days Until Expiry','Cost per Unit']],
                use_container_width=True
            )

    # ── Low Stock ─────────────────────────────────────────────────────────────
    with tabs[2]:
        low_df = inventory_df[inventory_df['Status'] == 'Low Stock']
        st.markdown(
            f"<div style='background:{PASTEL_YELLOW}; border-radius:12px; padding:14px 20px; "
            f"color:#5A5A7A; font-weight:600; margin-bottom:12px;'>"
            f"📉 {len(low_df)} items below reorder point.</div>",
            unsafe_allow_html=True
        )
        if not low_df.empty:
            st.dataframe(
                low_df[['Item ID','Product Name','Category','Quantity','Reorder Point','Supplier']],
                use_container_width=True
            )

    # ── All Waste Data ────────────────────────────────────────────────────────
    with tabs[3]:
        st.markdown("<h3 style='color:#7BBF9E;'>Waste Log</h3>", unsafe_allow_html=True)
        reason_filter = st.selectbox("Filter by Reason", ["All"] + list(waste_df['Reason'].unique()))
        w_df = waste_df if reason_filter == "All" else waste_df[waste_df['Reason'] == reason_filter]
        st.dataframe(w_df, use_container_width=True)

        fig_reason = px.pie(
            w_df, names='Reason', values='Cost',
            color_discrete_sequence=PASTEL_CHART_COLORS,
            hole=0.4
        )
        fig_reason = apply_pastel_theme(fig_reason, "Waste by Reason")
        st.plotly_chart(fig_reason, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Analytics
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📈 Analytics":
    st.markdown("<h1 style='color:#9B8EC4;'>📈 Analytics</h1>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Sales & Revenue", "Waste Analysis", "Inventory Health"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            monthly_rev = sales_df.groupby(sales_df['Date'].dt.month)['Revenue'].sum().reset_index()
            monthly_rev.columns = ['Month', 'Revenue']
            fig_rev = px.bar(
                monthly_rev, x='Month', y='Revenue',
                color_discrete_sequence=[PASTEL_LAVENDER]
            )
            fig_rev = apply_pastel_theme(fig_rev, "Monthly Revenue (\\))")
            st.plotly_chart(fig_rev, use_container_width=True)
        with col2:
            cat_rev = sales_df.groupby('Category')['Revenue'].sum().reset_index()
            fig_cat = px.pie(
                cat_rev, values='Revenue', names='Category',
                color_discrete_sequence=PASTEL_CHART_COLORS,
                hole=0.4
            )
            fig_cat = apply_pastel_theme(fig_cat, "Revenue by Category")
            st.plotly_chart(fig_cat, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            reason_waste = waste_df.groupby('Reason')['Cost'].sum().reset_index()
            fig_reason_bar = px.bar(
                reason_waste, x='Reason', y='Cost',
                color='Reason',
                color_discrete_sequence=PASTEL_CHART_COLORS
            )
            fig_reason_bar = apply_pastel_theme(fig_reason_bar, "Waste Cost by Reason (\\()")
            st.plotly_chart(fig_reason_bar, use_container_width=True)
        with col2:
            prev_waste = waste_df.groupby('Preventable')['Cost'].sum().reset_index()
            prev_waste['Preventable'] = prev_waste['Preventable'].map({True: 'Preventable', False: 'Not Preventable'})
            fig_prev = px.pie(
                prev_waste, values='Cost', names='Preventable',
                color_discrete_sequence=[PASTEL_MINT, PASTEL_CORAL],
                hole=0.4
            )
            fig_prev = apply_pastel_theme(fig_prev, "Preventable vs Non-Preventable Waste")
            st.plotly_chart(fig_prev, use_container_width=True)

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            cat_health = inventory_df.groupby(['Category','Status']).size().reset_index(name='Count')
            fig_health = px.bar(
                cat_health, x='Category', y='Count', color='Status',
                barmode='stack',
                color_discrete_map={
                    'Good'         : PASTEL_MINT,
                    'Low Stock'    : PASTEL_YELLOW,
                    'Expiring Soon': PASTEL_PEACH,
                    'Critical'     : PASTEL_CORAL
                }
            )
            fig_health = apply_pastel_theme(fig_health, "Inventory Health by Category")
            st.plotly_chart(fig_health, use_container_width=True)
        with col2:
            fig_scatter = px.scatter(
                inventory_df, x='Days Until Expiry', y='Quantity',
                color='Category', size='Cost per Unit',
                color_discrete_sequence=PASTEL_CHART_COLORS,
                hover_data=['Product Name']
            )
            fig_scatter = apply_pastel_theme(fig_scatter, "Quantity vs Days Until Expiry")
            st.plotly_chart(fig_scatter, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Predictions
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔮 Predictions":
    st.markdown("<h1 style='color:#9B8EC4;'>🔮 Waste Predictions</h1>", unsafe_allow_html=True)

    st.info("Predictive model using historical sales and waste patterns. Ranges shown as confidence bands.")

    col1, col2 = st.columns(2)

    with col1:
        forecast_days = st.slider("Forecast horizon (days)", 7, 90, 30)
        category_pred = st.selectbox("Category to predict", inventory_df['Category'].unique())

    with col2:
        confidence = st.slider("Confidence interval (%)", 80, 99, 95)

    # Simulate forecast
    future_dates = pd.date_range(start=datetime.now(), periods=forecast_days)
    base_waste   = waste_df[waste_df['Category'] == category_pred]['Quantity'].mean()
    forecast     = [base_waste * random.uniform(0.8, 1.2) for _ in range(forecast_days)]
    ci           = [(confidence / 100) * 0.2 * base_waste] * forecast_days

    fig_pred = go.Figure()
    fig_pred.add_trace(go.Scatter(
        x=list(future_dates) + list(future_dates[::-1]),
        y=[f + c for f, c in zip(forecast, ci)] + [f - c for f, c in zip(forecast[::-1], ci[::-1])],
        fill='toself',
        fillcolor=f'rgba(201,184,232,0.25)',
        line=dict(color='rgba(0,0,0,0)'),
        name=f'{confidence}% CI'
    ))
    fig_pred.add_trace(go.Scatter(
        x=future_dates, y=forecast,
        mode='lines+markers',
        name='Forecast',
        line=dict(color=PASTEL_LAVENDER, width=3),
        marker=dict(size=6, color=PASTEL_PINK)
    ))
    fig_pred = apply_pastel_theme(fig_pred, f"Waste Forecast — {category_pred}")
    st.plotly_chart(fig_pred, use_container_width=True)

    # Recommendations
    st.divider()
    st.markdown("<h3 style='color:#7BBF9E;'>💡 Recommendations</h3>", unsafe_allow_html=True)
    recs = [
        ("Reduce order quantity", PASTEL_MINT,     "Order 15% less to avoid over-stocking"),
        ("Discount ageing stock", PASTEL_YELLOW,   "Apply 20–30% discount on near-expiry items"),
        ("Donate surplus",        PASTEL_SKY,      "Partner with local food banks for surplus donation"),
        ("Adjust reorder point",  PASTEL_LAVENDER, "Recalibrate reorder points based on forecast"),
    ]
    c1, c2 = st.columns(2)
    for i, (title, colour, desc) in enumerate(recs):
        col = c1 if i % 2 == 0 else c2
        col.markdown(
            f"<div style='background:{colour}; border-radius:12px; padding:14px 18px; "
            f"margin-bottom:10px; color:#5A5A7A;'>"
            f"<b>{title}</b><br><span style='font-size:13px;'>{desc}</span></div>",
            unsafe_allow_html=True
        )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Settings
# ══════════════════════════════════════════════════════════════════════════════
elif page == "⚙️ Settings":
    st.markdown("<h1 style='color:#9B8EC4;'>⚙️ Settings</h1>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔔 Notifications", "📦 Inventory Rules", "📤 Export"])

    with tab1:
        st.markdown("<h3 style='color:#7BBF9E;'>Alert Thresholds</h3>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.number_input("Expiry warning (days)",          value=3,   min_value=1, max_value=14)
            st.number_input("Critical expiry threshold (days)", value=0, min_value=0, max_value=7)
        with c2:
            st.number_input("Low stock multiplier",   value=1.2, min_value=1.0, max_value=3.0, step=0.1)
            st.number_input("High waste risk qty",    value=30,  min_value=10,  max_value=200)

        st.divider()
        st.markdown("<h3 style='color:#7BBF9E;'>Notification Channels</h3>", unsafe_allow_html=True)
        st.checkbox("Email alerts",    value=True)
        st.checkbox("SMS alerts",      value=False)
        st.checkbox("Dashboard popup", value=True)
        st.checkbox("Daily digest",    value=True)

    with tab2:
        st.markdown("<h3 style='color:#7BBF9E;'>Reorder Policy</h3>", unsafe_allow_html=True)
        st.selectbox("Reorder strategy", ["Fixed Quantity", "EOQ Model", "Min-Max", "Demand Forecast"])
        st.slider("Safety stock buffer (%)", 5, 50, 20)
        st.slider("Lead time (days)",        1, 30,  7)

    with tab3:
        st.markdown("<h3 style='color:#7BBF9E;'>Export Data</h3>", unsafe_allow_html=True)
        ec1, ec2, ec3 = st.columns(3)
        with ec1:
            csv = inventory_df.to_csv(index=False)
            st.download_button(
                "📥 Inventory CSV", data=csv,
                file_name="inventory.csv", mime="text/csv"
            )
        with ec2:
            wcsv = waste_df.to_csv(index=False)
            st.download_button(
                "📥 Waste Data CSV", data=wcsv,
                file_name="waste_data.csv", mime="text/csv"
            )
        with ec3:
            scsv = sales_df.to_csv(index=False)
            st.download_button(
                "📥 Sales Data CSV", data=scsv,
                file_name="sales_data.csv", mime="text/csv"
            )
