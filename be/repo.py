import os
import tempfile
import time
import re
from github import Github
from git import Repo
from model import Model
import configparser
from token_limit import get_code_files
import traceback
import nltk


class CodeFile:
    def __init__(self, path: str, content: str, tokens: int):
        self.path = path
        self.content = content
        self.tokens = tokens
        _, self.ext = os.path.splitext(path) 

class RepoManager:
    def __init__(self, repo_name: str, github: Github):
        self.access_token = self.read_auth()
        self.github = github
        self.owner = github.get_user().login
        print(self.owner)
        self.repo = github.get_repo(f"{self.owner}/{repo_name}")

    def count_tokens(self, content: str) -> int:
        tokens = nltk.word_tokenize(content)
        return len(tokens)

    def get_code_files(self, path: str = '', token_limit: int = 6000, max_file_size: int = 100000, skeleton: bool = False): 
        file_priority = ['.md', '.rst', '.txt', '.py', '.js', '.html', '.css', '.java', '.cpp', '.c']

        def is_text_file(filepath):
            return not filepath.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.pdf', '.zip', '.tar.gz', '.svg', '.pkl'))

        def remove_svg_content(file_content, file_ext):
            if file_ext in ['.html', '.js']:
                file_content = re.sub(r'<svg[\s\S]*?<\/svg>', '', file_content)
            return file_content

        def add_file_if_within_limit(code_files, file: CodeFile, token_limit: int) -> bool:
            total_tokens = sum(cf.tokens for cf in code_files)
            if total_tokens + file.tokens <= token_limit:
                code_files.append(file)
                return True
            return False

        contents = self.repo.get_contents(path)
        contents = sorted(contents, key=lambda c: (c.type, file_priority.index(os.path.splitext(c.path)[1]) if os.path.splitext(c.path)[1] in file_priority else len(file_priority)))

        code_files = []

        for content in contents:

            if content.type == 'dir':
                if content.path in ['node_modules', '.next', 'nextjs', '__pycache__', 'Flask', 'jars']:
                    continue

                sub_code_files, _ = self.get_code_files(content.path, token_limit, max_file_size, skeleton)
                for sub_file in sub_code_files:
                    if not add_file_if_within_limit(code_files, sub_file, token_limit):
                        break

            elif content.type == 'file' and is_text_file(content.path):
                try:
                    if content.size > max_file_size:
                        continue

                    file_ext = os.path.splitext(content.path)[1]
                    file_content = content.decoded_content.decode('utf-8')
                    file_content = remove_svg_content(file_content, file_ext)
                    if skeleton:
                        file_content = self.parse_python(file_ext, file_content)

                    file_tokens = self.count_tokens(file_content)
                    new_file = CodeFile(content.path, file_content, tokens=file_tokens)

                    add_file_if_within_limit(code_files, new_file, token_limit)

                except Exception as e:
                    print(f"Error decoding file: {content.path}")
                    print(f"Error message: {str(e)}")
                    print(traceback.format_exc())

        total_tokens = sum(cf.tokens for cf in code_files)
        return code_files, total_tokens

    def parse_python(self, file_ext, code):
        if file_ext == ".py":
            return "\n".join([match.group(0) for match in re.finditer(r"^\s*(async\s+)?def\s+\w+\s*\(.*\)\s*:", code, re.MULTILINE)]) 

    def read_auth(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config.get('GitHub', 'access_token')

    def concatenate_code_files(self, code_files):
        content_list = []

        for code_file in code_files:
            if not code_file.content or code_file.content == "":
                continue
            else:
                content_list.append(f"---\n{code_file.path}\n{code_file.content}")

        return "\n".join(content_list)

    def generate_readme(self):
        code_files, _ = self.get_code_files()
        content_buffer = self.concatenate_code_files(code_files)
        print(f"content: {content_buffer}")
        completion = Model().generate_completion("gpt-4", f"{content_buffer}\n---\nREADME.md")
        readme = completion["choices"][0]["message"]["content"]
        return readme

    def generate_api(self):
        code_files, tokens = self.get_code_files()
        content_buffer = self.concatenate_code_files(code_files)
        completion_tokens = 7000 - tokens
        completion = Model().generate_completion("gpt-4", max_tokens=completion_tokens, prompt=f"{content_buffer}\nYou are a python developer that has an API first mindset. Generate an API for this code base using Python's FastAPI.\nYou should only respond with code snippets.")
    
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
            body="This pull request updates the README.md file with gitr",
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