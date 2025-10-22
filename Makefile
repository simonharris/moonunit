test:
	python -m unittest discover

build:
	docker build -t moonunit .

# check it works
phase:
	docker run -it moonunit python main.py --phase
