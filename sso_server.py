from flask import Flask, request, jsonify, session, redirect, url_for
import uuid
import hashlib
import time

app = Flask(__name__)
app.secret_key = 'secret_key'  # Change this to a secure random key

# In-memory storage for users and sessions (replace with a database in production)
users = {}
sso_sessions = {}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if username in users:
        return jsonify({"error": "Username already exists"}), 400
    
    users[username] = hash_password(password)
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['GET'])
def login_page():
    redirect_uri = request.args.get('redirect_uri')
    # In a real implementation, you'd render a login form here
    return f"""
    <form action="/login" method="post">
        <input type="text" name="username" placeholder="Username">
        <input type="password" name="password" placeholder="Password">
        <input type="hidden" name="redirect_uri" value="{redirect_uri}">
        <input type="submit" value="Login">
    </form>
    """

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    redirect_uri = request.form.get('redirect_uri')
    
    if username not in users or users[username] != hash_password(password):
        return "Invalid credentials", 401
    
    # Create SSO session
    session_id = str(uuid.uuid4())
    sso_sessions[session_id] = {
        "username": username,
        "created_at": time.time()
    }
    
    # Redirect to the service's callback URL with the session_id
    return redirect(f"{redirect_uri}?session_id={session_id}")

@app.route('/verify', methods=['GET'])
def verify():
    session_id = request.args.get('session_id')
    
    if session_id not in sso_sessions:
        return jsonify({"error": "Invalid session"}), 401
    
    # Check if session is expired (e.g., after 30 minutes)
    if time.time() - sso_sessions[session_id]["created_at"] > 1800:
        del sso_sessions[session_id]
        return jsonify({"error": "Session expired"}), 401
    
    return jsonify({"username": sso_sessions[session_id]["username"]}), 200

@app.route('/logout', methods=['POST'])
def logout():
    session_id = request.json.get('session_id')
    
    if session_id in sso_sessions:
        del sso_sessions[session_id]
    
    return jsonify({"message": "Logged out successfully"}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)