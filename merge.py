import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
@st.cache_data  # Cache data to avoid loading it multiple times
def load_data():
    # Assuming your dataset is in a CSV file named 'data.csv'
    data = pd.read_csv('final.csv')
    return data

data = load_data()

# Sidebar for selecting state
selected_state = st.sidebar.selectbox('Select State', data['Area_Name'].unique())

# Filter data for the selected state
state_data = data[data['Area_Name'] == selected_state]

# Group by 'Year', summing up 'total_case_sum'
grouped_data = state_data.groupby('Year')['total_case_sum'].sum().reset_index()

# Plot the graph
st.write(f"## Total Case Sum Over Years for {selected_state}")
plt.figure(figsize=(10, 6))
plt.plot(grouped_data['Year'], grouped_data['total_case_sum'], marker='o')
plt.xlabel('Year')
plt.ylabel('Total Case Sum')
plt.title(f'Total Case Sum Over Years for {selected_state}')
st.pyplot(plt)