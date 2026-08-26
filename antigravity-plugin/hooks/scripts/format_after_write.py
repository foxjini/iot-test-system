"""파일 저장 후 black으로 자동 포맷하는 훅. black이 없으면 조용히 건너뛴다."""

import subprocess
import sys


def main() -> int:
    if len(sys.argv) < 2 or not sys.argv[1].endswith(".py"):
        return 0
    try:
        subprocess.run(["black", "--quiet", sys.argv[1]], check=False)
    except FileNotFoundError:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
