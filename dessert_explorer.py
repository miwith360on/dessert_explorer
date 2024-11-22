import streamlit as st
import pandas as pd
import random

# Load the dataset
@st.cache
def load_data():
    return pd.read_csv("validated_global_dessert_data.csv")

data = load_data()

# App title and intro
st.title("🌍 Global Dessert Explorer")
st.sidebar.header("Explore by Filters")

# Sidebar filters
if data is not None:
    # Region Filter
    regions = sorted(data['region'].dropna().unique())  # Get unique regions
    if 'unknown' in regions:
        regions.remove('unknown')  # Remove "unknown"
    selected_region = st.sidebar.selectbox("Filter by Region", ["All"] + regions)
    
    # Flavor Profile Filter
    flavor_profiles = sorted(data['flavor_profile'].dropna().unique())  # Get unique flavor profiles
    if 'unknown' in flavor_profiles:
        flavor_profiles.remove('unknown')  # Remove "unknown"
    selected_flavor = st.sidebar.selectbox("Filter by Flavor Profile", ["All"] + flavor_profiles)

    # Apply Filters
    filtered_data = data.copy()
    if selected_region != "All":
        filtered_data = filtered_data[filtered_data['region'] == selected_region]
    if selected_flavor != "All":
        filtered_data = filtered_data[filtered_data['flavor_profile'].str.contains(selected_flavor, na=False, case=False)]

    # Display filtered data
    st.subheader(f"Filtered Desserts ({len(filtered_data)} found)")
    st.dataframe(filtered_data[['dessert_name', 'region', 'flavor_profile', 'calories', 'prep_time']])

    # Random Dessert Button
    if st.button("🎲 Surprise Me with a Dessert!"):
        random_dessert = filtered_data.sample(1).iloc[0]
        st.subheader(f"🍰 {random_dessert['dessert_name']}")
        st.image(random_dessert['image_url'])
        st.write(f"Region: {random_dessert['region']}")
        st.write(f"Flavor Profile: {random_dessert['flavor_profile']}")
        st.write(f"Calories: {random_dessert['calories']}")
        st.write(f"Prep Time: {random_dessert['prep_time']} minutes")
        st.write(f"Trivia: {random_dessert['cultural_trivia']}")

    # Trivia Section
    st.subheader("🧠 Dessert Trivia")
    if st.button("Show Random Trivia"):
        non_empty_trivia = data[data['cultural_trivia'] != "No trivia available"]
        random_trivia = non_empty_trivia.sample(1).iloc[0]
        st.write(f"Did you know? {random_trivia['cultural_trivia']} ({random_trivia['dessert_name']})")
else:
    st.warning("Dataset not loaded. Please upload the required dataset.")
