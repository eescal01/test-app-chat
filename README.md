Aquí tienes un **README profesional y completo en inglés** que documenta tu arquitectura, propósito de cada stack, y cómo desplegar paso a paso cada uno de ellos:

---

# 🧠 Serverless Chat Architecture with Google OAuth & Observability

This repository implements a modular and scalable **serverless architecture** using AWS SAM (Serverless Application Model). It provides:

* 🔐 **Passwordless login** using **Google OAuth 2.0** via Amazon Cognito
* 💬 A **DynamoDB-based real-time chat infrastructure**
* 🧪 A **test Lambda function** to verify deployments
* 📊 Optionally, monitoring Lambdas for observability (Vault, Chatwoot, SES)

---

## 📐 Architecture Overview

```
                                        ┌────────────────────┐
                                        │   Google Identity  │
                                        └─────────┬──────────┘
                                                  │
                                        🔐 Google OAuth 2.0
                                                  │
                                        ┌─────────▼──────────┐
                                        │   Amazon Cognito   │
                                        │ UserPool + AppClient│
                                        └─────────┬──────────┘
                                                  │
                                ┌─────────────────▼─────────────────┐
                                │  App frontend (e.g. Amplify/Web)  │
                                └─────────────────┬─────────────────┘
                                                  │ Auth tokens (JWT)
                     ┌────────────────────────────▼────────────────────────────┐
                     │                   API Gateway (optional)                │
                     └────────────────────────────┬────────────────────────────┘
                                                  │
                             ┌────────────────────▼────────────────────┐
                             │         Lambda Functions (Chat)         │
                             │        (Custom or test Lambda)          │
                             └────────────────────┬────────────────────┘
                                                  │
                                        ┌─────────▼─────────┐
                                        │   DynamoDB Table   │
                                        └────────────────────┘
                                                  │
                                       🧱 Single-table design

```

---

## 📁 Stack Components

| Stack Name                 | Description                                                            |
| -------------------------- | ---------------------------------------------------------------------- |
| **CognitoGoogleAuthStack** | Sets up Cognito User Pool, Google OAuth IdP, App Client, and Hosted UI |
| **CoreInfraStack**         | Creates the base DynamoDB table and scalable chat infrastructure       |
| **LambdaStack**            | Deploys monitoring Lambdas (optional for observability only)           |
| **TestLambdaStack**        | Deploys a test Lambda to validate the pipeline                         |
| **LayerStack**             | Builds and deploys a Python Lambda Layer with async chat client        |
| **Root Stack**             | Orchestrates all nested stacks for production deployment               |

---

## 🚀 Deployment Instructions

### ⚙️ Prerequisites

* Python 3.10+
* Poetry (`curl -sSL https://install.python-poetry.org | python3.10 -`)
* AWS CLI configured (`aws configure`)
* SAM CLI (`brew install aws/tap/aws-sam-cli`)
* A valid **Google OAuth Client ID/Secret**
* An **S3 Bucket** to upload packaged templates

---

### 🧪 1. Deploy Test Lambda (Optional)

To verify your deployment pipeline:

```bash
cd services/lambdas
sam deploy --template-file nested-lambdas-stack.yaml \
  --stack-name test-lambda-stack-dev \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides Stage=dev
```

---

### 🔐 2. Package & Upload Cognito + CoreInfra

Use the provided script to automatically package and upload stacks to S3:

```bash
python3 scripts/deploy_stack_root.py \
  --bucket your-bucket-name \
  --region us-east-1 \
  --google-client-id YOUR_GOOGLE_CLIENT_ID \
  --google-client-secret YOUR_GOOGLE_CLIENT_SECRET
```

What this script does:

* 📦 Packages and uploads:

  * Cognito stack (Google OAuth + UserPool)
  * Core infrastructure (DynamoDB, backend setup)
  * Monitoring Lambdas (if needed)
* 🚀 Deploys the **root stack** with nested stack references

---

### 📦 3. Deploy Lambda Layer (Chat client)

Use the following script to build a Python Lambda Layer and deploy it:

```bash
python3 scripts/deploy_layer_stack.py \
  --bucket your-bucket-name \
  --stack-name layer-chat-lambda \
  --stage dev
```

It will:

* Clean and zip your Python dependencies using Poetry
* Package the `root-layer-stack.yaml` template
* Deploy the layer as a stack for use in your Lambda functions

---

## 🧾 Project Structure

```
.
├── root-stack.yaml                # Root orchestrator stack
├── root-layer-stack.yaml         # Deploys the Lambda Layer
├── services/
│   ├── cognito/                  # Cognito + Google IdP
│   ├── core-infra/               # DynamoDB and backend infra
│   └── lambdas/                  # Lambdas (test or observability)
├── scripts/
│   ├── deploy_stack_root.py      # Packages & deploys main stacks
│   └── deploy_layer_stack.py     # Builds & deploys Lambda Layer
├── docker-compose.yml            # Builds layer in Docker env
├── Dockerfile                    # Lambda Layer build environment
└── Makefile                      # Build automation
```

---

## ✅ Result

Once deployed, you will have:

* A working Cognito login with Google (passwordless)
* A DynamoDB backend ready to support real-time chat
* The ability to reuse the chat layer in any Lambda
* Optional test Lambda to validate runtime setup

---

## 📎 Sample Cognito Login URL

```text
https://your-domain.auth.us-east-1.amazoncognito.com/login?
  response_type=code&
  client_id=xxxxxxxxxx&
  redirect_uri=https://yourapp/callback
```

Replace `your-domain`, `client_id`, and `redirect_uri` with values from `Outputs`.

---

Let me know if you want this in Markdown file format or need CI/CD setup for GitHub Actions too.
