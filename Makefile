##
## EPITECH PROJECT, 2026
## Intelligent_snake
## File description:
## Makefile
##

PYTHON = .venv/bin/python3
PIP = .venv/bin/pip
PYINSTALLER = .venv/bin/pyinstaller
ENTRY_POINT = game/main.py
NAME = ouroboros

all: install $(NAME)

install:
	$(PIP) install -r requirement.txt
	$(PIP) install pyinstaller

$(NAME):
	$(PYINSTALLER) --onefile --name=$(NAME) --paths=. --collect-all game $(ENTRY_POINT)
	cp dist/$(NAME) .

test:
	$(PYTHON) -m pytest tests/

clean:
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -rf build dist $(NAME).spec

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all install clean fclean test re
