from flask import Flask, request
import sqlite3
import os
import jwt
import subprocess

app = Flask(__name__)

# Vulnerability 1: SQL Injection
@app.route('/user')
def get_user():
    username = request.args.get('username')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return str(user)

# Vulnerability 2: Insecure Deserialization (JWT)
@app.route('/token')
def token():
    payload = request.args.get('payload')
    secret = 'secret'
    try:
        decoded = jwt.decode(payload, secret, algorithms=["HS256"])
        return f"Decoded: {decoded}"
    except jwt.exceptions.DecodeError:
        return "Invalid token"

# Vulnerability 3: Command Injection
@app.route('/ping')
def ping():
    host = request.args.get('host')
    response = subprocess.check_output(f"ping -c 1 {host}", shell=True)
    return response

# Vulnerability 4: Hardcoded Secret
@app.route('/secret')
def secret():
    return "The API key is: 12345-abcde-SECRET"

# Vulnerability 5: Using vulnerable package
@app.route('/')
def index():
    return "Welcome to the vulnerable benchmark project"

if __name__ == '__main__':
    app.run(debug=True)
