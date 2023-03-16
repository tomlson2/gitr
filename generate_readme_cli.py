import argparse
from repo import RepoManager
from model import Model

def main(repo_name, repo_owner):
    access_token = RepoManager.read_auth()
    manager = RepoManager(access_token)

    repo = manager.github.get_repo(f"{repo_owner}/{repo_name}")
    content_buffer = manager.aggregate_repo_content(repo)
    model = Model()
    completion = model.generate_completion(content_buffer)
    prompt = completion["choices"][0]["text"]
    pr_url = manager.create_readme_pr(repo, prompt)
    print(f"Created Pull Request: {pr_url}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate README.md for a GitHub repository and create a pull request.')
    parser.add_argument('repo_name', type=str, help='The name of the repository.')
    parser.add_argument('repo_owner', type=str, help='The owner of the repository.')

    args = parser.parse_args()
    main(args.repo_name, args.repo_owner)