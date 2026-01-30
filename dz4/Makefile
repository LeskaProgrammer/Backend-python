PIP := venv/Scripts/pip
PYTHON3 := venv/Scripts/python
TESTS := venv/Scripts/pytest -v ./test_controllers.py

clear:
	rm -rf venv

venv:
	py -m venv venv

install_requirements:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON3) server.py

test:
	$(TESTS)
