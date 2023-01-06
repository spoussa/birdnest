IMAGE=birdnest
HUB=docker.io
TAG=latest
USER=santeripoussa

build:
	docker build -t ${IMAGE}:${TAG} .
run:
	docker run -p 8000:8000 -it --init ${IMAGE}:${TAG}
tag: 
	docker tag ${IMAGE}:${TAG} ${HUB}/${USER}/${IMAGE}:${TAG}
push:
	docker push ${HUB}/${USER}/${IMAGE}:${TAG}
apply:
	kubectl apply -f compose.yaml
delete:
	kubectl delete -f compose.yaml