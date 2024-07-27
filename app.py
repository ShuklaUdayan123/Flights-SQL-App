import streamlit as st
import pandas as pd
from dbhelper import DB
import plotly.graph_objects as go
import plotly.express as px

# Initialize the database connection
db = DB()

st.sidebar.title('Flights Analytics')

user_option = st.sidebar.selectbox('Menu', ['Select One', 'Check Flights', 'Analytics'])

if user_option == 'Check Flights':
    st.title('Check Flights')

    col1, col2 = st.columns(2)
    city = db.fetch_city_names()
    
    if city:
        with col1:
            source = st.selectbox('Source', city)
        with col2:
            destination = st.selectbox('Destination', city)
        
        if st.button('Search'):
            results = db.fetch_all_flights(source, destination)
            if results:
                df_results = pd.DataFrame(results, columns=["Airline", "Route", "Dep_Time", "Duration", "Price"])
                st.dataframe(df_results)
            else:
                st.write("No flights found for the selected route.")
elif user_option == 'Analytics':
    airline, frequency= db.fetch_airline_frequency()
    fig = go.Figure(
        go.Pie(
            labels=airline,
            values=frequency,
            hoverinfo="label+percent",
            textinfo="value"
        )

    )
    st.header("Pie chart")
    st.plotly_chart(fig)

    city, frequency1 = db.busy_airport()

    fig= px.bar(
        x=city,
        y=frequency1
    )
    
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    date, frequency2 = db.daily_frequency()

    fig= px.line(
        x=date,
        y=frequency2
    )
    
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

else:
    pass
