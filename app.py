from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from repo import RepoManager

app = Flask(__name__)
CORS(app)

@app.route('/api/readme')
def generate_readme():
    print("request recieved")

    # Get the username and repo query parameters
    username = request.args.get('username')
    repo = request.args.get('repo')

    # Call your function to generate the README for the given username and repo
    manager = RepoManager(username, repo)
    readme = manager.generate_readme_pr()

    print('readme :' + readme)

    # Return the generated README as JSON
    return jsonify({'readme': readme})

@app.rout('/api/pr')
def create_pullrqeuest():
    print("generating pr")


if __name__ == "__main__":
    app.run()