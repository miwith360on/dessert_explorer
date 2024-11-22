import streamlit as st
import pandas as pd

# Title and Introduction
st.title("🍰 Global Dessert Explorer")
st.write("Explore the world's most delightful desserts!")
st.sidebar.header("Filter Options")

# Load Dataset
try:
    data = pd.read_csv("validated_global_dessert_data.csv")
    st.success("Dataset loaded successfully!")
except FileNotFoundError:
    st.error("Dataset not found. Please ensure 'validated_global_dessert_data.csv' is available.")
    st.stop()

# Data Cleaning - Replace "unknown" with meaningful placeholders
data['region'] = data['region'].replace("unknown", "Not specified")
data['flavor_profile'] = data['flavor_profile'].replace("unknown", "Not specified")
data['cultural_trivia'] = data['cultural_trivia'].replace("No trivia available", "Trivia not provided")

# Filters
regions = ["All"] + sorted(data['region'].unique())
flavors = ["All"] + sorted(data['flavor_profile'].unique())

region_filter = st.sidebar.selectbox("Select Region", regions)
flavor_filter = st.sidebar.selectbox("Select Flavor Profile", flavors)

filtered_data = data.copy()

if region_filter != "All":
    filtered_data = filtered_data[filtered_data['region'] == region_filter]
if flavor_filter != "All":
    filtered_data = filtered_data[filtered_data['flavor_profile'] == flavor_filter]

# Display Filtered Data
st.subheader("Filtered Desserts")
st.dataframe(filtered_data)

# Random Dessert with Trivia
if st.button("Surprise Me with a Dessert!"):
    if len(filtered_data) > 0:
        random_dessert = filtered_data.sample(1).iloc[0]
        st.image(random_dessert["image_url"], width=300)
        st.markdown(f"### {random_dessert['dessert_name']}")
        st.markdown(f"**Region:** {random_dessert['region']}")
        st.markdown(f"**Flavor Profile:** {random_dessert['flavor_profile']}")
        st.markdown(f"**Calories:** {random_dessert['calories']} kcal")
        st.markdown(f"**Prep Time:** {random_dessert['prep_time']} minutes")
        st.markdown(f"**Trivia:** {random_dessert['cultural_trivia']}")
    else:
        st.warning("No desserts found for the selected filters.")
else:
    st.info("Use the 'Surprise Me' button to display a random dessert.")

# Additional Trivia Button
st.subheader("🧠 Dessert Trivia")
if st.button("Show Random Trivia"):
    random_trivia = filtered_data.sample(1)["cultural_trivia"].iloc[0]
    st.markdown(f"**Trivia:** {random_trivia}")
else:
    st.info("Click the button to see a random trivia fact.")

# Note about placeholders
st.sidebar.info("Desserts with missing details have placeholders. Add new entries to improve the dataset.")

