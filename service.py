from flask import Flask, request, jsonify, session, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = 'secret_key'

SSO_SERVER = 'http://localhost:5000'  # Assume SSO server is running on this address

@app.route('/')
def index():
    if 'username' in session:
        return f"Welcome, {session['username']}! <a href='/logout'>Logout</a>"
    return "Please <a href='/login'>login</a>"

@app.route('/login')
def login():
    callback_url = url_for('sso_callback', _external=True)
    return redirect(f"{SSO_SERVER}/login?redirect_uri={callback_url}")

@app.route('/sso_callback')
def sso_callback():
    session_id = request.args.get('session_id')
    if not session_id:
        return "No session ID provided", 400

    # Verify the session with the SSO server
    response = requests.get(f"{SSO_SERVER}/verify", params={'session_id': session_id})
    
    if response.status_code == 200:
        user_data = response.json()
        session['username'] = user_data['username']
        return redirect(url_for('index'))
    else:
        return "Authentication failed", 401

@app.route('/logout')
def logout():
    if 'username' in session:
        session_id = session.get('session_id')
        if session_id:
            # Inform SSO server about logout
            requests.post(f"{SSO_SERVER}/logout", json={'session_id': session_id})
        session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5001, debug=True)