import time
from securekv.sanitizer.vault import CryptographicTokenSanitizer
from securekv.attestation.nras_provider import NVIDIAAttestationEnclave

def benchmark_latency():
    sanitizer = CryptographicTokenSanitizer()
    enclave = NVIDIAAttestationEnclave()
    sample = 'Enterprise audit trace: user=admin@internal.corp token=sk-99887766554433221100 action=unseal'
    
    start = time.perf_counter()
    iterations = 2000
    for _ in range(iterations):
        clean, s_map = sanitizer.sanitize_context(sample)
        quote = enclave.issue_evidence_quote('hash_sample')
        _ = sanitizer.rehydrate_stream(clean, s_map)
    
    avg_ms = ((time.perf_counter() - start) / iterations) * 1000
    print(f'[Benchmark] Average P99 Overhead per Inference Turn: {avg_ms:.3f} ms')

if __name__ == '__main__':
    benchmark_latency()
