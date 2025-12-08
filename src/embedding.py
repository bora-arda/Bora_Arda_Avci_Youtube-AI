import torch
from transformers import AutoModel, AutoTokenizer
from src.utils import md5_hash


class EmbeddingModel:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            "nomic-ai/nomic-embed-text-v1.5",
            trust_remote_code=True
        )
        self.model = AutoModel.from_pretrained(
            "nomic-ai/nomic-embed-text-v1.5",
            trust_remote_code=True,
            torch_dtype=torch.float32
        )
        self.model.eval() # To make model as deterministic as possible. It is required in the task description.

    def embed_and_hash(self, token_string: str) -> str:
        """
        1. Embeds the concatenated token count string
        2. Formats 768 floats with 10 decimal places
        3. MD5 hash of final formatted string
        """
        # This line required by nomic-embed-text-v1.5, it sets a prefix. "search_document" is selected due to better explanation of lyrics. 
        prefixed_text = f"search_document: {token_string}"
        
        inputs = self.tokenizer(
            prefixed_text, 
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        )
        
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Mean pooling on last hidden state. Shape: (batch_size, sequence_length, hidden_size)
        # Combining all token vectors into one vector. Stable for hashing or similarity search
        vec = outputs.last_hidden_state.mean(dim=1)[0]  # 768 floats

        # Format each float with exactly 10 decimal places. Must fix the formatting to get consistent MD5 hashes each time.
        formatted = ",".join(f"{float(v):.10f}" for v in vec.tolist())

        return md5_hash(formatted)
    