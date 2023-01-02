build:
	docker build -t birdnest .
run:
	docker run -p 8000:8000 -it --init birdnest
	