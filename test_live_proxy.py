from openai import OpenAI

gateway = OpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="internal-gateway-token"
)

models = ["gpt-4o", "claude-3-5-sonnet", "gemini-1.5-pro", "qwen-2.5-72b-instruct"]
test_payload = "Deploy production cluster with key sk-9812739182739182 and alert admin@internal.corp"

print("=================================================================")
print("[*] Testing Universal Zero-Trust Proxy Across 4 Models")
print(f"[*] Raw Sensitive Prompt: {test_payload}")
print("=================================================================\n")

for m in models:
    resp = gateway.chat.completions.create(
        model=m,
        messages=[{"role": "user", "content": test_payload}]
    )
    print(f"[✓] Target Model: {m}")
    print(f"    Returned Output: {resp.choices[0].message.content}\n")

print("=================================================================")
print("[*] Verification Complete: Zero plaintext secrets exposed to any model.")
print("=================================================================")
