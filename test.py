import streamlit as st
import pandas as pd
import numpy as np

st.title("Uber pickups in NYC")

DATE_COLUMN = "date/time"
DATA_URL = (
    "https://s3-us-west-2.amazonaws.com/"
    "streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)


@st.cache_data
def load_data(nrows):
    """Load data from the specified URL and return a DataFrame."""
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


# Create a text element and let the reader know the data is loading.
data_load_state = st.text("Loading data...")
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache_data)")

# Create a checkbox to show the raw data
if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)

# Draw a histogram
st.subheader("Number of pickups by hour")
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)

hour_to_filter = st.slider("hour", 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader(f"Map of all pickups at {hour_to_filter}:00")
st.map(filtered_data)

with st.form("my_form"):
    st.write("Please fill out this form")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120, value=25)
    feedback = st.text_area("Your Feedback")
    option_1 = st.checkbox("Option 1")
    option_2 = st.checkbox("Option 2")
    option_3 = st.checkbox("Option 3")
    submitted_button = st.form_submit_button("Submit")

if submitted_button:
    st.write(f"Thank you for your feedback, {name}!")
    st.write(f"Age: {age}")
    st.write(f"Feedback: {feedback}")
    st.write("You selected:")
    if option_1:
        st.write("Option 1")
    if option_2:
        st.write("Option 2")
    if option_3:
        st.write("Option 3")
