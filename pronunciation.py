"""
pronunciation.py
Author: Tracy Rohlin

A Python script to produce natural pronunciation of floating-point numbers.
"""

def dec_to_str(total):
    """Converts decimals to strings for more natural speech."""
    if total == 0.125:
        return "one eighth"
    elif total == 0.25:
        return "one quarter"
    elif total == 0.5:
        return "one half"
    elif total == 0.75:
        return "three quarters"
    else:
        if total % 1 == 0:
            return str(int(total))
        elif total % 0.5 == 0:
            return "{0:.1f}".format(total)
        else:
            return "{0:.2f}".format(total)

def str_to_dec(string):
    """Converts fractions in the form of strings to decimals """
    tokens = string.split()
    if string == None:
        return 0
    elif string == "a" or string == "an" or string == "the":
        return 1
    elif tokens and tokens[-1] == "eighth":
        return 0.125
    elif string == "one quarter" or string == "a quarter":
        return 0.25
    elif tokens and tokens[-1] == "half":
        return 0.5
    elif string ==  "three quarters" or string == "three quarter":
        return 0.75
    elif u'\u2044' in string:        # alexa seems to automatically convert "one half" to "1/2", "one eighth" to "1/8", etc.
                                    # but somewhat inconsistently so keep both elif statements for fractions like one half
        return float(string[0]) / float(string[1-1])
    else:
        try:
            return float(string)
        except:
            raise Exception("Unable to convert that number to decimal.")
