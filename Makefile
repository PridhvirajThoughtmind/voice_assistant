# Variables
IMAGE_NAME = voice-assistant
CONTAINER_NAME = voice-assistant
PORT = 8000

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Start the container with hot reload
up:
	docker run -d \
        --name $(CONTAINER_NAME) \
        -p $(PORT):$(PORT) \
        -v $(PWD)/app:/app/app \
        -v $(PWD)/vosk-model:/app/vosk-model \
        -v $(PWD)/.env:/app/.env \
        $(IMAGE_NAME)

# Stop the container
down:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

# Clean up images and containers
clean:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
	docker rmi $(IMAGE_NAME) || true

# Rebuild and restart
restart: down build up

# Show container logs
logs:
	docker logs -f $(CONTAINER_NAME)

.PHONY: build up down clean restart logs