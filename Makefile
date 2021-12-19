PYTHON=     python3
VENV=       venv

$(VENV): $(VENV)/.depend


$(VENV)/.depend: requirements.txt setup.py
	# make venv
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install $(PIP_OPTIONS) -r requirements.txt
	$(VENV)/bin/pip install $(PIP_OPTIONS) -e .
	touch $(VENV)/.depend


run: $(VENV)
	$(VENV)/bin/python server.py


clean: $(VENV)
	Removing virtual environment
	rm -r $(VENV)
