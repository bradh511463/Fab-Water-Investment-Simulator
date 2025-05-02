# === V7_4_ROI_STREAMLIT.PY (FULLY CORRECTED VERSION) ===
import streamlit as st
import sklearn
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import urllib.request
import os
import gdown   

MODEL_URL = "https://drive.google.com/uc?export=download&id=1pZ_vFRfqx1mw1RpoMR_fanrrOvHHMDiN"
MODEL_LOCAL_PATH = "v6_1_water_model_boosted.pkl"
        
# Download if missing or corrupted
if not os.path.exists(MODEL_LOCAL_PATH) or os.path.getsize(MODEL_LOCAL_PATH) < 1_000_000:
    gdown.download(MODEL_URL, MODEL_LOCAL_PATH, quiet=False)

# === LOAD MODELS ===
@st.cache_resource
def load_water_model():
    return joblib.load("v6_1_water_model_boosted.pkl")

@st.cache_resource
def load_model():
    return joblib.load("revenue_multiplier_model.pkl")

# === FEATURE ENGINEERING ===
def build_features(wafer_intention, year, rec, mon, zld, wafer_size=1.0):
    percent_reclaimed = min(rec * 10, 100)
    intensity_score = 0.75
    impact_score = rec * 1.0 + mon * 0.7 + zld * 0.7
    one_hot = [
        1 if wafer_intention == "Consumer Electronics" else 0,
        1 if wafer_intention == "High-Performance Logic" else 0,
        1 if wafer_intention == "Industrial Controls" else 0,
        1 if wafer_intention == "Medical Devices" else 0,
    ]
    return np.array([[wafer_size, year, percent_reclaimed, intensity_score, impact_score] + one_hot])

def build_features_for_water_model(wafer_intention, year, rec, mon, zld, wafer_size_mm):
    total_investment = rec + mon + zld
    investment_efficiency = total_investment / (wafer_size_mm / 100) if wafer_size_mm else 0
    impact_score = rec * 1.0 + mon * .7 + zld * 0.7
    reclaimed_pct = min(impact_score * 2.5, 100)

    data = {
        "Year": [year],
        "Year Squared": [year ** 2],
        "Wafer Size": [wafer_size_mm],
        "Wafer Intention": [wafer_intention],
        "Reclamation Investment": [rec],
        "Monitoring Investment": [mon],
        "ZLD Investment": [zld],
        "Total Investment": [total_investment],
        "Investment Efficiency ($10k)": [investment_efficiency],
        "Investment Impact Score": [impact_score],
        "Percent Water Reclaimed": [reclaimed_pct],
        "Water Intensity Score": [0.75],  # Placeholder if not dynamic
        "Investment Strategy": ["Maintain"],  # Default for now; can vary if UI updated
        "Wafer Step": ["Cleaning"]  # Default for now; could randomize if needed
    }

    return pd.DataFrame(data)


# === MARKET SHARE UTILITY ===
def get_market_share_split(year):
    share_200 = max(0.0, 1 - ((year - 2025) / 20)) if year <= 2045 else 0.0
    share_450 = min(1.0, max(0.0, (year - 2035) / 20)) if year >= 2035 else 0.0
    share_300 = 1.0 - share_200 - share_450
    return share_200, share_300, share_450

def get_market_share(wafer_size_mm, year):
    s200, s300, s450 = get_market_share_split(year)
    return {200: s200, 300: s300, 450: s450}.get(wafer_size_mm, 1.0)
# === ROI CALCULATION ===
def calculate_roi_v4(wafer_intention, wafer_size_mm, year, rec, mon, zld, multiplier):
    wafer_data = {
        200: {"price": 1500, "volume": 100_000},
        300: {"price": 18000, "volume": 200_000},
        450: {"price": 72000, "volume": 500_000}
    }
    roi_weights = {
        "High-Performance Logic": 2.2,
        "Consumer Electronics": 1.6,
        "Automotive": 1.4,
        "Medical Devices": 1.3,
        "Industrial Controls": 1.2
    }

    base = wafer_data[wafer_size_mm]
    volume = base["volume"]
    price = base["price"]
    roi_weight = roi_weights.get(wafer_intention, 1.0)
    market_share = get_market_share(wafer_size_mm, year)

    base_revenue = volume * price * roi_weight * market_share
    if multiplier:
        base_revenue *= multiplier

    total_investment = rec + mon + zld
    profit = base_revenue - (total_investment * 10000)

    # Load water model and predict
    water_model = load_water_model()
    predicted_eff = water_model.predict(
    build_features_for_water_model(wafer_intention, year, rec, mon, zld, wafer_size_mm)
    )[0]
 
    # Define baseline and apply logic
    water_per_wafer_by_size = {200: 1200, 300: 3600, 450: 7200}
    baseline = water_per_wafer_by_size.get(wafer_size_mm, 3600)

    actual_year = year
    year_penalty = 1 + 0.001 * (actual_year - 2025)
    predicted_eff *= year_penalty


    # Apply safe clipping logic
    predicted_eff = max(min(predicted_eff, baseline), baseline * 0.1)

    
    # Define wafer output volume
    wafer_output_by_size = {200: 100_000, 300: 200_000, 450: 500_000}
    annual_wafers = wafer_output_by_size.get(wafer_size_mm, 200_000)

    # Calculate impact
    gal_saved_y = (baseline - predicted_eff) * annual_wafers * market_share
    dollar_saved_y = gal_saved_y * 0.004
    roi = (dollar_saved_y / (total_investment * 10000)) * 100 if total_investment else 0

    return base_revenue, profit, roi, predicted_eff, gal_saved_y, dollar_saved_y


# === CHARTING FUNCTION ===
def draw_charts(years, wafer_roi_list, rec, mon, zld, wafer_intention, wafer_size_mm):
    print("=== Draw_Charts is Running ===")  # This goes inside the function

    water_model = load_water_model()  # Load v5_water_model.pkl
    total_investment = rec + mon + zld
    roi_percent_series = [
        (roi_y / (total_investment * 10000)) * 100 if total_investment else 0
        for roi_y in wafer_roi_list
    ]

    # === CHART 2: Gallons Saved Over Time (Model-Driven + Market-Aligned) ===
    gallons_saved_series = []
    for y in years:
        predicted_eff = water_model.predict(
            build_features_for_water_model(wafer_intention, y, rec, mon, zld, wafer_size_mm)
        )[0]

        # Dynamically adjust wafer output based on market share
        base_output = {200: 900000, 300: 1080000, 450: 1500000}.get(wafer_size_mm, 1080000)
        market_share = get_market_share(wafer_size_mm, y)
        wafer_output = base_output * market_share

        baseline = {200: 1200, 300: 3600, 450: 7200}.get(wafer_size_mm, 3600)
        gallons_saved = (baseline - predicted_eff) * wafer_output
        gallons_saved_series.append(gallons_saved)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=years,
        y=gallons_saved_series,
        mode='lines+markers',
        name="Gallons Saved"
    ))
    fig2.update_layout(
        title="Gallons Saved Over Time (Market-Aligned)",
        xaxis_title="Year",
        yaxis_title="Gallons Saved",
        template="plotly_dark",
        font=dict(size=20),
        xaxis=dict(tickmode='linear', dtick=5),
        height=450
    )
    st.plotly_chart(fig2, use_container_width=True, key="chart_gallons_saved")

    # === CHART 3
    model = load_model()
    composite_series = []
    for y in years:
        mult_y = model.predict(build_features(wafer_intention, y, rec, mon, zld, wafer_size_mm / 300))[0]
        _, _, roi_y, eff_y, _, _ = calculate_roi_v4(wafer_intention, wafer_size_mm, y, rec, mon, zld, mult_y)
        composite_series.append((roi_y + eff_y) / 2)
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=years, y=composite_series, mode='lines+markers', name="Composite Score"))
    fig3.update_layout(title="Composite Score Over Time", xaxis_title="Year", yaxis_title="Composite Score", template="plotly_dark", 
font=dict(size=20))
    st.plotly_chart(fig3, use_container_width=True, key="wafer_size")

    # CHART 4
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(x=years, y=gallons_saved_series, name="Gallons Saved", yaxis="y1"))
    fig4.add_trace(go.Scatter(x=years, y=roi_percent_series, mode="lines+markers", name="ROI (%)", yaxis="y2"))
    fig4.update_layout(title="ROI vs. Gallons Saved", xaxis=dict(title="Year"), yaxis=dict(title="Gallons Saved"), yaxis2=dict(title="ROI (%)", 
overlaying="y", side="right"), template="plotly_dark", font=dict(size=20))
    st.plotly_chart(fig4, use_container_width=True, key="gallons_time")

# === MAIN MODULE ===
def display_roi_module(wafer_intention, year, rec, mon, zld, eff_level, wafer_size=1.0, strategy="Maintain", wafer_size_mm=300, base_cost=5000):
    model = load_model()
    multiplier = model.predict(build_features(wafer_intention, year, rec, mon, zld, wafer_size))[0]
    total_investment = rec + mon + zld
    revenue, profit, roi, eff_level, gal_saved_y, dollar_saved_y = calculate_roi_v4(
        wafer_intention, wafer_size_mm, year, rec, mon, zld, multiplier)

    years = list(range(2025, 2076))
    wafer_roi_list = [
        calculate_roi_v4(wafer_intention, wafer_size_mm, y, rec, mon, zld,
                         model.predict(build_features(wafer_intention, y, rec, mon, zld, wafer_size))[0])[2]
        for y in years
    ]

    composite_score = (roi + eff_level) / 2

    # === Normalize Gallons Saved to Billions ===
    gallons_bil = gal_saved_y / 1_000_000_000

    # === Track and Show Delta ===
    if "last_gallons" not in st.session_state:
        st.session_state.last_gallons = gal_saved_y
    gallon_delta = gal_saved_y - st.session_state.last_gallons
    st.session_state.last_gallons = gal_saved_y

    # === Display Metrics ===
    st.markdown("""<h2 style='font-size:26px;'>Predicted ROI Breakdown</h2>""", unsafe_allow_html=True)

    # Convert to desired units
    revenue_bil     = revenue / 1_000_000_000
    profit_bil      = profit  / 1_000_000_000
    investment_mil  = (total_investment * 10_000) / 1_000_000  # rec+mon+zld in 10k units → dollars → millions

    # Set up 6 equal columns
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Gallons Saved (B)",          f"{gallons_bil:.3f}B")
    col2.metric("ROI from Water Investment",  f"{roi:.2f}%")
    col3.metric(f"Total Revenue {year}",      f"${revenue_bil:.3f}B")
    col4.metric(f"Total Profit {year}",       f"${profit_bil:.3f}B")
    col5.metric(f"Total Investment {year}",   f"${investment_mil:.3f}M")
    col6.metric("Composite Score",            f"{composite_score:.2f}")

    st.markdown("""<h2 style='font-size:26px;'>Scenario Summary</h2>""", unsafe_allow_html=True)

    st.markdown(f"""
        <p style='font-size:22px; line-height:1.6'>
        In <span style='color:#32CD32'><strong>{year}</strong></span>, this fab produces
        <span style='color:#32CD32'><strong>{wafer_size_mm:,}mm</strong></span> wafers
        for the <span style='color:#32CD32'><strong>{wafer_intention}</strong></span> industry,
        returning a profit of <span style='color:#32CD32'><strong>${profit:,.0f}</strong></span>.
        Due to an investment of <span style='color:#32CD32'><strong>${total_investment * 10000:,.0f}</strong></span>,
        <span style='color:#32CD32'><strong>{gal_saved_y:,.0f}</strong></span> gallons
        of water were saved, worth <span style='color:#32CD32'><strong>${dollar_saved_y:,.0f}</strong></span> in value.
        </p>
    """, unsafe_allow_html=True)

    st.markdown("""<h2 style='font-size:26px;'>Key Formulas</h2>""", unsafe_allow_html=True)

    formulas = {
       "Base Revenue": "volume × price × ROI weight × market share × ML multiplier",
       "Profit": "Base Revenue − (Investment × $10,000)",
       "Adjusted Profit": "Profit + Dollar Value of Water Saved",
       "ROI (Water-Aligned)": "(Adjusted Profit ÷ (Investment × $10,000)) × 100",
       "Gallons Saved": "(Baseline Water − Predicted Efficiency) × Annual Wafers",
       "Dollar Value of Water Saved": "Gallons Saved × $0.10",  # ← update here if $0.10 is used
       "Composite Score": "(ROI + Efficiency Score) ÷ 2"
       }

    styled_table = pd.DataFrame(list(formulas.items()), columns=["Formula Name", "Expression"]).style.set_table_styles([
      {'selector': 'th', 'props': [('font-size', '22px')]},
      {'selector': 'td', 'props': [('font-size', '22px')]}
      ])

    st.dataframe(styled_table, use_container_width=True)



    draw_charts(years, wafer_roi_list, rec, mon, zld, wafer_intention, wafer_size_mm)
    return roi, composite_score, eff_level

