from flask import Flask, render_template, request
import pandas as pd
import joblib
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database Setup
DB_PATH = 'predictions.db'

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                age INTEGER,
                job TEXT,
                balance INTEGER,
                prediction TEXT,
                probability REAL
            )
        ''')
        conn.commit()

init_db()

# Load the trained model
model_path = 'model.pkl'
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    model = None
    print("Warning: model.pkl not found. Please run train_model.py first.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/performance')
def performance():
    return render_template('performance.html')

@app.route('/dashboard')
def dashboard():
    history = []
    if os.path.exists(DB_PATH):
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM predictions ORDER BY timestamp DESC LIMIT 50')
            history = cursor.fetchall()
    return render_template('dashboard.html', history=history)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('base.html', content="<div class='container' style='text-align:center; padding:5rem;'><h1 style='color:var(--primary);'>404</h1><p>Page not found.</p><a href='/' class='btn-primary'>Return Home</a></div>"), 404

@app.errorhandler(500)
def internal_server_error(e):
    import traceback
    error_trace = getattr(e, 'original_exception', e)
    return render_template('base.html', content=f"<div class='container' style='text-align:left; padding:5rem;'><h1 style='color:var(--danger);'>500 Internal Error</h1><p>{str(error_trace)}</p><a href='/' class='btn-primary'>Return Home</a></div>"), 500

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Processing all 16 input variables
        # We need to ensure types match what the model expects (int for numbers)
        try:
            data = {
                'age': int(request.form.get('age')),
                'job': request.form.get('job'),
                'marital': request.form.get('marital'),
                'education': request.form.get('education'),
                'default': request.form.get('default'),
                'balance': int(request.form.get('balance')),
                'housing': request.form.get('housing'),
                'loan': request.form.get('loan'),
                'contact': request.form.get('contact'),
                'day': int(request.form.get('day')),
                'month': request.form.get('month'),
                'duration': int(request.form.get('duration')),
                'campaign': int(request.form.get('campaign')),
                'pdays': int(request.form.get('pdays')),
                'previous': int(request.form.get('previous')),
                'poutcome': request.form.get('poutcome')
            }
            
            # Create DataFrame for prediction
            input_df = pd.DataFrame([data])
            
            prediction = "Error"
            prediction_text = "Could not make a prediction."
            probability_pct = 0.0
            
            if model:
                # Predict
                pred = model.predict(input_df)[0]
                # Probability
                proba = model.predict_proba(input_df)[0]
                
                if pred == 1:
                    prediction = "High Probability"
                    probability_pct = round(proba[1] * 100, 1)
                    prediction_text = f"Analysis indicates a {probability_pct}% likelihood of term deposit subscription. Recommended Action: Prioritize for immediate engagement."
                    alert_class = "success"
                else:
                    prediction = "Low Probability"
                    probability_pct = round(proba[1] * 100, 1)
                    prediction_text = f"Analysis indicates only a {probability_pct}% likelihood of term deposit subscription. Recommended Action: Nurture with educational content."
                    alert_class = "danger"
                
                # Save to database
                with sqlite3.connect(DB_PATH) as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO predictions (timestamp, age, job, balance, prediction, probability)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data['age'], data['job'], data['balance'], prediction, probability_pct))
                    conn.commit()
            else:
                prediction_text = "Model not loaded."
                alert_class = "warning"

        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            return render_template('base.html', content=f"<div class='container' style='text-align:left; padding:5rem;'><h1 style='color:var(--danger);'>Exception Block Triggered</h1><p><strong>{type(e).__name__}</strong>: {str(e)}</p><pre style='color:var(--text-main); background:rgba(0,0,0,0.5); padding:2rem; border-radius:1rem; overflow-x:auto; text-align:left;'>{error_trace}</pre><a href='/' class='btn-primary' style='margin-top:2rem;'>Return Home</a></div>"), 500

        return render_template('result_fixed.html', data=data, prediction=prediction, prediction_text=prediction_text, alert_class=alert_class, probability=probability_pct)

if __name__ == '__main__':
    app.run(debug=True)

# Reload trigger 2
