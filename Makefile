build:
	python -m pip install --upgrade build
	python -m build 

clean:
	rm -rf ./dist
	rm -rf ./ergpy.egg-info

install:
	python -m pip install ./dist/ergpy-0.1.1.tar.gz

uninstall:
	python -m pip uninstall ergpy