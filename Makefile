CODE_DIR := src

.PHONY: format
format:
	black $(CODE_DIR)
	isort $(CODE_DIR)

.PHONY: lint
lint:
	black $(CODE_DIR) --diff
	isort $(CODE_DIR) --check-only --diff
	flake8 $(CODE_DIR)

.PHONY: clean
clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

.PHONY: prepare
prepare:
	git config core.hooksPath .gitconfig/hooks
