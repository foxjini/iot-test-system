"""테스트 백엔드(iot-test-system/backend)의 REST API를 감싼 클라이언트.

iot-test-system/mock_pi/client.py와 동일한 계약을 구현한다. 실기기 코드에서는
이 파일을 그대로 복사해서 쓰고, GPIO/카메라 관련 로직은 여기 섞지 않는다.
"""

import requests


class BackendClient:
    def __init__(self, base_url: str, device_id: int, api_key: str, timeout: float = 5.0):
        self.base_url = base_url.rstrip("/")
        self.device_id = device_id
        self.timeout = timeout
        self._headers = {"X-Device-Key": api_key}

    def _url(self, path: str) -> str:
        return f"{self.base_url}/api/devices/{self.device_id}{path}"

    def list_components(self) -> list[dict]:
        resp = requests.get(self._url("/components"), timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def push_telemetry(self, items: list[dict]) -> None:
        if not items:
            return
        resp = requests.post(
            self._url("/telemetry"),
            json={"items": items},
            headers=self._headers,
            timeout=self.timeout,
        )
        resp.raise_for_status()

    def pending_commands(self) -> list[dict]:
        resp = requests.get(
            self._url("/commands/pending"), headers=self._headers, timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()

    def ack_command(self, command_id: int, actual_state: dict, status: str = "acked") -> None:
        resp = requests.post(
            self._url(f"/commands/{command_id}/ack"),
            json={"actual_state": actual_state, "status": status},
            headers=self._headers,
            timeout=self.timeout,
        )
        resp.raise_for_status()

    def heartbeat(self) -> None:
        resp = requests.post(
            self._url("/heartbeat"), headers=self._headers, timeout=self.timeout
        )
        resp.raise_for_status()
