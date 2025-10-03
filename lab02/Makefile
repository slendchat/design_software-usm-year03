PYTHON = python
PACKAGE = pipeline_pkg
TESTS = tests

run:
	$(PYTHON) -m $(PACKAGE)

test:
	pytest -v $(TESTS)

install:
	pip install .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache

reset: clean
	rm -rf venv

help:
	@echo "Доступные команды:"
	@echo "  make run     - запуск программы (python -m pipeline_pkg)"
	@echo "  make test    - запуск pytest"
	@echo "  make install - установка зависимостей"
	@echo "  make clean   - удалить __pycache__ и мусор"
	@echo "  make reset   - полный сброс (с venv)"