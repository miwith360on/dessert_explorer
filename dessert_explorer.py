import streamlit as st
import pandas as pd

# Title of the app
st.title("Global Dessert Explorer")

# Load the dataset
try:
    # Load the data from the CSV file
    data = pd.read_csv("enriched_dessert_data.csv")
    st.write("Dataset loaded successfully!")
    st.write(data.head())  # Display the first few rows
except FileNotFoundError:
    st.error("Dataset not found. Please upload 'enriched_dessert_data.csv' to the correct directory.")

# Add a button to display a random dessert
if st.button("Surprise Me with a Dessert!"):
    random_dessert = data.sample(1)
    st.write("Here's your random dessert:")
    st.write(random_dessert)

# Add any additional features here (e.g., filters, visualizations)
