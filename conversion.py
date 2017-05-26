"""
conversion.py
Author: Travis Nguyen
Last Modified: May 26, 2017
"""

def celsius_to_fahrenheit(temp):
    return (float(9 * temp) / 5) + 32


def fahrenheit_to_celsius(temp):
    return float(5 * float(temp - 32)) / 9
