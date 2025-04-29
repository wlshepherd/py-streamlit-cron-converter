FORMATTING_LOOKUP_TABLE = {
    "weekday" :{
        1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 
        5: "Friday", 6: "Saturday", 7: "Sunday"
    },
    "month" : {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    },
    "hour" : {    
        0: "Midnight", 1: "1 AM", 2: "2 AM", 3: "3 AM", 4: "4 AM", 
        5: "5 AM", 6: "6 AM", 7: "7 AM", 8: "8 AM", 9: "9 AM", 
        10: "10 AM", 11: "11 AM", 12: "Noon", 13: "1 PM", 14: "2 PM", 
        15: "3 PM", 16: "4 PM", 17: "5 PM", 18: "6 PM", 19: "7 PM", 
        20: "8 PM", 21: "9 PM", 22: "10 PM", 23: "11 PM"
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


def is_input_in_alternate_lookup(input_value: str, unit: str) -> bool:
    """Checks if the input value is in the alternate lookup table for the given unit."""
    alternate_key = f"{unit}_alternate"
    lookup_table = FORMATTING_LOOKUP_TABLE.get(alternate_key)
    if lookup_table and input_value in lookup_table:
        return True
    return False


def cron_time_converter(input: str, min_value: int, max_value: int, unit: str):
    """Converts the input value to a cron-style representation with descriptive output."""
    lookup_table = FORMATTING_LOOKUP_TABLE.get(unit)
    alternate_table = FORMATTING_LOOKUP_TABLE.get(f"{unit}_alternate")

    # single value
    if input.isdigit():
        value = int(input)
        if min_value <= value <= max_value:
            if lookup_table:
                return lookup_table.get(value, f"The task will run at {unit} {value}")
            return f"The task will run at {unit} {value}."
        return f"Error: {unit} value out of range."

    # all values
    if input == "*":
        return f"At every {unit}."

    # list of values
    if "," in input:
        parts = input.split(",")
        formatted_parts = []
        for part in parts:
            if part.isdigit() and min_value <= int(part) <= max_value:
                formatted_parts.append(lookup_table.get(int(part), part) if lookup_table else part)
            elif part in alternate_table:
                formatted_parts.append(alternate_table.get(part, part))
            else:
                return f"Error: Invalid or out-of-range {unit} value."
        return f"At {unit}s: {', '.join(formatted_parts)}."
                
    # range of values
    if "-" in input and "/" not in input:
        parts = input.split("-")
        if len(parts) == 2:
            try:
                start = int(parts[0]) if parts[0].isdigit() else None
                end = int(parts[1]) if parts[1].isdigit() else None
                formatted_start = lookup_table.get(start) if start else alternate_table.get(parts[0])
                formatted_end = lookup_table.get(end) if end else alternate_table.get(parts[1])
                if formatted_start and formatted_end:
                    return f"At every {unit} from {formatted_start} to {formatted_end}."
                return f"Error: Range values must be valid {unit} inputs."
            except ValueError:
                return f"Error: Invalid range format or values."

    # step values
    if "/" in input:
        base, step = input.split("/")
        
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
    
    # check for alternate values
    if is_input_in_alternate_lookup(input, unit):
        formatted_value = alternate_table.get(input)
        if formatted_value:
            return f"The task will run at {formatted_value}."
        return f"Error: Invalid {unit} input."

    return f"Error: Invalid {unit} input."
