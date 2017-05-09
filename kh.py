from flask import Flask
from flask_ask import Ask, statement, question, convert_errors

app = Flask(__name__)
ask = Ask(app, "/")

@ask.launch
def launch():
    speech_text = "Hello, welcome to the kitchen helper.  What can I help you with today?"
    reprompt_text = "You can ask to convert one unit to another, or ask how much juice is in a lemon, lime, or orange."
    return question(speech_text).reprompt(reprompt_text)

# TODO Recipe loading?

    # Include steps?
    # Directions to read faster/slower
    # Quantity?


# TODO Unit Conversions

def dec_to_str(total):
    if total == 0.125:
        return "one eighth"
    elif total == 0.25:
        return "one quarter"
    elif total == 0.5:
        return "one half"
    elif total == 0.75:
        return "three quarters"
    else:
        return "0:3f".format(total)

def str_to_dec(string):
    if string == "one eighth":
        return 0.125
    elif string == "one quarter":
        return 0.25
    elif "one half":
        return 0.5
    elif string ==  "three quarters" or "three quarter":
        return 0.75
    else:
        try:
            return float(string)
        except:
            raise Exception("Unable to process that number")

@ask.intent('ImperialIntent')
def convert_imperial(amount, from_unit, to_unit):
    conversions = {"g":{"q":4, "p": 8, "c":16, "o":128, "t":256},
                   "q":{"g":0.25, "p":2, "c": 4, "o":32, "t":64},
                   "p":{"g":0.125, "q": 0.5, "c":2, "o":16, "t":32},
                   "c":{"g":0.0625, "q":0.25, "o": 8, "t":16},
                   "o":{"g":0.0078125, "q":0.03125, "c":0.125, "t":2},
                   "t":{"o": 0.5}
                   }
    quantity = str_to_dec(amount)
    if from_unit in conversions and to_unit in conversions[to_unit]:
        total = quantity * conversions[from_unit[0]][to_unit[0]]
        total = dec_to_str(round(total * 8) / 8)
        verb = "are" if total > 1 else "is"
        return statement("There {0} {1} {2} in {3} {4}".format(verb, total, to_unit, amount, from_unit))
    elif from_unit[:2] == "ta" and to_unit == "te":
        total = dec_to_str(round((quantity * 8 * 3)) / 8)
        verb = "are" if total > 1 else "is"
        return statement("There {0} {1} {2} in {3} (4)".format(verb, total, to_unit, amount, from_unit))
    elif from_unit[:2] == "te" and to_unit == "ta":
        total = dec_to_str(round((quantity * 8 / 3.0)) / 8)
        verb = "are" if total > 1 else "is"
        return statement("There {0} {1} {2} in {3} (4)".format(verb, total, to_unit, amount, from_unit))
    else:
        return statement("I'm sorry I did not understand.")


# TODO Ingredient substitutions


@ask.intent('JuiceIntent', convert={"num": int})
def juice(fruit, num):
    if fruit == "lemons" or fruit == "lemon":
        factor = 3
    elif fruit == "limes" or fruit == "lime":
        factor = 2
    else:
        factor = 4

    tbs = num * factor
    tsps = tbs * 3
    speech_text = "There are {0} tablespoons or {1} teaspoons of juice in {2} {3}".format(tbs, tsps, num, fruit)
    return statement(speech_text)

@ask.intent('ZestIntent', convert={"num": int})
def zest(fruit, num)
    if fruit == "lemons" or fruit == "lemon":
        factor = 3
    elif fruit == "limes" or fruit == "lime":
        factor = 2
    else:
        factor = 6

    tsps = factor * num
    tbs = dec_to_str(convert_imperial(tsps, "table", "tea")
    speech_text = "There are {0} teaspoons or {1} tablespoons of zest in {2} {3}".format(tsps, tbs, num, fruit)
    return statement(speech_text)

    # dried to fresh herb conversion

@ask.intent("HerbIntent", convert={"num": int})
def herb(num, orig_unit):
    verb = ""
    unit = ""
    total = 0
    if orig_unit == "cup" or "cups":                                 # if asking for dried in a cup
        tbs = 16 * num
        total = tbs * 1/3.0
        total = round(total * 2) / 2
        if total >= 16:
            cups = round(total / 16 * 8)/ 8
            unit = "cups" if cups > 1 else "cup"
            verb = "are" if cups > 1 else "is"
        else:
            unit = "tablespoons" if total > 1 else "tablespoon"
            verb = "are" if total > 1 else "is"
        amount_text = verb + str(total) + unit
    elif orig_unit == "tablespoon" or "tablespoons":                # if asking for dried in a tablespoon
        total = num * 1.0/3.0
        total = round(total * 4) / 4                            # want # of tsps by the quarter
        unit = "teaspoons" if total > 1 else "teaspoon"         # (get more granular with smaller units)
        verb = "are" if total > 1 else "is"
        amount_text = verb + str(total) + unit
    else:                                                       # if asking for dried in a tsp
        total = num * 1/3.0
        total = round(total * 8) / 8                            # want number of tsps by the eighth
        if total == 0:
            amount_text = "a pinch of "
        else:
            unit = "teaspoons" if total > 1 else "teaspoon"
            verb = "are" if total > 1 else "is"
            amount_text = verb + str(total) + unit
    return statement("There " + amount_text + "dried herbs in " + str(num) + " " + orig_unit + "of fresh herbs")






@ask.intent('AMAZON.StopIntent')
def stop():
    return statement("Goodbye")


@ask.intent('AMAZON.CancelIntent')
def cancel():
    return statement("Goodbye")


@ask.session_ended
def session_ended():
    return "{}", 200