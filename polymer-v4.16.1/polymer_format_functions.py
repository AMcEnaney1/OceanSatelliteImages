## Aidan McEnaney
## August 1st, 2023
## Functions used for various formatting tasks when calling POLYMER

def ensure_start_end_chars(text, chr):
    if not text.startswith(chr):
        text = chr + text
    if not text.endswith(chr):
        text = text + chr

    while chr + chr in name: # Makes sure we don't have multiple of chr in a row anywhere
        name = name.replace(chr + chr, chr) # Replace any occurrences of consecutive chr with a single chr
    return text