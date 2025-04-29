import streamlit as st

MINUTES_RANGE = (0, 59)
HOURS_RANGE = (0, 23)
DAYS_RANGE = (1, 31)
MONTH_RANGE = (1, 12)
WEEK_RANGE = (0, 6)

def cron_expression_generator(unit, min_value, max_value, option, input_value):
    """Function to generate individual cron expressions based on user input."""
    if option == "Single Value":
        if input_value.isdigit() and min_value <= int(input_value) <= max_value:
            return input_value
        else:
            st.error(f"Invalid value for {unit}. Enter a number between {min_value} and {max_value}.")
            return None
    elif option == "All Values (*)":
        return "*"
    elif option == "List of Values":
        values = input_value.split(",")
        if all(value.isdigit() and min_value <= int(value) <= max_value for value in values):
            return ",".join(values)
        else:
            st.error(f"Invalid list for {unit}. Ensure all values are within {min_value}-{max_value}.")
            return None
    elif option == "Range of Values":
        parts = input_value.split("-")
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            start, end = int(parts[0]), int(parts[1])
            if min_value <= start <= max_value and min_value <= end <= max_value and start <= end:
                return f"{start}-{end}"
            else:
                st.error(f"Invalid range for {unit}. Ensure values are within {min_value}-{max_value} and start <= end.")
                return None
    elif option == "Step Values":
        if "/" in input_value:
            parts = input_value.split("/")
            if len(parts) == 2 and parts[1].isdigit():
                step = int(parts[1])
                return f"{parts[0]}/{step}"
            else:
                st.error(f"Invalid step format for {unit}. Use '*/step' or 'start-end/step'.")
                return None
    return "*"


def display_generate_cron_expression():
    """Function to display and combine all parts into a single cron expression."""
    st.subheader("Cron Expression Generator")

    with st.form(key="cron_form"):
        minute_option = st.radio("Minute:", options=["Single Value", "All Values (*)", "List of Values", "Range of Values", "Step Values"], key="minute")
        minute_input = st.text_input(f"Enter minute(s) (range: {MINUTES_RANGE[0]}-{MINUTES_RANGE[1]}):", value="*", key="minute_input")

        hour_option = st.radio("Hour:", options=["Single Value", "All Values (*)", "List of Values", "Range of Values", "Step Values"], key="hour")
        hour_input = st.text_input(f"Enter hour(s) (range: {HOURS_RANGE[0]}-{HOURS_RANGE[1]}):", value="*", key="hour_input")

        day_option = st.radio("Day:", options=["Single Value", "All Values (*)", "List of Values", "Range of Values", "Step Values"], key="day")
        day_input = st.text_input(f"Enter day(s) (range: {DAYS_RANGE[0]}-{DAYS_RANGE[1]}):", value="*", key="day_input")

        month_option = st.radio("Month:", options=["Single Value", "All Values (*)", "List of Values", "Range of Values", "Step Values"], key="month")
        month_input = st.text_input(f"Enter month(s) (range: {MONTH_RANGE[0]}-{MONTH_RANGE[1]}):", value="*", key="month_input")

        weekday_option = st.radio("Weekday:", options=["Single Value", "All Values (*)", "List of Values", "Range of Values", "Step Values"], key="weekday")
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
