

# Getting Started

This guide will help you get started using Documatic.

## Prerequisites

In order to use Documatic, you need to have the following installed on your machine:

* Python 3.6+
* Flask
* Click

## Installation

The easiest way to install Documatic is using pip.

```
pip install documatic
```

If you'd like to install the latest version from source, clone the GitHub respository, install the dependencies and run the setup command:

```
git clone https://github.com/tomlson2/documatic
cd documatic
pip install -r requirements.txt
python setup.py install
```

## Usage

Documatic has one main command, which is used to generate a README:

```
documatic generate
```

This command will generate a README.md file based on the source code from the current directory.

## Contributing

Documatic is an open-source project and contributions are welcome! To contribute, please clone the repository, make your changes, and submit a pull request.

## License

Documatic is released under the MIT License. See [LICENSE](/LICENSE) for more details.