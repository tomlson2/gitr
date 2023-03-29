from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.sessions import SessionMiddleware

from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.responses import Response
from starlette.status import HTTP_302_FOUND

from repo import RepoManager
from github import Github
from model import Model
from typing import Optional
from user import User, init_db, Base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import configparser
import requests

DATABASE_URL = "sqlite:///./newdb.db"

SessionLocal = init_db(DATABASE_URL)
Base = declarative_base()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="fhdashfewbkqlckjlh")

origins = [
    "https://documatic-usbo-hqvtc9fqf-tomlson2.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def read_auth():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return (config.get('GitHub', 'client_id'), config.get('GitHub', 'client_secret'))

client_id, client_secret = read_auth()

@app.get("/login")
def login():
    scope = "public_repo repo"
    github_auth_url = f'https://github.com/login/oauth/authorize?client_id={client_id}&scope={scope}'
    return RedirectResponse(url=github_auth_url, status_code=HTTP_302_FOUND)

def get_user_access_token(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    return user.access_token

def get_current_user(request: Request):
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    return get_user_access_token(db=SessionLocal(), user_id=user_id)

@app.get("/callback")
async def callback(request: Request, code: str):
    token_url = 'https://github.com/login/oauth/access_token'
    data = {'client_id': client_id, 'client_secret': client_secret, 'code': code}
    headers = {'Accept': 'application/json'}
    response = requests.post(token_url, data=data, headers=headers)
    access_token = response.json().get('access_token')
    print(access_token)

    user_url = 'https://api.github.com/user'
    headers = {'Authorization': f'token {access_token}', 'Accept': 'application/json'}
    user_response = requests.get(user_url, headers=headers)
    user_data = user_response.json()
    print(user_data)
    
    db = SessionLocal()
    user = db.query(User).filter(User.github_id == user_data['id']).first()
    if not user:
        user = User(github_id=user_data['id'], username=user_data['login'], access_token=access_token)
        db.add(user)
        db.commit()

    request.session['user_id'] = user.id
    resp = RedirectResponse(url="http://localhost:3000/")
    resp.set_cookie(key='userLogin', value=user.username)
    return resp

@app.get("/api/readme")
async def generate_readme(request: Request, repo: str):
    user = get_current_user(request)
    if not user:
        return JSONResponse(content={'error': 'User not logged in'}, status_code=401)
    github = Github(user)

    manager = RepoManager(repo, github)
    readme = manager.generate_readme()

    return JSONResponse(content={'readme': readme})

@app.post("/api/pr")
async def create_pull_request(request: Request, repo: str, data: dict):
    readme = data.get('readme')

    user = get_current_user(request)
    if not user:
        return JSONResponse(content={'error': 'User not logged in'}, status_code=401)

    github = Github(user)

    manager = RepoManager(repo, github)
    link = manager.generate_pr(readme)

    return JSONResponse(content={'link': link})

@app.get("/api/auto-api")
async def generate_api(request: Request, repo: str):
    user = get_current_user(request)
    if not user:
        return JSONResponse(content={'error': 'User not logged in'}, status_code=401)
    github = Github(user)

    manager = RepoManager(repo, github)
    readme = manager.generate_api()

    return JSONResponse(content={'readme': readme})

@app.post("/api/update-readme")
async def update_readme(data: dict):
    readme = data.get('readme')
    update = data.get('update')

    res = Model().generate_edit('text-davinci-edit-001', readme, update, 0.8)
    new_readme = res['choices'][0]['text']

    return JSONResponse(content={'readme': new_readme})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)