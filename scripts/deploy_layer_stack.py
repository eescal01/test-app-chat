#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os
from datetime import datetime

def run(cmd, check=True, cwd=None):
    print(f"▶️  Executing: {' '.join(cmd)} (cwd={cwd or os.getcwd()})")
    result = subprocess.run(cmd, cwd=cwd)
    if check and result.returncode != 0:
        sys.exit(result.returncode)
    return result.returncode

def bucket_exists(bucket, region):
    return run(['aws', 's3api', 'head-bucket', '--bucket', bucket, '--region', region], check=False) == 0

def s3_prefix_exists(bucket, prefix, region):
    proc = subprocess.run([
        'aws', 's3api', 'list-objects-v2',
        '--bucket', bucket,
        '--prefix', f"{prefix}/",
        '--region', region
    ], capture_output=True)
    return b'"Key"' in proc.stdout

def create_s3_prefix(bucket, prefix, region):
    print(f"🟢 Creating S3 folder s3://{bucket}/{prefix}/")
    subprocess.run([
        'aws', 's3api', 'put-object',
        '--bucket', bucket,
        '--key', f"{prefix}/",
        '--region', region
    ])

def build_layer():
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
    parser = argparse.ArgumentParser(description="Build and deploy Lambda Layer from Poetry")
    parser.add_argument('--bucket', required=True, help='S3 bucket to upload layer')
    parser.add_argument('--stack-name', required=True, help='Name of the deployed SAM stack')
    parser.add_argument('--region', default='us-east-1', help='AWS region')
    parser.add_argument('--stage', default='dev', help='Deployment stage')
    parser.add_argument('--prefix', default='layer-chat-client', help='S3 prefix/folder for Layer objects')
    parser.add_argument('--template', default='root-layer-stack.yaml', help='Path to SAM template')
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
