.PHONY: build install devinstall preview publish check format clean test

build: clean
	python3 -m build

install: build
	pip3 install .

devinstall: build
	pip3 install -e .[dev]

preview: build
	python3 -m twine upload --repository-url "https://test.pypi.org/legacy/" dist/*

publish: build
	python3 -m twine upload --repository-url "https://upload.pypi.org/legacy/" dist/*

check:
	python3 -m mypy unicodecheck

format:
	python3 -m black -l 200 unicodecheck makedata.py

clean:
	python3 -c 'import shutil; shutil.rmtree("dist", ignore_errors=True)'
	python3 -c 'import shutil; shutil.rmtree("build", ignore_errors=True)'
	python3 -c 'import shutil; shutil.rmtree("unicodecheck.egg-info", ignore_errors=True)'
	python3 -c 'import shutil; shutil.rmtree(".mypy_cache", ignore_errors=True)'
	python3 -c 'import shutil; shutil.rmtree("data", ignore_errors=True)'

test:
	python3 -c 'import shutil; shutil.rmtree("data", ignore_errors=True)'
	python3 ./makedata.py
	python3 -m unicodecheck -m NFC -d -v data
	python3 -m unicodecheck -m NFD -d -v data
	python3 -m unicodecheck -m NFKC -d -v data
	python3 -m unicodecheck -m NFKD -d -v data
