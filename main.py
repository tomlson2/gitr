from repo import RepoManager
from model import Model
import time

# Example usage
access_token = RepoManager.read_auth()
manager = RepoManager(access_token)

repo_url = 'https://github.com/tomlson2/Documatic.git'
repo_name = 'Documatic'
repo_owner = 'tomlson2'
branch_name = f'update-readme-{int(time.time())}'
pr_title = 'Update README.md'
pr_body = 'This pull request updates the README.md file with Documatic.'

repo = manager.github.get_repo(f"{repo_owner}/{repo_name}")
content_buffer = manager.aggregate_repo_content(repo)
model = Model()

completion = model.generate_completion(content_buffer)
prompt = completion["choices"][0]["text"]
pr_url = manager.create_readme_pr(repo_url, repo_name, repo_owner, branch_name, pr_title, pr_body, completion)
print(f"Created Pull Request: {pr_url}")
