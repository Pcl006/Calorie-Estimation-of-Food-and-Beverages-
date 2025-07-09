import tensorflow
from flask import Flask,flash, request, render_template
import csv
import math
import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.python.keras.models import load_model
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow.keras.layers import BatchNormalization
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# define label meaning
label = ['apple pie:Estimate Calories 237 For 100 Grams Quantity',
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

nu_link = 'https://www.nutritionix.com/food/'

# Loading the best saved model to make predictions.
tensorflow.keras.backend.clear_session()
model = tf.keras.models.load_model('food.h5')
print('model successfully loaded!')

start = [0]
passed = [0]
pack = [[]]
num = [0]

nutrients = [
    {'name': 'protein', 'value': 0.0},
    {'name': 'calcium', 'value': 0.0},
    {'name': 'fat', 'value': 0.0},
    {'name': 'carbohydrates', 'value': 0.0},
    {'name': 'vitamins', 'value': 0.0}
]

with open('nutrition101.csv', 'r') as file:
    reader = csv.reader(file)
    nutrition_table = dict()
    for i, row in enumerate(reader):
        if i == 0:
            name = ''
            continue
        else:
            name = row[1].strip()
        nutrition_table[name] = [
            {'name': 'protein', 'value': float(row[2])},
            {'name': 'calcium', 'value': float(row[3])},
            {'name': 'fat', 'value': float(row[4])},
            {'name': 'carbohydrates', 'value': float(row[5])},
            {'name': 'vitamins', 'value': float(row[6])}
        ]


@app.route("/")
@app.route("/index")
def index():
	return render_template('index.html')

@app.route("/login")
def login():
	return render_template('login.html')

@app.route("/chart")
def chart():
	return render_template('chart.html')


@app.route('/recognize')
def recognize():
    return render_template('recognize.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.getlist("img")
    for f in file:
        filename = secure_filename(str(num[0] + 500) + '.jpg')
        num[0] += 1
        name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print('save name', name)
        f.save(name)

    pack[0] = []
    
    return render_template('recognize.html', img=file)


@app.route('/predict')
def predict():
    result = []
    # pack = []
    print('total image', num[0])
    for i in range(start[0], num[0]):
        pa = dict()

        filename = f'{UPLOAD_FOLDER}/{i + 500}.jpg'
        print('image filepath', filename)
        pred_img = filename
        pred_img = image.load_img(pred_img, target_size=(128, 128))
        pred_img = image.img_to_array(pred_img)
        pred_img = np.expand_dims(pred_img, axis=0)
        pred_img = pred_img / 255.

        pred = model.predict(pred_img)
        print("Pred")
        print(pred)

        if math.isnan(pred[0][0]) and math.isnan(pred[0][1]) and \
                math.isnan(pred[0][2]) and math.isnan(pred[0][3]):
            pred = np.array([0.05, 0.05, 0.05, 0.07, 0.09, 0.19, 0.55, 0.0, 0.0, 0.0, 0.0])

        top = pred.argsort()[0][-3:]
        label.sort()
        _true = label[top[2]]
        _trues = label[top[2]]
        print(_trues)
        pa['image'] = f'{UPLOAD_FOLDER}/{i + 500}.jpg'
        x = dict()
        x[_true] = float("{:.2f}".format(pred[0][top[2]] * 100))
        print(x[_true])
        x[label[top[1]]] = float("{:.2f}".format(pred[0][top[1]] * 100))
        print(x[label[top[1]]])
        x[label[top[0]]] = float("{:.2f}".format(pred[0][top[0]] * 100))

        pa['result'] = x
        print(x)
        pa['nutrition'] = nutrition_table[_true]
        pa['food'] = f'{nu_link}{_true}'
        pa['idx'] = i - start[0]
        pa['quantity'] = 100

        pack[0].append(pa)
        passed[0] += 1

    start[0] = passed[0]
    print('successfully packed')
    # compute the average source of calories
    for p in pack[0]:
        nutrients[0]['value'] = (nutrients[0]['value'] + p['nutrition'][0]['value'])
        nutrients[1]['value'] = (nutrients[1]['value'] + p['nutrition'][1]['value'])
        nutrients[2]['value'] = (nutrients[2]['value'] + p['nutrition'][2]['value'])
        nutrients[3]['value'] = (nutrients[3]['value'] + p['nutrition'][3]['value'])
        nutrients[4]['value'] = (nutrients[4]['value'] + p['nutrition'][4]['value'])

    nutrients[0]['value'] = nutrients[0]['value'] / num[0]
    nutrients[1]['value'] = nutrients[1]['value'] / num[0]
    nutrients[2]['value'] = nutrients[2]['value'] / num[0]
    nutrients[3]['value'] = nutrients[3]['value'] / num[0]
    nutrients[4]['value'] = nutrients[4]['value'] / num[0]

    return render_template('results.html', pack=pack[0], whole_nutrition=nutrients, prediction = _trues)


@app.route('/update', methods=['POST'])
def update():
    return render_template('index.html', img='static/P2.jpg')


if __name__ == "__main__":
    import click

    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='127.0.0.1')
    @click.argument('PORT', default=5000, type=int)
    def run(debug, threaded, host, port):
        """
        This function handles command line parameters.
        Run the server using
            python server.py
        Show the help text using
            python server.py --help
        """
        HOST, PORT = host, port
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)
    run()
