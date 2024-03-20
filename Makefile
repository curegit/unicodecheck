.PHONY: build install devinstall preview publish check format data test testdiff clean

build: clean
	python3 -m build

install: build
	pip3 install .

devinstall: build
	pip3 install -e .[dev]

preview: build
	python3 -m twine upload -u __token__ --repository-url "https://test.pypi.org/legacy/" dist/*

publish: build
	python3 -m twine upload -u __token__ --repository-url "https://upload.pypi.org/legacy/" dist/*

check:
	python3 -m mypy unicodecheck makedata.py

format:
	python3 -m black -l 200 unicodecheck makedata.py

data:
	python3 -c 'import shutil; shutil.rmtree("data", ignore_errors=True)'
	python3 -X dev ./makedata.py

test: data
	python3 -X dev -m unicodecheck -m NFC -v data
	python3 -X dev -m unicodecheck -m NFD -v data
	python3 -X dev -m unicodecheck -m NFKC -v data
	python3 -X dev -m unicodecheck -m NFKD -v data

testdiff: data
	python3 -X dev -m unicodecheck -m NFC -d -v data
	python3 -X dev -m unicodecheck -m NFD -d -v data
	python3 -X dev -m unicodecheck -m NFKC -d -v data
	python3 -X dev -m unicodecheck -m NFKD -d -v data

clean:
	python3 -c 'import shutil; shutil.rmtree("dist", ignore_errors=True)'
	python3 -c 'import shutil; shutil.rmtree("build", ignore_errors=True)'
	python3 -c 'import shutil; shutil.rmtree("unicodecheck.egg-info", ignore_errors=True)'
	python3 -c 'import shutil; shutil.rmtree(".mypy_cache", ignore_errors=True)'
	python3 -c 'import shutil; shutil.rmtree("data", ignore_errors=True)'
