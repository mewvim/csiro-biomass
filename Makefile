SHELL := /bin/bash
DD := docker

# Version management - pulled from pyproject.toml
DOCKER_HUB_USERNAME := mewvim
VERSION := $(shell grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
IMAGE_NAME := $(DOCKER_HUB_USERNAME)/csiro-biomass

# build version image
.PHONY: build-image-version
build-image-version:
	$(DD) build -t $(IMAGE_NAME):$(VERSION) -t $(IMAGE_NAME):$(VERSION) .
	@echo "Built image: $(IMAGE_NAME):$(VERSION)"

.PHONY: build-image-latest
build-image-latest:
	$(DD) build -t $(IMAGE_NAME):$(VERSION) -t $(IMAGE_NAME):latest .
	@echo "Built image: $(IMAGE_NAME):latest"

build-image: build-image-version build-image-latest

# publish to docker hub
.PHONY: publish-image
publish-image:
	$(DD) push $(IMAGE_NAME):$(VERSION)
	$(DD) push $(IMAGE_NAME):latest
	@echo "Published image $(VERSION) and latest"

# download data to local
.PHONY: download-version
download-version:
	@echo "downloading dataset"
	$(DD) run -d --rm --name download $(IMAGE_NAME):$(VERSION) \
		dataset --download datasetname

.PHONY: download-latest
download-latest:
	$(DD) run -d --rm --name download $(IMAGE_NAME):latest \
		dataset --download datasetname

