from flask import Flask, request, jsonify, redirect, session, url_for
from flask_cors import CORS
import os
from repo import RepoManager
from model import Model
from flask_sqlalchemy import SQLAlchemy
import configparser
import requests

def read_auth():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return (config.get('GitHub', 'client_id'), config.get('GitHub', 'client_secret'))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Or use your PostgreSQL connection string
db = SQLAlchemy(app)
CORS(app)

app.secret_key = 'your_secret_key_here'


client_id, client_secret = read_auth()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    github_id = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/login')
def login():
    github_auth_url = f'https://github.com/login/oauth/authorize?client_id={client_id}'
    return redirect(github_auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = 'https://github.com/login/oauth/access_token'
    data = {'client_id': client_id, 'client_secret': client_secret, 'code': code}
    headers = {'Accept': 'application/json'}
    response = requests.post(token_url, data=data, headers=headers)
    access_token = response.json().get('access_token')
    
    # Get user's GitHub profile
    user_url = 'https://api.github.com/user'
    headers = {'Authorization': f'token {access_token}', 'Accept': 'application/json'}
    user_response = requests.get(user_url, headers=headers)
    user_data = user_response.json()
    
    # Check if user exists in the database or create a new user
    user = User.query.filter_by(github_id=user_data['id']).first()
    if not user:
        user = User(github_id=user_data['id'], username=user_data['login'])
        db.session.add(user)
        db.session.commit()
    
    # Log in the user and redirect to the desired page
    # Replace this with your preferred method for handling user sessions
    session['user_id'] = user.id
    return redirect('http://localhost:3000')

@app.route('/api/readme')
def generate_readme():
    print("request recieved")

    # Get the username and repo query parameters
    username = request.args.get('username')
    repo = request.args.get('repo')

    # Call your function to generate the README for the given username and repo
    manager = RepoManager(username, repo)
    readme = manager.generate_readme()

    # Return the generated README as JSON
    return jsonify({'readme': readme})

@app.route('/api/pr', methods=['POST'])
def create_pullrqeuest():
    print("generating pr")
    username = request.args.get('username')
    repo = request.args.get('repo')
    data = request.get_json()
    readme = data.get('readme')

    manager = RepoManager(username, repo)
    link = manager.generate_pr(readme)

    return jsonify({'link': link})

@app.route('/api/update-readme', methods=['POST'])
def update_readme():
    data = request.get_json()
    readme = data.get('readme')
    update = data.get('update')

    res = Model().generate_edit('text-davinci-edit-001', readme, update, 0.9)
    new_readme = res['choices'][0]['text']
    print(new_readme)

    return jsonify({'readme': new_readme})




if __name__ == "__main__":
    app.run()