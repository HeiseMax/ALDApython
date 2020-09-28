import json
import time
import random

def all_ingredients(recipes):
    allIngredients = []
    for cocktail in recipes:
        for ingredient in recipes[cocktail]["ingredients"]:
            normalized_ingredient = normalize_string(ingredient)
            if normalized_ingredient not in allIngredients:
                allIngredients.append(normalized_ingredient)
    return allIngredients

def normalize_string(string):
    word_len = 0
    for letter in string:
        word_len += 1
        if letter == ",":
            word_len -= 1
            break
        if letter == "(":
            word_len -= 2
            break
    return (string[0:word_len].lower())

def normalize_dict(recipes): #formatiert die ingredients in recipes
    for cocktail in recipes:
        ingredients = []
        for ingredient in recipes[cocktail]["ingredients"]:
            ingredients.append(normalize_string(ingredient))
            recipes[cocktail]["ingredients"] = ingredients

def cocktails_inverse(recipes):
    normalize_dict(recipes)
    ingredients = all_ingredients(recipes)
    inverse_recipes = {}
    for ingredient in ingredients:
        inverse_recipes[ingredient] = []

    for cocktail in recipes:
        for ingredient in recipes[cocktail]["ingredients"]:
            inverse_recipes[ingredient].append(cocktail)

    inverse_recipes = sorted (inverse_recipes.items(),reverse = True, key=lambda kv: len(kv[1]))

    return inverse_recipes


with open('cocktails.json', encoding='utf-8') as json_file:
    recipes = json.load(json_file)

ingredients = all_ingredients(recipes)
print ("Die Zutaten sind:")
print (ingredients)
print ("Es gibt ",len(ingredients), "Zutaten")
inverse_recipes = cocktails_inverse(recipes)

with open('cocktails_inverse.json', 'w') as json_file:
  json.dump(inverse_recipes, json_file,  indent=4)

print("")
print("Die 15 meist benutzten Zutaten sind:")
counter = 0
for i in inverse_recipes:
    print (" ",i[0])
    counter += 1
    if counter == 15:
        break

def possible_cocktails(recipes, inverse_recipes, available_ingredients):
    cocktails = []
    ignore_list = ["cocktailkirschen", "Stielkirsche", "Ananas", "Orange", "Zimt", "Puderzucker", "Physalis",
                   "gurkenscheiben", "zucker", "erdbeeren", "mineralwasser", "wasser", "rohrzucker", "puderzucker",
                   "maraschinokirsche", "salz", "pfeffer", "olive", "muskat"]
    for ingredient in ignore_list:
        if ingredient not in available_ingredients:
            available_ingredients.append(ingredient)
    for cocktail in recipes:
        cocktails.append(cocktail)
    for x in range(len(available_ingredients)):
        available_ingredients[x] = normalize_string(available_ingredients[x])
    for ingredients in inverse_recipes:
        if ingredients[0] not in available_ingredients:
            cocktails = [x for x in cocktails if x not in ingredients[1]]
    return cocktails


available_ingredients = ["ananassaft","bananenlik\u00e3\u00b6r","brauner rum","galliano","orangensaft","eisw\u00e3\u00bcrfel", "Brandy", "orange", "crushed ice" ,"triple sec" , "zitronensaft"]
possibleCocktails = (possible_cocktails(recipes, inverse_recipes, available_ingredients))
print ("")
print("Mit ", available_ingredients," können sie ", len(possibleCocktails), " Cocktails zuberieten:")
print (possibleCocktails)
print("")
print("")


def optimal_ingredients(recipes, inverse_recipes):
    possible_ingredients = all_ingredients(recipes)
    ignore_list = ["cocktailkirschen", "Stielkirsche", "Ananas", "Orange", "Zimt", "Puderzucker", "Physalis",
                   "gurkenscheiben", "zucker", "erdbeeren", "mineralwasser", "wasser", "rohrzucker", "puderzucker",
                   "maraschinokirsche", "salz", "pfeffer", "olive", "muskat"]
    for i in range(len(inverse_recipes) - 1, len(inverse_recipes) - 352, -1): #die 350 unwichtigsten Zutaten werden aus der Liste entfernt
        if inverse_recipes[i][0] not in ignore_list:
            ignore_list.append(inverse_recipes[i][0])
    for i in possible_ingredients:
        if i not in ignore_list:
            possible_ingredients = [x for x in possible_ingredients if x not in ignore_list]

    # Diese Funktion wuerde alle moeglichen Kombinationen Testen, allerdings waere der Zeitaufwandt zu gross
    '''maxLen = 0 
    for i in range (0,len(possible_ingredients)-4):
        for j in range(i+1,len(possible_ingredients) - 3):
            for k in range(j+1,len(possible_ingredients) -2):
                for l in range(k+1,len(possible_ingredients)-1):
                    for m in range(l+1,len(possible_ingredients)):
                        available_ingredients = []
                        available_ingredients.append(possible_ingredients[i])
                        available_ingredients.append(possible_ingredients[j])
                        available_ingredients.append(possible_ingredients[k])
                        available_ingredients.append(possible_ingredients[l])
                        available_ingredients.append(possible_ingredients[m])
                        print (available_ingredients)
                        list = possible_cocktails(recipes, inverse_recipes, available_ingredients)
                        if len(list) > maxLen:
                            maxLen = len(list)
                            result = list'''


    # Die Zutaten werden jedes mal zufällig bestimmt, die Funktion läuft eine eingestellte Zeit
    time_limit_seconds = 10;
    print ("Laufzeit: ", (time_limit_seconds/60), " Minuten.")
    groesse = len(possible_ingredients) -1
    maxLen = 0
    a = time.monotonic()
    while True:
        available_ingredients = []
        available_ingredients.append(possible_ingredients[random.randint(0,groesse)])
        available_ingredients.append(possible_ingredients[random.randint(0,groesse)])
        available_ingredients.append(possible_ingredients[random.randint(0,groesse)])
        available_ingredients.append(possible_ingredients[random.randint(0,groesse)])
        available_ingredients.append(possible_ingredients[random.randint(0,groesse)])
        zutaten = []
        for f in range (0,5):
            zutaten.append(available_ingredients[f])
        list = possible_cocktails(recipes, inverse_recipes, available_ingredients)
        if len(list) > maxLen:
            maxLen = len(list)
            result = list
            resultZutaten = zutaten
        b = time.monotonic()
        if b - a > time_limit_seconds:
            break
    return result, resultZutaten #liefert sowohl Zutatenliste als auf die Cocktailliste

ctails,available = optimal_ingredients(recipes, inverse_recipes)
print("")
print ("Mit " ,available, " kann man diese ",len(ctails), " Cocktails herstellen: ", ctails)

print("")
print("Bestes Ergebnis, mit 30 Minuten Berechnung:")
print ("Mit  ['orangensaft', 'sekt', 'cranberrysaft', 'blue curacao', 'campari']  kann man diese  7  Cocktails herstellen:  ['Erdbeer - Sekt', 'GrÃ¼ne Wiese', 'HSV', 'Sekt mit Blue Curacao', 'Campari Orangensaft', 'Campari mit Prosecco', 'Green Widow Cocktail']" )