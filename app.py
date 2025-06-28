from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)

# Path to the CSV file inside static folder
CSV_PATH = os.path.join(app.root_path, 'static', 'foods_with_protein.csv')

# Load foods and protein data from CSV at app start
foods_data = {}
with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row['name'].strip()
        protein = float(row['protein'])
        foods_data[name] = protein  # protein per 100g

def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)

def protein_need_per_kg(bmi):
    if bmi < 18.5:
        return 1.5
    elif 18.5 <= bmi < 25:
        return 1.2
    elif 25 <= bmi < 30:
        return 1.0
    else:
        return 0.8

@app.route('/diet-plan', methods=['POST'])
def diet_plan():
    data = request.get_json()
    weight = data.get('weight')
    height = data.get('height')
    selected_foods = data.get('foods', [])

    if not weight or not height or not selected_foods:
        return jsonify({'error': 'Missing weight, height or foods'}), 400

    bmi = calculate_bmi(weight, height)
    protein_per_kg = protein_need_per_kg(bmi)
    target_protein = round(weight * protein_per_kg, 1)

    # Basic meals structure
    meal_plan = [
        "Wake up and drink 500 ml water.",
        "Meal 1 (within 30 mins): oats + 50g sprouts or boiled moong dal",
        "Meal 2 (after 2.5 hours): breakfast (light, no oil/sugar) + omelet (1 whole egg + 1 egg white + olive oil)",
        "Meal 3 (after 2.5 hours): green tea + 3 egg whites + any fruit",
        "Meal 4 (after 2.5 hours): 100g rice OR 3 chapatis + chicken + vegetable salad",
        "Meal 5 (before workout): green tea + 1 robusta banana",
        "Meal 6 (post workout): 4 egg whites + chicken",
        "Dinner: vegetable salad + leafy vegetables + 50g chicken"
    ]

    return jsonify({
        'bmi': round(bmi, 2),
        'protein_per_kg': protein_per_kg,
        'target_protein': target_protein,
        'daily_schedule': meal_plan
    })

if __name__ == '__main__':
    app.run(debug=True)
