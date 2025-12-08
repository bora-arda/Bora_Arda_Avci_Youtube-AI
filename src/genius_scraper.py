import os
import re
from apify_client import ApifyClient


class GeniusScraper:
    def __init__(self):
        self.client = ApifyClient(os.getenv("APIFY_TOKEN"))
        self.genius_task_id = os.getenv("APIFY_GENIUS_TASK_ID")

    def _make_search_query(self, artist: str, song: str) -> str:
        """
        Build a clean search query string for the actor input, e.g. "Rihanna Diamonds".
        Only printable characters and collapse whitespace.
        """
        def clean(s: str) -> str:
            s = s.strip()
            s = re.sub(r"\s+", " ", s)       
            s = re.sub(r"[^\w\s'()-]", "", s)
            return s

        artist_clean = clean(artist)
        song_clean = clean(song)
        return f"{artist_clean} {song_clean}"

    def fetch_lyrics(self, artist: str, song: str) -> str:
        """
        Scrapes lyrics for a given song using Apify's Genius actor.
        """
        query = self._make_search_query(artist, song)
        print(f"Searching lyrics of: {query}")

        input = {
            "search": query,
            "searchMode": "song"
        }

        try:
            # This sends a request to Apify to create a run of that task with the given input dictionary.
            run = self.client.task(self.genius_task_id).call(task_input=input) 
            
            # Accesses the dataset id where the actor wrote its results
            dataset = self.client.dataset(run["defaultDatasetId"]).iterate_items()


            for item in dataset: # Iterate over each result item produced by the actor.
                if "lyrics" in item and item["lyrics"]:
                    return item["lyrics"].strip() # Returns lyrics

            raise ValueError(f"Lyrics not found for: {song}")
        except Exception as e:
            print(f"Error fetching lyrics for '{song}': {str(e)}")
            raise
        