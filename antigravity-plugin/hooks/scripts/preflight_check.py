"""실행 전 .env 존재 여부를 점검하는 사전 훅."""

import sys
from pathlib import Path


def main() -> int:
    env_path = Path.cwd() / ".env"
    if not env_path.exists():
        print("[사전 점검] .env 파일이 없습니다. .env.example을 복사해서 만든 뒤 값을 채워주세요.")
        return 1
    print("[사전 점검] .env 확인됨.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
