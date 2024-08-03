import streamlit as st
import pandas as pd

# Load dataset
file_path = 'Integrated_Dataset (1).csv'  # Update this path if needed
data = pd.read_csv(file_path)

# Streamlit app
st.title("Relocation Analyst: City Recommendations and Details")
st.write("Find the best city for you based on your preferences or get details about a specific city.")

# Sidebar for city recommendations
st.sidebar.header("City Recommendations")

weather_preference = st.sidebar.selectbox("Preferred Weather", ["Any", "Rainy", "Sunny", "Cloudy"])
temperature_preference = st.sidebar.slider("Preferred Temperature (°C)", 15, 40, (20, 30))
humidity_preference = st.sidebar.slider("Preferred Humidity (%)", 0, 100, (30, 70))
air_quality_preference = st.sidebar.slider("Preferred Air Quality Index (lower is better)", 0, 150, 50)
cost_of_living_preference = st.sidebar.slider("Maximum Estimated Cost of Living", 20000, 1200000, 50000)

def recommend_cities(weather, temp_range, humidity_range, air_quality, cost_of_living):
    recommendations = data[
        ((data['weather'] == weather) | (weather == "Any")) &
        (data['temperature'] >= temp_range[0]) & (data['temperature'] <= temp_range[1]) &
        (data['humidity'] >= humidity_range[0]) & (data['humidity'] <= humidity_range[1]) &
        (data['air_quality'] <= air_quality) &
        (data['estimated_cost_of_living'] <= cost_of_living)
    ]
    return recommendations

recommended_cities = recommend_cities(weather_preference, temperature_preference, humidity_preference, air_quality_preference, cost_of_living_preference)

st.write("## City Recommendations")
if not recommended_cities.empty:
    st.write("Based on your preferences, we recommend the following cities:")
    st.dataframe(recommended_cities)
else:
    st.write("No cities match your preferences. Please adjust your preferences and try again.")

# Input city details
st.write("## City Details")
city_name = st.text_input("Enter a city name to get details:")

if city_name:
    city_details = data[data['city'].str.contains(city_name, case=False, na=False)]
    if not city_details.empty:
        st.write(f"Details for {city_name}:")
        st.dataframe(city_details)
    else:
        st.write(f"No details found for the city: {city_name}. Please check the city name and try again.")

# Chatbot
st.write("## Chat with our Bot")

def chatbot_response(question):
    question = question.lower()
    if 'temperature less than 20' in question:
        result = data[data['temperature'] < 20]
        return result if not result.empty else "No cities with temperature less than 20°C."
    elif 'humidity less than 50' in question:
        result = data[data['humidity'] < 50]
        return result if not result.empty else "No cities with humidity less than 50%."
    elif 'budget less than 50000' in question:
        result = data[data['estimated_cost_of_living'] < 50000]
        return result if not result.empty else "No cities with a budget less than 50000."
    elif 'best air quality' in question:
        result = data.nsmallest(5, 'air_quality')
        return result if not result.empty else "No data available for air quality."
    elif 'schools' in question:
        result = data[['city', 'schools']].dropna()
        return result if not result.empty else "No data available for schools."
    else:
        return "Sorry, I don't understand that question."

# Display chatbot logo
# Uncomment the following line if you have a logo file named 'chatbot_logo.png'
# st.image('chatbot_logo.png', width=100)

# Show chatbot button
if st.button('Chat with our bot'):
    questions = [
        "Find the cities with temperature less than 20",
        "Find the cities with humidity less than 50",
        "Find the cities with a budget less than 50000",
        "Find the cities with the best air quality",
        "Show me the schools in cities"
    ]
    question = st.selectbox("Choose a question:", questions)
    
    if question:
        response = chatbot_response(question)
        if isinstance(response, pd.DataFrame):
            st.write(response)
        else:
            st.write(response)
