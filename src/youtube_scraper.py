import os
from apify_client import ApifyClient


class YouTubeScraper:
    def __init__(self):
        self.client = ApifyClient(os.getenv("APIFY_TOKEN"))
        self.youtube_task_id = os.getenv("APIFY_YOUTUBE_TASK_ID")

    def extract_artist_from_url(self, youtube_url: str) -> str:
        """
        Uses Apify YouTube actor to retrieve metadata.
        Extracts artist name deterministically using fallback rules.
        """
        input = {"startUrls": [{"url": youtube_url}]}
        

        try:
            run = self.client.task(self.youtube_task_id).call(task_input=input)
            dataset = self.client.dataset(run["defaultDatasetId"]).iterate_items()

            for item in dataset:
                print(f"YouTube metadata keys: {item.keys()}")
                
                # Possible fields containing the artist name:
                if "artist" in item and item["artist"]:
                    return item["artist"].strip()

                if "channelName" in item and item["channelName"]:
                    return item["channelName"].strip()

                if "author" in item and item["author"]:
                    return item["author"].strip()

                if "channel" in item and item["channel"]:
                    return item["channel"].strip()

            raise ValueError("Could not extract artist name from YouTube metadata.")
        except Exception as e:
            print(f"Error extracting artist: {str(e)}")
            raise
        