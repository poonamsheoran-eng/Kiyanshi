from flask import Flask, request, jsonify, session
import json
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.secret_key = 'kiyanshi_organics_secret_key'

# File to store users
USERS_FILE = 'users.json'

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

ADMIN_NUMBER = '9999999999'

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    mobile = data.get('mobile', '').strip()
    password = data.get('password', '').strip()

    # Validate inputs
    if len(mobile) != 10 or not mobile.isdigit():
        return jsonify({'success': False, 'message': 'Enter a valid 10-digit mobile number.'})
    if len(password) != 6:
        return jsonify({'success': False, 'message': 'Password must be exactly 6 digits/characters.'})

    users = load_users()

    # Admin check
    if mobile == ADMIN_NUMBER:
        if mobile not in users:
            # Create admin account
            users[mobile] = {'password': password, 'role': 'admin', 'name': 'Admin'}
            save_users(users)
            return jsonify({'success': True, 'role': 'admin', 'message': 'Admin account created!', 'redirect': '/admin.html'})
        elif users[mobile]['password'] == password:
            return jsonify({'success': True, 'role': 'admin', 'message': 'Welcome Admin!', 'redirect': '/admin.html'})
        else:
            return jsonify({'success': False, 'message': 'Incorrect password for admin.'})

    # Regular user
    if mobile in users:
        if users[mobile]['password'] == password:
            return jsonify({'success': True, 'role': 'customer', 'message': f"Welcome back!", 'redirect': '/customer.html'})
        else:
            return jsonify({'success': False, 'message': 'Incorrect password. Try again.'})
    else:
        # New user - create account
        users[mobile] = {'password': password, 'role': 'customer', 'name': f'User_{mobile[-4:]}'}
        save_users(users)
        return jsonify({'success': True, 'role': 'customer', 'message': 'Account created! Welcome!', 'redirect': '/customer.html'})

@app.route('/users')
def get_users():
    users = load_users()
    return jsonify(users)

if __name__ == '__main__':
    print("✅ Kiyanshi Organics server running at http://localhost:5000")
    app.run(debug=True, port=5000)
