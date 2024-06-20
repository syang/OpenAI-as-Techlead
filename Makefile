# Define variables
POETRY := poetry
PYTHON := $(POETRY) run python
PYTEST := $(POETRY) run pytest

# Default target
.PHONY: all
all: install

# Install dependencies
.PHONY: install
install:
	$(POETRY) install

# Run tests
.PHONY: test
test:
	$(PYTEST)

# Run the main script
.PHONY: run
run:
	$(PYTHON) src/print_repo_contents.py

# Clean up
.PHONY: clean
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -r {} +

# Format code using black
.PHONY: format
format:
	$(POETRY) run black src tests

# Lint code using flake8
.PHONY: lint
lint:
	$(POETRY) run flake8 src tests

# Check dependencies for security vulnerabilities
.PHONY: check
check:
	$(POETRY) check
	$(POETRY) run safety check

# Show help
.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install    Install dependencies"
	@echo "  test       Run tests"
	@echo "  run        Run the main script"
	@echo "  clean      Clean up temporary files"
	@echo "  format     Format code using black"
	@echo "  lint       Lint code using flake8"
	@echo "  check      Check dependencies for security vulnerabilities"
	@echo "  help       Show this help message"

