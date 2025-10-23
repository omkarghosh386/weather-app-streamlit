import streamlit as st
import requests
from datetime import datetime


# ---------- Function: Apply Background Color ----------
def set_background(color_code):
    """Apply a background color dynamically using CSS."""
    st.markdown(
        f"""
        <style>
        body {{
            background-color: {color_code};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# ---------- Function: Convert Celsius to Fahrenheit ----------
def c_to_f(celsius):
    """Convert Celsius to Fahrenheit."""
    return round((celsius * 9 / 5) + 32, 1)


# ---------- Function: Fetch Current Weather ----------
def get_weather(city, api_key):
    """Fetch current weather data from OpenWeatherMap."""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    response = requests.get(url, params=params)
    return response.json()


# ---------- Function: Fetch 3-Day Forecast ----------
def get_forecast(city, api_key):
    """Fetch 3-day forecast data."""
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": api_key, "units": "metric"}
    response = requests.get(url, params=params)
    return response.json()


# ---------- Streamlit App Config ----------
st.set_page_config(
    page_title="Weather App ☁️",
    page_icon="🌦️",
    layout="centered"
)

st.title("🌤️ Weather App")
st.write("Get live weather updates with a 3-day forecast.")


# ---------- Sidebar: Theme Selector ----------
st.sidebar.header("🎨 Theme Options")

theme_color = st.sidebar.selectbox(
    "Choose Background Color:",
    (
        "Sky Blue (Default)",
        "Light Yellow",
        "Soft Gray",
        "Light Green",
        "Peach",
        "Lavender"
    )
)

# Map color names to HEX codes
color_map = {
    "Sky Blue (Default)": "#B3E5FC",
    "Light Yellow": "#FFF9C4",
    "Soft Gray": "#F5F5F5",
    "Light Green": "#C8E6C9",
    "Peach": "#FFE0B2",
    "Lavender": "#E1BEE7"
}

# Apply the selected background color
set_background(color_map[theme_color])


# ---------- Weather App Logic ----------
api_key = "7f7ba1f8b2a5159964ab91cf487cbc93"  # Replace with your key if needed
city_name = st.text_input("Enter City Name:")

# Unit toggle: Celsius or Fahrenheit
temp_unit = st.radio("Select Temperature Unit:", ("Celsius", "Fahrenheit"))

# Fetch weather on button click
if st.button("Get Weather"):
    if not city_name:
        st.warning("⚠️ Please enter a city name.")
    else:
        data = get_weather(city_name, api_key)

        if data.get("cod") != 200:
            st.error(f"❌ City not found: {city_name}")
        else:
            main = data.get("main", {})
            weather_desc = data["weather"][0]["description"].capitalize()
            icon_code = data["weather"][0]["icon"]
            temp_c = main.get("temp", "N/A")
            humidity = main.get("humidity", "N/A")
            pressure = main.get("pressure", "N/A")

            # Convert to Fahrenheit if selected
            temp_display = (
                f"{temp_c}°C" if temp_unit == "Celsius"
                else f"{c_to_f(temp_c)}°F"
            )

            # Weather Icon
            icon_url = (
                f"http://openweathermap.org/img/wn/"
                f"{icon_code}@2x.png"
            )

            st.image(icon_url, width=100)
            st.subheader(f"Weather in {city_name}")
            st.write(f"**Temperature:** {temp_display}")
            st.write(f"**Condition:** {weather_desc}")
            st.write(f"**Humidity:** {humidity}%")
            st.write(f"**Pressure:** {pressure} hPa")

            # ---------- 3-Day Forecast ----------
            forecast_data = get_forecast(city_name, api_key)
            st.markdown("---")
            st.subheader("📅 3-Day Forecast")

            if forecast_data.get("cod") == "200":
                forecasts = {}
                for item in forecast_data.get("list", []):
                    dt_txt = item["dt_txt"]
                    date, time = dt_txt.split()
                    if time == "12:00:00" and date not in forecasts:
                        temp = item["main"]["temp"]
                        desc = item["weather"][0]["description"].capitalize()
                        icon = item["weather"][0]["icon"]
                        forecasts[date] = (temp, desc, icon)

                for i, (date, (temp, desc, icon)) in enumerate(
                    forecasts.items()
                ):
                    if i >= 3:
                        break
                    date_obj = datetime.strptime(date, "%Y-%m-%d")
                    day_name = date_obj.strftime("%A")
                    temp_display = (
                        f"{temp}°C" if temp_unit == "Celsius"
                        else f"{c_to_f(temp)}°F"
                    )

                    col1, col2, col3 = st.columns([1, 2, 3])
                    with col1:
                        st.image(
                            f"http://openweathermap.org/img/wn/{icon}.png"
                        )
                    with col2:
                        st.write(f"**{day_name}**")
                    with col3:
                        st.write(f"{temp_display}, {desc}")