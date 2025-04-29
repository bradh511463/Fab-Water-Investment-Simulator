# === v7_1_streamlit.py ===

import streamlit as st
from v7_3_cas_st import draw_cas_flow
from v7_4_roi_streamlit import (
    display_roi_module,
    build_features,
    load_model,
    calculate_roi_v4
)

# === PAGE CONFIG ===
st.set_page_config(page_title="Semiconductor Fab Investment Simulator", layout="wide")

# === PAGE TITLE ===
st.title("Semiconductor Fab Investment Simulator")

# === SIDEBAR INPUTS ===
st.sidebar.header("Simulation Inputs")

wafer_intention = st.sidebar.selectbox(
    "Wafer Intention",
    ["Automotive", "Consumer Electronics", "High-Performance Logic", "Medical Devices", "Industrial Controls"],
    key="wafer_selector_main"
)

wafer_size_mm = st.sidebar.selectbox(
    "Wafer Size",
    options=[200, 300, 450],
    format_func=lambda x: f"{x}mm",
    index=1,
    key="wafer_size_selector"
)
wafer_size = wafer_size_mm / 300

strategy = st.sidebar.selectbox(
    "Investment Strategy",
    options=["Maintain", "Increase", "Decrease"],
    key="strategy_selector"
)

snapshot_year = st.sidebar.slider(
    "Snapshot Year", 2025, 2075, 2035,
    key="snapshot_year_main"
)

# === SLIDER: Water Reclamation ===
reclaim = st.sidebar.slider("Water Reclamation (500.0 = $5,000,000)", 0.0, 500.0, 100.0, step=10.0)
st.sidebar.caption(f"Selected Reclamation: {reclaim:.1f} units → ${int(reclaim * 10000):,}")

# === SLIDER: Monitoring ===
monitor = st.sidebar.slider("Monitoring (500.0 = $5,000,000)", 0.0, 500.0, 50.0, step=10.0)
st.sidebar.caption(f"Selected Monitoring: {monitor:.1f} units → ${int(monitor * 10000):,}")

# === SLIDER: ZLD ===
zld = st.sidebar.slider("ZLD (500.0 = $5,000,000)", 0.0, 500.0, 100.0, step=10.0)
st.sidebar.caption(f"Selected ZLD: {zld:.1f} units → ${int(zld * 10000):,}")

# === ROI MODULE ===
st.markdown("## Return on Investment Analysis")
roi_value, composite_score, eff_level = display_roi_module(
    wafer_intention, snapshot_year, reclaim, monitor, zld,
    eff_level=None, wafer_size=wafer_size, strategy=strategy,
    wafer_size_mm=wafer_size_mm, base_cost=5000
)

# === CAS MODULE ===

# 1. Recompute the ML multiplier
model = load_model()
multiplier = model.predict(
    build_features(wafer_intention, snapshot_year, reclaim, monitor, zld, wafer_size)
)[0]

# 2. Get revenue, profit and gallons saved
rev, prof, _, _, gal_saved_y, _ = calculate_roi_v4(
    wafer_intention,
    wafer_size_mm,
    snapshot_year,
    reclaim,
    monitor,
    zld,
    multiplier
)

# 3. Call the CAS diagram with all required args
with st.expander("", expanded=True):
    draw_cas_flow(
        reclaim=reclaim,
        monitor=monitor,
        zld=zld,
        wafer_size_mm=wafer_size_mm,
        wafer_intention=wafer_intention,
        strategy=strategy,
        revenue=rev,
        profit=prof,
        roi_value=roi_value,
        composite_score=composite_score,
        total_gal_saved=gal_saved_y,
        year=snapshot_year,
        eff_level=eff_level
    )

