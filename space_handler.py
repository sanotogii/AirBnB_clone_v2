import re

def check_spaces(input_string):
    # Define a regular expression pattern to match spaces after '=' and within double quotes
    pattern = r'=\s*"\s*([^"]*\s+[^"]*)\s*"'

    # Use re.findall() to find all matches of spaces after '=' and within double quotes
    matches = re.findall(pattern, input_string)

    # If matches are found, return True; otherwise, return False
    return bool(matches)

import re

def replace_spaces(input_string):
    # Define a regular expression pattern to match spaces enclosed within double quotes
    pattern = r'"\s([^"]*?)\s"'

    # Use re.sub() to replace spaces with underscores within double quotes
    modified_string = re.sub(pattern, lambda match: match.group(0).replace(' ', '_'), input_string)

    return modified_string