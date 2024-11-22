import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("expanded_global_dessert_data.csv")

# App title
st.title("🍰 Welcome to the Global Dessert Explorer!")
st.markdown("""
### About This App:
The **Global Dessert Explorer** is your gateway to discovering desserts from around the world! Whether you're a food enthusiast, a dessert lover, or just curious, this app allows you to:
- Filter desserts by region, flavor profile, and calorie range.
- Explore detailed information about each dessert, including cultural trivia.
- Visualize trends in desserts across regions and flavor profiles.

Use the filters in the sidebar to narrow down your search and find desserts that pique your interest. Enjoy exploring the sweet world of desserts! 🌍
""")

# Load data
data = load_data()

# Sidebar filters
st.sidebar.header("Filter Options")
regions = st.sidebar.multiselect("Select Region(s):", data["region"].unique(), default=data["region"].unique())
flavor_profiles = st.sidebar.multiselect("Select Flavor Profile(s):", data["flavor_profile"].str.split(", ").explode().unique(), default=[])
calorie_range = st.sidebar.slider("Select Calorie Range:", int(data["calories"].min()), int(data["calories"].max()), (50, 1000))

# Apply filters
filtered_data = data[
    (data["region"].isin(regions)) &
    (data["calories"].between(calorie_range[0], calorie_range[1]))
]
if flavor_profiles:
    filtered_data = filtered_data[filtered_data["flavor_profile"].str.contains("|".join(flavor_profiles), case=False, na=False)]

# Display filtered data
st.header("Filtered Desserts")
st.write(f"Showing {len(filtered_data)} desserts")
st.dataframe(filtered_data[["dessert_name", "region", "flavor_profile", "calories", "prep_time"]])

# Dessert details
st.header("Dessert Details")
selected_dessert = st.selectbox("Select a Dessert:", filtered_data["dessert_name"].unique())

if selected_dessert:
    dessert = filtered_data[filtered_data["dessert_name"] == selected_dessert].iloc[0]
    st.subheader(dessert["dessert_name"])
    st.image(dessert["image_url"], caption=dessert["dessert_name"], use_column_width=True)
    st.write(f"**Region:** {dessert['region']}")
    st.write(f"**Flavor Profile:** {dessert['flavor_profile']}")
    st.write(f"**Calories:** {dessert['calories']}")
    st.write(f"**Prep Time:** {dessert['prep_time']} minutes")
    st.write(f"**Trivia:** {dessert['cultural_trivia']}")

# Visualizations
st.header("Visualizations")
if st.checkbox("Show Dessert Counts by Region"):
    region_counts = filtered_data["region"].value_counts()
    plt.figure(figsize=(10, 6))
    plt.bar(region_counts.index, region_counts.values)
    plt.title("Count of Desserts by Region")
    plt.xlabel("Region")
    plt.ylabel("Number of Desserts")
    st.pyplot(plt)

if st.checkbox("Show Average Calories and Prep Time by Region"):
    avg_stats_by_region = filtered_data.groupby("region")[["calories", "prep_time"]].mean()
    plt.figure(figsize=(10, 6))
    plt.plot(avg_stats_by_region.index, avg_stats_by_region["calories"], marker="o", label="Average Calories")
    plt.plot(avg_stats_by_region.index, avg_stats_by_region["prep_time"], marker="o", label="Average Prep Time (minutes)")
    plt.title("Average Calories and Prep Time by Region")
    plt.xlabel("Region")
    plt.ylabel("Average Value")
    plt.legend()
    st.pyplot(plt)
