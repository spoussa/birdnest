build:
	docker build -t birdnest .
run:
	docker run -it --init birdnest
	