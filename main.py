import logging
import os
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, convert_errors

app = Flask(__name__)
ask = Ask(app, "/", None, "templates.yaml")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def launch():
    welcome_msg = render_template('welcome')
    reprompt_msg = render_template('reprompt')
    return question(welcome_msg).reprompt(reprompt_msg)

# TODO Recipe loading?

    # Include steps?
    # Directions to read faster/slower
    # Quantity?

# TODO Unit Conversions

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
    elif string == "one quarter":
        return 0.25
    elif tokens and tokens[-1] == "half":
        return 0.5
    elif string ==  "three quarters" or string == "three quarter":
        return 0.75
    else:
        try:
            return float(string)
        except:
            raise Exception("Unable to process that number")

@ask.intent('ImperialIntent')
def convert_imperial(from_unit, to_unit, fraction="0", whole_num="0"):
    """Converts from one unit to another unit in the imperial system."""
    conversions = {"ga":{"qu":4, "pi": 8, "cu":16, "ou":128, "ta":256},
                   "qu":{"ga":0.25, "pi":2, "cu": 4, "ou":32, "ta":64},
                   "pi":{"ga":0.125, "qu": 0.5, "cu":2, "ou":16, "ta":32},
                   "cu":{"ga":0.0625, "qu":0.25, "ou": 8, "ta":16},
                   "ou":{"ga":0.0078125, "qu":0.03125, "cu":0.125, "ta":2},
                   "ta":{"ou": 0.5}
                   }
    quantity = str_to_dec(whole_num) + str_to_dec(fraction)
    verb = ""
    total = 0
    unit_from = from_unit[:2]
    unit_to = to_unit[:2]
    try:
        if unit_from in conversions and unit_to in conversions[unit_from]:
            total = quantity * conversions[unit_from][unit_to]
            total = round(total * 8) / 8
            verb = "are" if total > 1 else "is"
        elif unit_from == "ta" and unit_to == "te":
            total = round((quantity * 8 * 3)) / 8
            verb = "are" if total > 1 else "is"
        elif unit_from == "te" and unit_to == "ta":
            total = round((quantity * 8 / 3.0)) / 8
            verb = "are" if total > 1 else "is"
    except:
        raise Exception("I'm sorry I did not understand.")


    if total == 0 and verb == "":
        speech_text = "Sorry, I didn't understand"
    else:
        if quantity < 1:
            orig_unit = from_unit[:-1] if from_unit[-1] == "s" else from_unit
            unit_text = "of a " + orig_unit
        else:
            unit_text = from_unit
        speech_text ="There {0} {1} {2} in {3} {4}".format(verb, dec_to_str(total), to_unit, dec_to_str(quantity), unit_text)

    return statement(speech_text)


# TODO Ingredient substitutions


@ask.intent('JuiceIntent', convert={"num": int}, default={"num":1})
def juice(fruit, num):
    """Explains how much juice is in a piece of fruit."""
    if fruit == "lemons" or fruit == "lemon":
        factor = 3
    elif fruit == "limes" or fruit == "lime":
        factor = 2
    else:
        factor = 4
    amount = str_to_dec(num)
    tbs = dec_to_str(amount * factor)
    tsps = dec_to_str(amount * factor * 3)
    speech_text = "There are {0} tablespoons or {1} teaspoons of juice in {2} {3}".format(tbs, tsps, num, fruit)
    return statement(speech_text)

@ask.intent('ZestIntent', default={"num":"1"})
def zest(fruit, num):
    """Explains how much zest is in a fruit"""
    if fruit == "lemons" or fruit == "lemon":
        factor = 3
    elif fruit == "limes" or fruit == "lime":
        factor = 2
    else:
        factor = 6
    amount = str_to_dec(num)
    tsps = dec_to_str(factor * amount)
    tbs = dec_to_str(round((factor*amount)/3.0, 1))
    speech_text = "There are {0} teaspoons or {1} tablespoons of zest in {2} {3}".format(tsps, tbs, num, fruit)
    return statement(speech_text)

# dried to fresh herb conversion

def herb_statement(verb, total, unit):
    """"Returns the correct amount of herb"""
    if total == 0:
        amount_text = "a pinch of"
    else:
       amount_text = verb + " " + dec_to_str(total) + " " +  unit
    return amount_text


@ask.intent("HerbIntent", default={'num': 'a'})
def herb(num, orig_unit):
    """Converts fresh herb to dried herb"""
    amount = str_to_dec(num)
    if orig_unit == "cup" or orig_unit == "cups":                                 # if asking for dried in a cup
        tbs = 16 * amount
        total = tbs * 1/3.0
        total = round(total * 2) / 2
        if total >= 16:
            cups = round(total / 16 * 8)/ 8
            unit = "cups" if cups > 1 else "cup"
            verb = "are" if cups > 1 else "is"
        else:
            unit = "tablespoons" if total > 1 else "tablespoon"
            verb = "are" if total > 1 else "is"
    elif orig_unit == "tablespoon" or orig_unit == "tablespoons":                # if asking for dried in a tablespoon
        total = amount * 1.0/3.0
        total = round(total * 4) / 4                            # want # of tsps by the quarter
        unit = "teaspoons" if total > 1 else "teaspoon"         # (get more granular with smaller units)
        verb = "are" if total > 1 else "is"
    else:                                                       # if asking for dried in a tsp
        total = amount * 1/3.0
        total = round(total * 8) / 8                            # want number of tsps by the eighth
        unit = "teaspoons" if total > 1 else "teaspoon"
        verb = "are" if total > 1 else "is"

    amount_text = herb_statement(verb, total, unit)

    speech_text = "There {0} dried herbs in {1} {2} of fresh herbs".format(amount_text, dec_to_str(num), orig_unit)
    return statement(speech_text)




@ask.intent('AMAZON.StopIntent')
def stop():
    return statement("Goodbye")


@ask.intent('AMAZON.CancelIntent')
def cancel():
    return statement("Goodbye")

@ask.intent('AMAZON.HelpIntent')
def stop():
    return statement("This app helps you in the kitchen as you cook.")

@ask.session_ended
def session_ended():
    return statement("BOOOOO")
    # return "{}", 200



if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
