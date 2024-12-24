# LTO Driver's Guide RAG Chatbot

## Overview
tbd

## Prerequisites
- Python 3.10 and up are installed
- Your ollama client must be running. For more information check: https://github.com/ollama/ollama
- `Make` installed on your system and you are using WSL 2

## Contributing
To get started:

1. Fork the repository.
2. Clone your fork:
   ```bash
   git clone https://github.com/markokow/lto_rag_reviewer.git
   ```
3. Navigate to the project directory:
   ```bash
   cd lto_rag_reviewer
   ```
4. Create a virtual environment and install dependencies:
   ```bash
   make install
   ```
5. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
6. Make your changes and commit them using Commitizen:
   ```bash
   git add .
   cz commit
   ```
7. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
8. Open a pull request to the main repository.
9. If any new dependencies are added by other team members, update your environment by running:
   ```bash
   poetry install
   ```

## Adding New Packages

To add a new package to the project:

1. Use Poetry to add the package:
   ```bash
   poetry add <package-name>
   ```
2. Commit the updated `pyproject.toml` and `poetry.lock` files:
   ```bash
   git add pyproject.toml poetry.lock
   cz commit
   ```
3. Push the changes and open a pull request if necessary.

## Notes

- The virtual environment is created in a directory named `.venv`.
- Poetry is used to manage dependencies.
- Pre-commit hooks are installed automatically during the `install` process.

## License

This project is open source and available under the MIT License.
