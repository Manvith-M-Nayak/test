import os
import subprocess
import pickle
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# Vulnerability 1: Hardcoded secret key
app.secret_key = "supersecret123"

# Vulnerability 2: Command injection
@app.route('/ping')
def ping():
    ip = request.args.get('ip')
    # User input is directly passed to shell
    result = os.system(f"ping -c 1 {ip}")
    return f"Pinged {ip} with result code {result}"

# Vulnerability 3: Insecure deserialization
@app.route('/load_data', methods=['POST'])
def load_data():
    data = request.data
    # Using pickle on untrusted data - RCE possible
    obj = pickle.loads(data)
    return str(obj)

# Vulnerability 4: SQL injection
@app.route('/login')
def login():
    user = request.args.get('username')
    password = request.args.get('password')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Unescaped input in SQL query
    query = f"SELECT * FROM users WHERE username = '{user}' AND password = '{password}'"
    cursor.execute(query)
    rows = cursor.fetchall()
    if rows:
        return "Logged in successfully"
    else:
        return "Invalid credentials"

# Vulnerability 5: Sensitive information exposure
@app.route('/debug')
def debug():
    return os.popen("env").read()  # Exposes server environment variables

# Vulnerability 6: Use of eval()
@app.route('/eval')
def run_eval():
    code = request.args.get('code')
    return str(eval(code))  # Dangerous if code comes from user input

# Vulnerability 7: Missing HTTPS enforcement
@app.before_request
def force_https():
    pass  # Does nothing, no HTTPS redirect or enforcement

# Vulnerability 8: No authentication for sensitive route
@app.route('/admin/delete_all')
def delete_all():
    os.remove("users.db")  # Anyone can access this URL and delete the DB
    return "All users deleted."

# Vulnerability 9: Poor logging practice
@app.route('/log')
def log_info():
    username = request.args.get("username")
    password = request.args.get("password")
    print(f"User tried to login: {username} with password: {password}")
    return "Logged"

# Vulnerability 10: Unvalidated redirect
@app.route('/redirect')
def redirect_user():
    target = request.args.get("url")
    return f'<meta http-equiv="refresh" content="0; url={target}">'

if __name__ == '__main__':
    app.run(debug=True)
