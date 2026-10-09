import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import io

# Page configuration
st.set_page_config(
    page_title="Auto DataDash - Analytics Studio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 0.25rem;
    }
    .sub-header {
        color: #64748B;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Sample Datasets Generator
@st.cache_data
def load_sample_dataset(name: str) -> pd.DataFrame:
    if name == "Global E-Commerce Sales":
        np.random.seed(42)
        categories = ["Electronics", "Fashion", "Home & Kitchen", "Books", "Beauty"]
        regions = ["North America", "Europe", "Asia-Pacific", "Latin America"]
        dates = pd.date_range(start="2024-01-01", periods=100, freq="D")
        data = {
            "TransactionID": [f"TXN-{1000 + i}" for i in range(100)],
            "Date": dates,
            "Category": np.random.choice(categories, 100),
            "Region": np.random.choice(regions, 100),
            "UnitsSold": np.random.randint(1, 20, 100),
            "UnitPrice": np.random.uniform(15.0, 450.0, 100).round(2),
            "DiscountPct": np.random.choice([0.0, 0.05, 0.1, 0.15, 0.2], 100),
            "CustomerRating": np.random.uniform(3.0, 5.0, 100).round(1),
        }
        df = pd.DataFrame(data)
        df["Revenue"] = (df["UnitsSold"] * df["UnitPrice"] * (1 - df["DiscountPct"])).round(2)
        return df

    elif name == "Tech Stock Performance":
        np.random.seed(101)
        tickers = ["NVDA", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "ORCL"]
        sectors = ["Semiconductors", "Consumer Tech", "Software", "Internet", "E-Commerce", "Social Media", "Automotive", "Cloud"]
        data = {
            "Ticker": tickers,
            "Sector": sectors,
            "PriceUSD": [128.5, 225.4, 445.8, 182.2, 195.6, 502.1, 214.3, 138.9],
            "DailyChangePct": [4.2, 1.1, 1.8, 2.3, 1.5, 3.1, -2.4, 0.8],
            "MarketCapBillion": [3150, 3420, 3310, 2280, 2040, 1280, 680, 385],
            "PERatio": [48.5, 33.2, 36.4, 25.1, 41.0, 28.3, 62.0, 31.4],
            "DividendYieldPct": [0.03, 0.45, 0.68, 0.44, 0.0, 0.0, 0.0, 1.15],
            "Beta": [1.68, 1.12, 0.98, 1.05, 1.28, 1.34, 2.05, 0.92]
        }
        return pd.DataFrame(data)

    elif name == "City Climate & Environmental":
        cities = ["Tokyo", "London", "New York", "Sydney", "São Paulo", "Singapore", "Cairo", "Stockholm", "Vancouver", "Dubai"]
        countries = ["Japan", "UK", "USA", "Australia", "Brazil", "Singapore", "Egypt", "Sweden", "Canada", "UAE"]
        data = {
            "City": cities,
            "Country": countries,
            "AvgTempC": [16.2, 11.5, 13.1, 18.8, 20.4, 27.8, 22.1, 7.9, 11.0, 28.5],
            "RainfallMM": [1528, 615, 1260, 1213, 1441, 2340, 24, 539, 1460, 68],
            "SunshineHours": [1876, 1633, 2680, 2592, 2003, 2022, 3541, 1821, 1938, 3568],
            "HumidityPct": [65, 78, 63, 64, 76, 83, 52, 74, 72, 58],
            "AirQualityScore": [42, 48, 55, 28, 68, 35, 94, 18, 22, 88],
            "CarbonEmissionsMt": [62.4, 31.2, 54.8, 38.1, 49.3, 51.0, 44.5, 14.2, 19.8, 72.1]
        }
        return pd.DataFrame(data)

    else:
        # HR Workforce
        depts = ["Engineering", "Product", "Sales", "Marketing", "Customer Support", "Finance", "Human Resources", "Design"]
        data = {
            "Department": depts,
            "Headcount": [240, 65, 180, 85, 150, 45, 35, 40],
            "AvgSalaryUSD": [145000, 138000, 112000, 98000, 68000, 125000, 88000, 118000],
            "RemotePct": [78, 82, 65, 75, 90, 60, 70, 85],
            "AvgTenureYears": [3.8, 4.2, 2.5, 3.1, 2.1, 5.4, 4.6, 3.5],
            "EngagementScore": [84, 88, 81, 83, 79, 86, 89, 87],
            "TurnoverRatePct": [8.5, 6.2, 16.4, 11.2, 19.5, 5.1, 7.0, 9.1]
        }
        return pd.DataFrame(data)

# Header
st.markdown('<div class="main-header">Auto DataDash</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Interactive Data Analytics Studio and Automated Dashboard Generator</div>', unsafe_allow_html=True)

# Sidebar - Dataset Selection & Upload
st.sidebar.header("📁 Data Source")
source_option = st.sidebar.radio("Select Input Method:", ["Use Preloaded Sample Dataset", "Upload Custom Spreadsheet"])

df = None
dataset_title = "Dataset"

if source_option == "Use Preloaded Sample Dataset":
    dataset_name = st.sidebar.selectbox(
        "Choose Dataset:",
        ["Global E-Commerce Sales", "Tech Stock Performance", "City Climate & Environmental", "HR Workforce Analytics"]
    )
    df = load_sample_dataset(dataset_name)
    dataset_title = dataset_name
else:
    uploaded_file = st.sidebar.file_uploader(
        "Upload file (Excel, CSV, TSV, JSON)",
        type=["xlsx", "xls", "csv", "tsv", "json"]
    )
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".tsv"):
                df = pd.read_csv(uploaded_file, sep="\t")
            elif uploaded_file.name.endswith((".xlsx", ".xls")):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith(".json"):
                df = pd.read_json(uploaded_file)
            dataset_title = uploaded_file.name
            st.sidebar.success(f"Loaded: {uploaded_file.name}")
        except Exception as e:
            st.sidebar.error(f"Error reading file: {e}")
    else:
        st.info("👈 Upload an Excel or CSV file in the sidebar, or select a preloaded sample dataset.")
        df = load_sample_dataset("Global E-Commerce Sales")
        dataset_title = "Global E-Commerce Sales (Default Demo)"

if df is not None and not df.empty:
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    # Tabs for structured navigation
    tab_overview, tab_charts, tab_explorer, tab_cleaner = st.tabs([
        "📈 Executive Dashboard & KPIs",
        "🎨 Custom Visualizations",
        "🔍 Data Table Explorer",
        "🧹 Quality & Cleaning Tools"
    ])

    # TAB 1: EXECUTIVE DASHBOARD & KPIS
    with tab_overview:
        st.subheader(f"📊 Performance Overview: {dataset_title}")

        # Top metric cards
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.metric("Total Records", f"{len(df):,}")
        with kpi2:
            st.metric("Columns", f"{len(df.columns)}")
        with kpi3:
            st.metric("Numeric Metrics", f"{len(numeric_cols)}")
        with kpi4:
            st.metric("Categorical Dimensions", f"{len(categorical_cols)}")

        # Secondary metrics from numeric columns
        if len(numeric_cols) >= 2:
            st.markdown("---")
            m_cols = st.columns(min(len(numeric_cols), 4))
            for idx, col in enumerate(numeric_cols[:4]):
                with m_cols[idx]:
                    avg_val = df[col].mean()
                    sum_val = df[col].sum()
                    st.metric(label=f"Avg {col}", value=f"{avg_val:,.2f}", delta=f"Sum: {sum_val:,.1f}")

        st.markdown("---")
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            if len(categorical_cols) > 0 and len(numeric_cols) > 0:
                cat_col = categorical_cols[0]
                num_col = numeric_cols[0]
                grouped = df.groupby(cat_col)[num_col].sum().reset_index().sort_values(by=num_col, ascending=False).head(10)
                fig1 = px.bar(
                    grouped,
                    x=cat_col,
                    y=num_col,
                    title=f"Total {num_col} by {cat_col}",
                    color=num_col,
                    color_continuous_scale="Blues"
                )
                fig1.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig1, use_container_width=True)
            elif len(numeric_cols) >= 2:
                fig1 = px.scatter(
                    df,
                    x=numeric_cols[0],
                    y=numeric_cols[1],
                    title=f"{numeric_cols[1]} vs {numeric_cols[0]}",
                    trendline="ols"
                )
                fig1.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig1, use_container_width=True)

        with chart_col2:
            if len(numeric_cols) >= 2:
                fig2 = px.histogram(
                    df,
                    x=numeric_cols[0],
                    nbins=20,
                    title=f"Distribution of {numeric_cols[0]}",
                    color_discrete_sequence=["#4F46E5"]
                )
                fig2.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig2, use_container_width=True)
            elif len(categorical_cols) > 0:
                cat_counts = df[categorical_cols[0]].value_counts().reset_index()
                cat_counts.columns = [categorical_cols[0], "Count"]
                fig2 = px.pie(
                    cat_counts,
                    names=categorical_cols[0],
                    values="Count",
                    title=f"Distribution across {categorical_cols[0]}",
                    hole=0.4
                )
                fig2.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig2, use_container_width=True)

    # TAB 2: CUSTOM VISUALIZATIONS
    with tab_charts:
        st.subheader("🛠️ Custom Chart Builder")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            chart_type = st.selectbox("Chart Type", ["Bar Chart", "Line Chart", "Area Chart", "Scatter Plot", "Box Plot", "Donut / Pie Chart"])
        with c2:
            x_axis = st.selectbox("X-Axis / Category", df.columns.tolist(), index=0)
        with c3:
            available_y = [c for c in df.columns if c != x_axis]
            y_axis = st.selectbox("Y-Axis / Metric", available_y if available_y else df.columns.tolist(), index=0)
        with c4:
            agg_method = st.selectbox("Aggregation Function", ["Sum", "Average (Mean)", "Count", "Minimum", "Maximum", "Median"])

        color_dim = st.selectbox("Optional Grouping / Color Dimension", ["None"] + [c for c in df.columns if c not in [x_axis, y_axis]])

        try:
            # Perform aggregation if X is categorical
            if x_axis in categorical_cols and y_axis in numeric_cols:
                agg_dict = {
                    "Sum": "sum",
                    "Average (Mean)": "mean",
                    "Count": "count",
                    "Minimum": "min",
                    "Maximum": "max",
                    "Median": "median"
                }
                agg_func = agg_dict.get(agg_method, "sum")
                if color_dim != "None":
                    plot_df = df.groupby([x_axis, color_dim])[y_axis].agg(agg_func).reset_index()
                else:
                    plot_df = df.groupby(x_axis)[y_axis].agg(agg_func).reset_index().sort_values(by=y_axis, ascending=False)
            else:
                plot_df = df

            color_arg = color_dim if color_dim != "None" else None

            if chart_type == "Bar Chart":
                fig = px.bar(plot_df, x=x_axis, y=y_axis, color=color_arg, barmode="group", title=f"{agg_method} of {y_axis} by {x_axis}")
            elif chart_type == "Line Chart":
                fig = px.line(plot_df, x=x_axis, y=y_axis, color=color_arg, markers=True, title=f"{y_axis} Trend by {x_axis}")
            elif chart_type == "Area Chart":
                fig = px.area(plot_df, x=x_axis, y=y_axis, color=color_arg, title=f"Area Plot of {y_axis} by {x_axis}")
            elif chart_type == "Scatter Plot":
                fig = px.scatter(df, x=x_axis, y=y_axis, color=color_arg, hover_data=df.columns.tolist()[:4], title=f"{y_axis} vs {x_axis}")
            elif chart_type == "Box Plot":
                fig = px.box(df, x=x_axis, y=y_axis, color=color_arg, title=f"Distribution of {y_axis} grouped by {x_axis}")
            else:
                # Pie chart
                pie_df = plot_df.head(10)
                fig = px.pie(pie_df, names=x_axis, values=y_axis, hole=0.35, title=f"{y_axis} breakdown by {x_axis}")

            fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=50, b=30))
            st.plotly_chart(fig, use_container_width=True)

        except Exception as err:
            st.error(f"Could not generate plot with selected axes: {err}")

    # TAB 3: DATA TABLE EXPLORER
    with tab_explorer:
        st.subheader("🔍 Interactive Data Table")
        search_query = st.text_input("Filter across rows (contains text):", "")

        filtered_df = df
        if search_query:
            mask = df.astype(str).apply(lambda row: row.str.contains(search_query, case=False).any(), axis=1)
            filtered_df = df[mask]
            st.caption(f"Showing {len(filtered_df)} of {len(df)} matching rows.")

        st.dataframe(filtered_df, use_container_width=True, height=400)

        # Export options
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            csv_data = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Filtered CSV", data=csv_data, file_name=f"{dataset_title}_export.csv", mime="text/csv")
        with col_exp2:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                filtered_df.to_excel(writer, index=False, sheet_name='Data')
            st.download_button("📥 Download Filtered Excel (.xlsx)", data=buffer.getvalue(), file_name=f"{dataset_title}_export.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # TAB 4: QUALITY & CLEANING TOOLS
    with tab_cleaner:
        st.subheader("🧹 Dataset Health & Statistical Summary")
        col_c1, col_c2 = st.columns(2)

        with col_c1:
            st.markdown("##### Column Profile & Data Types")
            profile_data = []
            for c in df.columns:
                null_count = df[c].isnull().sum()
                unique_count = df[c].nunique()
                profile_data.append({
                    "Column": c,
                    "Type": str(df[c].dtype),
                    "Null Values": null_count,
                    "Null %": round((null_count / len(df)) * 100, 1),
                    "Unique Values": unique_count
                })
            st.dataframe(pd.DataFrame(profile_data), use_container_width=True)

        with col_c2:
            st.markdown("##### Descriptive Statistics")
            st.dataframe(df.describe().round(2), use_container_width=True)

        if len(numeric_cols) > 1:
            st.markdown("##### Correlation Matrix")
            corr = df[numeric_cols].corr().round(2)
            fig_corr = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r", title="Feature Correlation")
            fig_corr.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_corr, use_container_width=True)
