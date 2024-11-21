import streamlit as st
import pandas as pd

# Header and instructions
st.title("🌍 Global Dessert Explorer")
st.write("Discover desserts from around the world!")
st.write("🎉 Use the sidebar to filter desserts or click 'Surprise Me with a Dessert!' for a random treat.")

# Load the dataset
try:
    data = pd.read_csv("enriched_dessert_data.csv.csv")
    st.write("Dataset loaded successfully!")
except FileNotFoundError:
    st.error("Dataset not found. Please upload 'enriched_dessert_data.csv.csv' to the correct directory.")
    data = None

# Sidebar for filtering
if data is not None:
    st.sidebar.header("Search Desserts")
    search_term = st.sidebar.text_input("Enter a keyword to search (e.g., Chocolate)")

    # Filter the dataset based on the search term
    if search_term:
        filtered_data = data[data['Dessert Name'].str.contains(search_term, case=False, na=False)]
        st.write(f"Results for '{search_term}':")
        st.write(filtered_data)
    else:
        st.write("Showing all desserts:")
        st.write(data)

    # Add a bar chart
    st.subheader("Dessert Distribution")
    dessert_counts = data["Dessert Name"].value_counts()
    st.bar_chart(dessert_counts)

    # Add dessert images
    st.subheader("Dessert Images")
    for index, row in data.iterrows():
        st.write(f"### {row['Dessert Name']}")
        st.image(row["Image URL"], width=300)

    # Add a random dessert button
    if st.button("Surprise Me with a Dessert!"):
        random_dessert = data.sample(1)
        st.write("Here's your random dessert:")
        st.write(random_dessert)
else:
    st.warning("The app cannot function without the dataset. Please ensure it's uploaded.")

