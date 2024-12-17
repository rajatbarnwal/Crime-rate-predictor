import streamlit as st
import pickle
import pandas as pd
import sklearn
from sklearn.preprocessing import LabelEncoder
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
import subprocess
import sys

# Function for graph view

def Analyze1():
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



# funtion for map view
def Analyze():
    st.set_page_config(layout="wide")
    json1 = f"states_india.geojson"

    m = folium.Map(location=[23.47, 77.94], tiles='CartoDB positron', name="Light Map",
                   zoom_start=5,
                   attr='My Data Attribution')

    india_covid = f"For_2010.csv"
    india_covid_data = pd.read_csv(india_covid)
    choice = ['total_case_sum', 'total_Murder_victim']
    choice_selected = st.selectbox("Select Choice ", choice)
    folium.Choropleth(
        geo_data=json1,
        name="choropleth",
        data=india_covid_data,
        columns=["state code", choice_selected],
        key_on="feature.properties.state_code",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=.1,
        legend_name=choice_selected + "(%)",
    ).add_to(m)
    folium.features.GeoJson('states_india.geojson', name="LSOA Code",
                            popup=folium.features.GeoJsonPopup(fields=['st_nm'])).add_to(m)
    folium_static(m, width=1600, height=950)


df= pd.read_csv('final.csv')

indian_states = [
    'Andaman & Nicobar Islands','Andhra Pradesh', 'Arunachal Pradesh', 'Assam',
 'Bihar', 'Chandigarh', 'Chhattisgarh','Delhi', 'Goa', 'Gujarat' ,'Haryana',
 'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand' ,'Karnataka' ,'Kerala',
 'Lakshadweep' ,'Madhya Pradesh', 'Maharashtra' ,'Manipur', 'Meghalaya',
 'Mizoram' ,'Nagaland' ,'Odisha' ,'Puducherry' ,'Punjab', 'Rajasthan', 'Sikkim',
 'Tamil Nadu', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
 'Dadra & Nagar Haveli' ,'Daman & Diu']

st.title("CRIME RATE PREDICTOR & ANALYSIS")
navi = st.sidebar.radio("Navigation",['HOME','PREDICTION','ANALYSIS'])

if navi == "HOME":
    st.image("crime-analysis.jpg")
    s, r = st.columns(2)
    if s.button("INFO.."):
        st.subheader("Method")
        st.image("infor.png")

    if r.button("Contacts"):
        st.write("NAME- RAJAT, MTECH CSE")


if navi == "PREDICTION":
    st.image("pred.png")
    st.subheader("Enter the values")
    m, k = st.columns(2)
    state = m.selectbox("Choose a state", indian_states)
    year = k.number_input("Enter the Year", 1950, 2100)

    le = LabelEncoder()
    df['Area_Name'] = le.fit_transform(df['Area_Name'])
# encoding the input data Area_Name.
    state = le.transform([state])[0]
    input_data = [[state,year]]
    st.write("Please click on the Below button")

    with open('crime_pickle', 'rb') as f:
        mp1 = pickle.load(f)
    result = mp1.predict(input_data)

    if st.button("PRED"):
        if result >= 20000 and result <= 200000:
            st.write("Total cases: ", result[0])
            st.write("Moderate Level")
        elif result >= 200001:
            st.write("Total cases: ", result[0])
            st.write("High Level")
        else:
            st.write("Total cases: ", result[0])
            st.write("Low Level")


    if st.button("Thanks"):
        st.balloons()


if navi == "ANALYSIS":
    st.subheader("To see the Analysis please choose the option accordingly")
    if st.button("MAP VIEW"):
        subprocess.run(["streamlit","run","main.py"])
    if st.button("GRAPH VIEW"):
        subprocess.run(["streamlit","run","merge.py"])







