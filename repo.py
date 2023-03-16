import os
import tempfile
import time
import re
from github import Github
from git import Repo
from model import Model
import configparser

class RepoManager:
    def __init__(self, repo_owner, repo_name):
        self.access_token = self.read_auth()
        self.github = Github(self.access_token)
        self.repo = self.github.get_repo(f"{repo_owner}/{repo_name}")
    
    def read_auth(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config.get('GitHub', 'access_token')

    def aggregate_repo_content(self, path='', token_limit=5000, max_file_size=100000):
        content_buffer = ""
        file_priority = ['.md', '.rst', '.txt', '.py', '.js', '.html', '.css', '.java', '.cpp', '.c']

        def is_text_file(filepath):
            return not filepath.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.pdf', '.zip', '.tar.gz', '.svg'))

        def remove_svg_content(file_content, file_ext):
            if file_ext in ['.html', '.js']:
                file_content = re.sub(r'<svg[\s\S]*?<\/svg>', '', file_content)
            return file_content

        contents = self.repo.get_contents(path)
        contents = sorted(contents, key=lambda c: (c.type, file_priority.index(os.path.splitext(c.path)[1]) if os.path.splitext(c.path)[1] in file_priority else len(file_priority)))

        for content in contents:
            if len(content_buffer) >= token_limit:
                break

            if content.type == 'dir':
                if content.path in ['node_modules', '.next', 'nextjs']:
                    continue                

                content_buffer += self.aggregate_repo_content(content.path, token_limit - len(content_buffer))
            elif content.type == 'file' and is_text_file(content.path):
                try:
                    # Skip large files
                    if content.size > max_file_size:
                        continue

                    file_ext = os.path.splitext(content.path)[1]
                    file_content = content.decoded_content.decode('utf-8')
                    file_content = remove_svg_content(file_content, file_ext)

                    if len(content_buffer) + len(file_content) > token_limit:
                        file_content = file_content[:token_limit - len(content_buffer)]

                    content_buffer += file_content + "\n"
                except:
                    print(f"Error decoding file: {content.path}")

        return content_buffer

    def create_readme_pr(self, completion):
        branch_name = f'update-readme-{int(time.time())}'

        # Clone the repository to a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            git_repo = Repo.clone_from(self.repo.clone_url, temp_dir)

            # Create a new branch
            git_repo.git.checkout('-b', branch_name)


            # Create or modify the README file
            readme_path = os.path.join(temp_dir, 'README.md')
            with open(readme_path, 'w') as readme_file:
                readme_file.write(completion)

            # Commit and push the changes
            git_repo.git.add(readme_path)
            git_repo.git.commit('-m', 'Updated README.md with Documatic')
            git_repo.git.push('--set-upstream', 'origin', branch_name)

        # Create a pull request
        pull_request = self.repo.create_pull(
            title="Update README.md",
            body="This pull request updates the README.md file with Documatic.",
            head=branch_name,
            base=self.repo.default_branch
        )

        return pull_request.html_url
    
    def generate_readme(self):
        prompt = self.aggregate_repo_content()
        completion = Model().generate_completion("text-davinci-003", prompt=prompt)
        self.create_readme_pr(completion["choices"][0]["text"])


    def generate_comments(self):
        pass