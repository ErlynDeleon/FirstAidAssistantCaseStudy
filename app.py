from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

ADVICE_FILE = os.path.join('data', 'advice.json')
PERSON_FILE = os.path.join('data', 'persons.json')

with open(ADVICE_FILE, 'r') as f:
    first_aid_data = json.load(f)

if not os.path.exists(PERSON_FILE):
    with open(PERSON_FILE, 'w') as f:
        json.dump([], f)

def load_people():
    with open(PERSON_FILE, 'r') as f:
        return json.load(f)

def save_person(person):
    people = load_people()
    people.append(person)
    with open(PERSON_FILE, 'w') as f:
        json.dump(people, f, indent=4)

@app.route('/')
def home():
    symptoms = list(first_aid_data.keys())
    return render_template('index.html', symptoms=symptoms)

def get_age_group(age):
    age = int(age)
    if age <= 1:
        return 'infant'
    elif age <= 12:
        return 'child'
    else:
        return 'adult'

@app.route('/result', methods=['POST'])
def result():
    name = request.form.get('name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    symptom = request.form.get('symptom', '').strip().lower()
    age_group = get_age_group(age)

    raw_advice = first_aid_data.get(symptom)

    if isinstance(raw_advice, dict):
        advice = raw_advice.get(age_group) or raw_advice.get("default") or "No specific advice for this age group."
    else:
        advice = raw_advice or "No advice found for this symptom."

    person = {
        'name': name,
        'age': age,
        'gender': gender,
        'symptom': symptom,
        'advice': advice
    }

    save_person(person)

    return render_template('result.html', person=person)
  
@app.route('/people')
def people():
    return render_template('people.html', people=load_people())
  
@app.route('/delete/<int:index>', methods=['POST'])
def delete_person(index):
    people = load_people()
    if 0 <= index < len(people):
        del people[index]
        with open(PERSON_FILE, 'w') as f:
            json.dump(people, f, indent=4)
    return redirect(url_for('people'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)