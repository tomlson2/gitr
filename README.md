
# Documatic

Documatic is an automated script for generating README files for Github Repositories, as well as adding comments to functions.

## Installation

Documatic is wrapped in a Python package and can be installed with `pip`:

```sh
pip install documatic
```

## Usage

Documatic is used by first creating an access token for a Github account, which can be done in the Github Settings page. An OpenAI-compatible API key is also needed in order to access OpenAI's text completion model.

Once the access token and API key are acquired, they can be set up in the `config.ini` configuration file. After that, the script can be run with the following command:

```sh
python generate_readme_cli.py <repo_owner> <repo_name>
```

Documatic will scrape all text files in the specified repository and use OpenAI's text completion model to generate a README document. The generated document will be added to a new branch and a pull request will be created.

For adding comments to functions, the command is as follows:

```sh
python generate_comments_cli.py <repo_owner> <repo_name>
```

Documatic will scrape all text files in the specified repository and use OpenAI's text edit model to generate comments for functions. The generated comments will be added to a new branch and a pull request will be created.

## Contributing

If you would like to contribute to this project, feel free to open a pull request or create an issue in the [Github repository](https://github.com/kadupitiya/documatic).

## License

Documatic is released under the MIT License. See [LICENSE](LICENSE) for details.