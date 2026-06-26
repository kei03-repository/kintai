import hashlib
import os
from pathlib import Path
from typing import Tuple
import boto3

_S3_ARN_PREFIX = "arn:aws:s3:::"


def _split_bucket_and_key(raw: str) -> Tuple[str, str]:
    if "/" not in raw:
        raise ValueError("S3 source must include object key")
    bucket, key = raw.split("/", 1)
    normalized_key = key.lstrip("/")
    if not bucket or not normalized_key:
        raise ValueError("S3 source must include both bucket and key")
    return bucket, normalized_key


def _parse_s3_source(source: str) -> Tuple[str, str]:
    if source.startswith("s3://"):
        return _split_bucket_and_key(source[len("s3://"):])

    if source.startswith(_S3_ARN_PREFIX):
        return _split_bucket_and_key(source[len(_S3_ARN_PREFIX):])

    raise ValueError(f"Unsupported template source: {source}")


def is_s3_source(source: str) -> bool:
    return source.startswith("s3://") or source.startswith(_S3_ARN_PREFIX)


def resolve_template_path(template_source: str) -> Path:
    if not is_s3_source(template_source):
        return Path(template_source)

    bucket, key = _parse_s3_source(template_source)
    cache_dir = Path(os.getenv("TEMPLATE_CACHE_DIR", "/tmp/template_cache"))
    cache_dir.mkdir(parents=True, exist_ok=True)

    file_hash = hashlib.sha256(template_source.encode("utf-8")).hexdigest()[:16]
    extension = Path(key).suffix or ".xlsx"
    cached_file = cache_dir / f"template_{file_hash}{extension}"

    if not cached_file.exists():
        s3 = boto3.client("s3")
        s3.download_file(bucket, key, str(cached_file))

    return cached_file
