#!/usr/bin/env python3
"""
🧠 Purpose:
Automates the packaging and deployment of a multi-stack AWS SAM infrastructure.
This includes:
  - Cognito User Pool with Google OAuth 2.0 integration
  - DynamoDB single-table infrastructure for real-time chat
  - Monitoring Lambdas for application observability

👨‍💻 Author:
Evert Escalante <eescal01>

🔧 Features:
- Validates if the target S3 bucket exists
- Packages each nested stack individually using `sam package`
- Uploads each packaged template to the specified S3 bucket
- Deploys the root SAM stack (`root-stack.yaml`) with parameter injection

🛠️ Command-line Arguments:
--bucket                (Required) S3 bucket used to store packaged templates
--stack-name            (Optional) Name of the root stack (default: cognito-google-auth-stack)
--region                (Optional) AWS region to deploy to (default: us-east-1)
--stage                 (Optional) Deployment stage/environment (dev, qa, prod). Default: dev
--google-client-id      (Required) OAuth 2.0 Client ID from Google Cloud Console
--google-client-secret  (Required) OAuth 2.0 Client Secret from Google Cloud Console

🚀 Example Execution:
```bash
python3 scripts/deploy_stack_root.py \
  --bucket my-deployment-bucket \
  --region us-east-1 \
  --stage dev \
  --google-client-id 1234567890-abc.apps.googleusercontent.com \
  --google-client-secret abcDEFsecretXYZ

"""

import argparse
import subprocess
import sys
import os
from pathlib import Path


def run(cmd, check=True, cwd=None):
    """
    Runs a shell command and prints output.

    Args:
        cmd (list): Command list to execute (e.g., ['sam', 'package', ...])
        check (bool): Whether to raise an error if the command fails.
        cwd (Path or str): Directory to execute the command from.

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
    Checks if the given S3 bucket exists in the specified region.

    Args:
        bucket (str): S3 bucket name
        region (str): AWS region

    Returns:
        bool: True if the bucket exists, False otherwise
    """
    return run(['aws', 's3api', 'head-bucket', '--bucket', bucket, '--region', region], check=False) == 0


def main():
    # --------------------------
    # 🧾 Parse CLI arguments
    # --------------------------
    parser = argparse.ArgumentParser(description="Deploy Cognito + CoreInfra stacks via SAM with nested templates")
    parser.add_argument('--bucket', required=True, help="S3 bucket to upload packaged templates")
    parser.add_argument('--stack-name', default='cognito-google-auth-stack', help="Name of the root stack")
    parser.add_argument('--region', default='us-east-1', help="AWS region to deploy the stack")
    parser.add_argument('--stage', default='dev', help="Deployment stage (e.g. dev, qa, prod)")
    parser.add_argument('--google-client-id', required=True, help="Google OAuth Client ID")
    parser.add_argument('--google-client-secret', required=True, help="Google OAuth Client Secret")
    args = parser.parse_args()

    # --------------------------
    # 🔍 Validate S3 bucket
    # --------------------------
    print(f"🔍 Checking if bucket s3://{args.bucket} exists...")
    if not bucket_exists(args.bucket, args.region):
        print(f"❌ S3 bucket {args.bucket} does not exist or is not accessible.")
        sys.exit(1)

    # --------------------------
    # 🔐 Cognito + Google OAuth
    # --------------------------
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

    # --------------------------
    # 💬 Core DynamoDB Infra
    # --------------------------
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

    # --------------------------
    # 📈 Observability Lambdas
    # --------------------------
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

    # --------------------------
    # 🚀 Deploy root stack
    # --------------------------
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


# Entry point
if __name__ == '__main__':
    main()
