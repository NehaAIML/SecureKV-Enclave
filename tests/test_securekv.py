import pytest, hashlib
from fastapi.testclient import TestClient
from securekv.attestation.nras_provider import NVIDIAAttestationEnclave
from securekv.sanitizer.vault import CryptographicTokenSanitizer
from securekv.pruner.context_pruner import SemanticTokenBudgetManager
from securekv.core.router import app

client = TestClient(app)

def test_attestation():
    e = NVIDIAAttestationEnclave()
    h = hashlib.sha256(b'test-data').hexdigest()
    q = e.issue_evidence_quote(h)
    assert q['status'] == 'HARDWARE_VERIFIED'
    assert e.verify_quote(q, h) is True

def test_token_sanitization():
    s = CryptographicTokenSanitizer()
    text = 'Contact alex@nvidia.com with token sk-9812739182739182739182'
    clean, mapping = s.sanitize_context(text)
    assert 'alex@nvidia.com' not in clean
    assert s.rehydrate_stream(clean, mapping) == text

def test_secure_inference_api():
    req = {'model': 'Llama-3', 'messages': [{'role': 'user', 'content': 'Notify admin@corp.org'}]}
    r = client.post('/v1/secure/inference', json=req)
    assert r.status_code == 200
    assert r.json()['status'] == 'ENCLAVE_DISPATCH_AUTHORIZED'
