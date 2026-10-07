import sys

print("[*] Running Universal Gateway Multi-Model Router Test")

try:
    from openai import OpenAI
except ImportError:
    print("[-] openai library not installed in this environment.")
    print("[*] Run: pip install openai")
    sys.exit(1)

# Point to your local or remote SecureKV unified proxy endpoint
ai_gateway = OpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="mock-enclave-key"
)

models_to_test = [
    "gpt-4o",
    "claude-3-5-sonnet",
    "gemini-1.5-pro",
    "qwen-2.5-72b-instruct"
]

test_prompt = "Deploy DB with key sk-9812739182739182 and notify ops@internal.corp"

print(f"\n[>] Raw Input Prompt (Sensitive): \n    {test_prompt}\n")

for model_name in models_to_test:
    print(f"[*] Dispatching to model target: {model_name}...")
    try:
        # SecureKV intercepts, strips the sk-... key, injects surrogate, and rehydrates
        res = ai_gateway.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": test_prompt}]
        )
        print(f"    [✓] Response received from {model_name}:")
        print(f"        {res.choices[0].message.content}\n")
    except Exception as e:
        print(f"    [!] Note: Gateway routing simulated or offline ({e.__class__.__name__})")
