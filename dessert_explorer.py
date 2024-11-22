import streamlit as st
import pandas as pd

# Title and description
st.title("🌍 Global Dessert Explorer")
st.write("Discover desserts from around the world!")
st.write("🎉 Use the sidebar to filter desserts or explore the data!")

# Load the dessert dataset
try:
    data = pd.read_csv("validated_global_dessert_data.csv")
    st.write("Dataset loaded successfully!")
except FileNotFoundError:
    st.error("Dataset not found. Please upload 'validated_global_dessert_data.csv' to the correct directory.")
    data = None

# Load filtering options
try:
    filter_options = pd.read_csv("filter_options_summary.csv")
    regions = eval(filter_options[filter_options["Filter"] == "Region"]["Options"].values[0])
    flavor_profiles = eval(filter_options[filter_options["Filter"] == "Flavor Profile"]["Options"].values[0])
except FileNotFoundError:
    st.warning("Filter options file not found. Defaulting to basic options.")
    regions = ["Global", "France", "Italy", "North America", "Asia", "Europe"]
    flavor_profiles = ["fruity", "sweet", "creamy", "light", "citrusy", "chocolatey", "earthy"]

# Sidebar filters
if data is not None:
    st.sidebar.header("Filter Desserts")

    # Region filter
    selected_region = st.sidebar.selectbox("Select a Region", ["All"] + regions)
    # Flavor profile filter
    selected_flavor = st.sidebar.selectbox("Select a Flavor Profile", ["All"] + flavor_profiles)

    # Apply filters
    filtered_data = data
    if selected_region != "All":
        filtered_data = filtered_data[filtered_data["region"] == selected_region]
    if selected_flavor != "All":
        filtered_data = filtered_data[filtered_data["flavor_profile"].str.contains(selected_flavor, na=False, case=False)]

    # Display filtered data
    st.subheader("Filtered Desserts")
    st.write(filtered_data)

    # Add bar chart for calories distribution
    st.subheader("Dessert Calories Distribution")
    st.bar_chart(filtered_data["calories"])

    # Add random dessert generator
    if st.button("Surprise Me with a Dessert!"):
        random_dessert = filtered_data.sample(1)
        st.write("Here's your random dessert:")
        st.write(random_dessert[["dessert_name", "region", "calories", "prep_time"]])
        st.image(random_dessert["image_url"].values[0], width=300)
else:
    st.warning("The app cannot function without the dataset. Please ensure it's uploaded.")
