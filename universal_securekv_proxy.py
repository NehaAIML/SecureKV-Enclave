import re
import json
import hashlib
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Tuple, List

class EnclaveVault:
    def __init__(self):
        self._surrogates: Dict[str, str] = {}
        self.rules: List[Tuple[re.Pattern, str]] = [
            (re.compile(r'sk-[a-zA-Z0-9_\-]{16,}'), "API_KEY"),
            (re.compile(r'Bearer\s+[a-zA-Z0-9_\-\.]{16,}'), "AUTH_TOKEN"),
            (re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'), "EMAIL"),
            (re.compile(r'postgres://[^\s\'"]+|mysql://[^\s\'"]+'), "DB_URI")
        ]

    def sanitize(self, text: str) -> str:
        sanitized = text
        for pattern, label in self.rules:
            for match in pattern.findall(sanitized):
                token_hash = hashlib.sha256(match.encode()).hexdigest()[:8]
                surrogate = f"<SEC_{label}_{token_hash}>"
                self._surrogates[surrogate] = match
                sanitized = sanitized.replace(match, surrogate)
        return sanitized

    def rehydrate(self, text: str) -> str:
        rehydrated = text
        for surrogate, original in self._surrogates.items():
            rehydrated = rehydrated.replace(surrogate, original)
        return rehydrated

vault = EnclaveVault()

class SecureKVProxyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/v1/chat/completions":
            self.send_response(404)
            self.end_headers()
            return

        content_length = int(self.headers.get('Content-Length', 0))
        body_bytes = self.rfile.read(content_length)
        body = json.loads(body_bytes.decode('utf-8'))

        model = body.get("model", "gpt-4o")
        messages = body.get("messages", [])

        # 1. Zero-Trust Ingress Sanitization
        print(f"\n[*] [INGRESS INTERCEPT] Model Target: {model}")
        sanitized_messages = []
        for msg in messages:
            raw_content = msg.get("content", "")
            clean_content = vault.sanitize(raw_content)
            sanitized_messages.append({"role": msg.get("role"), "content": clean_content})

        last_prompt = sanitized_messages[-1]['content'] if sanitized_messages else ""
        print(f"    [>] Sanitized context sent upstream: {last_prompt}")

        # 2. Simulated Upstream Frontier Provider Execution
        provider_tag = (
            "OpenAI" if "gpt" in model else
            "Anthropic" if "claude" in model else
            "Google" if "gemini" in model else
            "vLLM/Qwen"
        )
        
        surrogates_present = [k for k in vault._surrogates.keys() if k in last_prompt]
        surrogate_token = surrogates_present[0] if surrogates_present else "<SEC_TOKEN>"

        upstream_raw_reply = (
            f"[{provider_tag}] Task authorized. Successfully deployed using credential "
            f"{surrogate_token} with zero secrets retained in host memory."
        )

        # 3. Deterministic Client-Side Rehydration
        client_response_text = vault.rehydrate(upstream_raw_reply)
        print(f"    [<] Upstream Raw (Surrogates only): {upstream_raw_reply}")
        print(f"    [✓] Deterministic Rehydrated Output: {client_response_text}")

        response_payload = {
            "id": f"chatcmpl-{hashlib.md5(client_response_text.encode()).hexdigest()[:8]}",
            "object": "chat.completion",
            "model": model,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": client_response_text
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": len(last_prompt.split()),
                "completion_tokens": len(client_response_text.split()),
                "total_tokens": len(last_prompt.split()) + len(client_response_text.split())
            }
        }

        resp_bytes = json.dumps(response_payload).encode('utf-8')
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(resp_bytes)))
        self.end_headers()
        self.wfile.write(resp_bytes)

    def log_message(self, format, *args):
        # Silence default HTTP access logs for clean display
        return

if __name__ == "__main__":
    server_address = ('127.0.0.1', 8000)
    httpd = HTTPServer(server_address, SecureKVProxyHandler)
    print("=================================================================")
    print("[*] SecureKV Universal Proxy running on http://127.0.0.1:8000")
    print("[*] Ready to intercept OpenAI, Claude, Gemini & Qwen requests...")
    print("=================================================================")
    httpd.serve_forever()
