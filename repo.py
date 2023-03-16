import os
import tempfile
import time
import re
from github import Github
from git import Repo
from model import Model
import configparser


class CodeFile:
    def __init__(self, path, content):
    This class represents a file that contains code with comments.
        self.path = path
        self.content = content


class CodeComment:
    def __init__(self, file, comment):
        self.file = file
        self.comment = comment

    def generate(model):
        prompt = f"{self.file.content}\n---\n{self.file.path}\n---\n"
        completion = model.generate_completion("text-davinci-003", prompt=prompt)
        return completion["choices"][0]["text"].strip()


class RepoManager:
    def __init__(self, repo_owner, repo_name):
        self.access_token = self.read_auth()
        self.github = Github(self.access_token)
        self.repo = self.github.get_repo(f"{repo_owner}/{repo_name}")

    def read_auth(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config.get('GitHub', 'access_token')

    def get_code_files(self, path='', token_limit=10000, max_file_size=100000):
        file_priority = ['.md', '.rst', '.txt', '.py', '.js', '.html', '.css', '.java', '.cpp', '.c']

        def is_text_file(filepath):
            return not filepath.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.pdf', '.zip', '.tar.gz', '.svg'))

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
                if content.path in ['node_modules', '.next', 'nextjs', '__pycache__', 'Flask']:
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
                    code_files.append(CodeFile(content.path, file_content))
                except:
                    print(f"Error decoding file: {content.path}")

        return code_files

    def create_pr(self, branch_name, title, body, files_and_comments):
        # Clone the repository to a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            git_repo = Repo.clone_from(self.repo.clone_url, temp_dir)

            # Create a new branch
            git_repo.git.checkout('-b', branch_name)

                    # Add comments to each file and commit the changes
        for code_file, comment in files_and_comments:
            file_path = os.path.join(temp_dir, code_file.path)
            with open(file_path, 'a') as file:
                file.write(f"\n\n# Generated Comment\n{comment}\n")

            git_repo.git.add(file_path)
            git_repo.git.commit('-m', f'Added comment to {code_file.path}')

        # Push the changes
        git_repo.git.push('--set-upstream', 'origin', branch_name)

    # Create a pull request
    pull_request = self.repo.create_pull(
        title=title,
        body=body,
        head=branch_name,
        base=self.repo.default_branch
    )

    return pull_request

    def generate_comments(self):
        code_files = self.get_code_files()
        model = Model()

        files_and_comments = []

        for code_file in code_files:
            comment = CodeComment(code_file).generate(model)
            if comment:
                files_and_comments.append((code_file, comment))

        if not files_and_comments:
            print("No comments generated.")
            return

        branch_name = f'add-comments-{int(time.time())}'
        title = "Add generated comments to files"
        body = "This pull request adds generated comments to files in the repository."

        pull_request = self.create_pr(branch_name, title, body, files_and_comments)

        return pull_request
