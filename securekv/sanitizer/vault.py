import re, base64
from typing import Tuple, Dict
from cryptography.fernet import Fernet

class CryptographicTokenSanitizer:
    PII_PATTERNS = {
        'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',
        'API_KEY': r'\b(?:sk|ghp|nvapi)-[A-Za-z0-9_\-]{20,}\b'
    }

    def __init__(self, key: bytes = None):
        self.key = key or Fernet.generate_key()
        self.cipher = Fernet(self.key)
        self.surrogate_map: Dict[str, str] = {}

    def sanitize_context(self, prompt: str) -> Tuple[str, Dict[str, str]]:
        clean_prompt = prompt
        session_map = {}
        for pii_type, pattern in self.PII_PATTERNS.items():
            matches = set(re.findall(pattern, clean_prompt))
            for m in matches:
                encrypted = self.cipher.encrypt(m.encode()).decode()
                token_hash = base64.urlsafe_b64encode(m.encode()[:6]).decode().rstrip('=')
                surrogate = f'<SEC_{pii_type}_{token_hash}>'
                session_map[surrogate] = encrypted
                self.surrogate_map[surrogate] = encrypted
                clean_prompt = clean_prompt.replace(m, surrogate)
        return clean_prompt, session_map

    def rehydrate_stream(self, text: str, session_map: Dict[str, str] = None) -> str:
        active_map = session_map if session_map is not None else self.surrogate_map
        result = text
        for surrogate, encrypted_val in active_map.items():
            if surrogate in result:
                decrypted = self.cipher.decrypt(encrypted_val.encode()).decode()
                result = result.replace(surrogate, decrypted)
        return result
