import argparse
from repo import RepoManager

def main(repo_owner, repo_name):
    print(repo_owner, repo_name)
    manager = RepoManager(repo_owner, repo_name)
    completion = manager.generate_readme()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate README.md for a GitHub repository and create a pull request.')
    parser.add_argument('repo_owner', type=str, help='The owner of the repository.')
    parser.add_argument('repo_name', type=str, help='The name of the repository.')
    args = parser.parse_args()
    main(args.repo_owner, args.repo_name)