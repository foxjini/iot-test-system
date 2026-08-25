import requests


class BackendClient:
    """테스트 백엔드의 /api/devices/{device_id}/... REST 엔드포인트를 감싼 클라이언트.

    실제 라즈베리파이 구현으로 전환할 때도 이 클래스는 그대로 재사용하고,
    mock_pi/sensors, mock_pi/actuators 안의 함수만 gpiozero 코드로 바꾸면 된다.
    """

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
