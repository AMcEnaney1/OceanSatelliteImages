## Aidan McEnaney
## August 1st, 2023
## Functions used for various formatting tasks when calling POLYMER

def ensure_end_char(text, chr):
    if not text.endswith(chr):
        text = text + chr

    while chr + chr in text: # Makes sure we don't have multiple of chr in a row anywhere
        text = text.replace(chr + chr, chr) # Replace any occurrences of consecutive chr with a single chr
    return text

def try_cast_to_int(variable):
    try:
        result = int(variable)
        return result
    except ValueError:
        print(f"Error: Could not cast '{variable}' to an integer.")
        return False