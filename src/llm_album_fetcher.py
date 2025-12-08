import os
import requests
from src.utils import safe_json_parse


class AlbumFetcherLLM:
    """
    This class used for creating the LLM object and use it to acquire desired knowledge. It is singer's first album in our case.
    openai/gpt-4o-mini chosen due to being very cheap and consistent. Free models can hallucinate or get blocked by rate-limit.
    """
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "openai/gpt-4o-mini"

    
    def get_first_album_and_tracks(self, artist: str) -> dict:
        prompt = f"""
        You are a music expert. Return ONLY valid JSON.

        Task:
        1. Identify the first released studio album of {artist}.
        2. List ALL songs in the album in ORIGINAL track order.

        Format:
        {{
          "album": "...",
          "songs": ["song1", "song2", "song3", ...]
        }}
        """

        try:
            # API request
            resp = requests.post(
                self.url,
                headers={"Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0
                }
            ).json()

            if "error" in resp:
                raise RuntimeError(
                f"LLM API Error {resp['error'].get('code')}: "
                f"{resp['error'].get('metadata', {}).get('raw', resp['error']['message'])}"
                )
            
            raw = resp["choices"][0]["message"]["content"]
            
            return safe_json_parse(raw)
        
        except Exception as e:
            print("RAW RESPONSE FROM API:", resp)
            raise e
        