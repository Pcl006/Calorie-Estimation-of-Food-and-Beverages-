import requests
import pandas as pd


def get_nutrition(food_name):
    nutrition_data = pd.DataFrame(columns=['name', 'protein', 'calcium', 'fat', 'carbohydrates', 'vitamins'])
    for name in food_name:
        url = "https://api.nal.usda.gov/fdc/v1/foods/search?api_key=d4D6dSOc81pTAOY2gsNZ0YhjkMlhStLJRoII5SJu&query=" + name
        response = requests.get(url)
        data = response.json()
        flatten_json = pd.json_normalize(data["foods"])
        first_food = flatten_json.iloc[0]
        first_food_nutrition_list = first_food.foodNutrients
        for item in first_food_nutrition_list:
            if item['nutrientNumber'] == "203":
                protein = item['value']
                continue
            if item['nutrientNumber'] == "301":
                calcium = item['value']
                continue
            if item['nutrientNumber'] == "204":
                fat = item['value']
                continue
            if item['nutrientNumber'] == "205":
                carbs = item['value']
                continue
            if item['nutrientNumber'] == "318":
                vitamin_a = item['value']
                continue
            if item['nutrientNumber'] == "401":
                vitamin_c = item['value']
                continue

        vitamins = float(vitamin_a) + float(vitamin_c)
        print(name)
        nutrition_data = nutrition_data.append({
            'name': name,
            'protein': protein,
            'calcium': calcium / 1000,
            'fat': fat,
            'carbohydrates': carbs,
            'vitamins': vitamins / 1000
        }, ignore_index=True)

    return nutrition_data


nutrition101 = get_nutrition(['apple pie:Estimate Calories 237 For 100 Grams Quantity',
'baby back ribs:Estimate Calories 276 For 100 Grams Quantity',
'baklava:Estimate Calories 403 For 100 Grams Quantity',
'beef carpaccio:Estimate Calories 231 For 100 Grams Quantity',
'beef tartare:Estimate Calories 246 For 100 Grams Quantity',
'beet salad:Estimate Calories 231 For 100 Grams Quantity',
'beignets:Estimate Calories 291 For 100 Grams Quantity',
'bibimbap:Estimate Calories 113 For 100 Grams Quantity',
'bread pudding:Estimate Calories 188 For 100 Grams Quantity',
'breakfast burrito:Estimate Calories 169 For 100 Grams Quantity',
'bruschetta:Estimate Calories 206 For 100 Grams Quantity',
'caesar salad:Estimate Calories 158 For 100 Grams Quantity',
'cannoli:Estimate Calories 293 For 100 Grams Quantity',
'caprese salad:Estimate Calories 136 For 100 Grams Quantity',
'carrot cake:Estimate Calories 333 For 100 Grams Quantity',
'ceviche:Estimate Calories 68 For 100 Grams Quantity',
'cheese plate:Estimate Calories 389 For 100 Grams Quantity',
'cheesecake:Estimate Calories 321 For 100 Grams Quantity',
'chicken curry:Estimate Calories 104 For 100 Grams Quantity',
'chicken quesadilla:Estimate Calories 216 For 100 Grams Quantity',
'chicken wings:Estimate Calories 328 For 100 Grams Quantity',
'chocolate cake:Estimate Calories 389 For 100 Grams Quantity',
'chocolate mousse:Estimate Calories 225 For 100 Grams Quantity',
'churros:Estimate Calories 396 For 100 Grams Quantity',
'clam chowder:Estimate Calories 79 For 100 Grams Quantity',
'club sandwich:Estimate Calories 234 For 100 Grams Quantity',
'crab cakes:Estimate Calories 173 For 100 Grams Quantity',
'creme brulee:Estimate Calories 343 For 100 Grams Quantity',
'croque madame:Estimate Calories 199 For 100 Grams Quantity',
'cup cakes:Estimate Calories 389 For 100 Grams Quantity',
'deviled eggs:Estimate Calories 225 For 100 Grams Quantity',
'donuts:Estimate Calories 421 For 100 Grams Quantity',
'dumplings:Estimate Calories 230 For 100 Grams Quantity',
'edamame:Estimate Calories 121 For 100 Grams Quantity',
'eggs benedict:Estimate Calories 260 For 100 Grams Quantity',
'escargots:Estimate Calories 90 For 100 Grams Quantity',
'falafel:Estimate Calories 416 For 100 Grams Quantity',
'filet mignon:Estimate Calories 267 For 100 Grams Quantity',
'fish and_chips:Estimate Calories 134 For 100 Grams Quantity',
'foie gras:Estimate Calories 462 For 100 Grams Quantity',
'french fries:Estimate Calories 312 For 100 Grams Quantity',
'french onion soup:Estimate Calories 137 For 100 Grams Quantity',
'french toast:Estimate Calories 263 For 100 Grams Quantity',
'fried calamari:Estimate Calories 249 For 100 Grams Quantity',
'fried rice:Estimate Calories 174 For 100 Grams Quantity',
'frozen yogurt:Estimate Calories 127 For 100 Grams Quantity',
'garlic bread:Estimate Calories 350 For 100 Grams Quantity',
'gnocchi:Estimate Calories 201 For 100 Grams Quantity',
'greek salad:Estimate Calories 113 For 100 Grams Quantity',
'grilled cheese sandwich:Estimate Calories 344 For 100 Grams Quantity',
'grilled salmon:Estimate Calories 206 For 100 Grams Quantity',
'guacamole:Estimate Calories 151 For 100 Grams Quantity',
'gyoza:Estimate Calories 211 For 100 Grams Quantity',
'hamburger:Estimate Calories 239 For 100 Grams Quantity',
'hot and sour soup:Estimate Calories 39 For 100 Grams Quantity',
'hot dog:Estimate Calories 322 For 100 Grams Quantity',
'huevos rancheros:Estimate Calories 143 For 100 Grams Quantity',
'hummus:Estimate Calories 166 For 100 Grams Quantity',
'ice cream:Estimate Calories 207 For 100 Grams Quantity',
'lasagna:Estimate Calories 156 For 100 Grams Quantity',
'lobster bisque:Estimate Calories 106 For 100 Grams Quantity',
'lobster roll sandwich:Estimate Calories 199 For 100 Grams Quantity',
'macaroni and cheese:Estimate Calories 190 For 100 Grams Quantity',
'macarons:Estimate Calories 384 For 100 Grams Quantity',
'miso soup:Estimate Calories 24 For 100 Grams Quantity',
'mussels:Estimate Calories 172 For 100 Grams Quantity',
'nachos:Estimate Calories 224 For 100 Grams Quantity',
'omelette:Estimate Calories 181 For 100 Grams Quantity',
'onion rings:Estimate Calories 356 For 100 Grams Quantity',
'oysters:Estimate Calories 163 For 100 Grams Quantity',
'pad thai:Estimate Calories 170 For 100 Grams Quantity',
'paella:Estimate Calories 183 For 100 Grams Quantity',
'pancakes:Estimate Calories 227 For 100 Grams Quantity',
'panna cotta:Estimate Calories 319 For 100 Grams Quantity',
'peking duck:Estimate Calories 241 For 100 Grams Quantity',
'pho:Estimate Calories 90 For 100 Grams Quantity',
'pizza:Estimate Calories 266 For 100 Grams Quantity',
'pork chop:Estimate Calories 209 For 100 Grams Quantity',
'poutine:Estimate Calories 222 For 100 Grams Quantity',
'prime rib:Estimate Calories 341 For 100 Grams Quantity',
'pulled pork sandwich:Estimate Calories 175 For 100 Grams Quantity',
'ramen:Estimate Calories 135 For 100 Grams Quantity',
'ravioli:Estimate Calories 179 For 100 Grams Quantity',
'red velvet cake:Estimate Calories 337 For 100 Grams Quantity',
'risotto:Estimate Calories 122 For 100 Grams Quantity',
'samosa:Estimate Calories 261 For 100 Grams Quantity',
'sashimi:Estimate Calories 124 For 100 Grams Quantity',
'scallops:Estimate Calories 111 For 100 Grams Quantity',
'seaweed salad:Estimate Calories 115 For 100 Grams Quantity',
'shrimp and grits:Estimate Calories 149 For 100 Grams Quantity',
'spaghetti bolognese:Estimate Calories 101 For 100 Grams Quantity',
'spaghetti carbonara:Estimate Calories 199 For 100 Grams Quantity',
'spring rolls:Estimate Calories 230 For 100 Grams Quantity',
'steak:Estimate Calories 278 For 100 Grams Quantity',
'strawberry shortcake:Estimate Calories 172 For 100 Grams Quantity',
'sushi:Estimate Calories 165 For 100 Grams Quantity',
'tacos:Estimate Calories 206 For 100 Grams Quantity',
'takoyaki:Estimate Calories 149 For 100 Grams Quantity',
'tiramisu:Estimate Calories 329 For 100 Grams Quantity',
'tuna tartare:Estimate Calories 176 For 100 Grams Quantity',
'waffles:Estimate Calories 291 For 100 Grams Quantity']
                             )
nutrition101 = nutrition101.reset_index(drop=True)
nutrition101.to_csv("nutrition101.csv")
