from typing import List, Dict, Any

class SemanticTokenBudgetManager:
    def __init__(self, target_max_tokens: int = 4096):
        self.target_max_tokens = target_max_tokens

    def estimate_tokens(self, text: str) -> int:
        return max(1, len(text) // 4)

    def prune_chat_history(self, messages: List[Dict[str, str]], preserve_last_k: int = 2) -> Dict[str, Any]:
        initial_tokens = sum(self.estimate_tokens(m['content']) for m in messages)
        if len(messages) <= preserve_last_k + 1:
            return {'pruned_messages': messages, 'tokens_saved': 0, 'final_tokens': initial_tokens}

        system_msg = [m for m in messages if m.get('role') == 'system'][:1]
        conversational = [m for m in messages if m.get('role') != 'system']
        recent = conversational[-preserve_last_k:]
        historical = conversational[:-preserve_last_k]

        compressed = []
        for msg in historical:
            content = ' '.join(msg['content'].split())
            if len(content) > 120:
                content = content[:100] + '... [compacted]'
            compressed.append({'role': msg['role'], 'content': content})

        final_messages = system_msg + compressed + recent
        final_tokens = sum(self.estimate_tokens(m['content']) for m in final_messages)
        return {
            'pruned_messages': final_messages,
            'tokens_saved': max(0, initial_tokens - final_tokens),
            'final_tokens': final_tokens
        }
