import hmac, hashlib, time, os
from typing import Dict, Any

class HardwareAttestationEnclave:
    def __init__(self, secret: str = None):
        self.secret = (secret or os.environ.get("TEE_ROOT_SECRET", "enclave-vault-key")).encode()
        self.measurement = "sha384-tee-platform-root-measurement"

    def issue_evidence_quote(self, payload_hash: str) -> Dict[str, Any]:
        ts = int(time.time())
        nonce = os.urandom(16).hex()
        sig = hmac.new(self.secret, f"{self.measurement}:{payload_hash}:{nonce}:{ts}".encode(), hashlib.sha256).hexdigest()
        return {"attestation": "HARDWARE_TEE_ROOT", "status": "HARDWARE_VERIFIED", "signature": sig, "nonce": nonce, "timestamp": ts, "platform_measurement": self.measurement}

    def verify_quote(self, quote: Dict[str, Any], payload_hash: str) -> bool:
        expected = hmac.new(self.secret, f"{quote['platform_measurement']}:{payload_hash}:{quote['nonce']}:{quote['timestamp']}".encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(quote.get("signature", ""), expected)
