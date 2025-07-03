#!/usr/bin/env python3
"""
📦 deploy_layer_stack.py

🧠 Purpose:
Automates the process of building, packaging, and deploying an AWS Lambda Layer
from a Poetry-managed Python project using AWS SAM and S3.

👨‍💻 Maintainer:
Evert Escalante <eescal01>

🔧 Features:
- Verifies S3 bucket and prefix existence
- Exports Python dependencies using Poetry
- Builds a zipped Lambda Layer
- Uploads to S3
- Deploys a SAM stack for the Layer

🚀 Example usage:
python3 scripts/deploy_layer_stack.py \
  --bucket my-bucket-name \
  --stack-name chat-client-layer-dev \
  --region us-east-1 \
  --stage dev \
  --prefix layer-chat-client \
  --template root-layer-stack.yaml
"""

import argparse
import subprocess
import sys
import os
from datetime import datetime

def run(cmd, check=True, cwd=None):
    """
    Runs a shell command and optionally checks for failure.

    Args:
        cmd (list): Command to run (e.g., ['ls', '-la']).
        check (bool): Exit script if command fails.
        cwd (str, optional): Directory to execute the command from.

    Returns:
        int: Exit code of the command.
    """
    print(f"▶️  Executing: {' '.join(cmd)} (cwd={cwd or os.getcwd()})")
    result = subprocess.run(cmd, cwd=cwd)
    if check and result.returncode != 0:
        print("❌ Command failed.")
        sys.exit(result.returncode)
    return result.returncode

def bucket_exists(bucket, region):
    """
    Checks if an S3 bucket exists in the specified region.

    Args:
        bucket (str): Bucket name.
        region (str): AWS region.

    Returns:
        bool: True if the bucket exists.
    """
    return run(['aws', 's3api', 'head-bucket', '--bucket', bucket, '--region', region], check=False) == 0

def s3_prefix_exists(bucket, prefix, region):
    """
    Checks if a folder (prefix) exists in the S3 bucket.

    Args:
        bucket (str): S3 bucket name.
        prefix (str): Folder/prefix to check.
        region (str): AWS region.

    Returns:
        bool: True if prefix contains any objects.
    """
    proc = subprocess.run([
        'aws', 's3api', 'list-objects-v2',
        '--bucket', bucket,
        '--prefix', f"{prefix}/",
        '--region', region
    ], capture_output=True)
    return b'"Key"' in proc.stdout

def create_s3_prefix(bucket, prefix, region):
    """
    Creates an empty S3 object to represent a folder prefix.

    Args:
        bucket (str): Bucket name.
        prefix (str): Folder/prefix to create.
        region (str): AWS region.
    """
    print(f"🟢 Creating S3 folder s3://{bucket}/{prefix}/")
    subprocess.run([
        'aws', 's3api', 'put-object',
        '--bucket', bucket,
        '--key', f"{prefix}/",
        '--region', region
    ])

def build_layer():
    """
    Builds the Lambda Layer:

    - Cleans the previous layer directory
    - Uses Poetry to export dependencies
    - Installs them into a structure compatible with AWS Lambda Layer
    - Creates a ZIP package under /build
    """
    print("🧹 Cleaning previous build...")
    run(["rm", "-rf", "layer"])
    os.makedirs("layer/python", exist_ok=True)

    print("📦 Exporting dependencies with Poetry...")
    run(["poetry", "export", "-f", "requirements.txt", "--output", "requirements.txt", "--without-hashes"])

    print("📚 Installing dependencies into layer/python...")
    run(["python3.10", "-m", "pip", "install", "-r", "requirements.txt", "-t", "layer/python"])

    print("🧳 Zipping layer...")
    os.makedirs("build", exist_ok=True)
    run(["zip", "-r", "../build/chat-client-layer.zip", "."], cwd="layer")

def main():
    """
    Entry point of the script. Handles:

    - Argument parsing
    - Bucket and prefix verification/creation
    - Building the Lambda Layer
    - Packaging and deploying the SAM stack
    """
    parser = argparse.ArgumentParser(description="Build and deploy Lambda Layer from Poetry")
    parser.add_argument('--bucket', required=True, help='S3 bucket to upload the layer ZIP and templates')
    parser.add_argument('--stack-name', required=True, help='Name of the deployed SAM stack')
    parser.add_argument('--region', default='us-east-1', help='AWS region to deploy in')
    parser.add_argument('--stage', default='dev', help='Deployment stage (e.g., dev, qa, prod)')
    parser.add_argument('--prefix', default='layer-chat-client', help='S3 prefix for storing layer artifacts')
    parser.add_argument('--template', default='root-layer-stack.yaml', help='SAM template file path')
    args = parser.parse_args()

    print(f"🔍 Checking bucket s3://{args.bucket} in {args.region}...")
    if not bucket_exists(args.bucket, args.region):
        print(f"❌ Error: bucket {args.bucket} does not exist or is inaccessible.")
        sys.exit(1)

    if not s3_prefix_exists(args.bucket, args.prefix, args.region):
        create_s3_prefix(args.bucket, args.prefix, args.region)
    else:
        print(f"✅ S3 folder s3://{args.bucket}/{args.prefix}/ already exists.")

    build_layer()

    print("📦 Packaging with SAM...")
    run([
        'sam', 'package',
        '--template-file', args.template,
        '--s3-bucket', args.bucket,
        '--output-template-file', 'packaged-template.yaml',
        '--region', args.region,
        '--s3-prefix', args.prefix
    ])

    print(f"🚀 Deploying stack {args.stack_name}...")
    run([
        'sam', 'deploy',
        '--template-file', 'packaged-template.yaml',
        '--stack-name', args.stack_name,
        '--capabilities', 'CAPABILITY_IAM',
        '--region', args.region,
        '--parameter-overrides', f'Stage={args.stage} DeploymentBucket={args.bucket}'
    ])

    print("✅ Deployment completed successfully.")

if __name__ == '__main__':
    main()
