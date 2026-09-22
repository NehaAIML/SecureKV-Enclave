from typing import Optional, Dict, Any
from securekv.sanitizer.vault import CryptographicTokenSanitizer
from securekv.attestation.nras_provider import NVIDIAAttestationEnclave

class NeMoZeroTrustGuardrail:
    """
    Drop-in Action Extension for NVIDIA NeMo Guardrails configs (colang/actions.py).
    Enforces hardware attestation verification and deterministic token masking.
    """
    def __init__(self):
        self.sanitizer = CryptographicTokenSanitizer()
        self.enclave = NVIDIAAttestationEnclave()

    async def pre_llm_sanitize_action(self, user_input: str) -> Dict[str, Any]:
        clean_input, mapping = self.sanitizer.sanitize_context(user_input)
        quote = self.enclave.issue_evidence_quote(clean_input)
        return {
            "sanitized_input": clean_input,
            "session_map": mapping,
            "attested": quote.get("status") == "HARDWARE_VERIFIED"
        }

    async def post_llm_rehydrate_action(self, llm_output: str, session_map: Dict[str, str]) -> str:
        return self.sanitizer.rehydrate_stream(llm_output, session_map)
