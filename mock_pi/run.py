"""라즈베리파이 5를 대신하는 Mock 클라이언트.

백엔드에 등록된 컴포넌트 목록을 그대로 읽어와 동작하므로, 대시보드에서 팀이
센서/액추에이터 구성을 바꾸면 이 스크립트를 재시작할 필요 없이 자동으로 맞춰진다
(SYNC_INTERVAL_SEC 주기로 재조회).

사용법 (mock_pi 디렉토리에서):
    python run.py --device-id 1 --api-key <디바이스 등록 시 발급된 키>
  또는 .env에 BACKEND_URL/DEVICE_ID/API_KEY를 채워두고:
    python run.py
"""

import argparse
import os
import threading
import time

from dotenv import load_dotenv

from actuators import APPLIERS
from client import BackendClient
from sensors import GENERATORS

load_dotenv()


def _int_env(name: str) -> int | None:
    val = os.environ.get(name)
    return int(val) if val else None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="IoT 테스트 시스템 - Mock 라즈베리파이 클라이언트")
    parser.add_argument("--backend-url", default=os.environ.get("BACKEND_URL", "http://127.0.0.1:8000"))
    parser.add_argument("--device-id", type=int, default=_int_env("DEVICE_ID"))
    parser.add_argument("--api-key", default=os.environ.get("API_KEY"))
    parser.add_argument("--push-interval", type=float, default=float(os.environ.get("PUSH_INTERVAL_SEC", 2)))
    parser.add_argument("--poll-interval", type=float, default=float(os.environ.get("POLL_INTERVAL_SEC", 2)))
    parser.add_argument(
        "--heartbeat-interval", type=float, default=float(os.environ.get("HEARTBEAT_INTERVAL_SEC", 5))
    )
    parser.add_argument(
        "--sync-interval", type=float, default=float(os.environ.get("COMPONENT_SYNC_INTERVAL_SEC", 15))
    )
    args = parser.parse_args()
    if args.device_id is None or not args.api_key:
        parser.error("--device-id/--api-key 가 필요합니다 (또는 .env의 DEVICE_ID/API_KEY).")
    return args


class MockDevice:
    def __init__(self, client: BackendClient):
        self.client = client
        self._lock = threading.Lock()
        self._components: list[dict] = []

    def sync_components(self) -> None:
        components = self.client.list_components()
        with self._lock:
            self._components = components
        labels = ", ".join(f"{c['label']}({c['type_key']})" for c in components) or "(없음)"
        print(f"[동기화] 등록된 컴포넌트 {len(components)}개: {labels}")

    def sensors(self) -> list[dict]:
        with self._lock:
            return [c for c in self._components if c["category"] == "sensor"]

    def actuators_by_id(self) -> dict[int, dict]:
        with self._lock:
            return {c["id"]: c for c in self._components if c["category"] == "actuator"}


def sync_loop(device: MockDevice, interval: float, stop: threading.Event) -> None:
    while not stop.is_set():
        try:
            device.sync_components()
        except Exception as exc:  # noqa: BLE001 - 목업은 계속 재시도하며 계속 돈다
            print(f"[동기화 오류] {exc}")
        stop.wait(interval)


def sensor_loop(device: MockDevice, interval: float, stop: threading.Event) -> None:
    while not stop.is_set():
        items = []
        for comp in device.sensors():
            gen = GENERATORS.get(comp["type_key"])
            value = gen() if gen else None
            if value is not None:
                items.append({"component_id": comp["id"], "value": value})
        try:
            device.client.push_telemetry(items)
            if items:
                print(f"[센서 업로드] {len(items)}건")
        except Exception as exc:  # noqa: BLE001
            print(f"[센서 업로드 오류] {exc}")
        stop.wait(interval)


def command_loop(device: MockDevice, interval: float, stop: threading.Event) -> None:
    while not stop.is_set():
        try:
            actuators = device.actuators_by_id()
            for cmd in device.client.pending_commands():
                comp = actuators.get(cmd["component_id"])
                if comp is None:
                    continue
                apply_fn = APPLIERS.get(comp["type_key"])
                actual_state = apply_fn(cmd["desired_state"]) if apply_fn else cmd["desired_state"]
                device.client.ack_command(cmd["id"], actual_state)
                print(f"[명령 실행] {comp['label']}({comp['type_key']}) -> {actual_state}")
        except Exception as exc:  # noqa: BLE001
            print(f"[명령 처리 오류] {exc}")
        stop.wait(interval)


def heartbeat_loop(device: MockDevice, interval: float, stop: threading.Event) -> None:
    while not stop.is_set():
        try:
            device.client.heartbeat()
        except Exception as exc:  # noqa: BLE001
            print(f"[하트비트 오류] {exc}")
        stop.wait(interval)


def main() -> None:
    args = parse_args()
    client = BackendClient(args.backend_url, args.device_id, args.api_key)
    device = MockDevice(client)
    device.sync_components()

    stop = threading.Event()
    threads = [
        threading.Thread(target=sync_loop, args=(device, args.sync_interval, stop), daemon=True),
        threading.Thread(target=sensor_loop, args=(device, args.push_interval, stop), daemon=True),
        threading.Thread(target=command_loop, args=(device, args.poll_interval, stop), daemon=True),
        threading.Thread(target=heartbeat_loop, args=(device, args.heartbeat_interval, stop), daemon=True),
    ]
    for t in threads:
        t.start()

    print(f"Mock 라즈베리파이 실행 중 (device_id={args.device_id}, backend={args.backend_url}). Ctrl+C로 종료.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("종료 중...")
        stop.set()
        for t in threads:
            t.join(timeout=2)


if __name__ == "__main__":
    main()
