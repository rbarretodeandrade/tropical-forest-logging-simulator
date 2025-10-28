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
        background-color: rgba(139, 90, 43, 0.3);
        padding: 1rem;
    }}

    /* Sidebar text colors for wood background */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .stMarkdown {{
        color: #FFF8DC !important;
    }}

    /* Make sidebar sliders white/light colored */
    [data-testid="stSidebar"] .stSlider > div > div > div {{
        background-color: rgba(255, 255, 255, 0.3) !important;
    }}

    [data-testid="stSidebar"] .stSlider > div > div > div > div {{
        background-color: #FFFFFF !important;
    }}

    /* Slider thumb (the draggable circle) */
    [data-testid="stSidebar"] input[type="range"]::-webkit-slider-thumb {{
        background-color: #FFFFFF !important;
    }}

    [data-testid="stSidebar"] input[type="range"]::-moz-range-thumb {{
        background-color: #FFFFFF !important;
    }}

    /* Slider labels (Year 1, Intensity % 1, etc.) - make white */
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stSlider p {{
        color: #FFFFFF !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7) !important;
    }}

    /* Slider value numbers - make white */
    [data-testid="stSidebar"] .stSlider [data-baseweb="slider"] {{
        color: #FFFFFF !important;
    }}

    [data-testid="stSidebar"] .stSlider div[role="slider"] {{
        color: #FFFFFF !important;
    }}

    /* Slider tick labels and current value - make white */
    [data-testid="stSidebar"] .stSlider [data-baseweb="tick-bar"] span,
    [data-testid="stSidebar"] .stSlider [data-baseweb="thumb-value"],
    [data-testid="stSidebar"] .stSlider div div div span,
    [data-testid="stSidebar"] .stSlider span,
    [data-testid="stSidebar"] .stSlider * {{
        color: #FFFFFF !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7) !important;
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
def recover_carbon(initial_carbon, years, k_annual=0.0825):
    """
    Calculate carbon recovery using exponential approach to equilibrium.

    Args:
        initial_carbon: Starting carbon stock (Mg C/ha)
        years: Years of recovery
        k_annual: Recovery coefficient per year (default 0.0825)
            Equivalent to 0.33 per 5-year period
            Based on literature: 25% cut recovers to 95% in ~20 years

    Returns:
        Final carbon stock after recovery
    """
    carbon = initial_carbon
    for _ in range(years):
        carbon = carbon + k_annual * (300 - carbon)
    return carbon

def simulate_logging(operations):
    """
    Simulate logging operations and forest recovery over 25 years.
    Logging operations take 1 year to complete - impact appears the year AFTER.

    Args:
        operations: List of tuples (year, intensity_pct)

    Returns:
        DataFrame with Year, Baseline, Your_Logging, Difference columns
    """
    years = list(range(0, 26))
    baseline = [300.0] * len(years)
    your_logging = [300.0]  # Start at equilibrium

    for i in range(1, len(years)):
        current_year = years[i]
        prev_year = years[i-1]
        prev_carbon = your_logging[-1]

        # Check if logging started in the PREVIOUS year (takes 1 year to complete)
        logged = False
        for log_year, intensity in operations:
            if prev_year == log_year and intensity > 0:
                # Apply logging impact after 1-year operation
                your_logging.append(prev_carbon * (1 - intensity/100))
                logged = True
                break

        if not logged:
            # No logging, just recovery for 1 year
            new_carbon = recover_carbon(prev_carbon, 1)
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
    # Logging operations take 1 year - impact appears the year AFTER
    total_harvested = 0
    carbon = 300.0  # Start at equilibrium

    for i in range(1, len(df)):
        current_year = df['Year'].iloc[i]
        prev_year = df['Year'].iloc[i-1]

        # Check if logging started in the PREVIOUS year
        logged = False
        for log_year, intensity in operations:
            if prev_year == log_year and intensity > 0:
                # Harvest based on carbon BEFORE logging
                harvested = carbon * (intensity / 100)
                total_harvested += harvested
                # Update carbon after logging
                carbon = carbon * (1 - intensity / 100)
                logged = True
                break

        if not logged:
            # No logging, just recovery for 1 year
            carbon = recover_carbon(carbon, 1)


    wood_products = total_harvested * 0.4  # 40% long-term storage
    base_score = wood_products * 1.2

    # New scoring system: Bonus for sustainable, penalty for moderate, GAME OVER for severe
    if final_carbon < 270:  # <90%
        penalty = 0
        bonus = 0
        final_score = 0  # GAME OVER
        status = "❌ GAME OVER - Severe Degradation (<90%)"
        status_color = "red"
    elif final_carbon < 285:  # <95%
        penalty = -30
        bonus = 0
        final_score = base_score + penalty
        status = "⚠️ Moderate Degradation (<95%)"
        status_color = "orange"
    else:  # ≥95%
        penalty = 0
        bonus = 10
        final_score = base_score + bonus
        status = "✅ Sustainable (≥95%)"
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

# App title and introduction
st.title("🌴 Tropical Forest Logging Simulator")
st.markdown("### Interactive Tool for Exploring Reduced-Impact Logging Trade-offs")

st.info("""
Welcome to the Tropical Forest Logging Simulator! Your goal is to design a logging strategy that balances timber extraction with forest conservation. Using the sliders in the sidebar, plan **at least two logging operations** to be done over the next 25 years (a third operation is optional). This represents a sustainable business model with repeated entries rather than one-time extraction. The more timber you extract, the more points you get, but there's a catch - if your final carbon stocks after 25 years is below 95% or 90% of the 300 Mg C/ha baseline of a stable old-growth forest, you will lose certification (e.g. FSC) and funding (e.g. REDD+), affecting your score. Can you make a profit and still preserve the tropical forest carbon stocks?

**Scoring:**
- ≥95%: (Wood Products × 1.2) + 10 bonus ✅
- <95%: (Wood Products × 1.2) - 30 penalty ⚠️
- <90%: GAME OVER (0 points) ❌
""")

# Sidebar - Logging Operations
st.sidebar.header("🪓 Design Your Logging Plan")
st.sidebar.markdown("**Use any intensity from 5% to 25%**")

operations = []

for i in range(1, 4):
    st.sidebar.markdown(f"#### Logging Operation {i}")
    col1, col2 = st.sidebar.columns(2)

    # Default values for operations
    default_years = {1: 0, 2: 10, 3: 15}
    default_intensities = {1: 10, 2: 10, 3: 0}

    # Set minimum constraints per operation
    if i == 1:
        min_year = 0
        min_intensity = 5
    elif i == 2:
        min_year = 5
        min_intensity = 5
    else:  # i == 3
        min_year = 15
        min_intensity = 0

    with col1:
        year = st.slider(
            "Year",
            min_value=min_year,
            max_value=20,
            value=default_years.get(i, min_year),
            step=5,
            key=f"year_{i}"
        )

    with col2:
        intensity = st.slider(
            "Intensity %",
            min_value=min_intensity,
            max_value=25,
            value=default_intensities.get(i, min_intensity),
            step=5,
            key=f"intensity_{i}"
        )

    if intensity > 0:
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
        "🏆" if score_data['final_score'] > 50 else ""
    )

# Status indicator
if score_data['status_color'] == "green":
    st.success(f"✅ {score_data['status']}")
elif score_data['status_color'] == "orange":
    st.warning(f"⚠️ {score_data['status']}")
else:
    st.error(f"❌ {score_data['status']}")

# Chart
st.markdown("### 📊 Forest Carbon Dynamics Over 25 Years")

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

# Add markers for logging events (impact appears year+1 after operation starts)
for year, intensity in operations:
    impact_year = year + 1  # Logging takes 1 year to complete
    if impact_year < len(df):
        carbon_at_event = df[df['Year'] == impact_year]['Your_Logging'].values[0]
        fig.add_annotation(
            x=impact_year,
            y=carbon_at_event,
            text=f"{intensity}% cut",
            showarrow=True,
            arrowhead=2,
            arrowcolor="red",
            ax=0,
            ay=-40
        )

# Threshold lines
fig.add_hline(y=285, line_dash="dash", line_color="orange",
              annotation_text="95% threshold", annotation_position="right")
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

# Educational content
with st.expander("📚 Learn About the Science"):
    st.markdown("""
    ### Old-Growth Tropical Forest Dynamics

    **Why is the baseline flat at 300 Mg C/ha?**
    - Old-growth forests are in **dynamic equilibrium**
    - Tree growth = Tree mortality
    - Carbon uptake = Carbon loss (respiration, decomposition)
    - **Old-growth forests are NOT net carbon sinks!**

    **About the 300 Mg C/ha baseline:**
    - Represents **high-biomass old-growth tropical rainforests**
    - Central Amazon: typically **300-400 Mg C/ha** in intact forests
    - SE Asian dipterocarp forests: **215-320 Mg C/ha** aboveground living biomass
    - Basin-wide averages are lower (~150-250 Mg C/ha) but our scenarios focus on
      high-value, old-growth forest concessions
    - Regional variation depends on soil type, rainfall, elevation, and species composition

    ### Recovery Timeline After Logging

    **Recovery Model:** C(t+1) = C(t) + 0.0825 × (300 - C(t))

    This exponential recovery model is based on scientific literature showing that tropical
    forests recover **slowly** after reduced-impact logging:

    **Example: After 25% logging (300 → 225 Mg C/ha):**
    - Year 1: ~231 Mg (8% recovered)
    - Year 5: ~250 Mg (33% recovered)
    - Year 10: ~267 Mg (56% recovered)
    - Year 20: ~285 Mg (80% recovered - reaches 95% threshold!)
    - Year 25: ~290 Mg (87% recovered)

    **Recovery rates from peer-reviewed research:**
    - **10% biomass loss:** ~10 years to reach 95% of original carbon
    - **25% biomass loss:** ~20 years to reach 95% of original carbon
    - Annual carbon accumulation: **1.8-4.5 tC/ha/year** (site-dependent)
    - Recovery slows as forest approaches equilibrium (asymptotic pattern)

    **Key findings:**
    - Most studies with <25% initial loss show recovery within **10-20 years**
    - **Logging intensity** is the primary predictor of recovery time
    - Current cutting cycles (30-35 years) may be **too short** for full recovery
    - Even with biomass regrowth, logged forests remain **net carbon sources** for ≥10 years

    **Why is recovery slow?**
    - **Soil compaction** from heavy logging machinery reduces growth rates
    - **Canopy gaps** alter microclimate (temperature, humidity, light)
    - **Slow-growing hardwood species** dominate old-growth forests
    - **Succession dynamics:** Fast-growing pioneers must be replaced by climax species
    - **Infrastructure damage:** Roads and skid trails reduce productive forest area
    - **Deadwood decomposition:** Continued CO₂ emissions from logging debris for 10+ years

    **References:**
    - Saatchi et al. (2007). "Distribution of aboveground live biomass in the Amazon basin."
      *Global Change Biology* 13(4):816-837. [Central Amazon: 300-400 Mg C/ha]
    - Paoli et al. (2008). "Soil nutrients affect spatial patterns of aboveground biomass
      and emergent tree density in southwestern Borneo." *Oecologia* 155:287-299.
    - Nugroho et al. (2019). "Carbon recovery following selective logging in tropical
      rainforests in Kalimantan, Indonesia." *Forest Ecosystems* 6:37.
    - Fischer et al. (2021). "Scenarios in tropical forest degradation: carbon stock
      trajectories for REDD+." *Carbon Balance and Management* 12:6.
    - Macpherson et al. (2012). "Natural regeneration of tropical forests following
      logging." *Philosophical Transactions B* 367:1790-1801.

    ### 2-Tier Penalty System

    **Score = (Wood Products × 1.2) + Bonus/Penalty**

    - **≥95% (285 Mg):** ✅ +10 bonus (sustainable)
    - **<95% (285 Mg):** ⚠️ -30 penalty (moderate degradation)
    - **<90% (270 Mg):** ❌ GAME OVER (0 points - severe degradation)

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
- Two vs. three logging entries
- Light vs. heavy intensity
- Early vs. late timing
- Spacing between operations

Remember: Sustained yield requires repeat entries!
""")

st.sidebar.markdown("### 🎯 Score Ranges")
st.sidebar.markdown("""
- **50-60:** Excellent! 🌟
- **40-49:** Good
- **30-39:** Fair
- **<30:** Needs improvement
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
