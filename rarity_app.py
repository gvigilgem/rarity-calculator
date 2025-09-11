import streamlit as st

def rarity_score(height_prob, race_prob, income_prob, marital_prob, obesity_prob, size_prob, homeownership_prob):
    return round(1 / (height_prob * race_prob * income_prob * marital_prob * obesity_prob * size_prob * homeownership_prob))

# Population sizes for Search Zones (approximate, millions)
population_sizes = {
    "U.S.": 331, "Philippines": 115, "Thailand": 71, "Colombia": 51, "Vietnam": 98,
    "Russia": 146, "Ukraine": 41, "Brazil": 213, "Mexico": 130, "China": 1400, "Indonesia": 276
}

# Streamlit app
st.title("How Rare Are You—Compared to Your Ex?")
st.write("Enter your stats. Enter theirs. Find out who's actually rare—and who's just lucky you dated them. 😎")

st.header("Your Stats")
st.write("Hide sensitive fields if sharing publicly (they'll still count in calculations).")
gender_you = st.selectbox("Your Gender", ["Male", "Female"], index=0)
height_you = st.number_input("Your Height (inches)", min_value=60, max_value=84, value=76)  # 6'4"
race_you = st.selectbox("Your Race/Ethnicity", ["Mexican", "Filipina", "White", "Black", "Other"], index=0)
age_you = st.number_input("Your Age", min_value=18, max_value=100, value=35)
income_you = st.number_input("Your Annual Income ($)", min_value=0, value=130000)
marital_you = st.selectbox("Your Marital Status", ["Single", "Married"], index=0)
obesity_you = st.selectbox("Your Obesity Status", ["Non-obese", "Obese"], index=0)
homeownership_you = st.selectbox("Your Homeownership", ["Homeowner", "Renter"], index=0)
search_zone_you = st.selectbox("Where are you searching?", 
    ["U.S.", "Philippines", "Thailand", "Colombia", "Vietnam", "Russia", "Ukraine", "Brazil", "Mexico", "China", "Indonesia"], index=0)
if gender_you == "Male":
    fishing_rod_you = st.slider("Your Rod Count (1-10)", 1, 10, 10)  # 10 maps to 8"
else:
    cup_size_you = st.selectbox("Your Cup Count: How many?", ["1 Cup (A)", "2 Cups (B)", "3+ Cups (C or larger)"], index=0)
hide_income_you = st.checkbox("Hide Your Income", value=False)
hide_size_you = st.checkbox("Hide Your Rod/Cup Count", value=True)
hide_age_you = st.checkbox("Hide Your Age", value=False)

st.header("Your Ex's Stats")
st.write("Hide their sensitive fields if sharing publicly (they'll still count in calculations).")
gender_ronabel = st.selectbox("Their Gender", ["Male", "Female"], index=1)
height_ronabel = st.number_input("Their Height (inches)", min_value=60, max_value=84, value=64)  # 5'4"
race_ronabel = st.selectbox("Their Race/Ethnicity", ["Mexican", "Filipina", "White", "Black", "Other"], index=1)
age_ronabel = st.number_input("Their Age", min_value=18, max_value=100, value=35)
income_ronabel = st.number_input("Their Annual Income ($)", min_value=0, value=34000)
marital_ronabel = st.selectbox("Their Marital Status", ["Single", "Married"], index=0)
obesity_ronabel = st.selectbox("Their Obesity Status", ["Non-obese", "Obese"], index=0)
homeownership_ronabel = st.selectbox("Their Homeownership", ["Homeowner", "Renter"], index=1)
search_zone_ronabel = st.selectbox("Where are they searching?", 
    ["U.S.", "Philippines", "Thailand", "Colombia", "Vietnam", "Russia", "Ukraine", "Brazil", "Mexico", "China", "Indonesia"], index=0)
if gender_ronabel == "Male":
    fishing_rod_ronabel = st.slider("Their Rod Count (1-10)", 1, 10, 5)  # Default average
else:
    cup_size_ronabel = st.selectbox("Their Cup Count: How many?", ["1 Cup (A)", "2 Cups (B)", "3+ Cups (C or larger)"], index=0)
hide_income_ronabel = st.checkbox("Hide Their Income", value=True)
hide_size_ronabel = st.checkbox("Hide Their Rod/Cup Count", value=True)
hide_age_ronabel = st.checkbox("Hide Their Age", value=False)

# Map inputs to probabilities
race_probs = {"Mexican": 0.09, "Filipina": 0.015, "White": 0.60, "Black": 0.136, "Other": 0.159}
height_probs = {
    "Mexican_Male": {76: 0.0005},  # 6'4" (ENSANUT 2012/2018)
    "Filipina_Female": {64: 0.20},  # 5'4" (NHANES)
    "White_Male": {76: 0.002},  # 6'4" (NHANES)
    "White_Female": {64: 0.50},  # 5'4" (NHANES)
    "Black_Male": {76: 0.001},  # 6'4" (NHANES)
    "Black_Female": {64: 0.50},  # 5'4" (NHANES)
}
income_probs_you = {130000: 0.09}  # Top 9% in Arizona
income_probs_ronabel = {34000: 0.60}  # Median-ish
marital_probs_male = {"Mexican": 0.38, "White": 0.40, "Black": 0.50, "Filipina": 0.38, "Other": 0.40}
marital_probs_female = {"Filipina": 0.45, "White": 0.45, "Black": 0.55, "Mexican": 0.45, "Other": 0.45}
obesity_probs_male = {"Mexican": 0.50, "White": 0.58, "Black": 0.52, "Filipina": 0.50, "Other": 0.55}
obesity_probs_female = {"Filipina": 0.57, "White": 0.57, "Black": 0.40, "Mexican": 0.50, "Other": 0.50}
homeownership_probs = {
    "Mexican": {"Homeowner": 0.567, "Renter": 0.433},
    "Filipina": {"Homeowner": 0.63, "Renter": 0.37},
    "White": {"Homeowner": 0.75, "Renter": 0.25},
    "Black": {"Homeowner": 0.45, "Renter": 0.55},
    "Other": {"Homeowner": 0.60, "Renter": 0.40}
}
fishing_rod_probs = {10: 0.01, 5: 0.50}  # 8" vs. average
cup_probs = {"1 Cup (A)": 0.30, "2 Cups (B)": 0.20, "3+ Cups (C or larger)": 0.50}

# Adjust marital probs by age (simplified: 30-40 range vs. broader)
if 30 <= age_you <= 40:
    marital_probs_male[race_you] = marital_probs_male[race_you]
    marital_probs_female[race_you] = marital_probs_female[race_you]
else:
    marital_probs_male[race_you] = 0.45  # Broader range
    marital_probs_female[race_you] = 0.50
if 30 <= age_ronabel <= 40:
    marital_probs_male[race_ronabel] = marital_probs_male[race_ronabel]
    marital_probs_female[race_ronabel] = marital_probs_female[race_ronabel]
else:
    marital_probs_male[race_ronabel] = 0.45
    marital_probs_female[race_ronabel] = 0.50

# Get probabilities
you_key = f"{race_you}_{gender_you}"
ronabel_key = f"{race_ronabel}_{gender_ronabel}"
you_probs = {
    "height_prob": height_probs.get(you_key, {}).get(height_you, 0.01),
    "race_prob": race_probs[race_you] if search_zone_you == "U.S." else 0.50,  # Assume 50% abroad
    "income_prob": income_probs_you.get(income_you, 0.10),
    "marital_prob": marital_probs_male[race_you] if gender_you == "Male" else marital_probs_female[race_you],
    "obesity_prob": obesity_probs_male[race_you] if gender_you == "Male" else obesity_probs_female[race_you],
    "size_prob": fishing_rod_probs.get(fishing_rod_you, 0.10) if gender_you == "Male" else cup_probs.get(cup_size_you, 0.50),
    "homeownership_prob": homeownership_probs[race_you][homeownership_you]
}
ronabel_probs = {
    "height_prob": height_probs.get(ronabel_key, {}).get(height_ronabel, 0.20),
    "race_prob": race_probs[race_ronabel] if search_zone_ronabel == "U.S." else 0.50,
    "income_prob": income_probs_ronabel.get(income_ronabel, 0.60),
    "marital_prob": marital_probs_male[race_ronabel] if gender_ronabel == "Male" else marital_probs_female[race_ronabel],
    "obesity_prob": obesity_probs_male[race_ronabel] if gender_ronabel == "Male" else obesity_probs_female[race_ronabel],
    "size_prob": fishing_rod_probs.get(fishing_rod_ronabel, 0.10) if gender_ronabel == "Male" else cup_probs.get(cup_size_ronabel, 0.50),
    "homeownership_prob": homeownership_probs[race_ronabel][homeownership_ronabel]
}

# Calculate rarities
your_rarity = rarity_score(**you_probs)
ronabel_rarity = rarity_score(**ronabel_probs)
rarity_ratio = your_rarity / ronabel_rarity

# Calculate swipe math (100 encounters/year, 30-year dating window)
encounters_per_year = 100
dating_years = 30
swipes_needed_you = your_rarity
swipes_needed_ronabel = ronabel_rarity
years_to_meet_you = swipes_needed_you / encounters_per_year
years_to_meet_ronabel = swipes_needed_ronabel / encounters_per_year
lifetime_odds_you = min(1.0, encounters_per_year * dating_years / your_rarity) * 100
lifetime_odds_ronabel = min(1.0, encounters_per_year * dating_years / ronabel_rarity) * 100

# Build output strings with hide options
you_traits = [f"{height_you}\"", race_you]
if not hide_age_you:
    you_traits.append(f"age {age_you}")
if not hide_income_you:
    you_traits.append(f"${income_you:,}")
you_traits.extend([marital_you.lower(), obesity_you.lower()])
if not hide_size_you:
    you_traits.append("top-tier rod count" if gender_you == "Male" else "smaller cup count")
you_traits.append(homeownership_you.lower())
you_output = f"You ({', '.join(you_traits)}) are 1 in {your_rarity:,} people."

ronabel_traits = [f"{height_ronabel}\"", race_ronabel]
if not hide_age_ronabel:
    ronabel_traits.append(f"age {age_ronabel}")
if not hide_income_ronabel:
    ronabel_traits.append(f"${income_ronabel:,}")
ronabel_traits.extend([marital_ronabel.lower(), obesity_ronabel.lower()])
if not hide_size_ronabel:
    ronabel_traits.append("top-tier rod count" if gender_ronabel == "Male" else "smaller cup count")
ronabel_traits.append(homeownership_ronabel.lower())
ronabel_output = f"Your Ex ({', '.join(ronabel_traits)}) is 1 in {ronabel_rarity:,} people."

# Display results
st.header("Results")
st.write(you_output)
st.write(f"That's {int(swipes_needed_you):,} Tinder swipes, or about {int(years_to_meet_you):,} years of swiping in {search_zone_you}. Lifetime odds: {lifetime_odds_you:.6f}%.")
st.write(ronabel_output)
st.write(f"That's {int(swipes_needed_ronabel):,} Tinder swipes, or about {int(years_to_meet_ronabel):,} years of swiping in {search_zone_ronabel}. Lifetime odds: {lifetime_odds_ronabel:.2f}%. And that's just meeting them—good luck keeping them when they Google your criminal record. 😎")
st.write(f"You are {rarity_ratio:,.0f} times rarer than Your Ex!")
st.write("**Built by Feo**")

# Share button
st.write("Screenshot and share on social media to show who's the real unicorn!")