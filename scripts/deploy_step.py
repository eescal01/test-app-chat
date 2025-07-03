#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os
from pathlib import Path


def run(cmd, check=True, cwd=None):
    """Run a subprocess command and optionally exit on failure"""
    print(f"▶️  Executing: {' '.join(cmd)} (cwd={cwd or os.getcwd()})")
    result = subprocess.run(cmd, cwd=cwd)
    if check and result.returncode != 0:
        print("❌ Command failed.")
        sys.exit(result.returncode)
    return result.returncode


def bucket_exists(bucket, region):
    """Check if the S3 bucket exists in the specified region"""
    return run(['aws', 's3api', 'head-bucket', '--bucket', bucket, '--region', region], check=False) == 0


def main():
    parser = argparse.ArgumentParser(description="Deploy Cognito Google OAuth stack via SAM with nested templates")
    parser.add_argument('--bucket', required=True, help='S3 bucket to upload nested templates')
    parser.add_argument('--stack-name', default='cognito-google-auth-stack', help='Root stack name')
    parser.add_argument('--region', default='us-east-1', help='AWS region')
    parser.add_argument('--stage', default='dev', help='Deployment stage (dev, qa, prod)')
    parser.add_argument('--google-client-id', required=True, help='OAuth Client ID from Google')
    parser.add_argument('--google-client-secret', required=True, help='OAuth Client Secret from Google')
    args = parser.parse_args()

    # Define paths
    nested_dir = Path("services/cognito")
    nested_template = nested_dir / "nested-cognito-google-auth-stack.yaml"
    packaged_template = nested_dir / "nested-cognito-google-auth-stack-packaged.yaml"
    nested_s3_prefix = "services/cognito"

    print(f"🔍 Checking if bucket s3://{args.bucket} exists...")
    if not bucket_exists(args.bucket, args.region):
        print(f"❌ S3 bucket {args.bucket} does not exist or is not accessible.")
        sys.exit(1)

    # Package nested stack
    print(f"📦 Packaging nested Cognito stack: {nested_template}")
    run([
        'sam', 'package',
        '--template-file', nested_template.name,
        '--output-template-file', packaged_template.name,
        '--s3-bucket', args.bucket,
        '--region', args.region,
        '--s3-prefix', nested_s3_prefix
    ], cwd=nested_dir)

    # Upload packaged nested stack to S3
    print(f"📤 Uploading nested Cognito template to S3: {packaged_template}")
    run([
        'aws', 's3', 'cp',
        str(packaged_template),
        f's3://{args.bucket}/{nested_s3_prefix}/nested-cognito-google-auth-stack.yaml',
        '--region', args.region
    ])

    # Package root stack
    print("📦 Packaging root stack...")
    run([
        'sam', 'package',
        '--template-file', 'root-stack.yaml',
        '--s3-bucket', args.bucket,
        '--output-template-file', 'packaged-root.yaml',
        '--region', args.region
    ])

    # Deploy root stack
    print(f"🚀 Deploying root stack: {args.stack_name}")
    run([
        'sam', 'deploy',
        '--template-file', 'packaged-root.yaml',
        '--stack-name', args.stack_name,
        '--capabilities', 'CAPABILITY_IAM', 'CAPABILITY_AUTO_EXPAND', 'CAPABILITY_NAMED_IAM',
        '--region', args.region,
        '--parameter-overrides',
        f"Stage={args.stage} DeploymentBucket={args.bucket} "
        f"GoogleClientId={args.google_client_id} GoogleClientSecret={args.google_client_secret}"
    ])

    print("✅ Cognito + Google OAuth stack deployed successfully.")


if __name__ == '__main__':
    main()
