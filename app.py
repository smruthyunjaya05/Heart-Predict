from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load("heart_disease_model.pkl")

features = ['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 
            'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 
            'Oldpeak', 'ST_Slope']

label_maps = {
    'Sex': {'M': 1, 'F': 0},
    'ChestPainType': {'ATA': 0, 'NAP': 1, 'ASY': 2, 'TA': 3},
    'RestingECG': {'Normal': 0, 'ST': 1, 'LVH': 2},
    'ExerciseAngina': {'Y': 1, 'N': 0},
    'ST_Slope': {'Up': 0, 'Flat': 1, 'Down': 2}
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/assess', methods=['GET', 'POST'])
def assess():
    result = None
    if request.method == 'POST':
        data = {}
        for f in features:
            val = request.form[f]
            if f in label_maps:
                val = label_maps[f][val]
            else:
                val = float(val)
            data[f] = val
        df = pd.DataFrame([data])
        pred = model.predict(df)[0]
        result = "Heart Disease Detected" if pred == 1 else "No Heart Disease"
    return render_template('assess.html', features=features, result=result)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/risks')
def risks():
    return render_template('risks.html')

@app.route('/precautions')
def precautions():
    return render_template('precautions.html')

if __name__ == '__main__':
    app.run(debug=True)
