import streamlit as st
import math
import time
from scipy.stats import norm  # For height probability

# Simple rarity calculation based on factors
def calculate_rarity(gender, height, race, age, income, marital_status, obesity_status, homeownership, location, rod_count, cup_count=None):
    prob = 1.0
    
    # Gender
    if gender == 'male':
        prob *= 0.5
    elif gender == 'female':
        prob *= 0.5
    else:
        prob *= 1.0
    
    # Height (normal distribution around 67 inches, std 4)
    prob_height = norm.pdf(height, 67, 4) * 4  # Approximate probability
    prob *= max(prob_height, 0.001)
    
    # Race (rough US percentages)
    race_probs = {'mexican': 0.18, 'filipina': 0.02, 'caucasian': 0.6, 'african-american': 0.13, 'hispanic': 0.19, 'asian': 0.06, 'other': 0.02}
    prob *= race_probs.get(race.lower(), 0.02)
    
    # Age (uniform 18-80)
    prob *= 1 / 62
    
    # Income (log scale, rough - adjust based on value)
    if income > 100000:
        prob *= 0.1
    elif income > 50000:
        prob *= 0.3
    else:
        prob *= 0.6
    
    # Marital status
    marital_probs = {'single': 0.5, 'married': 0.4, 'divorced': 0.1}
    prob *= marital_probs.get(marital_status.lower(), 0.5)
    
    # Obesity
    obesity_probs = {'non-obese': 0.7, 'obese': 0.3}
    prob *= obesity_probs.get(obesity_status.lower(), 0.7)
    
    # Homeownership
    home_probs = {'homeowner': 0.65, 'renter': 0.35}
    prob *= home_probs.get(homeownership.lower(), 0.65)
    
    # Location (placeholder)
    location_probs = {'u.s.': 1.0}
    prob *= location_probs.get(location.lower(), 1.0)
    
    # Rod count (1-10, rarer higher)
    rod_probs = {str(i): max(0.1 - (i-1)*0.01, 0.01) for i in range(1, 11)}
    prob *= rod_probs.get(rod_count, 0.1)
    
    # Cup count for females (1-5, A-DD+)
    if gender == 'female' and cup_count:
        cup_probs = {'1': 0.3, '2': 0.25, '3': 0.25, '4': 0.15, '5': 0.05}
        prob *= cup_probs.get(cup_count, 0.3)
    
    rarity = 1 / prob
    return max(1000, min(1000000000, rarity))  # Cap at 1B for sanity

# Swipe calculation (assume 100 swipes/day, 365 days/year)
def calculate_swipes(rarity):
    daily_swipes = 100
    yearly_swipes = daily_swipes * 365
    swipes = rarity
    years = swipes / yearly_swipes
    lifetime_odds = (1 / rarity) * 100
    return swipes, years, lifetime_odds

st.markdown("""
# How Rare Are You—Compared to Your Ex?  
Enter your stats. Enter theirs. Find out who's actually rare—and who's just lucky you dated them. 😎
""")

hide_sensitive = st.checkbox("Hide sensitive fields if sharing publicly (they'll still count in calculations)")

# Your Stats
st.header("Your Stats")
col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("Your Gender", ["", "Male", "Female"])
    height = st.number_input("Your Height (inches)", min_value=0, max_value=100, value=0)
with col2:
    age = st.number_input("Your Age", min_value=0, max_value=100, value=0)
    income = st.number_input("Your Annual Income ($)", min_value=0, value=0)
race = st.selectbox("Your Race/Ethnicity", ["", "Mexican", "Filipina", "Caucasian", "African American", "Hispanic", "Asian", "Other"])
marital = st.selectbox("Your Marital Status", ["", "Single", "Married", "Divorced"])
obesity = st.selectbox("Your Obesity Status", ["", "Non-obese", "Obese"])
home = st.selectbox("Your Homeownership", ["", "Homeowner", "Renter"])
location = st.selectbox("Where are you searching?", ["", "U.S.", "Global"])

# Rod count
rod_count = st.selectbox("Your Rod Count (1-10)", ["", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])

# Cups for female
cup_count = ""
if gender == "Female":
    cup_count = st.selectbox("Your Cup Count: How many?", ["", "1 Cup (A)", "2 Cups (B)", "3 Cups (C)", "4 Cups (D)", "5 Cups (DD+)"])

# Ex Stats
st.header("Your Ex's Stats")
ex_hide = st.checkbox("Hide their sensitive fields if sharing publicly (they'll still count in calculations)")
ex_name = st.text_input("Ex's Name", placeholder="Enter ex's name")
if ex_name:
    ex_col1, ex_col2 = st.columns(2)
    with ex_col1:
        ex_gender = st.selectbox("Their Gender", ["", "Male", "Female"])
        ex_height = st.number_input("Their Height (inches)", min_value=0, max_value=100, value=0)
    with ex_col2:
        ex_age = st.number_input("Their Age", min_value=0, max_value=100, value=0)
        ex_income = st.number_input("Their Annual Income ($)", min_value=0, value=0)
    ex_race = st.selectbox("Their Race/Ethnicity", ["", "Mexican", "Filipina", "Caucasian", "African American", "Hispanic", "Asian", "Other"])
    ex_marital = st.selectbox("Their Marital Status", ["", "Single", "Married", "Divorced"])
    ex_obesity = st.selectbox("Their Obesity Status", ["", "Non-obese", "Obese"])
    ex_home = st.selectbox("Their Homeownership", ["", "Homeowner", "Renter"])
    ex_location = st.selectbox("Where are they searching?", ["", "U.S.", "Global"])
    
    # Ex rod
    ex_rod_count = st.selectbox("Their Rod Count (1-10)", ["", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
    
    # Ex cups
    ex_cup_count = ""
    if ex_gender == "Female":
        ex_cup_count = st.selectbox("Their Cup Count: How many?", ["", "1 Cup (A)", "2 Cups (B)", "3 Cups (C)", "4 Cups (D)", "5 Cups (DD+)"])
else:
    ex_gender, ex_height, ex_age, ex_income, ex_race, ex_marital, ex_obesity, ex_home, ex_location, ex_rod_count, ex_cup_count = "", 0, 0, 0, "", "", "", "", "", "", ""

if st.button("Calculate Rarity"):
    # Validation
    filled = [gender, height, race, age, income, marital, obesity, home, location, rod_count, cup_count]
    if sum(1 for f in filled if f) < 3:
        st.error("Please fill in at least 3 stats!")
    else:
        # Spinner
        progress_bar = st.progress(0)
        status_text = st.empty()
        for i in range(100):
            progress_bar.progress(i + 1)
            status_text.text(f'Thinking... {i+1}%')
            time.sleep(0.03)
        status_text.empty()
        
        # Calculate
        user_race = race.lower().replace(' ', '-')
        user_rarity = calculate_rarity(gender.lower(), height, user_race, age, income, marital, obesity, home, location, rod_count, cup_count)
        user_swipes, user_years, user_lifetime = calculate_swipes(user_rarity)
        
        ex_race = ex_race.lower().replace(' ', '-')
        ex_rarity = calculate_rarity(ex_gender.lower(), ex_height, ex_race, ex_age, ex_income, ex_marital, ex_obesity, ex_home, ex_location, ex_rod_count, ex_cup_count)
        ex_swipes, ex_years, ex_lifetime = calculate_swipes(ex_rarity)
        
        # Results
        st.header("Results")
        st.markdown(f"""
        **You** ({height}", {race}, age {age}, {marital}, {obesity}, {home}) are 1 in **{math.round(user_rarity)}** people.
        That's **{math.round(user_swipes)}** Tinder swipes, or about **{math.round(user_years)}** years of swiping in U.S.. Lifetime odds: **{user_lifetime:.6f}%**.
        """)
        
        st.markdown(f"""
        **Your Ex** ({ex_height}", {ex_race}, {ex_marital}, {ex_obesity}, {ex_home}) is 1 in **{math.round(ex_rarity)}** people.
        That's **{math.round(ex_swipes)}** Tinder swipes, or about **{math.round(ex_years)}** years of swiping in U.S.. Lifetime odds: **{ex_lifetime:.2f}%**. And that's just meeting them—good luck keeping them when they Google your criminal record. 😎
        """)
        
        ratio = math.round(user_rarity / ex_rarity)
        st.markdown(f"**You are {ratio} times rarer than Your Ex!**")
        
        st.markdown("**Built by Feo**")
        st.info("Screenshot and share on social media to show who's the real unicorn!")
        
        col_copy, col_share = st.columns(2)
        with col_copy:
            if st.button("Copy to Share"):
                text = f"You are 1 in {math.round(user_rarity)} people. {ex_name or 'Your Ex'} is 1 in {math.round(ex_rarity)}. You are {ratio} times rarer!"
                st.code(text)
                st.success("Copied! (Manual copy from code block)")
        with col_share:
            if st.button("Share Image"):
                st.success("Screenshot this page to share!")

if st.button("Reset Form"):
    st.rerun()
