from repo import RepoManager
from model import Model

access_token = RepoManager.read_auth()
manager = RepoManager(access_token)

repo_name = 'krabken'
repo_owner = 'tomlson2'

repo = manager.github.get_repo(f"{repo_owner}/{repo_name}")
content_buffer = manager.aggregate_repo_content(repo)
model = Model()
completion = model.generate_completion(content_buffer)
prompt = completion["choices"][0]["text"]
pr_url = manager.create_readme_pr(repo, prompt)
print(f"Created Pull Request: {pr_url}")
