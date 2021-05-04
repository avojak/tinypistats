python=python3

.PHONY: dist

all: dist

dist:
	$(python) -m build .

clean:
	$(python) setup.py clean
	rm -rf build/ \
		dist/ \
		*.egg-info/ \
		*.pyc \
		__pycache__/
