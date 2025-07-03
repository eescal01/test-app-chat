#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os
from pathlib import Path


def run(cmd, check=True, cwd=None):
    print(f"▶️  Executing: {' '.join(cmd)} (cwd={cwd or os.getcwd()})")
    result = subprocess.run(cmd, cwd=cwd)
    if check and result.returncode != 0:
        print("❌ Command failed.")
        sys.exit(result.returncode)
    return result.returncode


def bucket_exists(bucket, region):
    return run(['aws', 's3api', 'head-bucket', '--bucket', bucket, '--region', region], check=False) == 0


def main():
    parser = argparse.ArgumentParser(description="Deploy Cognito + CoreInfra stacks via SAM with nested templates")
    parser.add_argument('--bucket', required=True)
    parser.add_argument('--stack-name', default='cognito-google-auth-stack')
    parser.add_argument('--region', default='us-east-1')
    parser.add_argument('--stage', default='dev')
    parser.add_argument('--google-client-id', required=True)
    parser.add_argument('--google-client-secret', required=True)
    args = parser.parse_args()

    print(f"🔍 Checking if bucket s3://{args.bucket} exists...")
    if not bucket_exists(args.bucket, args.region):
        print(f"❌ S3 bucket {args.bucket} does not exist or is not accessible.")
        sys.exit(1)

    # 🧩 Cognito
    cognito_dir = Path("services/cognito")
    run([
        'sam', 'package',
        '--template-file', 'nested-cognito-google-auth-stack.yaml',
        '--output-template-file', 'nested-cognito-google-auth-stack-packaged.yaml',
        '--s3-bucket', args.bucket,
        '--region', args.region,
        '--s3-prefix', 'services/cognito'
    ], cwd=cognito_dir)
    run([
        'aws', 's3', 'cp',
        'nested-cognito-google-auth-stack-packaged.yaml',
        f's3://{args.bucket}/services/cognito/nested-cognito-google-auth-stack.yaml',
        '--region', args.region
    ], cwd=cognito_dir)

    # 🧱 CoreInfra
    coreinfra_dir = Path("services/core-infra")
    run([
        'sam', 'package',
        '--template-file', 'core-infra.yaml',
        '--output-template-file', 'core-infra-packaged.yaml',
        '--s3-bucket', args.bucket,
        '--region', args.region,
        '--s3-prefix', 'services/core-infra'
    ], cwd=coreinfra_dir)
    run([
        'aws', 's3', 'cp',
        'core-infra-packaged.yaml',
        f's3://{args.bucket}/services/core-infra/core-infra.yaml',
        '--region', args.region
    ], cwd=coreinfra_dir)

    # 📈 Monitor Lambdas (solo package + upload, no parámetros en root)
    monitor_dir = Path("services/lambdas")
    run([
        'sam', 'package',
        '--template-file', 'nested-lambdas-stack.yaml',
        '--output-template-file', 'nested-lambdas-stack-packaged.yaml',
        '--s3-bucket', args.bucket,
        '--region', args.region,
        '--s3-prefix', 'services/lambdas'
    ], cwd=monitor_dir)
    run([
        'aws', 's3', 'cp',
        'nested-lambdas-stack-packaged.yaml',
        f's3://{args.bucket}/services/lambdas/nested-lambdas-stack.yaml',
        '--region', args.region
    ], cwd=monitor_dir)

    # 🚀 Root stack deployment
    run([
        'sam', 'package',
        '--template-file', 'root-stack.yaml',
        '--s3-bucket', args.bucket,
        '--output-template-file', 'packaged-root.yaml',
        '--region', args.region
    ])
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

    print("✅ All stacks deployed successfully.")


if __name__ == '__main__':
    main()
