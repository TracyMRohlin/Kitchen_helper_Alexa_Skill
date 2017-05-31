import logging
import os
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, convert_errors
from pronunciation import str_to_dec, speak_decimals
from conversion import celsius_to_fahrenheit, fahrenheit_to_celsius

app = Flask(__name__)
ask = Ask(app, "/")

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

@ask.intent('TemperatureIntent', default={"temperature":"0", "source_unit":"celsius", "target_unit":"fahrenheit"})
def convert_temperature(temperature, source_unit, target_unit):
    init_temp = float(temperature)

    if (source_unit.lower() == "celsius" and target_unit.lower() == "fahrenheit"):
        out_temp = celsius_to_fahrenheit(init_temp)
    elif (source_unit.lower() == "fahrenheit" and target_unit.lower() == "celsius"):
        out_temp = fahrenheit_to_celsius(init_temp)
    else:
        out_temp = init_temp

    final_temp = speak_decimals(out_temp)
    return statement("{0} degrees {1} is equal to {2} degrees in {3}.".format(temperature, source_unit, final_temp, target_unit))

ingredients = {"allspice": {"default_unit":"teaspoon", "substitute":{"cinnamon":{"unit":"teaspoon", "amount":0.5},
                                "ginger":{"unit":"teaspoon", "amount":0.25},
                                "cloves":{"unit":"teaspoon", "amount":0.25}}},
                   "arrowroot starch":{"default_unit":"teaspoon", "substitute":{"flour":{"unit":"tablespoon", "amount":1},
                                        "cornstarch":{"unit":"teaspoon", "amount":1}}},
                   "baking mix": {"default_unit":"cup", "substitute":{"pancake mix": {"unit": "cup", "amount": 1}}},
                   "baking powder":{"default_unit":"teaspoon", "substitute":{"baking soda": {"unit": "teaspoon", "amount": 0.25},
                                                                             "cream of tartar": {"unit": "teaspoon", "amount": 0.5}}},
                   "baking soda": {"default_unit":"teaspoon", "substitute":{"baking powder": {"unit": "teaspoons", "amount": 4}}},
                   "beer":  {"default_unit":"cup", "substitute":{"chicken broth": {"unit": "cup", "amount": 1}}},
                   "brandy":  {"default_unit":"cup", "substitute":{"imitation brandy extract": {"unit": "teaspoon", "amount": 4},
                                                                   "water": {"unit": "cup", "amount": 1}}},
                   "bread crumbs":{"default_unit":"cup", "substitute":{"cracker crumbs": {"unit": "cup", "amount": 1}}},
                   "chicken broth":{"default_unit":"cup", "substitute":{"bouilon": {"unit": "cube", "amount": 1},
                                                                        "boiling water": {"unit": "cup", "amount": 1}}},
                   "beef broth":{"default_unit":"cup", "substitute":{"bouilon": {"unit": "cube", "amount": 1},
                                                                        "boiling water": {"unit": "cup", "amount": 1}}},
                   "broth":{"default_unit":"cup", "substitute":{"bouilon": {"unit": "cube", "amount": 1},
                                                                        "boiling water": {"unit": "cup", "amount": 1}}},
                   "brown sugar":{"default_unit":"cup", "substitute":{"whtie sugar": {"unit": "cube", "amount": 1},
                                                                        "molasses": {"unit": "cup", "amount": 0.25}}},
                   "salted butter":{"default_unit":"cup", "substitute":{"margarine": {"unit": "cup", "amount": 1}}},
                   "unsalted butter": {"default_unit":"cup", "substitute":{"shortening": {"unit": "cup", "amount": 1}}},
                   "buttermilk": {"default_unit":"cup", "substitute":{"yogurt": {"unit": "cup", "amount": 1}}},
                   "cheddar cheese": {"default_unit":"cup", "substitute":{"monterey jack": {"unit": "cup", "amount": 1}}},
                   "chervil": {"default_unit":"tablespoon", "substitute":{"parsely": {"unit": "tablespoon", "amount": 1}}},
                   "semisweet chocolate": {"default_unit":"ounce", "substitute":{"unsweetened chocolate": {"unit": "ounce", "amount": 1},
                                                                                 "sugar": {"unit":"teaspoon", "amount":1}}},
                   "unsweetened chocolate":{"default_unit":"ounce", "substitute":{"unsweetened cocoa": {"unit": "tablespoon", "amount": 3},
                                                                                  "shortening":{"unit": "tablespoon", "amount": 1}}},
                   "cocoa":{"default_unit":"cup", "substitute":{"cup": {"unit": "ounce", "amount": 4}}},
                   "corn syrup":{"default_unit":"cup", "substitute":{"honey": {"unit": "cup", "amount": 1}}},
                   "cottage cheese":{"default_unit":"cup", "substitute":{"ricotta cheese": {"unit": "cup", "amount": 1}}},
                    "cracker crumbs":{"default_unit":"cup", "substitute":{"bread crumb": {"unit": "cup", "amount": 1}}},
                    "half and half": {"default_unit":"cup", "substitute":{"milk": {"unit": "cup", "amount": 0.7/0.8},
                                                                          "butter":{"unit":"tablespoon", "amount": 1}}},
                    "heavy cream":{"default_unit":"cup", "substitute":{"milk": {"unit": "cup", "amount": 0.75},
                                                                       "butter":{"unit":"cup", "amount": 0.33}}},
                    "light cream":{"default_unit":"cup", "substitute":{"milk": {"unit": "cup", "amount": 0.75},
                                                                       "butter":{"unit":"tablespoon", "amount": 3}}},
                    "cream of tartar":{"default_unit":"teaspoon", "substitute":{"lemon juice": {"unit": "teaspoon", "amount": 2}}},
                    "egg":{"default_unit":"whole", "substitute":{"mayonaise": {"unit": "tablespoon", "amount": 3}}},
                    "evaporated milk":{"default_unit":"cup", "substitute":{"light cream": {"unit": "cup", "amount": 1}}},
                    "bread flour":{"default_unit":"cup", "substitute":{"all purpose flour": {"unit": "cup", "amount": 1},
                                                                       "wheat gluten":{"unit":"teaspoon", "amount":1}}},
                    "self rising flour":{"default_unit":"cup", "substitute":{"all purpose flour": {"unit": "cup", "amount": 7.0/8},
                                                                             "baking powder":{"unit":"teaspoon", "amount": 1.5},
                                                                            "salt":{"unit":"teaspoon", "amount": 0.5}}},
                    "garlic":{"default_unit":"clove", "substitute":{"garlic powder": {"unit": "teaspoon", "amount": 1/8.0}}},
                    "gelatin":{"default_unit":"tablespoon", "substitute":{"agar agar": {"unit": "teaspoon", "amount": 2}}},
                    "powdered ginger":{"default_unit":"teaspoon", "substitute":{"fresh ginger": {"unit": "teaspoon", "amount": 2}}},
                    "fresh ginger":{"default_unit":"teaspoon", "substitute":{"powdered ginger": {"unit": "teaspoon", "amount": 0.5}}},
                    "green onion":{"default_unit":"cup", "substitute":{"shallot": {"unit": "cup", "amount": 1}}},
                    "hazelnuts":{"default_unit":"cup", "substitute":{"almonds": {"unit": "cup", "amount": 1}}},
                    "honey":{"default_unit":"cup", "substitute":{"white sugar": {"unit": "cup", "amount": 1.25},
                                                                 "water":{"unit":"cup", "amount":0.33}}},
                    "hot pepper sauce":{"default_unit":"teaspoon", "substitute":{"cayenne pepper": {"unit": "teaspoon", "amount": 0.75},
                                                                                 "vinegar":{"unit":"teaspoon", "amount": 1}}},
                    "ketchup":{"default_unit":"cup", "substitute":{"tomato sauce": {"unit": "cup", "amount": 1},
                                                                   "vinegar":{"unit":"teaspoon", "amount":1},
                                                                   "sugar":{"unit":"tablespoon", "amount":1}}},
                    "lemongrass":{"default_unit":"stalk", "substitute":{"lemon zest": {"unit": "teaspoon", "amount": 1.5}}},
                    "lemon juice":{"default_unit":"teaspoon", "substitute":{"white wine": {"unit": "teaspoon", "amount": 1}}},
                    "lemon zest":{"default_unit":"teaspoon", "substitute":{"lemon juice": {"unit": "tablespoon", "amount": 2}}},
                    "lime juice":{"default_unit":"teaspoon", "substitute":{"white wine": {"unit": "teaspoon", "amount": 1}}},
                    "lime zest":{"default_unit":"teaspoon", "substitute":{"lemon zest": {"unit": "teaspoon", "amount": 1}}},
                    "macadamia nuts":{"default_unit":"cup", "substitute":{"almonds": {"unit": "cup", "amount": 1}}},
                    "margarine":{"default_unit":"cup", "substitute":{"butter": {"unit": "cup", "amount": 1}}},
                    "mayonaise":{"default_unit":"cup", "substitute":{"sour cream": {"unit": "cup", "amount": 1}}},
                    "molasses":{"default_unit":"cup", "substitute":{"brown sugar": {"unit": "cup", "amount": 0.75},
                                                                    "cream of tartar":{"unit":"teaspoon", "amount":1}}},
                    "mustard":{"default_unit":"tablespoon", "substitute":{"dried mustard": {"unit": "tablespoon", "amount": 1},
                                                                          "water":{"unit":"teaspoon", "amount":1},
                                                                          "vinegar":{"unit":"teaspoon", "amount":1},
                                                                          "sugar":{"unit":"teaspoon", "amount":1}}},
                    "onion":{"default_unit":"cup", "substitute":{"onion powder": {"unit": "cup", "amount": 0.25}}},
                    "orange zest":{"default_unit":"tablespoon", "substitute":{"orange extract": {"unit": "teaspoon", "amount": 0.5}}},
                    "paremesan cheese":{"default_unit":"cup", "substitute":{"asiago cheese": {"unit": "cup", "amount": 1}}},
                    "parsley":{"default_unit":"tablespoon", "substitute":{"chervil": {"unit": "tablespoon", "amount": 1}}},
                    "pepperoni":{"default_unit":"ounce", "substitute":{"salami": {"unit": "ounce", "amount": 1}}},
                    "raisins":{"default_unit":"cup", "substitute":{"dried cranberries": {"unit": "cup", "amount": 1}}},
                    "white rice":{"default_unit":"cup", "substitute":{"brown rice": {"unit": "cup", "amount": 1}}},
                    "ricotta":{"default_unit":"cup", "substitute":{"silken tofu": {"unit": "cup", "amount": 1}}},
                    "saffron":{"default_unit":"teaspoon", "substitute":{"tumeric": {"unit": "teaspoon", "amount": 1}}},
                    "salami":{"default_unit":"ounce", "substitute":{"pepperoni": {"unit": "ounce", "amount": 1}}},
                    "shallots":{"default_unit":"cup", "substitute":{"onion": {"unit": "cup", "amount": 1}}},
                    "shortening":{"default_unit":"cup", "substitute":{"butter": {"unit": "cup", "amount": 1}}},
                    "sour cream":{"default_unit":"cup", "substitute":{"plain yogurt": {"unit": "cup", "amount": 1}}},
                    "soy sauce":{"default_unit":"cup", "substitute":{"worcestershire sauce": {"unit": "cup", "amount": 0.5},
                                                                     "water":{"unit":"tablespoon", "amount":2}}},
                    "vinegar":{"default_unit":"teaspoon", "substitute":{"white wine": {"unit": "teaspoon", "amount": 2}}},
                    "white sugar":{"default_unit":"cup", "substitute":{"confectioners sugar": {"unit": "cup", "amount": 1.25}}},
                    "yogurt":{"default_unit":"cup", "substitute":{"sour cream": {"unit": "cup", "amount": 1}}},
               }

@ask.intent('SubstituteIntent', default={"fraction":"0", "whole_num":"1", "unit":""}, mapping={"unsalted butter": "butter",
                                                                                    "fresh ginger":"ginger",
                                                                                    "green onion":"scallion",
                                                                                    "white rice":"rice",
                                                                                    "yogurt": "plain yogurt",
                                                                                    "hot pepper sauce":"hot sauce"})
def common_substitutions(whole, fraction, item, unit):


    amount = str_to_dec(whole) + str_to_dec(fraction)
    things_to_substitute = []
    if item in ingredients:
        substitution = ingredients[item]
        if (unit != substitution["default_unit"]):  # user is asking for a weird conversion
            amount = 1
            unit = substitution["default_unit"]
        for sub_ingred, ingred_data in substitution["substitute"].items():
            amount_to_sub = speak_decimals(amount * ingred_data["amount"])
            target_unit = ingred_data["unit"] + "s" if amount > 1 else ingred_data["unit"]
            things_to_substitute.append("{0} {1} of {2}".format(amount_to_sub, target_unit, sub_ingred))
        if len(things_to_substitute) > 1:
            ingred_speech = " ".join(things_to_substitute[:-1]) + " and " + things_to_substitute[-1]
        else:
            ingred_speech = things_to_substitute[0]
        speech_text = "You can substitute {0} for {1} {2} of {3}".format(ingred_speech, speak_decimals(amount), unit, item)
        return statement(speech_text)

    else:
        return statement("Sorry, I do not recognize that ingredient you are trying to substitute.")

common_substitutions("1", "0", "allspice", "teaspoon")
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
                to_unit = to_unit + "s" if to_unit[-1] != "s" else to_unit
        elif unit_from == "ta" and unit_to == "te":
            total = round((quantity * 8 * 3)) / 8
            if total > 1:
                verb = "are"
                to_unit = to_unit + "s" if to_unit[-1] != "s" else to_unit
        elif unit_from == "te" and unit_to == "ta":
            total = round((quantity * 8 / 3.0)) / 8
            if total > 1:
                verb = "are"
                to_unit = to_unit +"s" if to_unit[-1] != "s" else to_unit # repetitive code is repetitive but *shrug*
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
        speech_text ="There {0} {1} {2} in {3} {4}".format(verb, speak_decimals(total), to_unit, speak_decimals(quantity), unit_text)
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
    tbs = speak_decimals(amount * factor)
    tsps = speak_decimals(amount * factor * 3)
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
    tsps = speak_decimals(factor * amount)
    tbs = speak_decimals(round((factor*amount)/3.0, 1))
    speech_text = "There are {0} teaspoons or {1} tablespoons of zest in {2} {3}".format(tsps, tbs, num, fruit)
    return statement(speech_text)

# dried to fresh herb conversion

def herb_statement(verb, total, unit):
    """"Returns the correct amount of herb"""
    if total == 0:
        amount_text = "a pinch of"
    else:
       amount_text = verb + " " + speak_decimals(total) + " " +  unit
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

meat_conversions = {"bone in rib roast":{"temp":"325","min":23, "max":30},
                        "boneless rib roast":{"temp":"325","min":39, "max":43},
                        "eye of round":{"temp":"325", "min":20, "max":22},
                        "beef tenderloin":{"min":45, "max":60},
                        "half beef tenderloin":{"temp":"425", "min":35, "max":45},
                        "turkey":{"temp":"325","min":30},
                        "chicken":{"temp":"375", "min":20, "max":30},
                        "duck":{"temp":"375", "min":18, "max":20},
                        "goose":{"temp":"325", "min":20, "max":25},
                        "pheasant":{"temp":"350", "min":30},
                        "quail":{'temp':"425", "min":20},
                        "leg of lamb":{"temp":"325", "min":20, "max":26},
                        "lamb roast":{"temp":"375", "min":20, "max":30},
                        "bone in pork loin":{"temp":"325", "min":20, "max":25},
                        "boneless pork loin":{"temp":"325", "min":22, "max":33},
                        "pork roast":{"temp":"325", "min":20, "max":25},
                        "pork tenderloin":{"temp":"425", "total_min":20, "total_max":30},
                        "bone in veal loin":{"temp":"325", "min":30, "max":34},
                        "bone in veal roast":{"temp":"325", "min":30, "max":34},
                        "boneless veal roast":{"temp":"325", "min":25, "max":30},
                        "boneless veal rump":{"temp":"325", "min":25, "max":30},
                        "boneless veal shoulder":{"temp":"325", "min":25, "max":30},
                        }

@ask.intent("RoastIntent", default={"whole_lbs":"0", "frac_lbs":"0"},
            mapping={"beef tenderloin":"whole beef tenderloin", "pork loin":"boneless pork loin"})
def roasting(whole_lbs, frac_lbs, meat):

    amount = str_to_dec(whole_lbs) + str_to_dec(frac_lbs)
    if meat not in meat_conversions:
        return statement("I'm sorry, I'm not quite sure I recognize what you are trying to cook.")

    if "min" in meat_conversions[meat] and "max" in meat_conversions[meat]:
        min = meat_conversions[meat]["min"] * amount
        max = meat_conversions[meat]["max"] * amount
        return statement("Your {0} will take between {1} and {2} minutes to cook at {3} degrees.".format(meat,
                                                                                                 speak_decimals(min),
                                                                                                 speak_decimals(max),
                                                                                                 meat_conversions[meat]["temp"]))
    elif "min" in meat_conversions[meat]:
        min = meat_conversions[meat]["min"] * amount
        return statement("Your {0} will be done around {1} if set in the oven at {2} degrees".format(meat,
                                                                                                     min,
                                                                                                     meat_conversions[meat]["temp"]))
    # pork tenderloin has a total min/max cooking time regardless of weight
    else:
        min = meat_conversions[meat]["total_min"]
        max = meat_conversions[meat]["total_max"]
        return statement("Your {0} will take between {1} and {2} minutes if cooked at {3} degrees.".format(meat,
                                                                                                 speak_decimals(min),
                                                                                                 speak_decimals(max),
                                                                                                 meat_conversions[meat]["temp"]))

# ham has weird cooking instrucitons so making a separate function
@ask.intent("HamIntent", default={"whole_lbs":"0", "frac_lbs":"0", "bone_type":"bone in", "cooked":"fully"})
def ham(whole_lbs, frac_lbs, bone_type, cooked):
    amount = str_to_dec(whole_lbs) + str_to_dec(frac_lbs)
    if bone_type == "boneless":
        min_time, max_time = 27, 33
    else:
        if cooked == "fully":
            if amount >= 14 and amount <= 16:
                min_time, max_time = 15, 18
            elif amount >= 7 and amount <= 8:
                min_time, max_time = 18, 25
            else:
                min_time, max_time = 27, 33
        else:
            if amount >= 14 and amount <= 16:
                min_time, max_time = 18, 20
            else:
                min_time, max_time = 22, 25

    min = min_time * amount
    max = max_time * amount
    return statement("Your ham will take between {0} and {1} minutes to cook at 325 degrees.".format(speak_decimals(min),
                                                                                                     speak_decimals(max)))



@ask.intent('AMAZON.StopIntent')
def stop():
    return statement("Goodbye")


@ask.intent('AMAZON.CancelIntent')
def cancel():
    return statement("Goodbye")

@ask.intent('AMAZON.HelpIntent')
def help():
    return statement("This app helps you in the kitchen as you cook.")

@ask.session_ended
def session_ended():
    return "{}", 200

if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
