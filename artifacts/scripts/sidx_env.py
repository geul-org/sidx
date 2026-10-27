"""sidx 루트의 .env에서 설정값을 읽는다.

환경변수에 이미 있으면 그 값을 쓰고, 없으면 저장소 루트의 .env(KEY=VALUE 줄)에서 찾는다.
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = ROOT / ".env"


def env(key):
    """key의 값. 환경변수 → .env 순으로 찾고, 없으면 종료한다."""
    if key in os.environ:
        return os.environ[key]
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            k, sep, v = line.strip().partition("=")
            if sep and not k.startswith("#") and k.strip() == key:
                return v.strip().strip('"').strip("'")
    raise SystemExit(f"{key}가 없다: {ENV_FILE}에 적는다(.env.example 참고)")
