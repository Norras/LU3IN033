

init:
	pip install -r requirements.txt

install:
	python -m pip install --upgrade pip
	pip install tkinter
exec:
	python interface.py