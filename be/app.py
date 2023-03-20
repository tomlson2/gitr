from flask import Flask, request, jsonify, redirect, session, make_response
from flask_cors import CORS
from repo import RepoManager
from github import Github
from model import Model
from flask_sqlalchemy import SQLAlchemy
import configparser
import requests

def read_auth():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return (config.get('GitHub', 'client_id'), config.get('GitHub', 'client_secret'))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)
app.secret_key = 'your_secret_key_here'
app.config["SESSION_COOKIE_DOMAIN"] = "127.0.0.1"

client_id, client_secret = read_auth()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    github_id = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False)
    access_token = db.Column(db.String, nullable=False)


with app.app_context():
    db.create_all()

def get_user_access_token(user_id):
    user = User.query.get(user_id)
    return user.access_token

def get_current_user():
    print(f"Session in get_current_user: {session}")
    user_id = session.get('user_id')
    print(f"User ID from session: {user_id}")
    if not user_id:
        return None
    user = User.query.get(user_id)
    return user

@app.route('/login')
def login():
    scope = "public_repo repo"
    github_auth_url = f'https://github.com/login/oauth/authorize?client_id={client_id}&scope={scope}'
    return redirect(github_auth_url)

@app.route('/api/user')
def return_user():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not logged in'}), 401
    print(user)
    access_token = get_user_access_token(user.id)
    github = Github(access_token)
    return jsonify({'userLogin': github.get_user().login})
    

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = 'https://github.com/login/oauth/access_token'
    data = {'client_id': client_id, 'client_secret': client_secret, 'code': code}
    headers = {'Accept': 'application/json'}
    response = requests.post(token_url, data=data, headers=headers)
    access_token = response.json().get('access_token')

    user_url = 'https://api.github.com/user'
    headers = {'Authorization': f'token {access_token}', 'Accept': 'application/json'}
    user_response = requests.get(user_url, headers=headers)
    user_data = user_response.json()
    
    user = User.query.filter_by(github_id=user_data['id']).first()
    if not user:
        user = User(github_id=user_data['id'], username=user_data['login'], access_token=access_token)
        db.session.add(user)
        db.session.commit()
    
    session['user_id'] = user.id
    print(f"User {user.username} logged in with session: {session}")
    resp = make_response(redirect('http://localhost:3000'))
    resp.set_cookie('userLogin', user.username)
    return resp

@app.route('/api/readme')
def generate_readme():
    repo = request.args.get('repo')

    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not logged in'}), 401
    print(user)
    access_token = get_user_access_token(user.id)
    github = Github(access_token)

    manager = RepoManager(repo, github)
    readme = manager.generate_readme()

    return jsonify({'readme': readme})

@app.route('/api/pr', methods=['POST'])
def create_pullrqeuest():
    repo = request.args.get('repo')
    data = request.get_json()
    readme = data.get('readme')

    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not logged in'}), 401

    access_token = get_user_access_token(user.id)

    github = Github(access_token)

    manager = RepoManager(repo, github)
    link = manager.generate_pr(readme)

    return jsonify({'link': link})

@app.route('/api/update-readme', methods=['POST'])
def update_readme():
    data = request.get_json()
    readme = data.get('readme')
    update = data.get('update')

    res = Model().generate_edit('text-davinci-edit-001', readme, update, 0.8)
    new_readme = res['choices'][0]['text']
    print(new_readme)

    return jsonify({'readme': new_readme})




if __name__ == "__main__":
    app.run()