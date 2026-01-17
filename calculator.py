import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# ============================================================================
# PAGE SETUP
# ============================================================================
# Configure the Streamlit page settings (must be first Streamlit command)
st.set_page_config(
    page_title="SCP Scale-Up Calculator",  # Browser tab title
    page_icon="🔬",  # Browser tab icon
    layout="wide"  # Use full width of browser
)

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================

st.markdown("""
<style>
    /* ===== SIDEBAR COMPACT ===== */
    /* Remove gaps between sidebar elements */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
        gap: 0rem !important;
    }
    /* Make sliders more compact */
    [data-testid="stSidebar"] .stSlider {
        padding-top: 0rem !important;
        padding-bottom: 0.2rem !important;
        margin-bottom: 0rem !important;
    }
    /* Remove extra spacing from sidebar elements */
    [data-testid="stSidebar"] .element-container {
        margin-bottom: 0rem !important;
        margin-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-top: 0rem !important;
    }
    /* Make sidebar headers smaller */
    [data-testid="stSidebar"] h2 {
        margin-top: 0.3rem !important;
        margin-bottom: 0.2rem !important;
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        font-size: 1rem !important;
    }
    /* Compact divider lines in sidebar */
    [data-testid="stSidebar"] hr {
        margin-top: 0.2rem !important;
        margin-bottom: 0.2rem !important;
    }
    /* Compact dropdown boxes */
    [data-testid="stSidebar"] .stSelectbox {
        margin-bottom: 0rem !important;
        padding-bottom: 0rem !important;
    }
    /* Reduce top padding of sidebar */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem !important;
    }
    /* Compact slider labels */
    [data-testid="stSidebar"] .stSlider label {
        margin-bottom: 0.1rem !important;
    }
    /* Compact all form element labels */
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stNumberInput label {
        margin-bottom: 0.1rem !important;
    }
    
    /* ===== MAIN CONTENT EXTREMELY COMPACT ===== */
    /* Remove spacing from main content elements */
    .main .element-container {
        margin-bottom: 0rem !important;
        margin-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-top: 0rem !important;
    }
    /* Compact metric cards */
    [data-testid="stMetric"] {
        padding: 0.2rem 0.5rem !important;
    }
    [data-testid="stMetricLabel"] {
        padding-bottom: 0rem !important;
        margin-bottom: 0rem !important;
    }
    [data-testid="stMetricValue"] {
        padding-top: 0rem !important;
        margin-top: 0rem !important;
    }
    /* Compact main headers */
    .main h1 {
        margin-bottom: 0.2rem !important;
        margin-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-top: 0rem !important;
        line-height: 1.2 !important;
    }
    .main h2 {
        margin-top: 0.2rem !important;
        margin-bottom: 0.2rem !important;
        padding: 0rem !important;
        line-height: 1.2 !important;
    }
    .main h3 {
        margin-top: 0.1rem !important;
        margin-bottom: 0.1rem !important;
        padding: 0rem !important;
        line-height: 1.2 !important;
    }
    /* Compact divider lines */
    .main hr {
        margin-top: 0.3rem !important;
        margin-bottom: 0.3rem !important;
    }
    /* Reduce gap between columns */
    [data-testid="stHorizontalBlock"] {
        gap: 0.3rem !important;
    }
    /* Compact tabs */
    [data-testid="stTabs"] {
        margin-top: 0.2rem !important;
        margin-bottom: 0rem !important;
    }
    [data-testid="stTabContent"] {
        padding-top: 0.3rem !important;
        padding-bottom: 0rem !important;
    }
    /* Compact markdown text */
    .main .stMarkdown {
        margin-bottom: 0rem !important;
        margin-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-top: 0rem !important;
    }
    .main .stMarkdown p {
        margin-bottom: 0.2rem !important;
        margin-top: 0rem !important;
    }
    /* Compact charts */
    .main .stPlotlyChart {
        margin-top: 0rem !important;
        margin-bottom: 0rem !important;
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }
    /* Reduce main page top padding */
    .main > div {
        padding-top: 0.5rem !important;
    }
    /* Remove gaps in vertical layouts */
    .main [data-testid="stVerticalBlock"] {
        gap: 0rem !important;
    }
    /* Compact paragraphs */
    .main p {
        margin-bottom: 0.1rem !important;
        margin-top: 0rem !important;
    }
    /* Compact lists */
    .main ul, .main ol {
        margin-top: 0rem !important;
        margin-bottom: 0.2rem !important;
        padding-top: 0rem !important;
    }
    .main li {
        margin-bottom: 0.1rem !important;
    }
    /* Compact alert messages */
    .main .stSuccess, .main .stWarning, .main .stError {
        padding: 0.3rem 0.5rem !important;
        margin-top: 0.2rem !important;
        margin-bottom: 0.2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# PAGE TITLE AND HEADER
# ============================================================================
st.title("🔬 Single Cell Protein (SCP) Scale-Up Analysis")
st.markdown("**Interactive tool for bioprocess optimization and the economic analysis**")
st.markdown("*By Susi | ⚠️ For demonstration purposes only*")
st.markdown("---") 

# ============================================================================
# ENGINEERING CONSTANTS
# ============================================================================
# These are fixed values based on literature and industry standards
# They represent typical bioprocess parameters
CONSTANTS = {
    'reactor_volume_L': 100_000,  # 100 m³ working volume (standard industrial size)
    'operating_hours_year': 8000,  # 91% uptime (allows for maintenance/downtime)
    'substrate_price_per_kg': 0.50,  # USD/kg (glucose - typical market price)
    'electricity_price': 0.12,  # USD/kWh (industrial electricity rate)
    'grid_emission_factor': 0.07,  # kg CO2 / kWh (renewable grid assumption)
    'mixing_power_per_m3': 1.0,  # kW/m³ (power needed to mix the bioreactor)
    'heat_per_kg_biomass': 4000,  # kcal/kg (metabolic heat generated)
    'cooling_water_base': 20,  # L/kg protein (base cooling water requirement)
    'reactor_base_cost': 6,  # Million USD for 100m³ reactor
    'scaling_exponent': 0.6,  # Six-tenths rule for equipment cost scaling
    'operators_per_reactor': 0.5,  # operators/reactor/shift (industry standard)
    'operator_salary_year': 60_000,  # USD/year per operator
    'base_footprint_m2': 500,  # m² for first reactor (includes utilities)
    'additional_reactor_footprint': 400,  # m² for each additional reactor
}

# ============================================================================
# SIDEBAR - USER INPUT PARAMETERS
# ============================================================================
# This section creates interactive sliders for users to adjust parameters

# --- Fermentation Parameters Section ---
st.sidebar.header("⚙️ Fermentation Parameters")

# Maximum specific growth rate (how fast cells grow)
mu_max = st.sidebar.slider(
    "Max Growth Rate μmax (h⁻¹)",  # Label shown to user
    min_value=0.20,  # Minimum slider value
    max_value=0.60,  # Maximum slider value
    value=0.45,  # Default starting value
    step=0.01,  # How much each slider increment changes
    help="Typical range: 0.2-0.6 h⁻¹ for bacteria (Bailey & Ollis, 1986)"  # Tooltip text
)

# Biomass yield (how efficiently substrate converts to biomass)
Yx_s = st.sidebar.slider(
    "Biomass Yield Yx/s (g/g)",
    min_value=0.40,
    max_value=0.60,
    value=0.52,
    step=0.01,
    help="Biomass yield on substrate (Roels, 1983)"
)

# Protein content (percentage of dry biomass that is protein)
protein_content_pct = st.sidebar.slider(
    "Protein Content (%)",
    min_value=50,
    max_value=80,
    value=65,
    step=1,
    help="Protein as % of dry biomass (Ritala et al., 2017)"
)

# Final biomass concentration achieved
final_biomass = st.sidebar.slider(
    "Final Biomass (g/L)",
    min_value=50.0,
    max_value=95.0,
    value=70.0,
    step=0.1,
    help="High cell density fed-batch (Ritala et al., 2017)"
)

# How long the fermentation takes
fermentation_time = st.sidebar.slider(
    "Fermentation Time (hours)",
    min_value=35,
    max_value=55,
    value=42,
    step=1,
    help="Typical fed-batch cycle: 35-55 hours"
)

st.sidebar.markdown("---")  # Visual separator between sections

# --- Production Parameters Section ---
st.sidebar.header("🏭 Production Parameters")

# Annual protein production target
target_production = st.sidebar.slider(
    "Target Production (tons protein/year)",
    min_value=100,
    max_value=5000,
    value=1000,
    step=100
)

# Size of each bioreactor
reactor_volume = st.sidebar.selectbox(
    "Reactor Volume (m³)",
    options=[10, 50, 100, 200, 500],  # Available reactor sizes
    index=2,  # Default selection (100 m³)
    help="Standard industrial bioreactor sizes"
)

st.sidebar.markdown("---")  # Visual separator

# --- Economic Parameters Section ---
st.sidebar.header("💰 Economic Parameters")

# Cost of glucose (main carbon source)
substrate_price = st.sidebar.slider(
    "Substrate Price ($/kg)",
    min_value=0.20,
    max_value=1.50,
    value=CONSTANTS['substrate_price_per_kg'],  # Use constant as default
    step=0.05,
    help="Glucose: $0.40-0.60/kg; Waste streams: $0.10-0.30/kg"
)

# Cost of electricity for mixing, cooling, etc.
energy_price = st.sidebar.slider(
    "Energy Price ($/kWh)",
    min_value=0.05,
    max_value=0.25,
    value=CONSTANTS['electricity_price'],  # Use constant as default
    step=0.01,
    help="Industrial electricity rates"
)

# ============================================================================
# DERIVED CALCULATIONS - Basic Performance Metrics
# ============================================================================
# These are calculated from the user inputs above

# Calculate protein concentration (g/L)
# Formula: biomass × protein percentage
protein_concentration = final_biomass * (protein_content_pct / 100)

# Calculate biomass productivity (g/L/h)
# Formula: final biomass ÷ time
biomass_productivity = final_biomass / fermentation_time

# Calculate protein productivity (g/L/h) - KEY METRIC
# Formula: protein concentration ÷ time
protein_productivity = protein_concentration / fermentation_time

# ============================================================================
# FED-BATCH SUBSTRATE CALCULATIONS
# ============================================================================
# Fed-batch: substrate is added gradually during fermentation
# This prevents inhibition and achieves higher cell density

S_initial = 35  # g/L - Initial substrate in batch phase
S_total_fed = 165  # g/L - Total substrate added throughout fermentation
S_residual = 5.0  # g/L - Substrate remaining at end (not consumed)

# Calculate actual substrate consumed
substrate_consumed = S_total_fed - S_residual

# Calculate substrate needed per kg of protein produced
# This is a key economic metric
substrate_kg_per_kg_protein = substrate_consumed / protein_concentration

# ============================================================================
# REACTOR SCALE-UP CALCULATIONS
# ============================================================================
# Calculate how many reactors are needed to hit production target

# Convert reactor volume to working volume
working_volume_m3 = reactor_volume * 0.8  # 80% working volume (safety margin)
working_volume_L = working_volume_m3 * 1000  # Convert m³ to liters

# Time between batches
turnaround_time = 24  # hours for cleaning, sterilization, preparation
cycle_time = fermentation_time + turnaround_time  # Total time per batch

# How many batches can we run per year?
batches_per_year = CONSTANTS['operating_hours_year'] / cycle_time

# How much protein per batch?
# Formula: (protein conc in g/L) × (volume in L) ÷ 1000 = kg
protein_per_batch = (protein_concentration * working_volume_L) / 1000  # kg

# Annual capacity of ONE reactor (tons/year)
annual_capacity_per_reactor = protein_per_batch * batches_per_year / 1000  # convert kg to tons

# How many reactors do we need? (round up to nearest whole number)
reactors_needed = np.ceil(target_production / annual_capacity_per_reactor)

# ============================================================================
# ECONOMIC CALCULATIONS - CAPEX (Capital Expenditure)
# ============================================================================
# CAPEX = one-time investment in equipment/facilities

# Use "six-tenths rule" for equipment cost scaling
# Cost scales with size^0.6 (not linearly)
reactor_size_ratio = reactor_volume / 100  # Ratio to base size (100 m³)
capex_per_reactor = CONSTANTS['reactor_base_cost'] * (reactor_size_ratio ** CONSTANTS['scaling_exponent'])

# Total CAPEX = cost per reactor × number of reactors
total_capex = capex_per_reactor * reactors_needed

# ============================================================================
# ECONOMIC CALCULATIONS - OPEX (Operating Expenditure)
# ============================================================================
# OPEX = recurring costs per year

# --- 1. SUBSTRATE COST (usually 60-65% of OPEX) ---
# Cost = (kg substrate / kg protein) × (price per kg substrate)
substrate_cost_per_kg = substrate_kg_per_kg_protein * substrate_price

# --- 2. ENERGY COST ---
# Convert annual capacity to kg for calculations
protein_per_reactor_kg_year = annual_capacity_per_reactor * 1000  # tons to kg

# Mixing energy (kWh per kg protein)
# Formula: (power per m³) × (reactor volume) × (hours per year) ÷ (annual production)
mixing_kwh_per_kg = (
    CONSTANTS['mixing_power_per_m3'] *  # kW/m³ (1.0)
    reactor_volume *  # m³
    CONSTANTS['operating_hours_year']  # h/year (8000)
) / protein_per_reactor_kg_year  # Divide by annual production in kg

# Cooling energy (kWh per kg protein)
# Calculate heat generated from fermentation
heat_generated_kcal_L = final_biomass * CONSTANTS['heat_per_kg_biomass'] / 1000
cooling_kwh_per_kg = heat_generated_kcal_L * 0.001  # Convert kcal to kWh (simplified)

# Total energy consumption per kg protein
total_energy_kwh_per_kg = mixing_kwh_per_kg + cooling_kwh_per_kg

# Energy cost = energy consumed × price per kWh
energy_cost_per_kg = total_energy_kwh_per_kg * energy_price

# --- 3. LABOR COST ---
# Total operators needed = reactors × operators per reactor
total_operators = reactors_needed * CONSTANTS['operators_per_reactor']

# Labor cost per kg = (total operators × salary) ÷ (annual production in kg)
labor_cost_per_kg = (total_operators * CONSTANTS['operator_salary_year']) / (target_production * 1000)

# --- 4. OVERHEAD COST ---
# Overhead includes: maintenance, QA/QC, administration, insurance
# Typically 30-40% of direct costs (substrate + energy + labor)
overhead_cost_per_kg = (substrate_cost_per_kg + energy_cost_per_kg + labor_cost_per_kg) * 0.4

# --- 5. TOTAL OPEX ---
# Sum of all operating costs per kg protein
total_opex_per_kg = substrate_cost_per_kg + energy_cost_per_kg + labor_cost_per_kg + overhead_cost_per_kg

# ============================================================================
# ENVIRONMENTAL IMPACT CALCULATIONS
# ============================================================================

# --- GHG (Greenhouse Gas) Emissions ---
# Substrate emissions (from growing/processing glucose)
substrate_emissions = substrate_kg_per_kg_protein * 0.25  # kg CO2 per kg glucose

# Energy emissions (from electricity generation)
energy_emissions = total_energy_kwh_per_kg * CONSTANTS['grid_emission_factor']

# Total GHG emissions per kg protein
total_ghg = substrate_emissions + energy_emissions

# --- Water Use ---
# Calculate heat load to determine cooling water needs
heat_load_factor = heat_generated_kcal_L / 20_000

# Cooling water requirement
cooling_water_L_per_kg = CONSTANTS['cooling_water_base'] * (1 + heat_load_factor * 0.5)

# Process water (for medium preparation, cleaning, etc.)
process_water_L_per_kg = 12

# Total water consumption per kg protein
total_water = cooling_water_L_per_kg + process_water_L_per_kg

# --- Land Use ---
# Calculate factory footprint based on number of reactors
if reactors_needed == 1:
    total_factory_footprint = CONSTANTS['base_footprint_m2']
else:
    # Base footprint + additional space for each extra reactor
    total_factory_footprint = (CONSTANTS['base_footprint_m2'] + 
                              (reactors_needed - 1) * CONSTANTS['additional_reactor_footprint'])

# Land use per kg protein produced
land_use_m2_per_kg = total_factory_footprint / (target_production * 1000)
land_use_cm2_per_kg = land_use_m2_per_kg * 10000  # Convert to cm² for easier reading

# ============================================================================
# DISPLAY RESULTS - TOP METRICS
# ============================================================================
# Create 4 columns for key performance indicators (KPIs)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🏭 Reactors Needed",
        value=f"{int(reactors_needed)}",
        delta=f"{reactor_volume}m³ each"  # Shows reactor size below
    )

with col2:
    st.metric(
        label="💰 Total OPEX",
        value=f"${total_opex_per_kg:.2f}/kg",
        delta=f"${substrate_cost_per_kg:.2f} substrate" if substrate_cost_per_kg > total_opex_per_kg * 0.4 else None
    )

with col3:
    st.metric(
        label="🏗️ CAPEX",
        value=f"${total_capex:.1f}M",
        delta=f"${capex_per_reactor:.1f}M per reactor"
    )

with col4:
    st.metric(
        label="🌍 GHG Emissions",
        value=f"{total_ghg:.2f} kg CO₂eq/kg",
        delta="30× less than beef" if total_ghg < 2.0 else None
    )

st.markdown("---")  # Separator line

# ============================================================================
# DETAILED RESULTS TABS
# ============================================================================
# Create tabs for different analysis views
tab1, tab2, tab3, tab4 = st.tabs(["📊 Cost Breakdown", "🏭 Production Details", "🌍 Environmental Impact", "📈 Benchmarks"])

# --- TAB 1: COST BREAKDOWN ---
with tab1:
    st.subheader("Cost Breakdown")
    
    # Create DataFrame for cost components
    cost_data = pd.DataFrame({
        'Category': ['Substrate', 'Energy', 'Labor', 'Overhead'],
        'Cost ($/kg)': [substrate_cost_per_kg, energy_cost_per_kg, labor_cost_per_kg, overhead_cost_per_kg]
    })
    
    # Create pie chart showing OPEX breakdown
    fig_cost = px.pie(
        cost_data,
        values='Cost ($/kg)',
        names='Category',
        title='OPEX Breakdown',
        hole=0.4  # Makes it a donut chart
    )
    fig_cost.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_cost, use_container_width=True)
    
    # Create 2 columns for detailed cost information
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Cost Components:**")
        # Loop through each cost component and show details
        for idx, row in cost_data.iterrows():
            percentage = (row['Cost ($/kg)'] / total_opex_per_kg) * 100
            st.write(f"- {row['Category']}: ${row['Cost ($/kg)']:.2f}/kg ({percentage:.1f}%)")
    
    with col2:
        st.markdown("**Key Metrics:**")
        st.write(f"- Total OPEX: **${total_opex_per_kg:.2f}/kg**")
        st.write(f"- Annual OPEX: **${(total_opex_per_kg * target_production * 1000 / 1e6):.2f}M**")
        st.write(f"- CAPEX: **${total_capex:.2f}M**")
        
        # Calculate payback period
        selling_price = 10.0  # Assumed selling price in $/kg
        if total_opex_per_kg < selling_price:
            # Annual profit = (selling price - OPEX) × production volume
            annual_profit = (selling_price - total_opex_per_kg) * target_production * 1000
            # Payback = CAPEX ÷ annual profit
            payback_years = (total_capex * 1_000_000) / annual_profit
            
            if payback_years < 20:
                st.write(f"- Payback period: **{payback_years:.1f} years** (assuming ${selling_price}/kg selling price)")
            else:
                st.write(f"- Payback period: **>20 years** (not viable)")
        else:
            st.write(f"- Payback period: **Not viable** (OPEX ${total_opex_per_kg:.2f}/kg > ${selling_price}/kg selling price)")

# --- TAB 2: PRODUCTION DETAILS ---
with tab2:
    st.subheader("Production Details")
    
    # Create 2 columns for fermentation and scale-up info
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Fermentation Performance:**")
        st.write(f"- Max growth rate: {mu_max:.3f} h⁻¹")
        st.write(f"- Biomass yield: {Yx_s:.3f} g/g")
        st.write(f"- Final biomass: {final_biomass:.1f} g/L")
        st.write(f"- Final protein: {protein_concentration:.1f} g/L")
        st.write(f"- Biomass productivity: {biomass_productivity:.2f} g/L/h")
        st.write(f"- Protein productivity: {protein_productivity:.2f} g/L/h")
        st.write(f"- Fermentation time: {fermentation_time}h")
        
    with col2:
        st.markdown("**Scale-Up Parameters:**")
        st.write(f"- Reactor size: {reactor_volume}m³ (working: {working_volume_m3}m³)")
        st.write(f"- Reactors needed: **{int(reactors_needed)}**")
        st.write(f"- Cycle time: {cycle_time}h (ferment + turnaround)")
        st.write(f"- Batches per year: {batches_per_year:.0f}")
        st.write(f"- Protein per batch: {protein_per_batch:.0f} kg")
        st.write(f"- Annual capacity: {annual_capacity_per_reactor * reactors_needed:.0f} tons")

# --- TAB 3: ENVIRONMENTAL IMPACT ---
with tab3:
    st.subheader("Environmental Impact")
    
    # Create 2 columns for chart and metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**GHG Emissions Breakdown:**")
        # Create DataFrame for GHG sources
        ghg_data = pd.DataFrame({
            'Source': ['Substrate Production', 'Energy Use'],
            'Emissions (kg CO₂eq/kg)': [substrate_emissions, energy_emissions]
        })
        
        # Create bar chart
        fig_ghg = px.bar(
            ghg_data,
            x='Source',
            y='Emissions (kg CO₂eq/kg)',
            title='GHG Emissions by Source',
            text='Emissions (kg CO₂eq/kg)'
        )
        fig_ghg.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        st.plotly_chart(fig_ghg, use_container_width=True)
    
    with col2:
        st.markdown("**Environmental Metrics:**")
        st.write(f"- **Total GHG:** {total_ghg:.2f} kg CO₂eq/kg protein")
        st.write(f"  - Substrate: {substrate_emissions:.2f} kg ({substrate_emissions/total_ghg*100:.0f}%)")
        st.write(f"  - Energy: {energy_emissions:.2f} kg ({energy_emissions/total_ghg*100:.0f}%)")
        st.write(f"- **Water use:** {total_water:.1f} L/kg protein")
        st.write(f"- **Land use:** {land_use_m2_per_kg:.5f} m²/kg ({land_use_cm2_per_kg:.1f} cm²/kg)")
        st.write(f"- **Energy consumption:** {total_energy_kwh_per_kg:.1f} kWh/kg protein")
        
        st.markdown("**Annual Impact:**")
        # Calculate total annual environmental impact
        annual_ghg = total_ghg * target_production  # Total GHG per year
        cars_equivalent = annual_ghg / 4.6  # EPA: average car = 4.6 tons CO2/year
        st.write(f"- GHG emissions: {annual_ghg:.0f} tons CO₂eq/year")
        st.write(f"- Equivalent to: {cars_equivalent:.0f} passenger cars")
        st.write(f"- Water consumption: {total_water * target_production / 1000:.0f} million L/year")
        st.write(f"- Factory footprint: {total_factory_footprint:.0f} m² ({total_factory_footprint/10000:.2f} hectares)")

# --- TAB 4: COMPETITIVE BENCHMARKS ---
with tab4:
    st.subheader("Competitive Benchmarks")
    
    # Create benchmark comparison data (from literature)
    benchmark_data = pd.DataFrame({
        'Protein Source': ['Your SCP', 'Beef', 'Chicken', 'Pork', 'Soy', 'Pea'],
        'GHG (kg CO₂eq/kg)': [total_ghg, 50, 8, 13, 2.5, 1.5],
        'Water (L/kg)': [total_water, 15000, 4000, 6000, 2500, 1500],
        'Land (m²/kg)': [land_use_m2_per_kg, 250, 45, 55, 15, 8],
        'Cost ($/kg)': [total_opex_per_kg, 6.0, 4.0, 4.5, 2.2, 2.7]
    })
    
    # Create 2 columns for comparison charts
    col1, col2 = st.columns(2)
    
    with col1:
        # GHG comparison chart
        fig_ghg_bench = px.bar(
            benchmark_data,
            x='Protein Source',
            y='GHG (kg CO₂eq/kg)',
            title='GHG Emissions Comparison',
            text='GHG (kg CO₂eq/kg)',
            color='Protein Source'
        )
        fig_ghg_bench.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        st.plotly_chart(fig_ghg_bench, use_container_width=True)
    
    with col2:
        # Cost comparison chart
        fig_cost_bench = px.bar(
            benchmark_data,
            x='Protein Source',
            y='Cost ($/kg)',
            title='Production Cost Comparison',
            text='Cost ($/kg)',
            color='Protein Source'
        )
        fig_cost_bench.update_traces(texttemplate='$%{text:.2f}', textposition='outside')
        st.plotly_chart(fig_cost_bench, use_container_width=True)

        # Provide competitive position assessment
st.markdown("**Competitive Position:**")

# Check if cost is competitive
if total_opex_per_kg < 2.5:
    st.success(f"✅ Your SCP cost (${total_opex_per_kg:.2f}/kg) is competitive with plant proteins")
elif total_opex_per_kg < 4.0:
    st.warning(f"⚠️ Your SCP cost (${total_opex_per_kg:.2f}/kg) is between plant and animal proteins")
else:
    st.error(f"❌ Your SCP cost (${total_opex_per_kg:.2f}/kg) is above animal proteins - optimization needed")

# Check if GHG is competitive
if total_ghg < 3.0:
    st.success(f"✅ Your SCP GHG ({total_ghg:.2f} kg CO₂eq/kg) is competitive with plant proteins")
else:
    st.warning(f"⚠️ Your SCP GHG ({total_ghg:.2f} kg CO₂eq/kg) needs optimization")

#===========================================================================
# FOOTER
#============================================================================
st.markdown("---")
st.markdown("Multiscale Bioprocess Optimization | SCP Production Analysis")

        