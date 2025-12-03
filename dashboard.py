import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

# -------------------- Page Config --------------------
st.set_page_config(
    page_title="RBI Monetary Policy Dashboard",
    page_icon="💰",
    layout="wide"
)
st.title("RBI Monetary Policy Dashboard 📊")

# -------------------- Custom CSS for Sky Blue & White Theme --------------------
st.markdown("""
<style>
/* ---------------- Tabs ---------------- */
/* Tab headers rounded with border */
button[role="tab"] {
    border-radius: 25px !important;
    background-color: #ffffff !important; /* keep inactive tab white */
    color: #000000 !important;            
    padding: 10px 20px !important;
    margin-right: 8px !important;
    border: 2px solid #81d4fa !important; /* light sky blue border */
    font-weight: 500;
    transition: all 0.3s ease;
}

/* Active tab header remains default (don't color it) */
button[role="tab"][aria-selected="true"] {
    font-weight: bold;
    border: 2px solid #0288d1 !important; /* dark blue border */
}

/* ---------------- App background & text ---------------- */
.stApp {
    background-color: #e0f7fa;  /* sky blue background */
    color: #000000 !important;
}

/* Make all text black */
.stApp, .stApp * {
    color: #000000 !important;
}

/* ---------------- KPI / Metric cards ---------------- */
.stMetric {
    background-color: #ffffff;  /* white cards */
    border-radius: 10px;
    padding: 10px;
    box-shadow: 3px 3px 10px rgba(0,0,0,0.1);
    color: #000000 !important;
}

/* ---------------- Sliders ---------------- */
div.stSlider {
    background-color: #ffffff !important; /* white slider container */
    padding: 8px 12px;
    border-radius: 12px;
    margin-bottom: 10px;
}

/* Slider track light sky blue */
div.stSlider > div[data-baseweb="slider"] > div {
    background: #81d4fa !important;
}

/* Slider thumb dark blue */
div.stSlider > div[data-baseweb="slider"] > div > div[role="slider"] {
    background: #0288d1 !important;
    border: 2px solid #0277bd !important;
}

/* Slider labels / values black */
.stSlider label, 
.stSlider div[data-testid="stMarkdownContainer"],
div.stSlider span {
    color: #000000 !important;
    font-weight: bold;
}

/* ---------------- Date Inputs ---------------- */
div[data-testid="stDateInput"] {
    background-color: #ffffff !important;
    padding: 5px 10px;
    border-radius: 10px;
    border: 2px solid #81d4fa !important; /* light sky blue border */
    color: #000000 !important;
    margin-bottom: 10px;
}

div[data-testid="stDateInput"] label {
    color: #000000 !important;
    font-weight: bold;
}

div[data-testid="stDateInput"] input {
    color: #000000 !important;
    background-color: #ffffff !important;
    border-radius: 6px;
}

/* ---------------- Plotly Charts ---------------- */
.js-plotly-plot .xtick text, 
.js-plotly-plot .ytick text, 
.js-plotly-plot .gtitle text, 
.js-plotly-plot .legend text {
    fill: #000000 !important;
}

.js-plotly-plot .plotly {
    background-color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar Styling ----------------
st.markdown("""
<style>
/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #0288d1;
    color: white;
}

/* Sidebar text */
[data-testid="stSidebar"] label, 
[data-testid="stSidebar"] .css-1d391kg {
    color: white !important;
    font-weight: bold;
}

/* Sidebar widgets (selectbox, slider, number input) */
[data-testid="stSidebar"] .stSelectbox, 
[data-testid="stSidebar"] .stSlider, 
[data-testid="stSidebar"] .stNumberInput {
    background-color: #0288d1;
    border-radius: 8px;
    color: white;
}

/* Placeholder text */
[data-testid="stSidebar"] input::placeholder {
    color: #e0f7fa;
}
</style>
""", unsafe_allow_html=True)

# -------------------- Sidebar Sliders --------------------
st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start Date", datetime.date(2023, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.date(2023, 12, 31))

# Tab 1: Policy Rates
repo_rate_range = st.sidebar.slider("Repo Rate Range (%)", 0.0, 15.0, (5.0, 8.0), 0.25)
reverse_repo_range = st.sidebar.slider("Reverse Repo Rate Range (%)", 0.0, 15.0, (5.0, 8.0), 0.25)

# Tab 2: Inflation
cpi_range = st.sidebar.slider("CPI Range (%)", 0.0, 15.0, (0.0, 10.0), 0.1)
wpi_range = st.sidebar.slider("WPI Range (%)", 0.0, 15.0, (0.0, 10.0), 0.1)
food_inflation_range = st.sidebar.slider("Food Inflation (%)", 0.0, 15.0, (0.0, 10.0), 0.1)

# Tab 3: Liquidity & Credit
credit_growth_range = st.sidebar.slider("Credit Growth (%)", 0.0, 20.0, (0.0, 10.0), 0.1)
liquidity_range = st.sidebar.slider("Liquidity (₹ Cr in Lakh)", 0, 1000000, (0, 1000000), 10000)

# Tab 4: Forex & Reserves
forex_range = st.sidebar.slider("Forex Reserves (USD bn)", 0, 1000, (0, 1000), 5)
usd_inr_range = st.sidebar.slider("USD/INR Rate", 50.0, 100.0, (70.0, 80.0), 0.1)

# Tab 5: Economic Indicators
gdp_range = st.sidebar.slider("GDP Growth (%)", 0.0, 15.0, (0.0, 10.0), 0.1)
iip_range = st.sidebar.slider("IIP (%)", -10.0, 20.0, (0.0, 10.0), 0.1)

# -------------------- Tabs --------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Policy Rate Overview", 
    "Inflation Dashboard", 
    "Liquidity & Credit", 
    "Forex & RBI Reserves", 
    "Economic Indicators", 
    "RBI Announcements"
])

# -------------------- Tab 1: Policy Rate Overview --------------------
with tab1:

    st.header("Policy Rates Overview")

    # Sample Data
    df_rates = pd.DataFrame({
        "Date": pd.date_range(start="2023-01-01", periods=12, freq="M"),
        "Repo Rate": [6.0, 6.25, 6.25, 6.5, 6.5, 6.75, 6.75, 7.0, 7.0, 7.25, 7.25, 7.5],
        "Reverse Repo Rate": [5.5, 5.75, 5.75, 6.0, 6.0, 6.25, 6.25, 6.5, 6.5, 6.75, 6.75, 7.0],
        "CRR": [4.0]*12,
        "SLR": [18.0]*12
    })

    # Filtering
    df_filtered = df_rates[
        (df_rates["Date"].dt.date >= start_date) &
        (df_rates["Date"].dt.date <= end_date) &
        (df_rates["Repo Rate"].between(repo_rate_range[0], repo_rate_range[1])) &
        (df_rates["Reverse Repo Rate"].between(reverse_repo_range[0], reverse_repo_range[1]))
    ]

    # Rolling averages
    df_filtered['Repo 3M Avg'] = df_filtered['Repo Rate'].rolling(3).mean()
    df_filtered['Reverse Repo 3M Avg'] = df_filtered['Reverse Repo Rate'].rolling(3).mean()

    # ---------------------------
    # MAIN CHART (Clean + Minimal)
    # ---------------------------
    fig = px.line(
        df_filtered,
        x='Date',
        y=['Repo Rate', 'Reverse Repo Rate', 'Repo 3M Avg', 'Reverse Repo 3M Avg'],
        markers=True,
        color_discrete_sequence=['#0277bd', '#00b0ff', '#4dd0e1', '#81d4fa'],
        labels={'value': 'Rate (%)', 'variable': 'Rate Type'}
    )

    fig.update_layout(
        title='Repo & Reverse Repo Rate (with 3M Avg)',
        paper_bgcolor='white',
        plot_bgcolor='white',
        title_font=dict(size=18, color='#000'),
        xaxis=dict(title='Date', gridcolor='lightgrey'),
        yaxis=dict(title='Rate (%)', gridcolor='lightgrey'),
        legend=dict(title='Rate Type')
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------------------------
    # KPI CARDS
    # ---------------------------
    latest = df_filtered.iloc[-1]
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Repo Rate (%)", latest["Repo Rate"])
    col2.metric("Reverse Repo Rate (%)", latest["Reverse Repo Rate"])
    col3.metric("CRR (%)", latest["CRR"])
    col4.metric("SLR (%)", latest["SLR"])

    # ---------------------------
    # SMALL CHARTS
    # ---------------------------
    colA, colB = st.columns(2)

    # Repo + Reverse Repo small line chart
    fig1 = px.line(
        df_filtered,
        x="Date",
        y=["Repo Rate", "Reverse Repo Rate"],
        markers=True,
        color_discrete_sequence=["#0277bd", "#00b0ff"],
        labels={"value": "Rate (%)"}
    )
    fig1.update_layout(
        title="Repo vs Reverse Repo Trend",
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(gridcolor="lightgrey"),
        yaxis=dict(gridcolor="lightgrey")
    )
    colA.plotly_chart(fig1, use_container_width=True)

    # CRR/SLR bar chart
    fig2 = px.bar(
        df_filtered,
        x="Date",
        y=["CRR", "SLR"],
        barmode="group",
        color_discrete_sequence=["#81d4fa", "#29b6f6"],
        labels={"value": "%"}
    )
    fig2.update_layout(
        title="CRR & SLR Trend",
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(gridcolor="lightgrey"),
        yaxis=dict(gridcolor="lightgrey")
    )
    colB.plotly_chart(fig2, use_container_width=True)
# ---------------------------

# -------------------- Tab 2: Inflation Dashboard --------------------
with tab2:
    st.header("Inflation Dashboard")

    # ------------------------
    # SAMPLE DATA
    # ------------------------
    df_inflation = pd.DataFrame({
        "Date": pd.date_range(start="2023-01-01", periods=12, freq="M"),
        "CPI": [5.0,5.1,5.2,5.0,5.3,5.4,5.5,5.2,5.1,5.0,4.9,4.8],
        "WPI": [3.5,3.6,3.7,3.6,3.5,3.4,3.5,3.6,3.7,3.6,3.5,3.4],
        "Food Inflation": [4.0,4.2,4.1,4.3,4.0,4.1,4.2,4.0,3.9,4.0,4.1,4.2],
        "Fuel": [3.1, 3.0, 2.9, 2.8, 3.0, 3.2, 3.1, 3.0, 3.2, 3.1, 3.0, 2.9],
        "Housing": [4.6,4.7,4.6,4.8,4.7,4.6,4.7,4.6,4.8,4.7,4.6,4.5],
        "Clothing": [3.5,3.6,3.4,3.5,3.6,3.7,3.5,3.4,3.5,3.6,3.7,3.5],
    })

    # ------------------------
    # FILTER DATA
    # ------------------------
    df_filtered = df_inflation[
        (df_inflation["Date"].dt.date >= start_date) &
        (df_inflation["Date"].dt.date <= end_date) &
        (df_inflation["CPI"] >= cpi_range[0]) & (df_inflation["CPI"] <= cpi_range[1]) &
        (df_inflation["WPI"] >= wpi_range[0]) & (df_inflation["WPI"] <= wpi_range[1]) &
        (df_inflation["Food Inflation"] >= food_inflation_range[0]) &
        (df_inflation["Food Inflation"] <= food_inflation_range[1])
    ]

    # ---------------------------------------------------
    # KPI CARDS
    # ---------------------------------------------------
    latest = df_filtered.iloc[-1]
    col1, col2, col3 = st.columns(3)

    col1.metric("CPI (%)", latest["CPI"], delta=f"{latest['CPI'] - df_filtered['CPI'].iloc[-2]:+.1f}")
    col2.metric("WPI (%)", latest["WPI"], delta=f"{latest['WPI'] - df_filtered['WPI'].iloc[-2]:+.1f}")
    col3.metric("Food Inflation (%)", latest["Food Inflation"], delta=f"{latest['Food Inflation'] - df_filtered['Food Inflation'].iloc[-2]:+.1f}")

    # ---------------------------------------------------
    # CPI vs WPI Line Chart
    # ---------------------------------------------------
    col1_chart, col2_chart = st.columns(2)

    fig1 = px.line(
        df_filtered,
        x="Date",
        y=["CPI", "WPI"],
        markers=True,
        color_discrete_sequence=["#0288d1", "#81d4fa"],
        labels={"value": "Inflation (%)", "variable": "Category"}
    )
    fig1.update_layout(plot_bgcolor="white", paper_bgcolor="white", title="CPI vs WPI")
    col1_chart.plotly_chart(fig1, use_container_width=True)

    # ---------------------------------------------------
    # FOOD INFLATION BAR CHART
    # ---------------------------------------------------
    fig2 = px.bar(
        df_filtered,
        x="Date",
        y="Food Inflation",
        color="Food Inflation",
        color_continuous_scale=px.colors.sequential.Blues
    )
    fig2.update_layout(plot_bgcolor="white", paper_bgcolor="white", title="Food Inflation Trend")
    col2_chart.plotly_chart(fig2, use_container_width=True)

    # ---------------------------------------------------
    # CPI CATEGORY BREAKDOWN
    # ---------------------------------------------------
    st.subheader("CPI Category Breakdown")
    fig3 = px.bar(
        df_filtered,
        x="Date",
        y=["Food Inflation", "Fuel", "Housing", "Clothing"],
        barmode="group",
        color_discrete_sequence=["#0288d1", "#4dd0e1", "#81d4fa", "#b2ebf2"]
    )
    fig3.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig3, use_container_width=True)

    # ---------------------------------------------------
    # CPI vs REPO RATE (Dual Axis)
    # ---------------------------------------------------
    st.subheader("CPI vs Repo Rate Comparison")

    df_filtered["Repo Rate"] = [6.5]*len(df_filtered)  # sample

    fig4 = go.Figure()

    fig4.add_trace(go.Scatter(
        x=df_filtered["Date"], y=df_filtered["CPI"],
        mode="lines+markers", name="CPI",
        line=dict(color="#0288d1")
    ))

    fig4.add_trace(go.Scatter(
        x=df_filtered["Date"], y=df_filtered["Repo Rate"],
        mode="lines+markers", name="Repo Rate",
        line=dict(color="#ff7043"), yaxis="y2"
    ))

    fig4.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(title="CPI (%)"),
        yaxis2=dict(title="Repo Rate (%)", overlaying="y", side="right"),
        title="CPI vs Repo Rate"
    )
    st.plotly_chart(fig4, use_container_width=True)

    # ---------------------------------------------------
    # MONTH-ON-MONTH CHANGE
    # ---------------------------------------------------
    st.subheader("Month-on-Month Inflation Change")

    df_filtered["MoM CPI Change"] = df_filtered["CPI"].diff()

    fig5 = px.bar(
        df_filtered,
        x="Date",
        y="MoM CPI Change",
        color="MoM CPI Change",
        color_continuous_scale=px.colors.sequential.Blues
    )
    fig5.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig5, use_container_width=True)

    # ---------------------------------------------------
    # HEATMAP (CATEGORY WISE)
    # ---------------------------------------------------
    st.subheader("Inflation Category Heatmap")

    heatmap_data = df_filtered[["Food Inflation", "Fuel", "Housing", "Clothing"]]
    heatmap_data.index = df_filtered["Date"].dt.strftime("%b")

    fig6 = px.imshow(
        heatmap_data.T,
        color_continuous_scale="Blues",
        aspect="auto"
    )
    fig6.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig6, use_container_width=True)

    # ---------------------------------------------------
    # AUTO SUMMARY
    # ---------------------------------------------------
    st.subheader("Inflation Summary")

    st.markdown(f"""
    **Inflation Insight:**  
    - CPI is currently **{latest['CPI']}%**.  
    - WPI stands at **{latest['WPI']}%**.  
    - Food inflation is **{latest['Food Inflation']}%**.  
    - Housing & Fuel inflation remain stable.  
    - Recent months show {"rising" if latest['CPI'] > df_filtered['CPI'].iloc[-2] else "falling"} inflation trends.
    """)

# -------------------- Tab 3: Liquidity & Credit --------------------
with tab3:

    st.header("Liquidity & Credit Growth Dashboard")

    # ---------------------------------------------------------
    # SAMPLE DATA (Matches theme + clean structure)
    # ---------------------------------------------------------
    df_liquidity = pd.DataFrame({
        "Date": pd.date_range(start="2023-01-01", periods=12, freq="M"),
        "Liquidity (₹ Cr)": [500000,520000,510000,530000,540000,550000,560000,570000,580000,590000,600000,610000],
        "Credit Growth (%)": [7.0,7.2,7.1,7.3,7.5,7.6,7.8,7.7,7.9,8.0,8.2,8.3],
        "Call Rate (%)": [5.9,6.0,6.1,6.0,6.2,6.3,6.2,6.1,6.4,6.5,6.3,6.4],
        "M1": [45,46,46.3,46.8,47,47.5,48,48.3,48.7,49,49.3,50],
        "M3": [150,151,152,153,153.5,154,155,156,157,158,159,160],
        "Yield 3M": [6.1,6.2,6.2,6.3,6.3,6.4,6.4,6.5,6.5,6.6,6.6,6.7],
        "Yield 1Y": [6.4,6.4,6.5,6.5,6.6,6.6,6.7,6.7,6.8,6.8,6.9,7.0],
        "Yield 5Y": [7.0,7.0,7.1,7.1,7.2,7.3,7.3,7.4,7.5,7.5,7.6,7.7],
        "Yield 10Y": [7.3,7.3,7.4,7.5,7.5,7.6,7.7,7.7,7.8,7.9,7.9,8.0]
    })

    # ---------------------------------------------------------
    # FILTER
    # ---------------------------------------------------------
    df_filtered = df_liquidity[
        (df_liquidity["Date"].dt.date >= start_date) &
        (df_liquidity["Date"].dt.date <= end_date) &
        (df_liquidity["Credit Growth (%)"].between(credit_growth_range[0], credit_growth_range[1])) &
        (df_liquidity["Liquidity (₹ Cr)"].between(liquidity_range[0], liquidity_range[1]))
    ]

    latest = df_filtered.iloc[-1]

    # ---------------------------------------------------------
    # KPI CARDS
    # ---------------------------------------------------------
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Liquidity (₹ Cr)", latest["Liquidity (₹ Cr)"])
    col2.metric("Credit Growth (%)", latest["Credit Growth (%)"])
    col3.metric("Call Rate (%)", latest["Call Rate (%)"])
    col4.metric("M3 (₹ Lakh Cr)", latest["M3"])

    # ---------------------------------------------------------
    # MAIN TREND CHART (Liquidity + Credit)
    # ---------------------------------------------------------
    fig1 = px.line(
        df_filtered, x="Date",
        y=["Liquidity (₹ Cr)", "Credit Growth (%)"],
        markers=True,
        color_discrete_sequence=["#0288d1", "#03a9f4"],
        labels={"value": "Values", "variable": "Indicator"}
    )
    fig1.update_layout(title="Liquidity vs Credit Growth Trend",
                       paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig1, use_container_width=True)

    # ---------------------------------------------------------
    # MONEY SUPPLY TRENDS (M1 & M3)
    # ---------------------------------------------------------
    st.subheader("Money Supply Trends (M1 & M3)")
    fig2 = px.line(
        df_filtered, x="Date", y=["M1", "M3"],
        markers=True, color_discrete_sequence=["#4dd0e1", "#81d4fa"]
    )
    fig2.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig2, use_container_width=True)

    # ---------------------------------------------------------
    # CALL RATE TREND
    # ---------------------------------------------------------
    st.subheader("Call Money Rate Trend")
    fig3 = px.line(
        df_filtered, x="Date", y="Call Rate (%)", markers=True,
        color_discrete_sequence=["#01579b"]
    )
    fig3.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig3, use_container_width=True)

    # ---------------------------------------------------------
    # YIELD CURVE TREND (3M, 1Y, 5Y, 10Y)
    # ---------------------------------------------------------
    st.subheader("Government Securities Yield Curve Trend")

    fig4 = px.line(
        df_filtered, x="Date",
        y=["Yield 3M", "Yield 1Y", "Yield 5Y", "Yield 10Y"],
        markers=True,
        color_discrete_sequence=["#0277bd", "#00b0ff", "#4dd0e1", "#81d4fa"]
    )
    fig4.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig4, use_container_width=True)

    # ---------------------------------------------------------
    # SUMMARY TABLE
    # ---------------------------------------------------------
    st.subheader("Summary Table")

    summary_df = pd.DataFrame({
        "Metric": [
            "Latest Liquidity (₹ Cr)",
            "Credit Growth (%)",
            "Call Rate (%)",
            "M1 Supply",
            "M3 Supply",
            "10Y G-Sec Yield"
        ],
        "Value": [
            latest["Liquidity (₹ Cr)"],
            latest["Credit Growth (%)"],
            latest["Call Rate (%)"],
            latest["M1"],
            latest["M3"],
            latest["Yield 10Y"]
        ]
    })

    st.dataframe(summary_df, hide_index=True)


# -------------------- Tab 4: Forex & RBI Reserves --------------------
with tab4:
    st.header("Forex Reserves & USD/INR")

    # Data
    df_forex = pd.DataFrame({
        "Date": pd.date_range(start="2023-01-01", periods=12, freq="M"),
        "Forex Reserves (USD bn)": [600,605,610,615,620,625,630,635,640,645,650,655],
        "USD/INR": [75.0,75.2,75.5,75.3,75.1,74.9,75.0,75.2,75.4,75.3,75.5,75.6]
    })

    # Filter
    df_filtered = df_forex[
        (df_forex["Date"].dt.date >= start_date) &
        (df_forex["Date"].dt.date <= end_date) &
        (df_forex["Forex Reserves (USD bn)"] >= forex_range[0]) &
        (df_forex["Forex Reserves (USD bn)"] <= forex_range[1]) &
        (df_forex["USD/INR"] >= usd_inr_range[0]) &
        (df_forex["USD/INR"] <= usd_inr_range[1])
    ]

    # Latest Metrics
    latest = df_filtered.iloc[-1]
    col1, col2 = st.columns(2)
    col1.metric("Forex Reserves (USD bn)", latest["Forex Reserves (USD bn)"])
    col2.metric("USD/INR Rate", latest["USD/INR"])

    # --- Main Line Chart (Theme Matched Colors)
    fig = px.line(
        df_filtered,
        x="Date",
        y=["Forex Reserves (USD bn)", "USD/INR"],
        markers=True,
        color_discrete_sequence=["#0277bd", "#00b0ff"]  # theme colors
    )
    fig.update_layout(
        title="Forex Reserves & USD/INR Trend",
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend_title_text=""
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Scatter Plot (Correlation) WITHOUT statsmodels
    fig_scatter = px.scatter(
        df_filtered,
        x="Forex Reserves (USD bn)",
        y="USD/INR",
        trendline=None,  # removed OLS to avoid statsmodels requirement
        color_discrete_sequence=["#0277bd"],
        title="Forex Reserves vs USD/INR"
    )
    fig_scatter.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # --- Summary Table
    st.subheader("Summary Table")
    summary = pd.DataFrame({
        "Metric": ["Avg Forex Reserves", "Min Forex", "Max Forex", "Avg USD/INR", "Min USD/INR", "Max USD/INR"],
        "Value": [
            round(df_filtered["Forex Reserves (USD bn)"].mean(), 2),
            df_filtered["Forex Reserves (USD bn)"].min(),
            df_filtered["Forex Reserves (USD bn)"].max(),
            round(df_filtered["USD/INR"].mean(), 2),
            df_filtered["USD/INR"].min(),
            df_filtered["USD/INR"].max()
        ]
    })
    st.dataframe(summary, use_container_width=True)


# -------------------- Tab 5: Economic Indicators --------------------
with tab5:
    st.header("📊 Economic Indicators")

    # Sample Economic Data
    df_econ = pd.DataFrame({
        "Date": pd.date_range(start="2023-01-01", periods=12, freq="M"),
        "GDP Growth (%)": [6.0, 6.1, 6.2, 6.0, 5.9, 6.0, 6.1, 6.2, 6.3, 6.1, 6.0, 5.9],
        "IIP (%)": [4.0, 4.1, 4.2, 4.0, 3.9, 4.0, 4.1, 4.2, 4.3, 4.1, 4.0, 3.9]
    })

    # Apply Filters
    df_filtered = df_econ[
        (df_econ["Date"].dt.date >= start_date) &
        (df_econ["Date"].dt.date <= end_date) &
        (df_econ["GDP Growth (%)"] >= gdp_range[0]) &
        (df_econ["GDP Growth (%)"] <= gdp_range[1]) &
        (df_econ["IIP (%)"] >= iip_range[0]) &
        (df_econ["IIP (%)"] <= iip_range[1])
    ]

    # Rolling Averages (for smooth trend)
    df_filtered["GDP 3M Avg"] = df_filtered["GDP Growth (%)"].rolling(3).mean()
    df_filtered["IIP 3M Avg"] = df_filtered["IIP (%)"].rolling(3).mean()

    # YoY Change
    gdp_yoy = df_filtered["GDP Growth (%)"].pct_change().iloc[-1] * 100
    iip_yoy = df_filtered["IIP (%)"].pct_change().iloc[-1] * 100

    # Latest Values
    latest = df_filtered.iloc[-1]

    # KPI Section
    col1, col2, col3 = st.columns(3)
    col1.metric("GDP Growth (%)", latest["GDP Growth (%)"], f"{gdp_yoy:.2f}% YoY")
    col2.metric("IIP (%)", latest["IIP (%)"], f"{iip_yoy:.2f}% YoY")

    # Economy Trend Logic
    trend = "Expanding 📈" if latest["GDP Growth (%)"] > df_filtered["GDP Growth (%)"].mean() else "Cooling 📉"
    col3.metric("Economic Trend", trend)

    # Line Chart
    fig = px.line(
        df_filtered,
        x="Date",
        y=["GDP Growth (%)", "IIP (%)", "GDP 3M Avg", "IIP 3M Avg"],
        markers=True,
        color_discrete_sequence=["#0288d1", "#03a9f4", "#81d4fa", "#b3e5fc"],
        labels={"value": "Percentage (%)", "variable": "Indicator"},
        title="GDP Growth vs IIP (with 3M Rolling Avg)"
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend_title="Indicators"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Summary Table
    st.markdown("### 📘 Summary Table")
    st.dataframe(
        df_filtered.style.format({
            "GDP Growth (%)": "{:.2f}",
            "IIP (%)": "{:.2f}",
            "GDP 3M Avg": "{:.2f}",
            "IIP 3M Avg": "{:.2f}"
        })
    )


# -------------------- Tab 6: RBI Announcements --------------------

with tab6:
    st.header("RBI Announcements & Policy Updates")

    # Sample Data (Enhanced with tags)
    df_announcements = pd.DataFrame({
        "Date": pd.date_range(start="2023-01-01", periods=8, freq="45D"),
        "Category": [
            "Policy Rate", "Liquidity", "Regulatory", "Policy Rate",
            "Liquidity", "Banking", "Regulatory", "Policy Rate"
        ],
        "Announcement": [
            "Repo Rate increased by 25 bps",
            "Liquidity injection of ₹50,000 Cr",
            "Guidelines revised for NBFCs",
            "Repo Rate unchanged",
            "CRR reduced by 50 bps",
            "SLR increased by 50 bps",
            "KYC rules simplified for small accounts",
            "Reverse Repo Rate unchanged"
        ],
        "Impact": [
            "Increase", "Positive", "Neutral", "Neutral",
            "Decrease", "Increase", "Neutral", "Neutral"
        ]
    })

    # Filtering by date
    df_filtered = df_announcements[
        (df_announcements["Date"].dt.date >= start_date) &
        (df_announcements["Date"].dt.date <= end_date)
    ]

    # Apply CSS to make selectbox sky blue
    st.markdown("""
        <style>
        div[data-baseweb="select"] > div {
            background-color: #81d4fa !important;
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Dropdown filter for category with unique key
    selected_category = st.selectbox(
        "Filter by Announcement Category:",
        ["All", "Policy Rate", "Liquidity", "Regulatory", "Banking"],
        key="tab6_category_select"
    )

    if selected_category != "All":
        df_filtered = df_filtered[df_filtered["Category"] == selected_category]

    # Summary KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Announcements", len(df_filtered))
    col2.metric("Policy Rate Updates", len(df_filtered[df_filtered["Category"] == "Policy Rate"]))
    col3.metric("Liquidity Measures", len(df_filtered[df_filtered["Category"] == "Liquidity"]))

    st.markdown("---")

    # Create colored announcement feed
    st.subheader("📢 RBI Policy Feed")

    for _, row in df_filtered.iterrows():
        color = "#0288d1" if row["Impact"] == "Increase" else (
            "#4dd0e1" if row["Impact"] == "Decrease" else "#81d4fa"
        )
        st.markdown(
            f"""
            <div style="
                background-color:{color};
                padding:12px;
                border-radius:10px;
                margin-bottom:10px;
                color:black;
                border:1px solid #b3e5fc;">
                <b>{row['Date'].strftime('%d %b %Y')}</b><br>
                <b>Category:</b> {row['Category']}<br>
                <b>Announcement:</b> {row['Announcement']}<br>
                <b>Impact:</b> {row['Impact']}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Final Summary Table
    st.subheader("Summary Table")
    st.dataframe(df_filtered.style.background_gradient(cmap="Blues"))

# Apply CSS to style the sidebar
st.markdown("""
    <style>
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #81d4fa;
        color: white;
    }

    /* Sidebar header */
    [data-testid="stSidebar"] .css-1d391kg {
        color: white;
        font-weight: bold;
    }

    /* Sidebar widgets */
    [data-testid="stSidebar"] .stSelectbox, 
    [data-testid="stSidebar"] .stSlider, 
    [data-testid="stSidebar"] .stNumberInput {
        background-color: #81d4fa;
        border-radius: 8px;
        color: black;
    }

    /* Sidebar text inside widgets */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        color: black;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)
