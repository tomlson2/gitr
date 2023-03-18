import os
import tempfile
import time
import re
from github import Github
from git import Repo
from model import Model
import configparser


class CodeFile:
    def __init__(self, path: str, content: str):
        self.path = path
        self.content = content
        _, self.ext = os.path.splitext(path) 

class RepoManager:
    def __init__(self, repo_name: str, github: Github):
        self.access_token = self.read_auth()
        self.github = github
        self.owner = github.get_user().login
        print(self.owner)
        self.repo = github.get_repo(f"{self.owner}/{repo_name}")
    
    def parse_python(self, file_ext, code):
        if file_ext == ".py":
            return "\n".join([match.group(0) for match in re.finditer(r"^\s*(async\s+)?def\s+\w+\s*\(.*\)\s*:", code, re.MULTILINE)]) 

    def read_auth(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config.get('GitHub', 'access_token')

    def get_code_files(self, path: str = '', token_limit: int = 10000, max_file_size: int = 100000, skeleton: bool = False):
        file_priority = ['.md', '.rst', '.txt', '.py', '.js', '.html', '.css', '.java', '.cpp', '.c']

        def is_text_file(filepath):
            return not filepath.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.pdf', '.zip', '.tar.gz', '.svg', '.pkl'))

        def remove_svg_content(file_content, file_ext):
            if file_ext in ['.html', '.js']:
                file_content = re.sub(r'<svg[\s\S]*?<\/svg>', '', file_content)
            return file_content

        contents = self.repo.get_contents(path)
        contents = sorted(contents, key=lambda c: (c.type, file_priority.index(os.path.splitext(c.path)[1]) if os.path.splitext(c.path)[1] in file_priority else len(file_priority)))

        code_files = []

        for content in contents:
            if len(code_files) >= token_limit:
                break

            if content.type == 'dir':
                if content.path in ['node_modules', '.next', 'nextjs', '__pycache__', 'Flask', 'jars']:
                    continue                

                code_files += self.get_code_files(content.path, token_limit - len(code_files))
            elif content.type == 'file' and is_text_file(content.path):
                try:
                    # Skip large files
                    if content.size > max_file_size:
                        continue

                    file_ext = os.path.splitext(content.path)[1]
                    file_content = content.decoded_content.decode('utf-8')
                    file_content = remove_svg_content(file_content, file_ext)
                    if skeleton:
                        file_content = self.parse_python(file_ext, file_content)
                    code_files.append(CodeFile(content.path, file_content))
                except:
                    print(f"Error decoding file: {content.path}")

        return code_files
    
    def concatenate_code_files(self, code_files):
        content_list = []

        for code_file in code_files:
            if not code_file.content or code_file.content == "":
                continue
            else:
                content_list.append(f"---\n{code_file.path}\n{code_file.content}")

        return "\n".join(content_list)

    def generate_readme(self):
        content_buffer = self.concatenate_code_files(self.get_code_files())
        completion = Model().generate_completion("text-davinci-003", f"{content_buffer}\n---\nREADME.md")
        readme = completion["choices"][0]["text"]
        return readme

    
    def generate_pr(self, readme):
        branch_name = f'update-readme-{int(time.time())}'

        # Clone the repository to a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            git_repo = Repo.clone_from(self.repo.clone_url, temp_dir)

            # Create a new branch
            git_repo.git.checkout('-b', branch_name)


            # Create or modify the README file
            readme_path = os.path.join(temp_dir, 'README.md')
            with open(readme_path, 'w') as readme_file:
                readme_file.write(readme)

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

    def readme_exists(self):
        try:
            self.repo.get_contents('README.md')
            return True
        except:
            return False

    def get_latest_commit_message(self):
        commit = self.repo.get_commits()[0]
        return commit.commit.message