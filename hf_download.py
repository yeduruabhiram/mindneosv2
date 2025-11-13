#!/usr/bin/env python3
"""
Simple Hugging Face downloader utility.

Usage examples (set token first, see README):
  python hf_download.py --repo-id <repo> --filename <file>  # download a single file
  python hf_download.py --repo-id <repo>                    # download entire repo snapshot

This script reads your Hugging Face token from the HF_TOKEN or HUGGINGFACE_HUB_TOKEN
environment variable. Do NOT hardcode tokens in code or commit them.
"""
import argparse
import os
import sys

# Prefer a helpful error when huggingface_hub isn't installed for the Python
# interpreter running this script. This avoids confusion when multiple venvs
# exist.
try:
    from huggingface_hub import hf_hub_download, snapshot_download
except ImportError:
    this_python = sys.executable or 'python'
    print("ERROR: missing dependency 'huggingface_hub' for this Python interpreter:", this_python)
    print("Install it with:")
    print(f"  {this_python} -m pip install huggingface_hub")
    sys.exit(1)


def get_token():
    # Check common env vars
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_HUB_TOKEN")
    return token


def download_file(repo_id, filename, revision=None, repo_type="model", token=None, cache_dir=None):
    print(f"Downloading file '{filename}' from '{repo_id}'...")
    path = hf_hub_download(repo_id=repo_id, filename=filename, repo_type=repo_type, revision=revision, token=token, cache_dir=cache_dir)
    print(f"Downloaded to: {path}")
    return path


def download_snapshot(repo_id, revision=None, repo_type="model", token=None, cache_dir=None):
    print(f"Downloading snapshot of '{repo_id}' (this may take a while)...")
    path = snapshot_download(repo_id=repo_id, repo_type=repo_type, revision=revision, token=token, cache_dir=cache_dir)
    print(f"Snapshot downloaded to: {path}")
    return path


def main():
    parser = argparse.ArgumentParser(description="Download files or full repo snapshot from Hugging Face Hub.")
    parser.add_argument("--repo-id", required=True, help="Repository id on HF, e.g. user/model-name or BigScience/bloom")
    parser.add_argument("--filename", help="Optional: specific filename in the repo to download")
    parser.add_argument("--revision", help="Optional: branch/commit/revision to download (default: main/auto)")
    parser.add_argument("--repo-type", default="model", choices=["model","dataset","space","dataset-search"], help="Repo type (default: model)")
    parser.add_argument("--cache-dir", help="Optional cache dir for huggingface_hub")

    args = parser.parse_args()

    token = get_token()
    if not token:
        print("ERROR: No Hugging Face token found. Set HF_TOKEN or HUGGINGFACE_HUB_TOKEN environment variable.")
        print("See HF_DOWNLOAD_README.md for instructions.")
        sys.exit(2)

    try:
        if args.filename:
            download_file(repo_id=args.repo_id, filename=args.filename, revision=args.revision, repo_type=args.repo_type, token=token, cache_dir=args.cache_dir)
        else:
            download_snapshot(repo_id=args.repo_id, revision=args.revision, repo_type=args.repo_type, token=token, cache_dir=args.cache_dir)
    except Exception as e:
        print(f"Download failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
