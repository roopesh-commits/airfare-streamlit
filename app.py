import streamlit as st
import pandas as pd
import plotly.express as px

from database import get_data
from processor import (
    calculate_index,
    calculate_route_index,
    get_airline_average,
    get_wow_change,
    get_best_value_airline,
    get_route_volatility,
    filter_data,
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="India Airfare Price Index",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

PLOTLY_TEMPLATE = "plotly_white"
COLOR_SEQUENCE = px.colors.qualitative.Set2

st.markdown(
    """
    <style>
    div[data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.25);
        border-radius: 10px;
        padding: 14px 16px 8px 16px;
    }
    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricValue"],
    div[data-testid="stMetricDelta"] {
        color: var(--text-color);
    }
    div[data-testid="stMetricLabel"] {
        font-weight: 600;
    }
    .block-container {
        padding-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# LOAD DATA (cached inside get_data)
# --------------------------------------------------

raw_df = get_data()
raw_df["date"] = pd.to_datetime(raw_df["date"])


# --------------------------------------------------
# HEADER
# --------------------------------------------------

header_col, badge_col = st.columns([5, 1])

with header_col:
    st.title("✈️ India Airfare Price Index")
    st.caption(
        "SIH26056 Prototype · Real-time airfare data collection, "
        "processing and price index analysis"
    )

with badge_col:
    st.markdown(
        f"<div style='text-align:right; padding-top:18px; color:gray;'>"
        f"Last refreshed<br><b>{pd.Timestamp.now().strftime('%d %b %Y, %I:%M %p')}</b></div>",
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# FLIGHT BANNER (floating objects, self-contained)
# --------------------------------------------------

FLIGHT_BANNER_HTML = """
<div style="
    position:relative;
    width:100%;
    height:190px;
    border-radius:14px;
    overflow:hidden;
    background:linear-gradient(180deg,#0B1B33 0%,#213A5F 55%,#3E5A80 100%);
    font-family:'IBM Plex Sans', sans-serif;
">
  <div class="cloud c1"><svg viewBox="0 0 200 100" width="100%"><path d="M40 70 Q20 70 20 52 Q20 34 42 34 Q46 14 72 14 Q100 14 106 36 Q130 34 130 54 Q130 70 108 70 Z" fill="#EAF1FA"/></svg></div>
  <div class="cloud c2"><svg viewBox="0 0 200 100" width="100%"><path d="M40 70 Q20 70 20 52 Q20 34 42 34 Q46 14 72 14 Q100 14 106 36 Q130 34 130 54 Q130 70 108 70 Z" fill="#DDE7F5"/></svg></div>

  <div class="obj plane">
    <svg viewBox="0 0 160 110" width="100%">
      <defs>
        <linearGradient id="wA" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stop-color="#FDFDFC"/><stop offset="1" stop-color="#D9DEE8"/>
        </linearGradient>
        <linearGradient id="wB" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stop-color="#F2F3F1"/><stop offset="1" stop-color="#B9C1D1"/>
        </linearGradient>
      </defs>
      <path d="M78 6 L128 84 L80 70 L86 100 L70 88 L64 70 L18 88 Z" fill="url(#wA)" stroke="#B9C1D1" stroke-width="1"/>
      <path d="M78 6 L80 70 L18 88 Z" fill="url(#wB)" opacity="0.9"/>
    </svg>
    <div class="shadow"></div>
  </div>

  <div class="obj compass">
    <svg viewBox="0 0 100 100" width="100%">
      <circle cx="50" cy="50" r="46" fill="#F6F1E4" stroke="#B8792A" stroke-width="2"/>
      <circle cx="50" cy="50" r="36" fill="none" stroke="#B8792A" stroke-width="1" opacity="0.5"/>
      <path d="M50 18 L58 50 L50 82 L42 50 Z" fill="#B8792A"/>
      <circle cx="50" cy="50" r="4" fill="#3A2A12"/>
    </svg>
    <div class="shadow"></div>
  </div>

  <div class="obj tag">
    <svg viewBox="0 0 110 130" width="100%">
      <path d="M20 8 H80 L96 30 V116 Q96 122 90 122 H26 Q20 122 20 116 Z" fill="#FBF7EE" stroke="#D8CBAE" stroke-width="1.5"/>
      <circle cx="58" cy="22" r="5" fill="none" stroke="#B8792A" stroke-width="2"/>
      <line x1="30" y1="60" x2="86" y2="60" stroke="#D8CBAE" stroke-width="1.5"/>
      <line x1="30" y1="76" x2="70" y2="76" stroke="#D8CBAE" stroke-width="1.5"/>
      <line x1="30" y1="92" x2="78" y2="92" stroke="#D8CBAE" stroke-width="1.5"/>
    </svg>
    <div class="shadow"></div>
  </div>

  <div style="position:absolute; left:26px; bottom:16px; color:#C7D0E0; font-size:12px; letter-spacing:0.02em;">
    India Airfare Price Index &middot; live route tracking
  </div>
</div>

<style>
  .cloud{ position:absolute; pointer-events:none; }
  .c1{ top:12px; left:2%; width:170px; opacity:0.55; animation:drift1 22s linear infinite; }
  .c2{ top:70px; left:-10%; width:210px; opacity:0.38; animation:drift2 30s linear infinite; }
  @keyframes drift1{ 0%{ transform:translateX(0);} 100%{ transform:translateX(340px);} }
  @keyframes drift2{ 0%{ transform:translateX(0);} 100%{ transform:translateX(420px);} }

  .obj{ position:absolute; pointer-events:none; filter:drop-shadow(0 14px 16px rgba(0,0,0,0.35)); }
  .plane{ top:14px; right:8%; width:100px; animation:bob 6.5s ease-in-out infinite; }
  .compass{ bottom:14px; right:26%; width:64px; animation:bob 7.8s ease-in-out infinite; animation-delay:-2s; }
  .tag{ top:38px; left:38%; width:60px; animation:bob 5.6s ease-in-out infinite; animation-delay:-3.5s; }

  @keyframes bob{
    0%,100%{ transform:translateY(0) rotate(-6deg); }
    50%{ transform:translateY(-14px) rotate(6deg); }
  }

  .shadow{
    position:absolute; left:50%; bottom:-10px; width:70%; height:10px;
    transform:translateX(-50%);
    background:radial-gradient(ellipse at center, rgba(0,0,0,0.35), rgba(0,0,0,0) 70%);
    animation:shrink 6.5s ease-in-out infinite;
  }
  @keyframes shrink{
    0%,100%{ transform:translateX(-50%) scale(1); opacity:0.5; }
    50%{ transform:translateX(-50%) scale(0.7); opacity:0.25; }
  }

  @media (prefers-reduced-motion: reduce){
    .cloud, .obj, .shadow{ animation:none !important; }
  }
</style>
"""

st.iframe(FLIGHT_BANNER_HTML, height=200)

st.divider()


# --------------------------------------------------
# SIDEBAR — FILTERS
# --------------------------------------------------

st.sidebar.header("🔎 Filters")

min_date = raw_df["date"].min().date()
max_date = raw_df["date"].max().date()

date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

# Guard against a single-date selection mid-drag
if isinstance(date_range, tuple) and len(date_range) == 1:
    date_range = (date_range[0], date_range[0])

airline_options = sorted(raw_df["airline"].unique())
selected_airlines = st.sidebar.multiselect(
    "Airlines",
    airline_options,
    default=airline_options,
)

fare_class_options = sorted(raw_df["fare_class"].unique())
selected_fare_classes = st.sidebar.multiselect(
    "Fare class",
    fare_class_options,
    default=fare_class_options,
)

st.sidebar.divider()
st.sidebar.subheader("Route")

origins = sorted(raw_df["origin"].unique())
selected_origin = st.sidebar.selectbox("Origin", origins)

destinations = sorted(
    raw_df[raw_df["origin"] == selected_origin]["destination"].unique()
)
selected_destination = st.sidebar.selectbox("Destination", destinations)

st.sidebar.divider()
st.sidebar.caption(
    "Prototype uses simulated airfare observations. Production "
    "version will connect to live airline / OTA sources."
)

# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

df = filter_data(
    raw_df,
    date_range=date_range,
    airlines=selected_airlines,
    fare_classes=selected_fare_classes,
)

if df.empty:
    st.warning("No observations match the current filters. Widen your filters to see data.")
    st.stop()

route_df = df[
    (df["origin"] == selected_origin) &
    (df["destination"] == selected_destination)
]


# --------------------------------------------------
# OVERALL INDEX + KPIs
# --------------------------------------------------

index_df = calculate_index(df)

base_fare = index_df["total_fare"].iloc[0]
current_fare = index_df["total_fare"].iloc[-1]
current_index = (current_fare / base_fare) * 100
percentage_change = current_index - 100

wow_change = get_wow_change(index_df)
best_airline, best_airline_fare = get_best_value_airline(df)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Airfare Price Index",
    f"{current_index:.1f}",
    f"{percentage_change:+.1f}% vs base",
)

col2.metric(
    "Current Avg Fare",
    f"₹{current_fare:,.0f}",
    f"{wow_change:+.1f}% WoW" if wow_change is not None else None,
)

col3.metric("Base Fare", f"₹{base_fare:,.0f}")

col4.metric(
    "Best Value Airline",
    best_airline or "—",
    f"₹{best_airline_fare:,.0f} avg" if best_airline_fare else None,
)

col5.metric("Observations", f"{len(df):,}")

st.divider()


# --------------------------------------------------
# TABBED VIEWS
# --------------------------------------------------

tab_overview, tab_route, tab_airline, tab_data = st.tabs(
    ["📈 Overview", "🛫 Route Analysis", "🏷️ Airline Comparison", "📊 Data Explorer"]
)


# ---------------- OVERVIEW TAB ----------------
with tab_overview:

    st.subheader("Airfare Price Index Trend")

    fig_index = px.line(
        index_df,
        x="date",
        y="index",
        markers=True,
        template=PLOTLY_TEMPLATE,
        labels={"date": "Date", "index": "Airfare Index"},
    )
    fig_index.add_hline(
        y=100,
        line_dash="dash",
        line_color="gray",
        annotation_text="Base = 100",
    )
    fig_index.update_traces(line_color=COLOR_SEQUENCE[0])
    fig_index.update_layout(hovermode="x unified")
    st.plotly_chart(fig_index, width="stretch")

    left, right = st.columns(2)

    with left:
        st.subheader("Fare Distribution by Route")
        route_labels = df.copy()
        route_labels["route"] = route_labels["origin"] + " → " + route_labels["destination"]
        fig_box = px.box(
            route_labels,
            x="route",
            y="total_fare",
            color="route",
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=COLOR_SEQUENCE,
            labels={"total_fare": "Total Fare (₹)", "route": "Route"},
        )
        fig_box.update_layout(showlegend=False, xaxis_tickangle=-30)
        st.plotly_chart(fig_box, width="stretch")

    with right:
        st.subheader("Route Price Volatility")
        volatility_df = get_route_volatility(df)
        fig_vol = px.bar(
            volatility_df,
            x="volatility",
            y="route",
            orientation="h",
            template=PLOTLY_TEMPLATE,
            color="volatility",
            color_continuous_scale="Oranges",
            labels={"volatility": "Volatility (%)", "route": "Route"},
        )
        fig_vol.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_vol, width="stretch")
        st.caption("Higher volatility = fares swing more day to day on that route.")


# ---------------- ROUTE ANALYSIS TAB ----------------
with tab_route:

    st.subheader(f"Price Trend: {selected_origin} → {selected_destination}")

    if route_df.empty:
        st.info("No observations for this route in the current filters.")
    else:
        route_trend = (
            route_df.groupby(["date", "airline"])["total_fare"]
            .mean()
            .reset_index()
        )

        fig_route = px.line(
            route_trend,
            x="date",
            y="total_fare",
            color="airline",
            markers=True,
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=COLOR_SEQUENCE,
            labels={"date": "Date", "total_fare": "Total Fare (₹)", "airline": "Airline"},
        )
        fig_route.update_layout(hovermode="x unified")
        st.plotly_chart(fig_route, width="stretch")

        route_index_df = calculate_route_index(
            df, selected_origin, selected_destination
        )
        if not route_index_df.empty:
            st.subheader("Route-Specific Index")
            fig_route_index = px.area(
                route_index_df,
                x="date",
                y="index",
                template=PLOTLY_TEMPLATE,
                labels={"date": "Date", "index": "Route Index"},
            )
            fig_route_index.add_hline(y=100, line_dash="dash", line_color="gray")
            fig_route_index.update_traces(line_color=COLOR_SEQUENCE[1])
            st.plotly_chart(fig_route_index, width="stretch")

        st.subheader("Fare Class Split on This Route")
        class_split = (
            route_df.groupby("fare_class")["total_fare"]
            .mean()
            .reset_index()
        )
        fig_class = px.pie(
            class_split,
            names="fare_class",
            values="total_fare",
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=COLOR_SEQUENCE,
            hole=0.45,
        )
        st.plotly_chart(fig_class, width="stretch")


# ---------------- AIRLINE COMPARISON TAB ----------------
with tab_airline:

    st.subheader("Airline Fare Comparison")

    compare_scope = st.radio(
        "Compare across",
        ["Selected route", "All routes (filtered)"],
        horizontal=True,
    )

    scope_df = route_df if compare_scope == "Selected route" else df

    if scope_df.empty:
        st.info("No observations available for this comparison.")
    else:
        airline_avg = get_airline_average(scope_df)

        fig_airline = px.bar(
            airline_avg,
            x="airline",
            y="total_fare",
            color="airline",
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=COLOR_SEQUENCE,
            labels={"airline": "Airline", "total_fare": "Average Fare (₹)"},
            title=f"Average Fare — {compare_scope}",
        )
        fig_airline.update_layout(showlegend=False)
        st.plotly_chart(fig_airline, width="stretch")

        st.subheader("Fare vs Availability")
        avail_df = (
            scope_df.groupby("airline")
            .agg(avg_fare=("total_fare", "mean"), avg_availability=("availability", "mean"))
            .reset_index()
        )
        fig_scatter = px.scatter(
            avail_df,
            x="avg_availability",
            y="avg_fare",
            text="airline",
            color="airline",
            size="avg_fare",
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=COLOR_SEQUENCE,
            labels={"avg_availability": "Avg Seats Available", "avg_fare": "Avg Fare (₹)"},
        )
        fig_scatter.update_traces(textposition="top center")
        fig_scatter.update_layout(showlegend=False)
        st.plotly_chart(fig_scatter, width="stretch")
        st.caption("Bottom-right is the sweet spot: lower fares, more seats open.")


# ---------------- DATA EXPLORER TAB ----------------
with tab_data:

    st.subheader("Fare Observations")

    search_scope = st.radio(
        "Show",
        ["Selected route", "All filtered data"],
        horizontal=True,
        key="data_scope",
    )

    table_df = route_df if search_scope == "Selected route" else df

    st.dataframe(
        table_df.sort_values("date", ascending=False),
        width="stretch",
        height=420,
    )

    st.download_button(
        "⬇️ Download as CSV",
        data=table_df.to_csv(index=False).encode("utf-8"),
        file_name="airfare_observations.csv",
        mime="text/csv",
    )


# --------------------------------------------------
# SYSTEM INFORMATION
# --------------------------------------------------

st.divider()

with st.expander("🔄 Prototype Data Pipeline", expanded=False):

    st.code(
        """
Airline / OTA Sources
        ↓
Automated Data Collection
        ↓
Data Cleaning & Validation
        ↓
SQLite Database
        ↓
Index Calculation Engine
        ↓
Analytics Dashboard
""",
        language="text",
    )

    st.info(
        "Prototype currently uses simulated airfare observations "
        "to demonstrate the complete data-to-index pipeline. "
        "The production version will integrate automated data "
        "collection from permitted airline and OTA sources."
    )