.DEFAULT_GOAL := all

.PHONY: all
all: install run

.PHONY: install
install: venv
	# Activate venv and install pip packages
	source venv/bin/activate && pip install -r requirements.txt

venv:
	# No .PHONY, so venv is created only if it doesn't exist
	test -d venv || python3 -m venv venv

.PHONY: run
run:
	python3 chatbotNba.py

.PHONY: clean
clean:
	rm -rf venv
