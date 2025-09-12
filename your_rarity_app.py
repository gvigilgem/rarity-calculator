python
import streamlit as st
import math
import time

# Simple rarity calculation
def calculate_rarity(age, gender, height, weight, race, cups, rod_length, ex_rarity=False):
    prob = 1.0
    prob *= (1 / 101)  # Age
    if gender == 'male' or gender == 'female':
        prob *= 0.5
    elif gender:
        prob *= 0.01
    prob *= (1 / 100)  # Height in inches
    prob *= (1 / 500)  # Weight
    race_probs = {'caucasian': 0.6, 'african-american': 0.13, 'hispanic': 0.19, 'asian': 0.06, 'other': 0.02}
    prob *= race_probs.get(race, 0.02)
    
    # Cups as bra size for females only
    if gender == 'female':
        cup_probs = {'1': 0.3, '2': 0.25, '3': 0.25, '4': 0.15, '5': 0.05}  # 1=A, 2=B, etc.
        prob *= cup_probs.get(cups, 0.3)
    else:
        prob *= 1.0  # No cup factor for males
    
    # Fishing Rod Length: 1-10 (implied inches, tactful)
    rod_probs = {'1': 0.2, '2': 0.15, '3': 0.12, '4': 0.1, '5': 0.08, '6': 0.07, '7': 0.06, '8': 0.05, '9': 0.04, '10': 0.03}
    prob *= rod_probs.get(rod_length, 0.2)
    
    rarity = 1 / prob
    return max(1000, min(10000000, rarity))

st.title("Rarity Calculator")

# Your Stats
st.header("Your Stats")
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Your Name", placeholder="Enter your name")
    age = st.number_input("Age", min_value=0, max_value=100, value=0)
    gender = st.selectbox("Gender", ["", "Male", "Female"])
with col2:
    height = st.number_input("Height (inches)", min_value=0, max_value=100, value=0)
    weight = st.number_input("Weight (lbs)", min_value=0, max_value=500, value=0)

race = st.selectbox("Race/Ethnicity", ["", "Caucasian", "African American", "Hispanic", "Asian", "Other"])

# Cups: Only show for females
if gender == "Female":
    cups = st.selectbox("Cups (Bra Size: 1=A, 2=B, 3=C, 4=D, 5=DD+)", ["", "1", "2", "3", "4", "5"])
else:
    cups = ""

# Fishing Rod Length: Tactful 1-10 scale
rod_length = st.selectbox("Fishing Rod Length (1-10)", ["", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])

# Compare to Ex (Optional)
ex_name = st.text_input("Ex's Name", placeholder="Enter ex's name")
ex_data = {}
if ex_name:
    ex_col1, ex_col2 = st.columns(2)
    with ex_col1:
        ex_data['name'] = ex_name
        ex_data['age'] = st.number_input("Ex's Age", min_value=0, max_value=100, value=0)
        ex_data['gender'] = st.selectbox("Ex's Gender", ["", "Male", "Female"])
    with ex_col2:
        ex_data['height'] = st.number_input("Ex's Height (inches)", min_value=0, max_value=100, value=0)
        ex_data['weight'] = st.number_input("Ex's Weight (lbs)", min_value=0, max_value=500, value=0)
    ex_data['race'] = st.selectbox("Ex's Race/Ethnicity", ["", "Caucasian", "African American", "Hispanic", "Asian", "Other"])
    
    # Ex cups only for female
    if ex_data['gender'] == "Female":
        ex_data['cups'] = st.selectbox("Ex's Cups (1=A, 2=B, 3=C, 4=D, 5=DD+)", ["", "1", "2", "3", "4", "5"])
    else:
        ex_data['cups'] = ""
    
    ex_data['rod_length'] = st.selectbox("Ex's Fishing Rod Length (1-10)", ["", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
else:
    ex_data = {}

if st.button("Calculate Rarity"):
    # Validation
    filled = [name, str(age), gender, str(height), str(weight), race, cups, rod_length]
    if sum(1 for f in filled if f and f != '0' and f != '') < 2:
        st.error("Please fill in your name and at least one stat!")
    else:
        # Spinner simulation (3 seconds)
        progress_bar = st.progress(0)
        status_text = st.empty()
        for i in range(100):
            progress_bar.progress(i + 1)
            status_text.text(f'Thinking... {i+1}%')
            time.sleep(0.03)
        status_text.empty()
        
        # Calculate user rarity
        user_race = race.lower().replace(' ', '-')
        rarity = calculate_rarity(age, gender.lower(), height, weight, user_race, cups, rod_length)
        percent = (1 / rarity * 100)
        
        st.header(f"{name or 'Your'} Rarity Results")
        st.markdown(f"**Based on your stats, {name or 'you'} is in the top {percent:.4f}% of rarity!**  \nThis means you're one in **{math.round(rarity)}**.")
        
        # Ex comparison
        if ex_name:
            ex_race = ex_data['race'].lower().replace(' ', '-')
            ex_rarity = calculate_rarity(ex_data['age'], ex_data['gender'].lower(), ex_data['height'], ex_data['weight'], ex_race, ex_data['cups'], ex_data['rod_length'])
            ex_percent = (1 / ex_rarity * 100)
            if rarity > ex_rarity:
                st.info(f"Compared to {ex_name}, you're **rarer** (they are {ex_percent:.4f}%)!")
            else:
                st.info(f"You're **as rare as** {ex_name} (both {percent:.4f}%)!")
        
        col_copy, col_share = st.columns(2)
        with col_copy:
            if st.button("Copy to Share"):
                text = f"{name or 'You'} is in the top {percent:.4f}% of rarity! One in {math.round(rarity)}."
                if ex_name:
                    text += f"\nCompared to {ex_name}, you're {'rarer' if rarity > ex_rarity else 'as rare as'} them!"
                st.code(text)
                st.success("Copied to clipboard! (Manual copy from code block)")
        with col_share:
            if st.button("Share Image"):
                st.markdown(f"""
                ---
                # Your Rarity Score!
                ## {name or 'You'}: Top {percent:.4f}% (1 in {math.round(rarity)})
                {f"Compared to {ex_name}: {'Rarer!' if rarity > ex_rarity else 'As rare!'}" if ex_name else ''}
                Generated by Rarity Calculator
                ---
                """)
                st.success("Share this markdown as an image or text!")
        
        if st.button("Reset Form"):
            st.session_state.clear()
            st.rerun()

# Reset button always visible
if st.button("Reset Form"):
    st.session_state.clear()
    st.rerun()
