.PHONY: create_venv install install-no-dev clean remove_venv update-lock help
.DEFAULT_GOAL := help

ENV_DIR := .venv
PYTHON := python3
POETRY := $(ENV_DIR)/bin/poetry

help:
	@echo "Available targets:"
	@awk -F ':.*?## ' '/^[a-zA-Z]/ && NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

create_venv:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(ENV_DIR)

	@echo "Installing Poetry..."
	$(ENV_DIR)/bin/pip install --upgrade pip
	$(ENV_DIR)/bin/pip install poetry

install: create_venv
	@echo "Installing all dependencies..."
	$(POETRY) install
	@echo "Installing pre-commit hooks..."
	/home/jeryl4913/lto_rag_reviewer/LTO_RAG/bin/pre-commit install

install-no-dev: create_venv
	@echo "Installing production dependencies (no dev)..."
	$(POETRY) install --no-dev

clean:
	@echo "Cleaning up artifact files..."
	find . -name '.coverage' -delete
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '.pytest_cache' -type d -exec rm -rf {} +
	find . -name '__pycache__' -type d -exec rm -rf {} +
	find . -name '.ipynb_checkpoints' -type d -exec rm -rf {} +

remove_venv:
	@echo "Removing virtual environment..."
	rm -rf $(ENV_DIR)
	@echo "Environment removed."
