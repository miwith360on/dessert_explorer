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
regions = data['region'].unique()
selected_region = st.sidebar.selectbox("Filter by Region", regions)

flavor_profiles = data['flavor_profile'].unique()
selected_flavor = st.sidebar.selectbox("Filter by Flavor Profile", flavor_profiles)

filtered_data = data[
    (data['region'] == selected_region) &
    (data['flavor_profile'] == selected_flavor)
]

# Display filtered data
st.write(f"Filtered Desserts: {len(filtered_data)}")
st.dataframe(filtered_data[['dessert_name', 'region', 'flavor_profile', 'calories', 'prep_time']])

# Random Dessert Button
if st.button("Surprise Me with a Dessert!"):
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
