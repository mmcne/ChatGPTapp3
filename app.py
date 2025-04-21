import os
from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

app.secret_key = os.environ.get("SECRET_KEY", "dev_key")

@app.route('/hello/<name>', methods=['GET', 'POST'])
def hello(name):
    if 'history' not in session:
        session['history'] = []

    result = None

    if request.method == 'POST':
        num1 = float(request.form['num1'])
        operator = request.form['operator']
        num2 = float(request.form['num2'])

        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            result = num1 / num2 if num2 != 0 else 'Error (div by 0)'

        # Save the result in session history
        calc_string = f"{num1} {operator} {num2} = {result}"
        session['history'].append(calc_string)
        session.modified = True  # tell Flask session has changed

    return render_template('hello.html', name=name, result=result, history=session['history'])


@app.route('/clear_history')
def clear_history():
    session.pop('history', None)
    # Redirect back to the same name page (pass it in query param)
    name = request.args.get('name', 'User')
    return redirect(url_for('hello', name=name))


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    return redirect(url_for('hello', name=name))

if __name__ == '__main__':
    app.run(debug=True)




