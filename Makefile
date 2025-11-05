APP_NAME ?= hotel-bookings-guard
IMAGE_TAG ?= latest
CONTAINER_NAME ?= $(APP_NAME)-container


build:
	docker build -t $(APP_NAME):$(IMAGE_TAG) .

run:
	docker run --rm -it \
		--name $(CONTAINER_NAME) \
		-p 8000:8000 \
		$(APP_NAME):$(IMAGE_TAG)

stop:
	docker stop $(CONTAINER_NAME) || true

clean:
	docker rm -f $(CONTAINER_NAME) || true

rebuild: clean build run