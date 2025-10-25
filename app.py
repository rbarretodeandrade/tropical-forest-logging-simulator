"""
Tropical Forest Reduced-Impact Logging Simulator
Streamlit Web Application

Interactive tool for exploring trade-offs between timber extraction
and forest carbon conservation in old-growth tropical rainforests.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Tropical Forest Logging Simulator",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load and encode background image
def get_base64_image(image_path):
    """Convert image to base64 string for CSS embedding"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Get base64 encoded images
bg_image = get_base64_image("1_eyes_in_the_sky.jpg")
sidebar_image = get_base64_image("wood-3212803_1920-compressor.jpg")

# Custom CSS for tropical forest theme
st.markdown(f"""
<style>
    /* Main background - tropical forest canopy */
    .stApp {{
        background-image: url('data:image/jpeg;base64,{bg_image}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Sidebar - wood grain texture */
    [data-testid="stSidebar"] {{
        background-image: url('data:image/jpeg;base64,{sidebar_image}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}

    /* Make sidebar content more visible on wood texture */
    [data-testid="stSidebar"] > div:first-child {{
        background-color: rgba(139, 90, 43, 0.85);
        padding: 1rem;
    }}

    /* Sidebar text colors for wood background */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .stMarkdown {{
        color: #FFF8DC !important;
    }}

    /* Main content area - white semi-transparent background */
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}

    /* Metric cards - white background with rounded corners */
    [data-testid="stMetricValue"] {{
        background-color: white;
        border-radius: 10px;
        padding: 10px;
    }}

    [data-testid="stMetric"] {{
        background-color: white;
        border-radius: 10px;
        padding: 15px;
    }}

    /* Info/warning/error boxes with rounded corners */
    .stAlert {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 10px !important;
    }}

    /* Expander sections with rounded corners */
    .streamlit-expanderHeader {{
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
    }}

    .streamlit-expanderContent {{
        border-radius: 0 0 10px 10px;
    }}

    /* Expander titles - make them white with aggressive universal selector */
    .streamlit-expanderHeader *,
    .streamlit-expanderHeader,
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] label,
    details summary,
    details > summary > div {{
        color: #FFFFFF !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7) !important;
    }}

    /* Expander content text ONLY - make white without affecting main content */
    [data-testid="stExpander"] p,
    [data-testid="stExpander"] li,
    [data-testid="stExpander"] span,
    [data-testid="stExpander"] strong,
    [data-testid="stExpander"] h3,
    [data-testid="stExpander"] h4,
    [data-testid="stExpander"] code,
    details[open] p,
    details[open] li,
    details[open] span {{
        color: #FFFFFF !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.6) !important;
    }}

    /* Keep main content text dark for readability on white background */
    .main [data-testid="stMarkdownContainer"]:not([data-testid="stExpander"] [data-testid="stMarkdownContainer"]) p,
    .main .stAlert p {{
        color: #333333 !important;
        text-shadow: none !important;
    }}

    /* Plotly chart with rounded corners */
    [data-testid="stPlotlyChart"] {{
        border-radius: 10px;
        overflow: hidden;
    }}

    [data-testid="stPlotlyChart"] > div {{
        border-radius: 10px;
    }}

    /* Make ALL titles white with shadow for forest background */
    h1, .main h1, [data-testid="stMarkdownContainer"] h1 {{
        color: #FFFFFF !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7) !important;
    }}

    h2, .main h2, [data-testid="stMarkdownContainer"] h2 {{
        color: #FFFFFF !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7) !important;
    }}

    h3, .main h3, [data-testid="stMarkdownContainer"] h3 {{
        color: #FFFFFF !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7) !important;
    }}
</style>
""", unsafe_allow_html=True)

# Recovery function
def recover_carbon(initial_carbon, years, k=0.12):
    """
    Calculate carbon recovery using exponential approach to equilibrium.

    Args:
        initial_carbon: Starting carbon stock (Mg C/ha)
        years: Years of recovery
        k: Recovery coefficient per 5-year period (default 0.12)

    Returns:
        Final carbon stock after recovery
    """
    carbon = initial_carbon
    periods = years // 5
    for _ in range(periods):
        carbon = carbon + k * (300 - carbon)
    return carbon

def simulate_logging(operations):
    """
    Simulate logging operations and forest recovery over 100 years.

    Args:
        operations: List of tuples (year, intensity_pct)

    Returns:
        DataFrame with Year, Baseline, Your_Logging, Difference columns
    """
    years = list(range(0, 101, 5))
    baseline = [300.0] * len(years)
    your_logging = [300.0]  # Start at equilibrium

    for i in range(1, len(years)):
        current_year = years[i]
        prev_carbon = your_logging[-1]

        # Check if logging occurs this year
        logged = False
        for log_year, intensity in operations:
            if current_year == log_year and intensity > 0:
                # Apply logging
                your_logging.append(prev_carbon * (1 - intensity/100))
                logged = True
                break

        if not logged:
            # No logging, just recovery
            recovery_years = 5
            new_carbon = recover_carbon(prev_carbon, recovery_years)
            your_logging.append(new_carbon)

    df = pd.DataFrame({
        'Year': years,
        'Baseline': baseline,
        'Your_Logging': your_logging,
        'Difference': [y - b for y, b in zip(your_logging, baseline)]
    })

    return df

def calculate_score(df, operations):
    """
    Calculate final score using 2-tier penalty system.

    Args:
        df: DataFrame with simulation results
        operations: List of logging operations

    Returns:
        Dictionary with scoring details
    """
    final_carbon = df['Your_Logging'].iloc[-1]

    # Calculate total wood harvested
    # Need to recalculate based on carbon BEFORE logging, not after
    total_harvested = 0
    carbon = 300.0  # Start at equilibrium

    for i in range(1, len(df)):
        current_year = df['Year'].iloc[i]

        # Check if logging occurs this year
        for log_year, intensity in operations:
            if current_year == log_year and intensity > 0:
                # Harvest based on carbon BEFORE logging
                harvested = carbon * (intensity / 100)
                total_harvested += harvested
                # Update carbon after logging
                carbon = carbon * (1 - intensity / 100)
                break
        else:
            # No logging, just recovery
            carbon = recover_carbon(carbon, 5)


    wood_products = total_harvested * 0.4  # 40% long-term storage
    base_score = wood_products * 2

    # New scoring system: Bonus for sustainable, penalty for moderate, GAME OVER for severe
    if final_carbon < 270:  # <90%
        penalty = 0
        bonus = 0
        final_score = 0  # GAME OVER
        status = "❌ GAME OVER - Severe Degradation (<90%)"
        status_color = "red"
    elif final_carbon < 291:  # <97%
        penalty = -40
        bonus = 0
        final_score = base_score + penalty
        status = "⚠️ Moderate Degradation (<97%)"
        status_color = "orange"
    else:  # ≥97%
        penalty = 0
        bonus = 10
        final_score = base_score + bonus
        status = "✅ Sustainable (≥97%)"
        status_color = "green"

    return {
        'final_carbon': final_carbon,
        'pct_baseline': (final_carbon / 300) * 100,
        'total_harvested': total_harvested,
        'wood_products': wood_products,
        'base_score': base_score,
        'penalty': penalty,
        'bonus': bonus,
        'final_score': final_score,
        'status': status,
        'status_color': status_color
    }

# Scenario descriptions
SCENARIOS = {
    "Amazon Basin (Brazil)": {
        "description": "FSC-certified concession with high-value mahogany and hardwoods. High environmental scrutiny.",
        "context": "Premium timber markets, international certification requirements",
        "intensities": [15, 25, 35],
        "icon": "🌳"
    },
    "SE Asian Dipterocarp (Borneo)": {
        "description": "Steep terrain with high erosion risk. Critical orangutan habitat. REDD+ credits available.",
        "context": "Difficult terrain, biodiversity concerns, carbon credit opportunities",
        "intensities": [15, 20, 30],
        "icon": "🌴"
    },
    "Congo Basin (Central Africa)": {
        "description": "Remote location with minimal infrastructure. Important wildlife corridor.",
        "context": "High extraction costs, low accessibility, conservation priorities",
        "intensities": [10, 20, 35],
        "icon": "🦍"
    },
    "Central America (Costa Rica/Panama)": {
        "description": "Biological corridor with high ecotourism value. PES payments available.",
        "context": "Tourism revenue, ecosystem services payments, environmental protection",
        "intensities": [10, 20, 30],
        "icon": "🐒"
    }
}

# App title and introduction
st.title("🌴 Tropical Forest Logging Simulator")
st.markdown("### Interactive Tool for Exploring Reduced-Impact Logging Trade-offs")

st.info("""
**Context:** Old-growth tropical rainforest at equilibrium (300 Mg C/ha).
**Your Goal:** Design a logging strategy that balances timber extraction with forest conservation. If your Final Carbon is below 97% or 90% of the Baseline, you will lose certification (e.g. FSC) and funding (e.g. REDD+), affecting your score.
**Scoring:**
- ≥97%: (Wood Products × 2) + 10 bonus ✅
- <97%: (Wood Products × 2) - 40 penalty ⚠️
- <90%: GAME OVER (0 points) ❌
""")

# Sidebar - Scenario Selection
st.sidebar.header("📍 Select Your Scenario")
scenario_name = st.sidebar.selectbox(
    "Choose a region:",
    list(SCENARIOS.keys())
)

scenario = SCENARIOS[scenario_name]
st.sidebar.markdown(f"### {scenario['icon']} {scenario_name}")
st.sidebar.markdown(f"**Context:** {scenario['description']}")
st.sidebar.markdown(f"*{scenario['context']}*")

st.sidebar.divider()

# Sidebar - Logging Operations
st.sidebar.header("🪓 Design Your Logging Plan")
st.sidebar.markdown("**Recommended intensities for this scenario:**")
st.sidebar.markdown(f"Low: {scenario['intensities'][0]}% | Medium: {scenario['intensities'][1]}% | High: {scenario['intensities'][2]}%")

operations = []

for i in range(1, 4):
    st.sidebar.markdown(f"#### Logging Operation {i}")
    col1, col2 = st.sidebar.columns(2)

    # Default values for three 10% operations
    default_years = {1: 10, 2: 40, 3: 70}
    default_intensities = {1: 10, 2: 10, 3: 10}

    with col1:
        year = st.slider(
            f"Year {i}",
            min_value=0,
            max_value=95,
            value=default_years.get(i, 0),
            step=5,
            key=f"year_{i}"
        )

    with col2:
        intensity = st.slider(
            f"Intensity % {i}",
            min_value=0,
            max_value=40,
            value=default_intensities.get(i, 0),
            step=5,
            key=f"intensity_{i}"
        )

    if year > 0 and intensity > 0:
        operations.append((year, intensity))

# Run simulation
df = simulate_logging(operations)
score_data = calculate_score(df, operations)

# Main content area - Results
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Final Carbon",
        f"{score_data['final_carbon']:.1f} Mg/ha",
        f"{score_data['pct_baseline']:.1f}% of baseline"
    )

with col2:
    st.metric(
        "Wood Products",
        f"{score_data['wood_products']:.1f} Mg C/ha",
        f"Base: {score_data['base_score']:.1f} pts"
    )

with col3:
    # Show bonus or penalty
    modifier_value = score_data['bonus'] if score_data['bonus'] > 0 else score_data['penalty']
    modifier_label = "Bonus" if score_data['bonus'] > 0 else "Penalty"
    st.metric(
        modifier_label,
        f"{modifier_value:+d} points" if modifier_value != 0 else "0 points",
        score_data['status']
    )

with col4:
    st.metric(
        "FINAL SCORE",
        f"{score_data['final_score']:.1f}",
        "🏆" if score_data['final_score'] > 60 else ""
    )

# Status indicator
if score_data['status_color'] == "green":
    st.success(f"✅ {score_data['status']}")
elif score_data['status_color'] == "orange":
    st.warning(f"⚠️ {score_data['status']}")
else:
    st.error(f"❌ {score_data['status']}")

# Chart
st.markdown("### 📊 Forest Carbon Dynamics Over 100 Years")

fig = go.Figure()

# Baseline
fig.add_trace(go.Scatter(
    x=df['Year'],
    y=df['Baseline'],
    mode='lines',
    name='Baseline (No Logging)',
    line=dict(color='green', width=3),
    hovertemplate='Year %{x}<br>Carbon: %{y:.1f} Mg/ha<extra></extra>'
))

# Your logging
fig.add_trace(go.Scatter(
    x=df['Year'],
    y=df['Your_Logging'],
    mode='lines+markers',
    name='Your Logging Strategy',
    line=dict(color='darkorange', width=3),
    marker=dict(size=6),
    hovertemplate='Year %{x}<br>Carbon: %{y:.1f} Mg/ha<extra></extra>'
))

# Add markers for logging events
for year, intensity in operations:
    carbon_at_event = df[df['Year'] == year]['Your_Logging'].values[0]
    fig.add_annotation(
        x=year,
        y=carbon_at_event,
        text=f"{intensity}% cut",
        showarrow=True,
        arrowhead=2,
        arrowcolor="red",
        ax=0,
        ay=-40
    )

# Threshold lines
fig.add_hline(y=291, line_dash="dash", line_color="orange",
              annotation_text="97% threshold", annotation_position="right")
fig.add_hline(y=270, line_dash="dash", line_color="red",
              annotation_text="90% threshold", annotation_position="right")

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Aboveground Carbon (Mg C/ha)",
    yaxis=dict(range=[0, 350]),
    height=500,
    hovermode='x unified',
    legend=dict(
        yanchor="bottom",
        y=0.01,
        xanchor="left",
        x=0.01,
        bgcolor="rgba(255, 255, 255, 0.9)"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(size=12, color='#333333')
)

st.plotly_chart(fig, use_container_width=True)

# Strategy comparison
with st.expander("📈 Compare with Optimal Strategies"):
    st.markdown("### How does your strategy compare?")

    comparison_strategies = [
        ("Two 25% (Years 10, 55)", [(10, 25), (55, 25)]),
        ("Two 20% (Years 10, 55)", [(10, 20), (55, 20)]),
        ("One 25% (Year 10)", [(10, 25)]),
        ("One 35% (Year 10)", [(10, 35)]),
        ("Three 15% (Years 10, 45, 80)", [(10, 15), (45, 15), (80, 15)])
    ]

    comparison_data = []
    for name, ops in comparison_strategies:
        sim_df = simulate_logging(ops)
        score = calculate_score(sim_df, ops)
        comparison_data.append({
            'Strategy': name,
            'Final Carbon (Mg)': f"{score['final_carbon']:.1f}",
            '% Baseline': f"{score['pct_baseline']:.1f}%",
            'Wood Products': f"{score['wood_products']:.1f}",
            'Penalty': score['penalty'],
            'Score': f"{score['final_score']:.1f}"
        })

    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, width='stretch')

# Educational content
with st.expander("📚 Learn About the Science"):
    st.markdown("""
    ### Old-Growth Tropical Forest Dynamics

    **Why is the baseline flat at 300 Mg C/ha?**
    - Old-growth forests are in **dynamic equilibrium**
    - Tree growth = Tree mortality
    - Carbon uptake = Carbon loss (respiration, decomposition)
    - **Old-growth forests are NOT net carbon sinks!**

    ### Very Slow Recovery

    **Recovery Model:** C(t+5) = C(t) + 0.12 × (300 - C(t))

    After 25% logging (300 → 225 Mg C/ha):
    - Year 25: ~245 Mg (27% recovered)
    - Year 50: ~267 Mg (56% recovered)
    - Year 75: ~283 Mg (77% recovered)
    - Year 100: ~294 Mg (92% recovered)

    **Why so slow?**
    - Soil compaction from machinery
    - Changed microclimate conditions
    - Slow-growing hardwood species
    - Pioneer species must be replaced by climax species

    ### 2-Tier Penalty System

    **Score = (Wood Products × 2) - Penalty**

    - **≥97% (291 Mg):** ✅ No penalty (sustainable)
    - **<97% (291 Mg):** ⚠️ -40 points (moderate degradation)
    - **<90% (270 Mg):** ❌ -80 points (severe degradation)

    This system:
    - Rewards **sustained yield** through multiple moderate entries
    - Penalizes single heavy extraction
    - Heavily penalizes aggressive strategies
    """)

# Sidebar - Additional info
st.sidebar.divider()
st.sidebar.markdown("### 💡 Tips")
st.sidebar.info("""
**Experiment and find the best strategy!**

Try different combinations:
- Single vs. multiple logging entries
- Light vs. heavy intensity
- Early vs. late timing
- Spacing between operations
""")

st.sidebar.markdown("### 🎯 Score Ranges")
st.sidebar.markdown("""
- **70-80:** Excellent! 🌟
- **50-69:** Good
- **40-49:** Fair
- **<40:** Needs improvement
""")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: white; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);'>
        <p style='margin-bottom: 0.2rem;'>Developed by</p>
        <p style='margin-bottom: 0.2rem;'><strong>Rafael B. de Andrade</strong></p>
        <p style='margin-bottom: 0.2rem;'>Assistant Professor of Environmental Studies</p>
        <p style='margin-bottom: 0.2rem;'>St. Mary's College of Maryland</p>
        <p style='margin-bottom: 0;'><a href='mailto:rbdeandrade@smcm.edu' style='color: #90EE90; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);'>rbdeandrade@smcm.edu</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
