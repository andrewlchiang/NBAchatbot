.DEFAULT_GOAL := all

.PHONY: all
all: install run

.PHONY: install
install: venv
	# Activate venv and install smthing inside
	source venv/bin/activate && pip install -r requirements.txt
	# Other commands here

venv:
	# Create venv if it doesn't exist
	# test -d venv || virtualenv -p python3 --no-site-packages venv
	test -d venv || python3 -m venv venv

.PHONY: run
run:
	python3 chatbotNba.py

clean:
	rm -rf venv
	find . -iname "*.pyc" -delete
