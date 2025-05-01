# === v7_3_cas_st.py ===

import streamlit as st
import plotly.graph_objects as go

# === COLOR PALETTE ===
NODE_COLORS = {
    'Wafer Size': '#AED6F1',
    'Wafer Intention': '#BB8FCE',
    'Reclamation': '#F39C12',
    'Monitoring': '#DC7633',
    'ZLD': '#A569BD',
    'Investment Strategy': '#5DADE2',
    'Gallons Saved': '#58D68D',
    'Cleaning': '#82E0AA',
    'Etching': '#82E0AA',
    'Diffusion': '#82E0AA',
    'Lithography': '#82E0AA',
    'Metrology': '#82E0AA',
    'Revenue': '#3498DB',
    'Profit': '#2ECC71',
    'Investment Efficiency': '#1ABC9C',
    'ROI %': '#9B59B6',
    'Composite Score': 'gold'
}

# === NODE POSITIONS ===
POSITIONS = {
    'Wafer Size': (0, 1.0),
    'Wafer Intention': (0, 0.85),
    'Reclamation': (-0.6, 0.7),
    'Monitoring': (0, 0.7),
    'ZLD': (0.6, 0.7),
    'Investment Strategy': (0, 0.55),
    'Gallons Saved': (0, 0.4),
    'Cleaning': (-0.8, 0.25),
    'Etching': (-0.4, 0.25),
    'Diffusion': (0, 0.25),
    'Lithography': (0.4, 0.25),
    'Metrology': (0.8, 0.25),
    'Revenue': (-0.5, 0.1),
    'Profit': (0, 0.1),
    'Investment Efficiency': (0.5, 0.1),
    'ROI %': (0, -0.05),
    'Composite Score': (0, -0.2)
}

# === FORWARD LINKS ===
FORWARD_LINKS = [
    ('Wafer Size', 'Wafer Intention'),
    ('Wafer Intention', 'Reclamation'),
    ('Wafer Intention', 'Monitoring'),
    ('Wafer Intention', 'ZLD'),
    ('Reclamation', 'Investment Strategy'),
    ('Monitoring', 'Investment Strategy'),
    ('ZLD', 'Investment Strategy'),
    ('Investment Strategy', 'Gallons Saved'),
    ('Gallons Saved', 'Revenue'),
    ('Gallons Saved', 'Profit'),
    ('Gallons Saved', 'Investment Efficiency'),
    ('Gallons Saved', 'ROI %'),
    ('Revenue', 'Composite Score'),
    ('Profit', 'Composite Score'),
    ('Investment Efficiency', 'Composite Score'),
    ('ROI %', 'Composite Score')
]

# === DYNAMIC FEEDBACK MESSAGES ===
def dynamic_feedback_message(source, target, revenue, profit, roi_value, total_gal_saved, year, wafer_size_mm, wafer_intention):
    if source == 'Revenue' and target == 'Wafer Size':
        if wafer_size_mm == 300 and year >= 2040:
            return f"300mm wafers outdated by {year}. Shift to 450mm recommended."
        else:
            return f"Current wafer size {wafer_size_mm}mm aligned with market."
    if source == 'Profit' and target == 'Investment Strategy':
        return "Profit declining. Suggest Decrease Strategy."
    if source == 'Investment Efficiency' and target == 'Investment Strategy':
        return "Investment Efficiency low. Recommend rebalancing."
    if source == 'ROI %':
        return f"ROI at {roi_value:.2f}%. Consider investment adjustment."
    return ""

# === DRAWING FUNCTION ===
def draw_cas_flow(
    reclaim, monitor, zld,
    wafer_size_mm, wafer_intention,
    strategy, revenue, profit,
    roi_value, composite_score,
    total_gal_saved, year, eff_level
):
    fig = go.Figure()

    # === SIDEBAR LEGEND CONTROLS (Visual Samples) ===
    st.sidebar.title("CAS CDL Display Options")
    st.sidebar.markdown("---")  # Separator line

    show_positive_feedback = st.sidebar.checkbox(
        label="Positive Feedback", value=True
    )
    st.sidebar.markdown(
        "<div style='height:0px; width:50px; border-top:2px dashed green; margin-bottom:10px;'></div>",
        unsafe_allow_html=True
    )

    show_negative_feedback = st.sidebar.checkbox(
        label="Negative Feedback", value=True
    )
    st.sidebar.markdown(
        "<div style='height:0px; width:50px; border-top:2px dashed red; margin-bottom:10px;'></div>",
        unsafe_allow_html=True
    )

    show_economic_flow = st.sidebar.checkbox(
        label="Economic Flow", value=True
    )
    st.sidebar.markdown(
        "<div style='width:50px; height:15px; background:rgba(52,152,219,0.3); border:1px solid white; margin-bottom:10px;'></div>",
        unsafe_allow_html=True
    )

    show_sustainability_flow = st.sidebar.checkbox(
        label="Sustainability Flow", value=True
    )
    st.sidebar.markdown(
        "<div style='width:50px; height:15px; background:rgba(88,214,141,0.3); border:1px solid white; margin-bottom:10px;'></div>",
        unsafe_allow_html=True
    )

    st.sidebar.markdown("---")  # Separator after legend

    # --- (Your normal code continues below here: Gallons Saved, Node Hover, etc.) ---

    # --- Calculate Process Gallons Saved ---
    gallons_saved_split = {
        'Cleaning': total_gal_saved * 0.30,
        'Etching': total_gal_saved * 0.20, 
        'Diffusion': total_gal_saved * 0.20,
        'Lithography': total_gal_saved * 0.20,
        'Metrology': total_gal_saved * 0.10   
    }

    # --- Node Hovertexts ---
    node_hover = {
        'Wafer Size': "Market Trends:\n- 300mm decline ~2045\n- 450mm growth ~2030\n- 200mm slow decline",
        'Wafer Intention': "ROI Weights:\nHPL 2.2x, Automotive 1.4x, Industrial 1.2x, Consumer 1.6x",
        'Reclamation': f"Reclamation:\n${reclaim*10000:,.0f}",
        'Monitoring': f"Monitoring:\n${monitor*10000:,.0f}",
        'ZLD': f"ZLD:\n${zld*10000:,.0f}",
        'Investment Strategy': f"Strategy: {strategy}",
        'Gallons Saved': f"Formula:\n(Baseline - Efficiency) × Wafers\n{total_gal_saved:,.0f} gal ({year})",
        'Cleaning': f"Cleaning:\n{gallons_saved_split['Cleaning']:,.0f} gal",
        'Etching': f"Etching:\n{gallons_saved_split['Etching']:,.0f} gal",
        'Diffusion': f"Diffusion:\n{gallons_saved_split['Diffusion']:,.0f} gal",
        'Lithography': f"Lithography:\n{gallons_saved_split['Lithography']:,.0f} gal",
        'Metrology': f"Metrology:\n{gallons_saved_split['Metrology']:,.0f} gal",
        'Revenue': f"Revenue:\n${revenue:,.0f} ({year})",
        'Profit': f"Profit:\n${profit:,.0f} ({year})",
        'Investment Efficiency': f"Efficiency:\n{eff_level:.2f} mL/wafer",
        'ROI %': f"ROI:\n{roi_value:.2f}% ({year})",
        'Composite Score': f"Composite:\n{composite_score:.2f}"
    }

    # --- Draw Nodes ---
    for label, (x, y) in POSITIONS.items():
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode='markers+text',
            marker=dict(size=40, color=NODE_COLORS[label], line=dict(width=2, color='white')),
            text=[label],
            textposition="bottom center",
            hovertext=node_hover.get(label, label),
            hoverinfo="text",
            showlegend=False
        ))

    # --- Draw Forward Arrows (Hierarchy) ---
    for src, tgt in FORWARD_LINKS:
        x0, y0 = POSITIONS[src]
        x1, y1 = POSITIONS[tgt]
        fig.add_trace(go.Scatter(
            x=[x0, x1], y=[y0, y1],
            mode='lines',
            line=dict(color='white', width=2),
            hoverinfo='none',
            showlegend=False
        ))

    # --- Draw Feedback Arrows Conditionally ---
    if show_negative_feedback:
        for src, tgt in [
            ('Revenue', 'Wafer Size'),
            ('Profit', 'Investment Strategy'),
            ('Investment Efficiency', 'Investment Strategy'),
            ('ROI %', 'Reclamation'),
            ('ROI %', 'Monitoring'),
            ('ROI %', 'ZLD')
        ]:
            x0, y0 = POSITIONS[src]
            x1, y1 = POSITIONS[tgt]
            fig.add_trace(go.Scatter(
                x=[x0, (x0+x1)/2, x1],
                y=[y0, (y0+y1)/2 + 0.1, y1],
                mode='lines+markers',
                marker=dict(size=5, color='red', opacity=0),
                line=dict(color='red', width=2, dash='dash'),
                hovertext=dynamic_feedback_message(src, tgt, revenue, profit, roi_value, total_gal_saved, year, wafer_size_mm, wafer_intention),
                hoverinfo='text',
                showlegend=False
            ))

    if show_positive_feedback:
        for src, tgt in [
            ('Gallons Saved', 'Investment Strategy'),
            ('Gallons Saved', 'Cleaning'),
            ('Gallons Saved', 'Etching'),
            ('Gallons Saved', 'Diffusion'),
            ('Gallons Saved', 'Lithography'),
            ('Gallons Saved', 'Metrology')
        ]:
            x0, y0 = POSITIONS[src]
            x1, y1 = POSITIONS[tgt]
            fig.add_trace(go.Scatter(
                x=[x0, (x0+x1)/2, x1],
                y=[y0, (y0+y1)/2 + 0.1, y1],
                mode='lines+markers',
                marker=dict(size=5, color='green', opacity=0),
                line=dict(color='green', width=2, dash='dash'),
                hovertext=f"Positive: {src} boosts {tgt}",
                hoverinfo='text',
                showlegend=False
            ))

    # --- Draw Group Shading Conditionally ---
    if show_sustainability_flow:
        fig.add_shape(type='rect', x0=-1.2, y0=0.09, x1=1.2, y1=0.5,
                      line=dict(color='white', width=2), fillcolor='rgba(88,214,141,0.1)', layer='below')
        fig.add_annotation(x=-1.0, y=0.4, text="Sustainability Flow", showarrow=False, font=dict(color="white", size=18))

    if show_economic_flow:
        fig.add_shape(type='rect', x0=-1.2, y0=-0.25, x1=1.2, y1=0.05,
                      line=dict(color='white', width=2), fillcolor='rgba(52,152,219,0.1)', layer='below')
        fig.add_annotation(x=-1.0, y=0.02, text="Economic Flow", showarrow=False, font=dict(color="white", size=18))

    # --- Main CAS CDL Diagram Title ---
    fig.add_annotation(
        text="CAS CDL Diagram",
        xref="paper", yref="paper",
        x=0, y=1.02,
        showarrow=False,
        font=dict(size=26, color="white"),
        align="left"
    )



    # --- Layout Finalization ---
    fig.update_layout(
        height=750,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='#404040',
        plot_bgcolor='#404040',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )

    st.plotly_chart(fig, use_container_width=True)

