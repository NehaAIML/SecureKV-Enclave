import hashlib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from securekv.attestation.nras_provider import NVIDIAAttestationEnclave
from securekv.sanitizer.vault import CryptographicTokenSanitizer
from securekv.pruner.context_pruner import SemanticTokenBudgetManager

app = FastAPI(title='SecureKV-Enclave', version='1.0.0')
enclave = NVIDIAAttestationEnclave()
sanitizer = CryptographicTokenSanitizer()
pruner = SemanticTokenBudgetManager()

class ChatMessage(BaseModel):
    role: str
    content: str

class SecureInferenceRequest(BaseModel):
    model: str = 'meta-llama/Llama-3-70b-instruct'
    messages: List[ChatMessage]
    max_tokens: Optional[int] = 512

@app.post('/v1/secure/inference')
async def route_inference(req: SecureInferenceRequest):
    raw_payload = ''.join([m.content for m in req.messages])
    payload_hash = hashlib.sha256(raw_payload.encode()).hexdigest()

    quote = enclave.issue_evidence_quote(payload_hash)
    if not enclave.verify_quote(quote, payload_hash):
        raise HTTPException(status_code=403, detail='Attestation Failed')

    msg_dicts = [m.model_dump() for m in req.messages]
    pruning = pruner.prune_chat_history(msg_dicts)

    latest = pruning['pruned_messages'][-1]['content']
    sanitized_text, session_map = sanitizer.sanitize_context(latest)

    return {
        'model': req.model,
        'attestation': quote,
        'tokens_saved': pruning['tokens_saved'],
        'sanitized_prompt': sanitized_text,
        'sanitized_entities_count': len(session_map),
        'status': 'ENCLAVE_DISPATCH_AUTHORIZED'
    }

@app.get('/healthz')
def healthz():
    return {'status': 'HEALTHY', 'tee_measurement': enclave.platform_measurement}
