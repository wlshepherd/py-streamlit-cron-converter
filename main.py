import streamlit as st
from functions.human_readable import cron_time_converter
from functions.generate_expression import cron_expression_generator

st.title("Cron Conversion Tool")
st.subheader("Convert your cron expressions to human-readable format and vice versa.")

MINUTES_RANGE = (0, 59)
HOURS_RANGE = (0, 23)
DAYS_RANGE = (1, 31)
MONTH_RANGE = (1, 12)
WEEK_RANGE = (1, 31)


st.sidebar.title("Mode Selection")
mode = st.sidebar.radio("Choose a mode:", ["Human Readable Format", "Generate Cron Expression"])


def display_human_readable_format():
    """Function to display the human-readable format of cron expressions."""
    st.subheader("Cron Expression to Human Readable Format")
    with st.form("cron_form"):
        cron_expression = st.text_input("Enter your cron expression:")
        submitted_button = st.form_submit_button("Convert")
        if submitted_button and cron_expression:
            try:
                inputs = cron_expression.split()
                user_input_minutes, user_input_hours, user_input_days, user_input_months, user_input_weeks = inputs
                    
                results = {
                    "minute_result": cron_time_converter(user_input_minutes, MINUTES_RANGE[0], MINUTES_RANGE[1], "minute"),
                    "hour_result": cron_time_converter(user_input_hours, HOURS_RANGE[0], HOURS_RANGE[1], "hour"),
                    "day_result": cron_time_converter(user_input_days, DAYS_RANGE[0], DAYS_RANGE[1], "day"),
                    "month_result": cron_time_converter(user_input_months, MONTH_RANGE[0], MONTH_RANGE[1], "month"),
                    "weekday_result": cron_time_converter(user_input_weeks, WEEK_RANGE[0], WEEK_RANGE[1], "weekday"),
                }
                    
                st.write(f"Minutes: {results['minute_result']}")
                st.write(f"Hour: {results['hour_result']}")
                st.write(f"Day of the Month: {results['day_result']}")
                st.write(f"Month: {results['month_result']}")
                st.write(f"Day of the Week: {results['weekday_result']}")
                
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter a cron expression.")


def display_generate_cron_expression():
    """Function to display and combine all parts into a single cron expression."""
    st.subheader("Cron Expression Generator")
    with st.form(key="cron_form"):
        minute_option = st.radio("Minute:", options=["All Values (*)", "Single Value", "List of Values", "Range of Values", "Step Values"], key="minute")
        minute_input = st.text_input(f"Enter minute(s) (range: {MINUTES_RANGE[0]}-{MINUTES_RANGE[1]}):", value="*", key="minute_input")
        
        hour_option = st.radio("Hour:", options=["All Values (*)", "Single Value", "List of Values", "Range of Values", "Step Values"], key="hour")
        hour_input = st.text_input(f"Enter hour(s) (range: {HOURS_RANGE[0]}-{HOURS_RANGE[1]}):", value="*", key="hour_input")
        
        day_option = st.radio("Day:", options=["All Values (*)", "Single Value", "List of Values", "Range of Values", "Step Values"], key="day")
        day_input = st.text_input(f"Enter day(s) (range: {DAYS_RANGE[0]}-{DAYS_RANGE[1]}):", value="*", key="day_input")
        
        month_option = st.radio("Month:", options=["All Values (*)", "Single Value", "List of Values", "Range of Values", "Step Values"], key="month")
        month_input = st.text_input(f"Enter month(s) (range: {MONTH_RANGE[0]}-{MONTH_RANGE[1]}):", value="*", key="month_input")
        
        weekday_option = st.radio("Weekday:", options=["All Values (*)", "Single Value", "List of Values", "Range of Values", "Step Values"], key="weekday")
        weekday_input = st.text_input(f"Enter weekday(s) (range: {WEEK_RANGE[0]}-{WEEK_RANGE[1]}):", value="*", key="weekday_input")
        
        submit_button = st.form_submit_button(label="Generate Cron Expression")

    if submit_button:
        minute = cron_expression_generator("minute", MINUTES_RANGE[0], MINUTES_RANGE[1], minute_option, minute_input)
        hour = cron_expression_generator("hour", HOURS_RANGE[0], HOURS_RANGE[1], hour_option, hour_input)
        day = cron_expression_generator("day", DAYS_RANGE[0], DAYS_RANGE[1], day_option, day_input)
        month = cron_expression_generator("month", MONTH_RANGE[0], MONTH_RANGE[1], month_option, month_input)
        weekday = cron_expression_generator("weekday", WEEK_RANGE[0], WEEK_RANGE[1], weekday_option, weekday_input)

        if all([minute, hour, day, month, weekday]):
            cron_expression = f"{minute} {hour} {day} {month} {weekday}"
            st.write(f"**Generated Cron Expression:** {cron_expression}")
            
        else:
            st.error("Error generating cron expression. Please check your inputs.")
        
        
def main():
    """Main function to run the Streamlit app."""
    if mode == "Human Readable Format":
        display_human_readable_format()
    elif mode == "Generate Cron Expression":
        display_generate_cron_expression()


if __name__ == "__main__":
    main()
