import os
import tempfile
from github import Github
from git import Repo

# Replace with your access token

def read_auth():
    with open('ghtoken.txt', 'r') as file:
        auth_key = file.readline().strip()
    return auth_key

access_token = read_auth()

# Function to generate a new README content
def generate_readme(repo_name):
    return f"# {repo_name}\n\nThis is an auto-generated README for the {repo_name} repository."

def create_readme_pr(repo_url, repo_name, repo_owner, branch_name, pr_title, pr_body):
    # Connect to GitHub using the access token
    github = Github(access_token)
    repo = github.get_repo(f"{repo_owner}/{repo_name}")

    # Clone the repository to a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        git_repo = Repo.clone_from(repo_url, temp_dir)

        # Create a new branch
        git_repo.git.checkout('-b', branch_name)

        # Create or modify the README file
        readme_path = os.path.join(temp_dir, 'README.md')
        with open(readme_path, 'w') as readme_file:
            readme_file.write(generate_readme(repo_name))

        # Commit and push the changes
        git_repo.git.add(readme_path)
        git_repo.git.commit('-m', 'Updated README.md')
        git_repo.git.push('--set-upstream', 'origin', branch_name)

    # Create a pull request
    pull_request = repo.create_pull(
        title=pr_title,
        body=pr_body,
        head=branch_name,
        base='master'
    )

    return pull_request.html_url

# Example usage
repo_url = 'https://github.com/owner_of_the_repository/repository_name.git'
repo_name = 'repository_name'
repo_owner = 'owner_of_the_repository'
branch_name = 'update-readme'
pr_title = 'Update README.md'
pr_body = 'This pull request updates the README.md file with auto-generated content.'

pr_url = create_readme_pr(repo_url, repo_name, repo_owner, branch_name, pr_title, pr_body)
print(f"Created Pull Request: {pr_url}")