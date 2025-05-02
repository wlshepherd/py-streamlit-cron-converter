FORMATTING_LOOKUP_TABLE = {
    "minute": {
        i: f"{i} past" for i in range(0, 60)
    },
    
    "hour" : {    
        0: "Midnight", 1: "1 AM", 2: "2 AM", 3: "3 AM", 4: "4 AM", 
        5: "5 AM", 6: "6 AM", 7: "7 AM", 8: "8 AM", 9: "9 AM", 
        10: "10 AM", 11: "11 AM", 12: "Noon", 13: "1 PM", 14: "2 PM", 
        15: "3 PM", 16: "4 PM", 17: "5 PM", 18: "6 PM", 19: "7 PM", 
        20: "8 PM", 21: "9 PM", 22: "10 PM", 23: "11 PM"
    },
    
    "day" : {
        1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th",
        6: "6th", 7: "7th", 8: "8th", 9: "9th", 10: "10th",
        11: "11th", 12: "12th", 13: "13th", 14: "14th", 15: "15th",
        16: "16th", 17: "17th", 18: "18th", 19: "19th", 20: "20th",
        21: "21st", 22: "22nd", 23: "23rd", 24: "24th", 25: "25th",
        26: "26th", 27: "27th", 28: "28th", 29: "29th", 30: "30th",
        31: "31st"
    },
    
    "month" : {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    },
    
    "weekday" :{
        1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 
        5: "Friday", 6: "Saturday", 7: "Sunday"
    },
    
    "month_alternate" : {
        "JAN": "January", "FEB": "February", "MAR": "March", "APR": "April",
        "MAY": "May", "JUN": "June", "JUL": "July", "AUG": "August",
        "SEP": "September", "OCT": "October", "NOV": "November", "DEC": "December"
    },
    
    "weekday_alternate" : {
        "MON": "Monday", "TUE": "Tuesday", "WED": "Wednesday", "THU": "Thursday",
        "FRI": "Friday", "SAT": "Saturday", "SUN": "Sunday"
    }
}


def single_value_converter(input: str, min_value: int, max_value: int, unit: str):
    """Converts a single value input to a human-readable format."""
    lookup_table = FORMATTING_LOOKUP_TABLE.get(unit)
    if min_value <= int(input) <= max_value:
        return lookup_table.get(int(input))
    else:
        return f"Error: {input} is out of range for {unit}."
    

def format_list(values: list, max_value: int, min_value: int, unit: str,):
    """Formats a list of values into a human-readable string."""
    lookup_table = FORMATTING_LOOKUP_TABLE.get(unit)
    formatted_values = []
    for part in values:
        try:
            part_int = int(part)
            if min_value <= part_int <= max_value:
                formatted_values.append(lookup_table.get(part_int, str(part_int)))
            else:
                return f"Error: {part} is out of range for {unit}."
        except ValueError:
            if part in lookup_table:  
                formatted_values.append(lookup_table.get(part, part))
            else:
                return f"Error: Invalid {unit} value."
    return f"At {unit}s: {', '.join(formatted_values)}."


def format_range(start: str, end: str, min_value: int, max_value: int, unit: str):
    """Formats a range of values into a human-readable string."""
    lookup_table = FORMATTING_LOOKUP_TABLE.get(unit, {})
    alternate_table = FORMATTING_LOOKUP_TABLE.get(f"{unit}_alternate", {})
    if start.isdigit() and end.isdigit():
        start, end = int(start), int(end)
        if not (min_value <= start <= max_value and min_value <= end <= max_value):
            return f"Error: Range values must be within {min_value} and {max_value}."
        formatted_start = lookup_table.get(start, alternate_table.get(str(start), str(start)))
        formatted_end = lookup_table.get(end, alternate_table.get(str(end), str(end)))
        return f"At every {unit} from {formatted_start} to {formatted_end}."
    return f"Error: Invalid range format or values."


def format_step(base: str, step: str, min_value: int, max_value: int, unit: str):
    """Formats step values into a human-readable string."""
    lookup_table = FORMATTING_LOOKUP_TABLE.get(unit)
    alternate_table = FORMATTING_LOOKUP_TABLE.get(f"{unit}_alternate")
    if not step.isdigit() or int(step) <= 0:
        return f"Error: Invalid {unit} step value."
    step = int(step)
    if base == "*":
        return f"At every {step} {unit}."
    if "-" in base:
        try:
            start, end = map(int, base.split("-"))
            if min_value <= start <= end <= max_value:
                return f"At every {step} {unit} from {lookup_table.get(start, start)} to {lookup_table.get(end, end)}."
        except ValueError:
            return f"Error: Invalid range or step value."
    if base.isdigit() and min_value <= int(base) <= max_value:
        return f"The task will run at {lookup_table.get(int(base), base)} and every {step} {unit} after that."
    elif base in alternate_table:
        return f"The task will run at {alternate_table.get(base)} and every {step} {unit} after that."
    return f"Error: Invalid base value."   


def is_input_in_alternate_lookup(input_value: str, unit: str) -> bool:
    """Checks if the input value is in the alternate lookup table for the given unit."""
    alternate_key = f"{unit}_alternate"
    lookup_table = FORMATTING_LOOKUP_TABLE.get(alternate_key)
    if lookup_table and input_value in lookup_table:
        return True
    return False


def cron_time_converter(input: str, min_value: int, max_value: int, unit: str):
    """Converts the input value to a cron-style representation with descriptive output."""
    alternate_table = FORMATTING_LOOKUP_TABLE.get(f"{unit}_alternate")
    if input == "*":
        return f"At every {unit}."
    if input.isdigit():
        single_value = single_value_converter(input, min_value, max_value, unit)
        return single_value if "Error" in single_value else f"At {unit} {single_value}"
    if "," in input:
        values = input.split(",")
        return format_list(values, max_value, min_value, unit)
    if "-" in input and "/" not in input:
        start_value, end_value = input.split("-")
        return format_range(start_value, end_value, min_value, max_value, unit)
    if "/" in input:
        base, step = input.split("/")
        return format_step(base, step, min_value, max_value, unit)
    if is_input_in_alternate_lookup(input, unit):
        formatted_value = alternate_table.get(input)
        if formatted_value:
            return f"The task will run at {formatted_value}."
    else:
        return f"Error: Invalid {unit} input."
