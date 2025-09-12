import streamlit as st
import time
import math

# Title
st.title("Rarity Calculator")

# Session state for results
if 'results_shown' not in st.session_state:
    st.session_state.results_shown = False
if 'rarity_percent' not in st.session_state:
    st.session_state.rarity_percent = None
if 'rarity_number' not in st.session_state:
    st.session_state.rarity_number = None
if 'comparison_text' not in st.session_state:
    st.session_state.comparison_text = None

# Calculate rarity function (probabilistic model)
def calculate_rarity(age, gender, height, weight, race, cups, rods):
    prob = 1.0
    # Age: uniform 0-100
    prob *= (1 / 101)
    # Gender
    if gender == 'male' or gender == 'female':
        prob *= 0.5
    elif gender:
        prob *= 0.01
    # Height
    prob *= (1 / 100)
    # Weight
    prob *= (1 / 500)
    # Race probabilities (rough estimates)
    race_probs = {'caucasian': 0.6, 'african-american': 0.13, 'hispanic': 0.19, 'asian': 0.06, 'other': 0.02}
    if race in race_probs:
        prob *= race_probs[race]
    else:
        prob *= 0.02
    # Cups
    cup_probs = {'bronze': 0.5, 'silver': 0.3, 'gold': 0.1}
    if cups in cup_probs:
        prob *= cup_probs[cups]
    else:
        prob *= 0.05
    # Rods
    rod_probs = {'iron': 0.5, 'steel': 0.3, 'mythril': 0.1}
    if rods in rod_probs:
        prob *= rod_probs[rods]
    else:
        prob *= 0.05
    rarity = 1 / prob
    return max(1000, min(10000000, rarity))

# Validation
def validate_inputs(name, age, gender, height, weight, race, cups, rods):
    filled = [name, age, gender, height, weight, race, cups, rods]
    non_default = [f for f in filled if f and f != '0' and f != 'Select' and f != '']
    return len(non_default) >= 2

# Form for user stats
with st.form("user_form"):
    st.subheader("Your Stats")
    name = st.text_input("Your Name", placeholder="Enter your name")
    age = st.number_input("Age", min_value=0, max_value=100, value=0)
    gender = st.selectbox("Gender", options=["Select", "Male", "Female", "Other"])
    height = st.number_input("Height (inches)", min_value=0, max_value=100, value=0)
    weight = st.number_input("Weight (lbs)", min_value=0, max_value=500, value=0)
    race = st.selectbox("Race/Ethnicity", options=["Select", "Caucasian", "African American", "Hispanic", "Asian", "Other"])
    cups = st.selectbox("Cups (Legendary Gear)", options=["Select", "Bronze Cup", "Silver Cup", "Gold Cup"])
    rods = st.selectbox("Rods (Epic Weapon)", options=["Select", "Iron Rod", "Steel Rod", "Mythril Rod"])
    
    # Ex form
    st.subheader("Compare to Ex (Optional)")
    ex_name = st.text_input("Ex's Name", placeholder="Enter ex's name")
    ex_age = st.number_input("Ex's Age", min_value=0, max_value=100, value=0)
    ex_gender = st.selectbox("Ex's Gender", options=["Select", "Male", "Female", "Other"])
    ex_height = st.number_input("Ex's Height (inches)", min_value=0, max_value=100, value=0)
    ex_weight = st.number_input("Ex's Weight (lbs)", min_value=0, max_value=500, value=0)
    ex_race = st.selectbox("Ex's Race/Ethnicity", options=["Select", "Caucasian", "African American", "Hispanic", "Asian", "Other"])
    ex_cups = st.selectbox("Ex's Cups (Legendary Gear)", options=["Select", "Bronze Cup", "Silver Cup", "Gold Cup"])
    ex_rods = st.selectbox("Ex's Rods (Epic Weapon)", options=["Select", "Iron Rod", "Steel Rod", "Mythril Rod"])
    
    submitted = st.form_submit_button("Calculate Rarity")

# Handle submission
if submitted:
    if not validate_inputs(name or "You", str(age), gender, str(height), str(weight), race, cups, rods):
        st.error("Please fill in your name and at least one stat (e.g., age or cups) for accurate results!")
    else:
        with st.spinner("Thinking... Generating your unique rarity score!"):
            time.sleep(3)  # 3-second delay for drama
        
        # Calculate user rarity
        user_rarity = calculate_rarity(age, gender, height, weight, race, cups, rods)
        user_percent = (1 / user_rarity * 100)
        
        st.session_state.rarity_percent = f"{user_percent:.4f}%"
        st.session_state.rarity_number = math.round(user_rarity)
        st.session_state.results_shown = True
        
        # Display results
        st.subheader(f"{name or 'You'}'s Rarity Results")
        st.success(f"Based on your stats, {name or 'You'} is in the top **{st.session_state.rarity_percent}** of rarity! This means you're one in {st.session_state.rarity_number}.")
        
        # Comparison if ex provided
        if ex_name:
            ex_rarity = calculate_rarity(ex_age, ex_gender, ex_height, ex_weight, ex_race, ex_cups, ex_rods)
            ex_percent = (1 / ex_rarity * 100)
            if user_rarity > ex_rarity:
                st.session_state.comparison_text = f"Rarer than {ex_name} (who is {ex_percent:.4f}%)!"
            else:
                st.session_state.comparison_text = f"As rare as {ex_name} (both {st.session_state.rarity_percent}%)!"
            st.info(f"Compared to {ex_name}, you're {st.session_state.comparison_text}")
        
        # Share buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Copy to Share"):
                share_text = f"{name or 'You'} is in the top {st.session_state.rarity_percent} of rarity! One in {st.session_state.rarity_number}."
                if st.session_state.comparison_text:
                    share_text += f"\n{st.session_state.comparison_text}"
                st.code(share_text, language=None)  # Display for manual copy
                st.success("Text ready to copy!")
        with col2:
            if st.button("Share Image"):
                # Simple text-based "image" simulation (for real image, use matplotlib or PIL)
                st.image("https://via.placeholder.com/800x400/007bff/ffffff?text=Your+Rarity+Score!+{name}+is+1+in+{st.session_state.rarity_number}", caption="Share this image!")
                # Reset after share
                st.session_state.results_shown = False
                st.rerun()
        
        # Reset button
        if st.button("Reset Form"):
            st.session_state.results_shown = False
            st.rerun()

# Show results if previously calculated (persistence)
if st.session_state.results_shown:
    st.subheader(f"{name or 'You'}'s Rarity Results")
    st.success(f"Based on your stats, {name or 'You'} is in the top **{st.session_state.rarity_percent}** of rarity! This means you're one in {st.session_state.rarity_number}.")
    if st.session_state.comparison_text:
        st.info(st.session_state.comparison_text)
