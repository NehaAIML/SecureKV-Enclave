import hashlib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from securekv.attestation.enclave import HardwareAttestationEnclave
from securekv.sanitizer.vault import CryptographicTokenSanitizer
from securekv.pruner.context_pruner import SemanticTokenBudgetManager

app = FastAPI(title="SecureKV-Enclave", version="1.0.0")
enclave = HardwareAttestationEnclave()
sanitizer = CryptographicTokenSanitizer()
pruner = SemanticTokenBudgetManager()

class ChatMessage(BaseModel):
    role: str
    content: str

class SecureInferenceRequest(BaseModel):
    model: str = "enterprise-llm-enclave"
    messages: List[ChatMessage]

@app.post("/v1/secure/inference")
async def route_inference(req: SecureInferenceRequest):
    raw = "".join([m.content for m in req.messages])
    h = hashlib.sha256(raw.encode()).hexdigest()
    q = enclave.issue_evidence_quote(h)
    if not enclave.verify_quote(q, h):
        raise HTTPException(status_code=403, detail="TEE Attestation Failed")
    pruned = pruner.prune_chat_history([m.model_dump() for m in req.messages])
    clean, s_map = sanitizer.sanitize_context(pruned["pruned_messages"][-1]["content"])
    return {"model": req.model, "attestation": q, "tokens_saved": pruned["tokens_saved"], "sanitized_prompt": clean, "status": "ENCLAVE_DISPATCH_AUTHORIZED"}

@app.get("/healthz")
def healthz():
    return {"status": "HEALTHY"}
