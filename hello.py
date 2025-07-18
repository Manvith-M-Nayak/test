# filename: insecure_app.py

from flask import Flask, request, render_template_string
import os
import subprocess
import sqlite3

app = Flask(__name__)

# Unsafe global variables
DATABASE = 'users.db'
SECRET_KEY = 'hardcoded-secret-key'

@app.route('/')
def index():
    return '<h1>Welcome to the Insecure App!</h1><form action="/search" method="get"><input name="query"><input type="submit"></form>'

@app.route('/search')
def search():
    # SQL Injection vulnerability
    query = request.args.get('query', '')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    sql = f"SELECT * FROM users WHERE name = '{query}'"  # Dangerous!
    result = cursor.execute(sql).fetchall()
    conn.close()

    return render_template_string('<h2>Results:</h2>{{ result }}', result=result)

@app.route('/upload', methods=['POST'])
def upload():
    # Arbitrary file upload vulnerability
    file = request.files['file']
    file.save(os.path.join('/tmp/uploads', file.filename))  # No sanitization or checks
    return 'File uploaded!'

@app.route('/exec')
def execute():
    # Remote command execution vulnerability
    cmd = request.args.get('cmd')
    output = subprocess.check_output(cmd, shell=True)  # Extremely dangerous!
    return f"<pre>{output.decode()}</pre>"

@app.route('/admin')
def admin():
    # Hardcoded credentials vulnerability
    username = request.args.get('username')
    password = request.args.get('password')
    if username == 'admin' and password == '1234':  # Easily guessable
        return 'Welcome admin!'
    return 'Access denied'

@app.route('/xss')
def xss():
    # Cross-Site Scripting (XSS) vulnerability
    name = request.args.get('name', '')
    return f"<h2>Hello {name}</h2>"  # Unsanitized user input directly rendered

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
