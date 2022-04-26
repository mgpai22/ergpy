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

vacuum:
	make clean
	make uninstall

test1:
	make vacuum
	make build
	make install
	python examples/example_1.py
	make vacuum 