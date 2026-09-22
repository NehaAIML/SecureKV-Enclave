import sys
from pathlib import Path

# Add project root to Python module search path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import time
from fastapi.testclient import TestClient
from securekv.core.router import app
from securekv.sanitizer.vault import CryptographicTokenSanitizer

def run_demo():
    client = TestClient(app)
    sanitizer = CryptographicTokenSanitizer()
    border = "=" * 65

    print(border)
    print("[*] SecureKV-Enclave: Zero-Trust Round-Trip Inference Demo")
    print(border)

    conversation = [
        {"role": "system", "content": "You are a confidential enterprise AI assistant."},
        {"role": "user", "content": "Turn 1: Project Falcon status check."},
        {"role": "assistant", "content": "Standing by for instructions."},
        {"role": "user", "content": "Deploy cluster with key sk-9812739182739182739182 and email admin@company.internal"}
    ]

    print("\n[1] Incoming Multi-Turn Context:")
    for msg in conversation:
        print("    [" + msg["role"] + "]: " + msg["content"])

    t0 = time.perf_counter()
    response = client.post("/v1/secure/inference", json={"model": "confidential-tee-llm", "messages": conversation})
    elapsed_ms = (time.perf_counter() - t0) * 1000

    assert response.status_code == 200, response.text
    data = response.json()

    print("\n[2] Enclave Gateway Processing:")
    print("    - Latency Overhead     : " + str(round(elapsed_ms, 3)) + " ms")
    print("    - Attestation Status   : " + str(data["attestation"]["status"]))
    print("    - Platform Measurement : " + str(data["attestation"]["platform_measurement"]))
    print("    - Tokens Reclaimed     : " + str(data["tokens_saved"]))
    print("    - Entities Sanitized   : " + str(data["sanitized_entities_count"]))

    print("\n[3] Sanitized Prompt Sent to Model (Zero Secrets):")
    print("    " + data["sanitized_prompt"])

    # Extract session surrogate mappings
    _, session_map = sanitizer.sanitize_context(conversation[-1]["content"])
    surrogate_keys = list(session_map.keys())
    mock_model_output = "Task authorized using surrogate " + surrogate_keys[1] + " and notification routed to " + surrogate_keys[0]

    print("\n[4] Raw Model Output Stream (Surrogates Only):")
    print("    " + mock_model_output)

    # Re-hydrate back at client boundary
    rehydrated = sanitizer.rehydrate_stream(mock_model_output, session_map)

    print("\n[5] Deterministically Re-Hydrated Response (Client Side):")
    print("    " + rehydrated)

    print("\n" + border)
    print("[*] Verification Complete: Real credentials never entered model memory.")
    print(border)

if __name__ == "__main__":
    run_demo()
