import json
import threading
import time
import requests
import websocket
from src.config import settings
from src.utils import clean_telemetry_payload

class IoTClient:
    _instance = None
    _lock = threading.Lock()
    _data_lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(IoTClient, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized: return
        self.data = {}
        self.is_connected = False
        self.token = None
        self.ws = None
        self._initialized = True
        
        # Eğer Docker değilse 127.0.0.1 çalışır. 
        # Verifier çalıştığına göre burası doğru.
        self.local_base_url = "http://127.0.0.1:9090"
        self.local_ws_url = "ws://127.0.0.1:9090"
        
        self._start_background_worker()

    def _get_token(self):
        try:
            resp = requests.post(
                f"{self.local_base_url}/api/auth/login",
                json={"username": settings.TB_USER, "password": settings.TB_PASS},
                timeout=5
            )
            return resp.json().get("token") if resp.status_code == 200 else None
        except Exception: return None

    def _fetch_snapshot(self):
        """İlk bağlantıda son veriyi HTTP ile çek (Hızlı Başlangıç)"""
        if not self.token: return
        try:
            # DEVICE ID BURADA KULLANILIYOR! YANLIŞSA BURASI PATLAR.
            url = f"{self.local_base_url}/api/plugins/telemetry/DEVICE/{settings.TB_DEVICE_ID}/values/timeseries?keys=llm_payload"
            resp = requests.get(url, headers={"X-Authorization": f"Bearer {self.token}"}, timeout=5)
            if resp.status_code == 200:
                val = resp.json().get("llm_payload", [{}])[0].get("value")
                if val:
                    clean = clean_telemetry_payload(val)
                    with self._data_lock:
                        self.data["llm_payload"] = clean
        except Exception: pass

    def _ws_loop(self):
        while True:
            self.token = self._get_token()
            if not self.token:
                time.sleep(5)
                continue
            
            # Bağlanmadan önce bir kere snapshot alalım
            self._fetch_snapshot()
            
            ws_url = f"{self.local_ws_url}/api/ws/plugins/telemetry?token={self.token}"
            
            self.ws = websocket.WebSocketApp(
                ws_url,
                on_open=self._on_open,
                on_message=self._on_message,
                on_error=lambda ws, err: print(f"IoT WS Error: {err}"),
                on_close=lambda ws, code, msg: setattr(self, 'is_connected', False)
            )
            self.ws.run_forever(ping_interval=30, ping_timeout=10)
            time.sleep(5)

    def _on_open(self, ws):
        self.is_connected = True
        # DEVICE ID BURADA DA KULLANILIYOR
        ws.send(json.dumps({
            "tsSubCmds": [{
                "entityType": "DEVICE", 
                "entityId": settings.TB_DEVICE_ID, 
                "scope": "LATEST_TELEMETRY", 
                "cmdId": 1
            }]
        }))

    def _on_message(self, ws, msg):
        try:
            payload = json.loads(msg)
            if "data" in payload and "llm_payload" in payload["data"]:
                raw = payload["data"]["llm_payload"][0][1]
                clean_val = clean_telemetry_payload(raw)
                with self._data_lock:
                    self.data["llm_payload"] = clean_val
        except Exception: pass

    def _start_background_worker(self):
        t = threading.Thread(target=self._ws_loop, daemon=True)
        t.start()

    def get_latest_payload(self) -> str:
        with self._data_lock:
            # ARTIK YALAN YOK: Veri yoksa None dönüyor.
            val = self.data.get("llm_payload", None)
        return str(val) if val else None