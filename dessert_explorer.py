import streamlit as st
import pandas as pd

# Title of the app
st.title("Global Dessert Explorer")

# Load the dataset
try:
    # Attempt to load the dataset
    data = pd.read_csv("enriched_dessert_data.csv.csv")
    st.write("Dataset loaded successfully!")
    st.write(data.head())  # Display the first few rows
except FileNotFoundError:
    st.error("Dataset not found. Please upload 'enriched_dessert_data.csv.csv' to the correct directory.")
    data = None  # Ensure `data` is defined, even if loading fails

# Check if data is loaded before proceeding
if data is not None:
    # Add a button to display a random dessert
    if st.button("Surprise Me with a Dessert!"):
        random_dessert = data.sample(1)
        st.write("Here's your random dessert:")
        st.write(random_dessert)
else:
    st.warning("The app cannot function without the dataset. Please ensure it's uploaded.")

