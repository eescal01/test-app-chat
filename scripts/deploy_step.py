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
    parser = argparse.ArgumentParser(description="Deploy Cognito + CoreInfra stacks via SAM with nested templates")
    parser.add_argument('--bucket', required=True, help='S3 bucket to upload nested templates')
    parser.add_argument('--stack-name', default='cognito-google-auth-stack', help='Root stack name')
    parser.add_argument('--region', default='us-east-1', help='AWS region')
    parser.add_argument('--stage', default='dev', help='Deployment stage (dev, qa, prod)')
    parser.add_argument('--google-client-id', required=True, help='OAuth Client ID from Google')
    parser.add_argument('--google-client-secret', required=True, help='OAuth Client Secret from Google')
    args = parser.parse_args()

    print(f"🔍 Checking if bucket s3://{args.bucket} exists...")
    if not bucket_exists(args.bucket, args.region):
        print(f"❌ S3 bucket {args.bucket} does not exist or is not accessible.")
        sys.exit(1)

    # --------------------------------------------
    # 🧩 Cognito nested stack
    # --------------------------------------------
    cognito_dir = Path("services/cognito")
    cognito_template = cognito_dir / "nested-cognito-google-auth-stack.yaml"
    cognito_packaged = cognito_dir / "nested-cognito-google-auth-stack-packaged.yaml"
    cognito_s3_prefix = "services/cognito"

    print(f"📦 Packaging nested Cognito stack: {cognito_template}")
    run([
        'sam', 'package',
        '--template-file', cognito_template.name,
        '--output-template-file', cognito_packaged.name,
        '--s3-bucket', args.bucket,
        '--region', args.region,
        '--s3-prefix', cognito_s3_prefix
    ], cwd=cognito_dir)

    print(f"📤 Uploading nested Cognito template to S3: {cognito_packaged}")
    run([
        'aws', 's3', 'cp',
        str(cognito_packaged),
        f's3://{args.bucket}/{cognito_s3_prefix}/nested-cognito-google-auth-stack.yaml',
        '--region', args.region
    ])

    # --------------------------------------------
    # 🧱 Core Infrastructure nested stack (DynamoDB)
    # --------------------------------------------
    coreinfra_dir = Path("services/core-infra")
    coreinfra_template = coreinfra_dir / "core-infra.yaml"
    coreinfra_packaged = coreinfra_dir / "core-infra-packaged.yaml"
    coreinfra_s3_prefix = "services/core-infra"

    print(f"📦 Packaging nested CoreInfra stack: {coreinfra_template}")
    run([
        'sam', 'package',
        '--template-file', coreinfra_template.name,
        '--output-template-file', coreinfra_packaged.name,
        '--s3-bucket', args.bucket,
        '--region', args.region,
        '--s3-prefix', coreinfra_s3_prefix
    ], cwd=coreinfra_dir)

    print(f"📤 Uploading nested CoreInfra template to S3: {coreinfra_packaged}")
    run([
        'aws', 's3', 'cp',
        str(coreinfra_packaged),
        f's3://{args.bucket}/{coreinfra_s3_prefix}/core-infra.yaml',
        '--region', args.region
    ])

    # --------------------------------------------
    # 🚀 Package and deploy root stack
    # --------------------------------------------
    print("📦 Packaging root stack...")
    run([
        'sam', 'package',
        '--template-file', 'root-stack.yaml',
        '--s3-bucket', args.bucket,
        '--output-template-file', 'packaged-root.yaml',
        '--region', args.region
    ])

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

    print("✅ Cognito + CoreInfra stacks deployed successfully.")


if __name__ == '__main__':
    main()
