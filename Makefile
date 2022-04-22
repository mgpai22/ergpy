build:
	python -m pip install --upgrade build
	python -m build 

clean:
	rm -rf ./dist
	rm -rf ./ergpy.egg-info

install:
	python -m pip install -e .

uninstall:
	python -m pip uninstall ergpy --yes