from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('data/finance.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            type TEXT,
            amount REAL,
            description TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('data/finance.db')
    c = conn.cursor()
    c.execute('SELECT * FROM transactions')
    transactions = c.fetchall()
    conn.close()

    total_income = sum(x[2] for x in transactions if x[1] == 'income')
    total_expense = sum(x[2] for x in transactions if x[1] == 'expense')
    balance = total_income - total_expense

    # Simulated AI-style financial tip
    tip = "You're on track!"
    if balance < 0:
        tip = "You're spending more than you're earning. Consider reducing expenses."
    elif balance < total_income * 0.2:
        tip = "Your savings are under 20%. Try to build an emergency fund."

    return render_template('index.html', transactions=transactions, income=total_income, expense=total_expense, balance=balance, tip=tip)

@app.route('/add', methods=['POST'])
def add():
    type = request.form['type']
    amount = float(request.form['amount'])
    description = request.form['description']
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('data/finance.db')
    c = conn.cursor()
    c.execute('INSERT INTO transactions (type, amount, description, date) VALUES (?, ?, ?, ?)', (type, amount, description, date))
    conn.commit()
    conn.close()

    return redirect('/')
@app.route('/delete/<int:transaction_id>', methods=['POST'])
def delete(transaction_id):
    conn = sqlite3.connect('data/finance.db')
    c = conn.cursor()
    c.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
