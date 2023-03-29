import os
import re

def count_tokens(file_content):
    return len(file_content.split())

def get_code_files(path: str = '', token_limit: int = 7000, max_file_size: int = 100000, skeleton: bool = False):
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
    total_tokens = 0

    for content in contents:
        if total_tokens >= token_limit:
            break

        if content.type == 'dir':
            if content.path in ['node_modules', '.next', 'nextjs', '__pycache__', 'Flask', 'jars']:
                continue

            sub_code_files, sub_total_tokens = self.get_code_files(content.path, token_limit - total_tokens)
            code_files += sub_code_files
            total_tokens += sub_total_tokens

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

                file_tokens = count_tokens(file_content)
                if total_tokens + file_tokens <= token_limit:
                    code_files.append(CodeFile(content.path, file_content))
                    total_tokens += file_tokens

            except:
                print(f"Error decoding file: {content.path}")

    return code_files, total_tokens
