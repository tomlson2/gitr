
# Documatic

Documatic is a tool for automatically generating documentation for a GitHub repository. It can generate a README.md file for your repository and create a pull request with the generated content. It can also generate comments for functions in your code and create a pull request with the generated comments.

## Installation

Clone the repository and install the dependencies.

```
git clone https://github.com/<username>/Documatic.git
cd Documatic
pip install -r requirements.txt
```

## Usage

### Generate README

You can generate a README.md file for your repository and create a pull request with the generated content by running the following command.

```
python generate_readme_cli.py <repo_owner> <repo_name>
```

You can also generate a README.md file from the API endpoint.

```
curl -X GET http://localhost:5000/api/readme?username=<repo_owner>&repo=<repo_name>
```

### Generate Comments

You can generate comments for functions in your code and create a pull request with the generated comments by running the following command.

```
python generate_comments_cli.py <repo_owner> <repo_name>
