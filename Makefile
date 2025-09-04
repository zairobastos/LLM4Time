.PHONY: clean build check upload upload-test docs docs-serve clean-docs all

clean:
	rm -rf build/ dist/ *.egg-info/
	rm -rf docs/build/

build: clean
	python -m build

check: build
	twine check dist/*

upload-test: check
	twine upload --repository testpypi dist/*

upload: check
	twine upload dist/*

docs: clean-docs
	cd docs && make html

docs-serve: docs
	cd docs/build/html && python -m http.server 8000

clean-docs:
	rm -rf docs/build/
	rm -f docs/source/llm4time*.rst
	rm -f docs/source/modules.rst

all: docs upload
