# ------------------------------------------------------------------
# Makefile for Google OAuth 2.0 + Cognito SAM Stack
# Author: Emmanuel Palacio Gaviria (@SixTanDev)
# ------------------------------------------------------------------

PYTHON=python3.10
LAYER_NAME=chat-client-layer
BUILD_DIR=build
LAYER_DIR=layer/python
PROJECT_NAME=auth-google
TEMPLATE=root-stack.yaml
REGION=us-east-1
BUCKET?=auth-e-google-artifacts-dev
STACK_NAME?=auth-google-root-dev
STAGE?=dev

# ------------------------------------------------------------------
# ⚙️ SAM Deployment and Teardown Commands
# ------------------------------------------------------------------

## 📦 Package and deploy the stack using AWS SAM
deploy:
ifeq ($(strip $(BUCKET)),)
	$(error BUCKET is not defined. Usage: make deploy BUCKET=<bucket-name>)
endif
	@echo "🚀 Packaging and deploying stack $(STACK_NAME)..."
	sam package \
		--template-file $(TEMPLATE) \
		--s3-bucket $(BUCKET) \
		--output-template-file packaged.yaml
	sam deploy \
		--template-file packaged.yaml \
		--stack-name $(STACK_NAME) \
		--capabilities CAPABILITY_IAM \
		--region $(REGION)
	@echo "✅ Stack successfully deployed."

## 💣 Delete the deployed stack completely
delete:
	@echo "⚠️  Deleting stack $(STACK_NAME) in region $(REGION)..."
	sam delete \
		--stack-name $(STACK_NAME) \
		--region $(REGION) \
		--no-prompts
	@echo "✅ Stack deleted."

# ------------------------------------------------------------------
# ☁️ S3 Bucket Utilities
# ------------------------------------------------------------------

## 🪣 Create S3 bucket for SAM deployment
s3-create:
ifeq ($(strip $(BUCKET)),)
	$(error BUCKET is not defined. Usage: make s3-create BUCKET=<bucket-name>)
endif
	aws s3 mb s3://$(BUCKET) --region $(REGION)
	@echo "✅ Bucket s3://$(BUCKET) created."

## 🧼 Empty contents of the bucket
s3-empty:
ifeq ($(strip $(BUCKET)),)
	$(error BUCKET is not defined. Usage: make s3-empty BUCKET=<bucket-name>)
endif
	aws s3 rm s3://$(BUCKET) --recursive --region $(REGION)
	@echo "🗑️  Bucket s3://$(BUCKET) emptied."

## ❌ Fully delete the S3 bucket
s3-delete:
ifeq ($(strip $(BUCKET)),)
	$(error BUCKET is not defined. Usage: make s3-delete BUCKET=<bucket-name>)
endif
	aws s3 rb s3://$(BUCKET) --force --region $(REGION)
	@echo "✅ Bucket s3://$(BUCKET) deleted."

# ------------------------------------------------------------------
# 🧭 Help
# ------------------------------------------------------------------

help:
	@echo ""
	@echo "🛠️  Available Makefile commands for $(PROJECT_NAME):"
	@echo ""
	@echo "📦 deploy        – Package and deploy stack via AWS SAM"
	@echo "   usage: make deploy BUCKET=<bucket-name>"
	@echo ""
	@echo "💣 delete        – Delete the deployed SAM stack"
	@echo ""
	@echo "🪣 s3-create     – Create S3 bucket for SAM artifacts"
	@echo "   usage: make s3-create BUCKET=<bucket-name>"
	@echo ""
	@echo "🧼 s3-empty      – Empty S3 bucket"
	@echo "   usage: make s3-empty BUCKET=<bucket-name>"
	@echo ""
	@echo "❌ s3-delete     – Delete S3 bucket"
	@echo "   usage: make s3-delete BUCKET=<bucket-name>"
	@echo ""

## 📦 Export dependencies using Poetry to requirements.txt
export_requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

## 📚 Install Python dependencies into the layer directory
install_dependencies:
	$(PYTHON) -m pip install -r requirements.txt -t $(LAYER_DIR)

## 🧳 Build the final ZIP layer ready for AWS Lambda
build_layer:
	mkdir -p $(BUILD_DIR)
	cd layer && zip -r ../$(BUILD_DIR)/$(LAYER_NAME).zip .

all:
	@echo "✅ Starting full pipeline using Poetry..."
	$(MAKE) export_requirements
	$(MAKE) install_dependencies
	$(MAKE) build_layer

# ------------------------------------------------------------------
# 🐳 Docker Build Helpers
# ------------------------------------------------------------------

docker-build:
	docker build -t kuma-layer-builder .

docker-all:
	docker run --rm -v "$$(pwd)":/app -w /app kuma-layer-builder make all

docker-compose-all:
	docker-compose build
	docker-compose run --rm layer-builder make all

docker-compose-clean-build:
	docker-compose build --no-cache
	docker-compose run --rm layer-builder make all

# 🧹 Clean all packaged templates
clean-packaged:
	@echo "🧹 Removing packaged YAML templates..."
	find . -type f -name "*-packaged.yaml" -exec rm -v {} \;
	@echo "✅ Done: All packaged templates have been removed."


.PHONY: deploy delete s3-create s3-empty s3-delete help all clean \
	docker-build docker-all docker-compose-all docker-compose-clean-build clean-packaged
