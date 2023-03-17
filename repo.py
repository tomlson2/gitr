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
    def __init__(self, repo_owner: str, repo_name: str):
        self.access_token = self.read_auth()
        self.github = Github(self.access_token)
        self.repo = self.github.get_repo(f"{repo_owner}/{repo_name}")
    
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

    
    def generate_readme_pr(self):
        content_buffer = self.concatenate_code_files(self.get_code_files())
        completion = Model().generate_completion("text-davinci-003", f"{content_buffer}\n---\nREADME.md")
        completion = completion["choices"][0]["text"]
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

        return completion

    def generate_comments_for_functions(self):
        code_files = self.get_code_files()
        model = Model()

        branch_name = f'add-comments-{int(time.time())}'
        # Clone the repository to a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            git_repo = Repo.clone_from(self.repo.clone_url, temp_dir)

            # Create a new branch
            git_repo.git.checkout('-b', branch_name)

            # Add comments to each file
            for code_file in code_files:
                print(code_file.path[-3:])
                if not code_file.content or code_file.path[-3:] != ".py":
                    continue
                file_path = os.path.join(temp_dir, code_file.path)
                with open(file_path, 'r') as file:
                    original_content = file.read()

                completion = model.generate_completion("text-davinci-003", prompt=f'{code_file.content} you are a professional software engineer that has been tasked with adding docstrings to your code base. Give the output in the form of:\ndef...\n"""docstring"""')
                # Generate comments for the parsed "function-only" code
                function_with_comment = completion["choices"][0]["text"]
                print(code_file.content)
                print(function_with_comment)

                # Integrate comments back into the original code
                updated_content = self.integrate_comments(original_content, code_file.content, function_with_comment)
                if updated_content == original_content:
                    continue

                with open(file_path, 'w') as file:
                    file.write(updated_content)

                # Commit the changes
                git_repo.git.add(file_path)
                git_repo.git.commit('-m', f'Added comment to {code_file.path}')

            # Push the changes
            git_repo.git.push('--set-upstream', 'origin', branch_name)

        # Create a pull request
        pull_request = self.repo.create_pull(
            title="Add generated comments to functions",
            body="This pull request adds generated comments to functions in the repository.",
            head=branch_name,
            base=self.repo.default_branch
        )

        return pull_request

    def integrate_comments(self, original_content, function_only_content, function_with_comment):
        # Create a mapping of function signatures to their corresponding comments
        function_map = {}
        function_lines = function_only_content.splitlines()
        function_with_comment_lines = function_with_comment.splitlines()

        for line in function_with_comment_lines:
            if line.strip() in function_lines:
                function_signature = line.strip()
                comment_lines = []
                index = function_with_comment_lines.index(line)

                # Collect comment lines before the function signature
                while index > 0:
                    index -= 1
                    comment_line = function_with_comment_lines[index]
                    if comment_line.strip().startswith('"""'):
                        comment_lines.insert(0, comment_line)
                        if len(comment_lines) > 1 and comment_lines[-2].strip().startswith('"""'):
                            break
                    else:
                        break

                function_map[function_signature] = '\n'.join(comment_lines)

        # Replace the function signatures in the original content with the comments and function signatures
        updated_content = original_content
        for function_signature, comment in function_map.items():
            updated_content = updated_content.replace(function_signature, f"{comment}\n{function_signature}")

        return updated_content
