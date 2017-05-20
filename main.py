import logging
import os
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, convert_errors
from pronunciation import dec_to_str, str_to_dec

app = Flask(__name__)
ask = Ask(app, "/", None, "templates.yaml")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def launch():
    hello_msg = render_template('hello')
    reprompt_msg = render_template('hello_reprompt')
    return question(hello_msg).reprompt(reprompt_msg)

# TODO Recipe loading?

    # Include steps?
    # Directions to read faster/slower
    # Quantity?

# TODO Unit Conversions

@ask.intent("ThanksIntent")
def welcome():
    welcome_msg = render_template('welcome')
    return statement(welcome_msg)

@ask.intent("LoveIntent")
def love():
    love_msg = render_template('love')
    return statement(love_msg)

def convert_temperature(temperature, target_unit):
    if target_unit == "celsius":
        return statement("TO-DO")
    elif target_unit == "fahrenheit":
        return statement("TO-DO")
    else:
        return statement("TO-DO")

@ask.intent('ImperialIntent', default={"fraction":"0", "whole_num":"0"})
def convert_imperial(from_unit, to_unit, whole_num, fraction):
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
            if total > 1:
                verb = "are"
                to_unit += "s" if to_unit[-1] != "s" else to_unit
        elif unit_from == "ta" and unit_to == "te":
            total = round((quantity * 8 * 3)) / 8
            if total > 1:
                verb = "are"
                to_unit += "s" if to_unit[-1] != "s" else to_unit
        elif unit_from == "te" and unit_to == "ta":
            total = round((quantity * 8 / 3.0)) / 8
            if total > 1:
                verb = "are"
                to_unit += "s" if to_unit[-1] != "s" else to_unit # repetitive code is repetitive but *shrug*
        else:
            return statement("That unit cannot be converted to the one you wish.")
    except Exception as e:
        print(e)


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


@ask.intent('JuiceIntent', default={"num":"a"})
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


@ask.intent("HerbIntent", default={'num': 'a'}, mapping={"orig_unit":"herb_unit"})
def herb(num, orig_unit):
    """Converts fresh herb to dried herb"""
    amount = str_to_dec(num)
    if orig_unit[:2] == "cu":                                 # if asking for dried in a cup
        total = 16 * amount                                     # find how many tablespoons in that cup
        if total % 3 == 0:
            total = total / 3.0
            unit = "tablespoons" if total > 1 else "tablespoon"
            verb = "are" if total > 1 else "is"
        else:
            unit = "teaspoons" if total > 1 else "teaspoon"
            verb = "are" if total > 1 else "is"
    elif orig_unit[:2] == "ta":                # if asking for dried in a tablespoon
        total = amount                                          # one to one ratio for dried herbs
        unit = "teaspoons" if total > 1 else "teaspoon"         # (get more granular with smaller units)
        verb = "are" if total > 1 else "is"
    elif orig_unit[:2] == "te":                                                       # if asking for dried in a tsp
        total = round((amount * 0.33) * 8) / 8                  # as a general rule 1:3 ratio for dried to fresh
        unit = "teaspoons" if total > 1 else "teaspoon"
        verb = "are" if total > 1 else "is"
    else:
        return statement("I'm sorry, that is not a valid unit to convert to.")

    amount_text = herb_statement(verb, total, unit)

    speech_text = "There {0} dried herbs in {1} {2} of fresh herbs".format(amount_text, num, orig_unit)
    return statement(speech_text)




@ask.intent('AMAZON.StopIntent')
def stop():
    return statement("Goodbye")


@ask.intent('AMAZON.CancelIntent')
def cancel():
    return statement("Goodbye")

@ask.intent('AMAZON.HelpIntent')
def help():
    return statement("This app helps you in the kitchen as you cook.")



if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
