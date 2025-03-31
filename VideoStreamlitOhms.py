import streamlit as st

def calculate_ohm_law(values):
    def is_consistent(computed, given, tolerance=1e-3):
        return abs(computed - given) / given < tolerance if given != 0 else computed == 0

    try:
        # Convert inputs to floats (empty strings become None)
        for var in ['V', 'I', 'R', 'P']:
            values[var] = float(values[var]) if values[var] else None
            if values[var] is not None and values[var] < 0:
                raise ValueError("Negative values not allowed")

        # Ohm's Law calculations
        if sum(1 for v in [values['V'], values['I'], values['R']] if v is not None) >= 2:
            if values['V'] is None:
                values['V'] = values['I'] * values['R']
            elif values['I'] is None:
                if values['R'] == 0:
                    raise ValueError("Resistance (R) cannot be zero when calculating current (I)")
                values['I'] = values['V'] / values['R']
            elif values['R'] is None:
                if values['I'] == 0:
                    raise ValueError("Current (I) cannot be zero when calculating resistance (R)")
                values['R'] = values['V'] / values['I']

            if all(values[var] is not None for var in ['V', 'I', 'R']):
                if not is_consistent(values['V'], values['I'] * values['R']):
                    raise ValueError("Inconsistent values: V ≠ I × R")

        # Power calculations
        if values['P'] is None:
            if values['V'] is not None and values['I'] is not None:
                values['P'] = values['V'] * values['I']

        if values['P'] is not None:
            if values['V'] is None and values['I'] is not None:
                values['V'] = values['P'] / values['I']
            if values['I'] is None and values['V'] is not None:
                values['I'] = values['P'] / values['V']
            if values['R'] is None and values['V'] is not None:
                values['R'] = (values['V'] ** 2) / values['P']
            if values['R'] is None and values['I'] is not None:
                values['R'] = values['P'] / (values['I'] ** 2)

        # Final validation and remaining calculations
        if sum(1 for var in ['V', 'I', 'R'] if values[var] is not None) < 2:
            raise ValueError("Insufficient values to calculate unknowns")

        if values['P'] is not None:
            if values['V'] is None and values['R'] is not None:
                values['V'] = (values['P'] * values['R']) ** 0.5
            if values['I'] is None and values['R'] is not None:
                values['I'] = (values['P'] / values['R']) ** 0.5

        return values

    except (ValueError, ZeroDivisionError, TypeError) as e:
        st.error(f"Error: {str(e)}")
        return None

# Streamlit UI
st.title("Ohm's Law Calculator")
st.markdown("Enter known values (leave unknowns empty):")

cols = st.columns(4)
input_values = {}
units = {'V': 'Voltage (V)', 'I': 'Current (I)', 'R': 'Resistance (Ω)', 'P': 'Power (W)'}
for i, var in enumerate(['V', 'I', 'R', 'P']):
    with cols[i]:
        input_values[var] = st.text_input(units[var], key=var)

if st.button("Calculate"):
    results = calculate_ohm_law(input_values)
    
    if results:
        st.success("Calculation Results:")
        result_cols = st.columns(4)
        for i, var in enumerate(['V', 'I', 'R', 'P']):
            with result_cols[i]:
                val = results.get(var)
                if val is not None:
                    st.metric(label=units[var], value=f"{val:.4g}")
                else:
                    st.markdown(f"**{units[var]}**\n\nCannot determine")

st.markdown("---")
st.subheader("Video Tutorial")
st.markdown("""
**Learn Ohm's Law fundamentals**  
Watch this explanation by The Organic Chemistry Tutor:
""")

# YouTube embed code (using Streamlit components)
video_url = "https://www.youtube.com/watch?v=_rSHqvjDksg"  # Ohm's Law video ID
from streamlit import components

# Responsive video embed with collapsible section
with st.expander("Show/Hide Video", expanded=True):
    components.v1.html(
        f"""
        <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%;">
            <iframe src="{video_url}" 
                    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
                    frameborder="0" 
                    allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
                    allowfullscreen>
            </iframe>
        </div>
        """,
        height=400,
    )

# Optional: Add direct link
st.markdown("""
[Watch on YouTube](https://www.youtube.com/watch?v=_rSHqvjDksg)
""")
