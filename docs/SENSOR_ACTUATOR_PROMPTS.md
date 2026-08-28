# [부록] 센서·액추에이터 17종 전체 프롬프트 예시 모음

> `STUDENT_HANDBOOK.md`의 **4장(센서 모듈 구현, Lab 2)**과 **5장(액추에이터 모듈 구현,
> Lab 3)**은 DHT11·Cds 조도센서·SG-90 서보·LED 4종만 예시로 다룬다. 우리 팀 프로젝트가
> 다른 부품을 쓴다면 참고할 예시가 없어 막막할 수 있는데, 이 파일이 그 자리를 메운다 —
> 카탈로그(`rules/02-catalog-contract.md`, `backend/app/catalog.py`)의 **17종 전체**에
> 대해 같은 형식(💬 프롬프트 예시 → 🤖 생성된 소스 코드)으로 준비했다.
>
> ⚠️ 여기서 만드는 `sensors/*.py`·`actuators/*.py`의 **하드웨어 로직(gpiozero
> 클래스, 배선, mock 폴백)은 팀의 진짜 시스템에도 그대로 재사용**한다. 다만 이
> 코드가 백엔드와 통신하는 방식(REST 경로/헤더)은 임시 테스트 시스템 기준이라,
> 진짜 백엔드(`agent-vibe-coding-starter-kit2`)에 연동할 때는 `client.py`만 그
> 시스템의 `hardware-agent` 방식으로 다시 만든다 — `antigravity-plugin/README.md`의
> "이 플러그인의 역할" 참고.

## 사용법

1. 우리 팀 프로젝트에 필요한 항목을 아래에서 찾는다.
2. "💬 프롬프트 예시"를 Antigravity 채팅창에 그대로 붙여넣되, **굵게 표시된 핀
   번호·부품 사양은 우리 팀의 실제 배선에 맞게 고친다.**
3. "🤖 생성된 소스 코드"는 정답이 아니라 **비교 기준**이다 — Antigravity가 만들어준
   코드가 이것과 크게 다르면(특히 반환하는 딕셔너리 키 이름), `STUDENT_HANDBOOK.md`
   9.1절의 3대 검증 원칙에 따라 다시 확인한다.
4. DHT11·조도센서·서보·LED는 `STUDENT_HANDBOOK.md` 4~5장에 이미 있으므로 여기서는
   같은 내용을 그대로 다시 실었다 — 이 파일 하나만 봐도 17종 전체가 끝나도록.
5. 모든 예시는 `os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"`와 하드웨어가 없는
   PC에서도 죽지 않는 mock 폴백을 기본 포함한다 (`HAS_HARDWARE` 패턴).

---

## A. 센서 10종 (Lab 2 확장)

### A-1. `pressure` — 압력센서

아날로그 출력 센서라 MCP3008(SPI ADC)이 필요하다. SPI0(CE0=GPIO8, 자동 배선)를 쓴다.

#### 💬 프롬프트 예시
```text
압력센서(아날로그 출력)를 MCP3008 ADC의 0번 채널에 연결했어 (SPI0, CE0 사용).
gpiozero.MCP3008을 이용해서 0~1(비율)로 읽히는 값을 0~1000 kPa 범위로 환산해
value(float, kPa) 키를 가진 딕셔너리를 반환하는 sensors/pressure_sensor.py를 작성해줘.
실기기가 없는 PC 환경에서도 500.0 kPa 기본값이 반환되도록 예외 처리를 넣어줘.
```

#### 🤖 생성된 소스 코드: `sensors/pressure_sensor.py`
```python
import os

os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"

try:
    from gpiozero import MCP3008
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False

class PressureSensor:
    def __init__(self, channel=0):
        self.channel = channel
        self._adc = MCP3008(channel=channel) if HAS_HARDWARE else None

    def read(self) -> dict:
        """
        카탈로그 계약:
        - value: float (kPa, 0~1000)
        """
        if not HAS_HARDWARE or self._adc is None:
            return {"value": 500.0}
        try:
            return {"value": round(self._adc.value * 1000.0, 1)}
        except Exception as e:
            print(f"[Pressure] 읽기 오류: {e}")
            return {"value": 0.0}

    def close(self):
        if self._adc:
            self._adc.close()

_default_sensor = None
def generate() -> dict | None:
    global _default_sensor
    if _default_sensor is None:
        _default_sensor = PressureSensor(channel=0)
    return _default_sensor.read()
```

---

### A-2. `keypad` — 숫자 키패드

4x3 매트릭스 키패드(행 4핀 + 열 3핀)를 gpiozero의 `DigitalOutputDevice`/`DigitalInputDevice`로 직접 스캔한다.

#### 💬 프롬프트 예시
```text
4x3 매트릭스 키패드를 연결했어. 행(row) 핀은 GPIO5, GPIO6, GPIO13, GPIO19이고
열(col) 핀은 GPIO26, GPIO21, GPIO20이야 (키 배열: 1~9, *, 0, #).
행에 순서대로 HIGH를 주고 열을 읽는 방식으로 스캔해서, 눌린 키가 있으면
key(string), event(string, 항상 "press") 딕셔너리를 반환하고 없으면 None을 반환하는
sensors/keypad_sensor.py를 작성해줘. 실기기가 없으면 항상 None을 반환하게 해줘.
```

#### 🤖 생성된 소스 코드: `sensors/keypad_sensor.py`
```python
import os

os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"

try:
    from gpiozero import DigitalOutputDevice, DigitalInputDevice
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False

_KEYS = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
    ["*", "0", "#"],
]

class KeypadSensor:
    def __init__(self, row_pins=(5, 6, 13, 19), col_pins=(26, 21, 20)):
        self._rows = [DigitalOutputDevice(p, initial_value=False) for p in row_pins] if HAS_HARDWARE else []
        self._cols = [DigitalInputDevice(p, pull_up=False) for p in col_pins] if HAS_HARDWARE else []

    def read(self) -> dict | None:
        """
        카탈로그 계약:
        - key: string ("0"~"9", "*", "#")
        - event: string ("press")
        """
        if not HAS_HARDWARE:
            return None

        for r_idx, row in enumerate(self._rows):
            row.on()
            for c_idx, col in enumerate(self._cols):
                if col.is_active:
                    row.off()
                    return {"key": _KEYS[r_idx][c_idx], "event": "press"}
            row.off()
        return None

    def close(self):
        for d in [*self._rows, *self._cols]:
            d.close()

_default_sensor = None
def generate() -> dict | None:
    global _default_sensor
    if _default_sensor is None:
        _default_sensor = KeypadSensor()
    return _default_sensor.read()
```

---

### A-3. `reed_switch` — 리드 스위치

gpiozero의 `Button`을 그대로 쓴다 (자석이 가까우면 닫힘).

#### 💬 프롬프트 예시
```text
리드 스위치를 GPIO27에 연결했어 (다른 쪽은 GND, 내부 풀업 사용).
gpiozero.Button을 이용해서 closed(bool) 키를 가진 딕셔너리를 반환하는
sensors/reed_switch_sensor.py를 작성해줘. 실기기가 없으면 항상 False를 반환하게 해줘.
```

#### 🤖 생성된 소스 코드: `sensors/reed_switch_sensor.py`
```python
import os

os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"

try:
    from gpiozero import Button
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False

class ReedSwitchSensor:
    def __init__(self, pin=27):
        self._button = Button(pin, pull_up=True) if HAS_HARDWARE else None

    def read(self) -> dict:
        """
        카탈로그 계약:
        - closed: bool
        """
        if not HAS_HARDWARE or self._button is None:
            return {"closed": False}
        return {"closed": self._button.is_pressed}

    def close(self):
        if self._button:
            self._button.close()

_default_sensor = None
def generate() -> dict | None:
    global _default_sensor
    if _default_sensor is None:
        _default_sensor = ReedSwitchSensor(pin=27)
    return _default_sensor.read()
```

---

### A-4. `flame` — 불꽃센서

디지털 감지 핀 + (있다면) MCP3008 1번 채널로 강도를 함께 읽는다. `pressure`와 같은
MCP3008 칩을 채널만 다르게 공유해도 된다.

#### 💬 프롬프트 예시
```text
불꽃센서의 디지털 출력(DO)을 GPIO25에 연결했어 (감지 시 LOW인 액티브-로우 모듈이야).
아날로그 출력(AO)은 MCP3008의 1번 채널에 연결했어.
detected(bool), intensity(float, 0~100) 딕셔너리를 반환하는 sensors/flame_sensor.py를
작성해줘. 실기기가 없으면 detected=False, intensity=2.0을 반환하게 해줘.
```

#### 🤖 생성된 소스 코드: `sensors/flame_sensor.py`
```python
import os

os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"

try:
    from gpiozero import Button, MCP3008
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False

class FlameSensor:
    def __init__(self, digital_pin=25, adc_channel=1):
        # 액티브-로우 모듈: 감지되면 핀이 LOW -> pull_up=True일 때 is_pressed=True
        self._digital = Button(digital_pin, pull_up=True) if HAS_HARDWARE else None
        self._adc = MCP3008(channel=adc_channel) if HAS_HARDWARE else None

    def read(self) -> dict:
        """
        카탈로그 계약:
        - detected: bool
        - intensity: float (%, 0~100)
        """
        if not HAS_HARDWARE or self._digital is None:
            return {"detected": False, "intensity": 2.0}

        detected = self._digital.is_pressed
        intensity = round(self._adc.value * 100.0, 1) if self._adc else 0.0
        return {"detected": detected, "intensity": intensity}

    def close(self):
        if self._digital:
            self._digital.close()
        if self._adc:
            self._adc.close()

_default_sensor = None
def generate() -> dict | None:
    global _default_sensor
    if _default_sensor is None:
        _default_sensor = FlameSensor(digital_pin=25, adc_channel=1)
    return _default_sensor.read()
```

---

### A-5. `dht11` — 온습도센서 (`STUDENT_HANDBOOK.md` 4.1과 동일)

#### 💬 프롬프트 예시
```text
라즈베리파이 5의 GPIO4 번 핀에 DHT11 온습도 센서를 연결했어.
카탈로그 계약에 맞게 온도는 temperature_c(°C), 습도는 humidity_pct(%) 키를 가진 딕셔너리를 반환하는 sensors/dht11_sensor.py 코드를 작성해줘.
라즈베리파이 5 핀팩토리 lgpio 설정과 DHT11의 타이밍 오류에 대비한 3회 재시도(Retry) 로직도 포함해줘.
실기기가 없는 PC 환경에서도 에러 없이 가상 데이터가 반환되도록 예외 처리를 넣어줘.
```

#### 🤖 생성된 소스 코드: `sensors/dht11_sensor.py`
```python
import os
import time

os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"

try:
    import board
    import adafruit_dht
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False

class DHT11Sensor:
    def __init__(self, pin=4):
        self.pin = pin
        self._sensor = None
        if HAS_HARDWARE:
            d_pin = getattr(board, f"D{pin}", board.D4)
            self._sensor = adafruit_dht.DHT11(d_pin, use_pulseio=False)

    def read(self) -> dict:
        """
        카탈로그 계약:
        - temperature_c: float (°C)
        - humidity_pct: float (%)
        """
        if not HAS_HARDWARE or self._sensor is None:
            return {"temperature_c": 24.5, "humidity_pct": 55.0}

        for _ in range(3):
            try:
                temp = float(self._sensor.temperature)
                hum = float(self._sensor.humidity)
                return {"temperature_c": round(temp, 1), "humidity_pct": round(hum, 1)}
            except RuntimeError:
                time.sleep(1.0)
            except Exception as e:
                print(f"[DHT11] 오류 발생: {e}")
                break

        return {"temperature_c": 0.0, "humidity_pct": 0.0}

    def close(self):
        if self._sensor:
            self._sensor.exit()

_default_sensor = None
def generate() -> dict | None:
    global _default_sensor
    if _default_sensor is None:
        _default_sensor = DHT11Sensor(pin=4)
    return _default_sensor.read()
```

---

### A-6. `hcsr04` — 초음파센서(HC-SR04)

gpiozero에 `DistanceSensor`가 내장되어 있어 가장 간단하다.

#### 💬 프롬프트 예시
```text
초음파 센서(HC-SR04)를 연결했어. TRIG는 GPIO23, ECHO는 GPIO24야.
gpiozero.DistanceSensor를 이용해서 distance_cm(float, cm) 키를 가진 딕셔너리를
반환하는 sensors/hcsr04_sensor.py를 작성해줘 (DistanceSensor.distance는 0~1m
단위이니 cm로 환산해줘). 실기기가 없으면 30.0 cm 기본값을 반환하게 해줘.
```

#### 🤖 생성된 소스 코드: `sensors/hcsr04_sensor.py`
```python
import os

os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"

try:
    from gpiozero import DistanceSensor
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False

class HcSr04Sensor:
    def __init__(self, trigger=23, echo=24):
        self._sensor = DistanceSensor(echo=echo, trigger=trigger, max_distance=4.0) if HAS_HARDWARE else None

    def read(self) -> dict:
        """
        카탈로그 계약:
        - distance_cm: float (cm, 2~400)
        """
        if not HAS_HARDWARE or self._sensor is None:
            return {"distance_cm": 30.0}
        try:
            return {"distance_cm": round(self._sensor.distance * 100.0, 1)}
        except Exception as e:
            print(f"[HC-SR04] 읽기 오류: {e}")
            return {"distance_cm": 0.0}

    def close(self):
        if self._sensor:
            self._sensor.close()

_default_sensor = None
def generate() -> dict | None:
    global _default_sensor
    if _default_sensor is None:
        _default_sensor = HcSr04Sensor(trigger=23, echo=24)
    return _default_sensor.read()
```

---

### A-7. `push_button` — 푸시버튼

#### 💬 프롬프트 예시
```text
푸시버튼을 GPIO16에 연결했어 (다른 쪽은 GND, 내부 풀업 사용).
gpiozero.Button을 이용해서 pressed(bool) 키를 가진 딕셔너리를 반환하는
sensors/push_button_sensor.py를 작성해줘. 실기기가 없으면 항상 False를 반환하게 해줘.
```

#### 🤖 생성된 소스 코드: `sensors/push_button_sensor.py`
```python
import os

os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"

try:
    from gpiozero import Button
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False

class PushButtonSensor:
    def __init__(self, pin=16):
        self._button = Button(pin, pull_up=True) if HAS_HARDWARE else None

    def read(self) -> dict:
        """
        카탈로그 계약:
        - pressed: bool
        """
        if not HAS_HARDWARE or self._button is None:
            return {"pressed": False}
        return {"pressed": self._button.is_pressed}

    def close(self):
        if self._button:
            self._button.close()

_default_sensor = None
def generate() -> dict | None:
    global _default_sensor
    if _default_sensor is None:
        _default_sensor = PushButtonSensor(pin=16)
    return _default_sensor.read()
```

---

### A-8. `illuminance` — 조도센서(Cds, `STUDENT_HANDBOOK.md` 4.2와 동일)

#### 💬 프롬프트 예시
```text
Cds 조도 센서와 1uF 커패시터를 GPIO17에 연결했어 (RC 충전 시간 방식 LightSensor).
카탈로그 계약인 lux(float, 0~2000 lx)를 반환하는 sensors/cds_sensor.py 코드를 작성해줘.
gpiozero.LightSensor를 사용하고, 하드웨어가 없을 때도 450.0 lx의 기본값을 반환하도록 구현해줘.
```

#### 🤖 생성된 소스 코드: `sensors/cds_sensor.py`
```python
import os

os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"

try:
    from gpiozero import LightSensor
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False

class CdsSensor:
    def __init__(self, pin=17):
        self.pin = pin
        self._sensor = None
        if HAS_HARDWARE:
            self._sensor = LightSensor(self.pin)

    def read(self) -> dict:
        """
        카탈로그 계약:
        - lux: float (lx, 0~2000)
        """
        if not HAS_HARDWARE or self._sensor is None:
            return {"lux": 450.0}
        try:
            raw_val = self._sensor.value
            lux_val = round(raw_val * 2000.0, 1)
            return {"lux": lux_val}
        except Exception as e:
            print(f"[Cds] 읽기 오류: {e}")
            return {"lux": 0.0}

    def close(self):
        if self._sensor:
            self._sensor.close()

_default_sensor = None
def generate() -> dict | None:
    global _default_sensor
    if _default_sensor is None:
        _default_sensor = CdsSensor(pin=17)
    return _default_sensor.read()
```

---

### A-9. `qr_scanner` — QR/바코드 인식

카메라(USB 웹캠 또는 Pi Camera)로 처리한다. GPIO 핀은 쓰지 않는다. 처리 위치(라즈베리파이
직접 vs 백엔드 오프로드) 선택은 `antigravity-plugin/skills/vision-trigger/`,
`STUDENT_HANDBOOK.md` 8장 참고 — 아래는 옵션 A(라즈베리파이 직접 처리) 기준이다.

#### 💬 프롬프트 예시
```text
USB 웹캠으로 QR 코드를 인식하는 sensors/qr_scanner_sensor.py를 작성해줘.
OpenCV의 cv2.QRCodeDetector()를 사용해서, 인식되면 detected(bool)=True와 payload(string)에
문자열을 담고, 인식 안 되면 detected=False, payload=""를 반환해줘.
웹캠이 없는 PC 환경에서도 에러 없이 detected=False를 반환하도록 예외 처리를 넣어줘.
```

#### 🤖 생성된 소스 코드: `sensors/qr_scanner_sensor.py`
```python
try:
    import cv2
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False

class QrScannerSensor:
    def __init__(self, camera_index=0):
        self._detector = cv2.QRCodeDetector() if HAS_HARDWARE else None
        self._cap = cv2.VideoCapture(camera_index) if HAS_HARDWARE else None

    def read(self) -> dict:
        """
        카탈로그 계약:
        - detected: bool
        - payload: string
        """
        if not HAS_HARDWARE or self._cap is None or not self._cap.isOpened():
            return {"detected": False, "payload": ""}

        ok, frame = self._cap.read()
        if not ok:
            return {"detected": False, "payload": ""}

        try:
            payload, _points, _straight_qr = self._detector.detectAndDecode(frame)
            return {"detected": bool(payload), "payload": payload or ""}
        except Exception as e:
            print(f"[QR] 인식 오류: {e}")
            return {"detected": False, "payload": ""}

    def close(self):
        if self._cap:
            self._cap.release()

_default_sensor = None
def generate() -> dict | None:
    global _default_sensor
    if _default_sensor is None:
        _default_sensor = QrScannerSensor(camera_index=0)
    return _default_sensor.read()
```

---

### A-10. `object_detector` — 영상 객체 인식

라즈베리파이 5는 GPU가 없어 경량(nano) 모델을 쓴다. 무거우면 백엔드 오프로드를
검토한다 (`antigravity-plugin/skills/vision-trigger/references/options.md`).

#### 💬 프롬프트 예시
```text
USB 웹캠 영상에서 경량 YOLO(nano) 모델로 객체를 인식하는
sensors/object_detector_sensor.py를 작성해줘 (ultralytics 라이브러리 사용).
가장 신뢰도(confidence) 높은 객체 1개를 label(string), confidence(float, 0~1),
count(int, 전체 인식 개수) 딕셔너리로 반환해줘.
인식된 게 없으면 label="", confidence=0.0, count=0을 반환하고,
라이브러리나 웹캠이 없는 PC 환경에서도 에러 없이 같은 기본값이 반환되게 해줘.
```

#### 🤖 생성된 소스 코드: `sensors/object_detector_sensor.py`
```python
try:
    import cv2
    from ultralytics import YOLO
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False

class ObjectDetectorSensor:
    def __init__(self, camera_index=0, model_name="yolo11n.pt"):
        self._model = YOLO(model_name) if HAS_HARDWARE else None
        self._cap = cv2.VideoCapture(camera_index) if HAS_HARDWARE else None

    def read(self) -> dict:
        """
        카탈로그 계약:
        - label: string
        - confidence: float (0~1)
        - count: int
        """
        empty = {"label": "", "confidence": 0.0, "count": 0}
        if not HAS_HARDWARE or self._cap is None or not self._cap.isOpened():
            return empty

        ok, frame = self._cap.read()
        if not ok:
            return empty

        try:
            results = self._model(frame, verbose=False)[0]
            if len(results.boxes) == 0:
                return empty
            best = results.boxes[results.boxes.conf.argmax()]
            label = results.names[int(best.cls[0])]
            return {
                "label": label,
                "confidence": round(float(best.conf[0]), 2),
                "count": len(results.boxes),
            }
        except Exception as e:
            print(f"[ObjectDetector] 인식 오류: {e}")
            return empty

    def close(self):
        if self._cap:
            self._cap.release()

_default_sensor = None
def generate() -> dict | None:
    global _default_sensor
    if _default_sensor is None:
        _default_sensor = ObjectDetectorSensor(camera_index=0)
    return _default_sensor.read()
```

---

## B. 액추에이터 7종 (Lab 3 확장)

### B-1. `led` — LED (`STUDENT_HANDBOOK.md` 5.2와 동일)

#### 💬 프롬프트 예시
```text
GPIO22에 연결된 LED를 제어하는 actuators/led.py를 만들어줘.
카탈로그 계약: on(bool), brightness_pct(float, 0~100).
gpiozero.PWMLED를 사용해 밝기 조절이 가능하도록 해줘.
```

#### 🤖 생성된 소스 코드: `actuators/led.py`
```python
import os

os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"

try:
    from gpiozero import PWMLED
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False

class LedActuator:
    def __init__(self, pin=22):
        self.pin = pin
        self.is_on = False
        self.brightness_pct = 100.0
        self._led = PWMLED(pin) if HAS_HARDWARE else None

    def apply(self, desired: dict) -> dict:
        if "on" in desired:
            self.is_on = bool(desired["on"])
        if "brightness_pct" in desired:
            self.brightness_pct = float(desired["brightness_pct"])

        if HAS_HARDWARE and self._led:
            if self.is_on:
                self._led.value = max(0.0, min(1.0, self.brightness_pct / 100.0))
            else:
                self._led.off()

        return {"on": self.is_on, "brightness_pct": self.brightness_pct}

_default_led = None
def apply(desired: dict) -> dict:
    global _default_led
    if _default_led is None:
        _default_led = LedActuator(pin=22)
    return _default_led.apply(desired)
```

---

### B-2. `dc_motor` — DC모터

모터드라이버(L298N 등)의 IN1/IN2에 연결한다. `gpiozero.Motor`가 정/역방향을 부호로 처리해준다.

#### 💬 프롬프트 예시
```text
L298N 모터드라이버를 통해 DC모터를 연결했어. IN1은 GPIO12, IN2는 GPIO13이야.
카탈로그 계약: speed_pct(float, -100~100, 양수=정방향/음수=역방향).
gpiozero.Motor를 사용하는 actuators/dc_motor.py를 작성해줘.
```

#### 🤖 생성된 소스 코드: `actuators/dc_motor.py`
```python
import os

os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"

try:
    from gpiozero import Motor
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False

class DcMotorActuator:
    def __init__(self, forward_pin=12, backward_pin=13):
        self.speed_pct = 0.0
        self._motor = Motor(forward=forward_pin, backward=backward_pin) if HAS_HARDWARE else None

    def apply(self, desired: dict) -> dict:
        """
        카탈로그 계약:
        - speed_pct: float (-100~100)
        """
        speed = float(desired.get("speed_pct", 0.0))
        speed = max(-100.0, min(100.0, speed))
        self.speed_pct = speed

        if HAS_HARDWARE and self._motor:
            ratio = abs(speed) / 100.0
            if speed > 0:
                self._motor.forward(ratio)
            elif speed < 0:
                self._motor.backward(ratio)
            else:
                self._motor.stop()

        return {"speed_pct": self.speed_pct}

_default_actuator = None
def apply(desired: dict) -> dict:
    global _default_actuator
    if _default_actuator is None:
        _default_actuator = DcMotorActuator(forward_pin=12, backward_pin=13)
    return _default_actuator.apply(desired)
```

---

### B-3. `solenoid` — 솔레노이드

릴레이/트랜지스터로 구동하는 단순 on/off 출력이다.

#### 💬 프롬프트 예시
```text
솔레노이드를 릴레이 모듈을 통해 GPIO6에 연결했어.
카탈로그 계약: on(bool). gpiozero.OutputDevice를 사용하는 actuators/solenoid.py를 작성해줘.
```

#### 🤖 생성된 소스 코드: `actuators/solenoid.py`
```python
import os

os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"

try:
    from gpiozero import OutputDevice
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False

class SolenoidActuator:
    def __init__(self, pin=6):
        self.is_on = False
        self._device = OutputDevice(pin) if HAS_HARDWARE else None

    def apply(self, desired: dict) -> dict:
        """
        카탈로그 계약:
        - on: bool
        """
        if "on" in desired:
            self.is_on = bool(desired["on"])

        if HAS_HARDWARE and self._device:
            self._device.on() if self.is_on else self._device.off()

        return {"on": self.is_on}

_default_actuator = None
def apply(desired: dict) -> dict:
    global _default_actuator
    if _default_actuator is None:
        _default_actuator = SolenoidActuator(pin=6)
    return _default_actuator.apply(desired)
```

---

### B-4. `neopixel` — 네오픽셀 LED(WS2812)

정밀 비트 타이밍이 필요해 gpiozero가 아니라 `adafruit-circuitpython-neopixel`을 쓴다.

#### 💬 프롬프트 예시
```text
WS2812 네오픽셀 LED 스트립(8개)을 GPIO21의 데이터 핀에 연결했어.
adafruit-circuitpython-neopixel 라이브러리를 사용해서
color([r,g,b], 0~255)와 brightness_pct(float, 0~100)를 받아
전체 픽셀에 적용하는 actuators/neopixel.py를 작성해줘.
라이브러리가 없는 PC 환경에서도 에러 없이 동작하게 해줘.
```

#### 🤖 생성된 소스 코드: `actuators/neopixel.py`
```python
try:
    import board
    import neopixel
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False

class NeopixelActuator:
    def __init__(self, pin_name="D21", num_pixels=8):
        self.color = [0, 0, 0]
        self.brightness_pct = 100.0
        self._pixels = None
        if HAS_HARDWARE:
            pin = getattr(board, pin_name)
            self._pixels = neopixel.NeoPixel(pin, num_pixels, brightness=1.0, auto_write=False)

    def apply(self, desired: dict) -> dict:
        """
        카탈로그 계약:
        - color: [r, g, b] (각 0~255)
        - brightness_pct: float (%, 0~100)
        """
        if "color" in desired:
            self.color = [int(c) for c in desired["color"]]
        if "brightness_pct" in desired:
            self.brightness_pct = float(desired["brightness_pct"])

        if HAS_HARDWARE and self._pixels:
            self._pixels.brightness = max(0.0, min(1.0, self.brightness_pct / 100.0))
            self._pixels.fill(tuple(self.color))
            self._pixels.show()

        return {"color": self.color, "brightness_pct": self.brightness_pct}

_default_actuator = None
def apply(desired: dict) -> dict:
    global _default_actuator
    if _default_actuator is None:
        _default_actuator = NeopixelActuator(pin_name="D21", num_pixels=8)
    return _default_actuator.apply(desired)
```

---

### B-5. `buzzer` — 부저

`freq_hz`를 직접 지정해야 하므로 음계 단위인 `TonalBuzzer`보다 `PWMOutputDevice`의
`.frequency` 속성을 직접 쓰는 편이 계약에 더 잘 맞는다.

#### 💬 프롬프트 예시
```text
능동 부저를 GPIO19에 연결했어.
카탈로그 계약: on(bool), freq_hz(int, Hz, 100~5000).
gpiozero.PWMOutputDevice의 frequency 속성을 이용해 주파수를 직접 지정하는
actuators/buzzer.py를 작성해줘.
```

#### 🤖 생성된 소스 코드: `actuators/buzzer.py`
```python
import os

os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"

try:
    from gpiozero import PWMOutputDevice
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False

class BuzzerActuator:
    def __init__(self, pin=19):
        self.is_on = False
        self.freq_hz = 1000
        self._device = PWMOutputDevice(pin, frequency=self.freq_hz) if HAS_HARDWARE else None

    def apply(self, desired: dict) -> dict:
        """
        카탈로그 계약:
        - on: bool
        - freq_hz: int (Hz, 100~5000)
        """
        if "on" in desired:
            self.is_on = bool(desired["on"])
        if "freq_hz" in desired:
            self.freq_hz = int(desired["freq_hz"])

        if HAS_HARDWARE and self._device:
            self._device.frequency = self.freq_hz
            self._device.on() if self.is_on else self._device.off()

        return {"on": self.is_on, "freq_hz": self.freq_hz}

_default_actuator = None
def apply(desired: dict) -> dict:
    global _default_actuator
    if _default_actuator is None:
        _default_actuator = BuzzerActuator(pin=19)
    return _default_actuator.apply(desired)
```

---

### B-6. `servo` — 서보모터(SG-90, `STUDENT_HANDBOOK.md` 5.1과 동일)

#### 💬 프롬프트 예시
```text
SG-90 마이크로 서보모터를 GPIO18에 연결했어.
카탈로그 계약에 따라 desired 딕셔너리에서 angle_deg(0~180도)를 받아 각도를 변경하고, 실제 설정된 각도를 반환하는 actuators/servo.py 코드를 작성해줘.
gpiozero.AngularServo를 사용하고, SG-90의 펄스 폭(min_pulse_width=0.0005, max_pulse_width=0.0024)을 지정해줘.
```

#### 🤖 생성된 소스 코드: `actuators/servo.py`
```python
import os
import time

os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"

try:
    from gpiozero import AngularServo
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False

class ServoActuator:
    def __init__(self, pin=18):
        self.pin = pin
        self._servo = None
        self.current_angle = 90.0
        if HAS_HARDWARE:
            self._servo = AngularServo(
                self.pin, min_angle=0, max_angle=180,
                min_pulse_width=0.0005, max_pulse_width=0.0024,
            )
            self._servo.angle = self.current_angle

    def apply(self, desired: dict) -> dict:
        """
        카탈로그 계약:
        - angle_deg: float (0~180)
        """
        angle = float(desired.get("angle_deg", self.current_angle))
        angle = max(0.0, min(180.0, angle))
        self.current_angle = angle

        if HAS_HARDWARE and self._servo is not None:
            self._servo.angle = angle
            time.sleep(0.3)

        return {"angle_deg": self.current_angle}

    def close(self):
        if self._servo:
            self._servo.close()

_default_actuator = None
def apply(desired: dict) -> dict:
    global _default_actuator
    if _default_actuator is None:
        _default_actuator = ServoActuator(pin=18)
    return _default_actuator.apply(desired)
```

---

### B-7. `relay` — 릴레이

솔레노이드와 같은 `OutputDevice` 패턴이지만, 모듈에 따라 신호가 반전(active-low)될
수 있어 실제 배선 후 동작 방향을 꼭 확인한다.

#### 💬 프롬프트 예시
```text
릴레이 모듈을 GPIO26에 연결했어 (필요하면 active_high=False로 바꿀 수 있게 해줘 —
모듈에 따라 신호가 반전될 수 있어서).
카탈로그 계약: on(bool). gpiozero.OutputDevice를 사용하는 actuators/relay.py를 작성해줘.
```

#### 🤖 생성된 소스 코드: `actuators/relay.py`
```python
import os

os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"

try:
    from gpiozero import OutputDevice
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False

class RelayActuator:
    def __init__(self, pin=26, active_high=True):
        self.is_on = False
        self._device = OutputDevice(pin, active_high=active_high) if HAS_HARDWARE else None

    def apply(self, desired: dict) -> dict:
        """
        카탈로그 계약:
        - on: bool
        """
        if "on" in desired:
            self.is_on = bool(desired["on"])

        if HAS_HARDWARE and self._device:
            self._device.on() if self.is_on else self._device.off()

        return {"on": self.is_on}

_default_actuator = None
def apply(desired: dict) -> dict:
    global _default_actuator
    if _default_actuator is None:
        _default_actuator = RelayActuator(pin=26, active_high=True)
    return _default_actuator.apply(desired)
```

---

## 더 볼 곳

- 오류가 나면 `STUDENT_HANDBOOK.md` 9.2절(자주 발생하는 오류와 해결 방법)을 먼저 확인한다.
- 핀 번호는 전부 예시다 — 우리 팀 실제 배선과 다르면 프롬프트의 굵은 글씨 부분만 바꿔서 다시 요청한다.
- 여러 부품을 동시에 쓸 때는 GPIO 핀이 서로 겹치지 않는지 반드시 확인한다
  (`STUDENT_HANDBOOK.md` 9.1절, `antigravity-plugin/hooks/`의 핀 중복 점검 훅 참고).
- 비전(QR/객체 인식)을 백엔드로 오프로드하고 싶다면 `antigravity-plugin/skills/vision-trigger/`를 참고한다.
