# The database won't allow for backslashes, quotes or double quotes.  So through this function we will prepare any string that has those attributes to allow it to be inputted
    # into the database

# Takes string and replaces quotes, double quotes, and backslashes w/ proper backslash placements
def stringify(s): 

    s = s.replace("\\", "\\\\") #replacing backslash
    s = s.replace("'", "\\'") #replacing single quote
    s = s.replace('"', '\\"') #replacing double quote

    return s


# This is unused, I thought it was going to be an issue but it wasn't.