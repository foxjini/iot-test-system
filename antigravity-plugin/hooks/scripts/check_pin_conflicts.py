"""sensors/, actuators/ 안에서 쓰인 GPIO 핀 번호를 모아 중복을 경고한다.

정규식 기반 휴리스틱 스캔이다 (변수로 핀 번호를 넘기는 경우는 잡아내지 못하고,
관련 없는 숫자를 핀으로 오인할 수도 있다) — 참고용으로만 쓴다.
"""

import re
import sys
from pathlib import Path

PIN_PATTERN = re.compile(r"\b(?:pin|trigger|echo)\s*=\s*(\d{1,2})\b|\((\d{1,2})\)")


def scan(base: Path) -> dict[int, list[str]]:
    pins: dict[int, list[str]] = {}
    for folder in ("sensors", "actuators"):
        folder_path = base / folder
        if not folder_path.exists():
            continue
        for file in folder_path.glob("*.py"):
            text = file.read_text(encoding="utf-8")
            for match in PIN_PATTERN.finditer(text):
                pin = int(match.group(1) or match.group(2))
                pins.setdefault(pin, []).append(str(file))
    return pins


def main() -> int:
    pins = scan(Path.cwd())
    conflicts = {pin: files for pin, files in pins.items() if len(set(files)) > 1}
    if conflicts:
        print("[핀 중복 경고] 같은 핀 번호가 여러 파일에서 발견되었습니다 (오탐일 수 있음):")
        for pin, files in conflicts.items():
            print(f"  GPIO{pin}: {', '.join(sorted(set(files)))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
