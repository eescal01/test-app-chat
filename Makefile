# ------------------------------------------------------------------
# Makefile for Google OAuth 2.0 + Cognito SAM Stack
# Author: Emmanuel Palacio Gaviria (@SixTanDev)
# ------------------------------------------------------------------

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

.PHONY: deploy delete s3-create s3-empty s3-delete help
