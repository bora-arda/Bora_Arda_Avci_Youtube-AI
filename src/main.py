from dotenv import load_dotenv
load_dotenv() # LOADING ENVIRONMENT VARIABLES

import sys
import json
from src.youtube_scraper import YouTubeScraper
from src.llm_album_fetcher import AlbumFetcherLLM
from src.genius_scraper import GeniusScraper
from src.lyrics_processing import LyricsProcessor
from src.embedding import EmbeddingModel


def run_workflow(url: str, mode: str):
    try:
        # Creating instances of each class required
        yt = YouTubeScraper()
        llm = AlbumFetcherLLM()
        genius = GeniusScraper()
        proc = LyricsProcessor()
        embedder = EmbeddingModel()

        # Step 1: Artist
        print("Step 1: Extracting artist from YouTube...")
        artist = yt.extract_artist_from_url(url)
        print(f"Artist: {artist}")

        # Step 2: Album & songs
        print("\nStep 2: Fetching first album and tracks...")
        album_info = llm.get_first_album_and_tracks(artist) # Acquiring album info using llm
        album_name = album_info["album"]
        songs = album_info["songs"]
        print(f"Album: {album_name}")
        print(f"Songs: {len(songs)} tracks found")

        result_songs = []
        token_counts = []

        # Step 3: Lyrics + stats
        print("\nStep 3: Fetching lyrics and computing stats...")
        for i, song in enumerate(songs, 1):
            print(f"  [{i}/{len(songs)}] Processing: {song}")
            try:
                lyrics = genius.fetch_lyrics(artist, song) # Fetching lyrics
                stats = proc.process(lyrics) # Processing lyrics to acquire desired stats.
                result_songs.append({
                    "name": song,
                    **stats
                })
                token_counts.append(stats["lyrics_length_tokens"])
            except Exception as e:
                print(f"    Error processing '{song}': {str(e)}")
                # Skip this song and continue
                continue

        if not result_songs:
            raise ValueError("No songs were successfully processed")

        total_tokens = sum(token_counts) # Total token count
        avg_tokens = round(total_tokens / len(token_counts), 2) # Average token count

        final_json = {
            "artist": artist,
            "album_name": album_name,
            "songs": result_songs,
            "total_tokens_all_songs": total_tokens,
            "avg_tokens_per_song": avg_tokens
        }

        if mode == "json":
            return json.dumps(final_json, indent=2)

        elif mode == "hash":
            print("\nStep 4: Computing embedding hash...")
            token_string = ",".join(str(t) for t in token_counts)
            print(f"Token string: {token_string}")
            final_hash = embedder.embed_and_hash(token_string)
            return final_hash

        else:
            raise ValueError("Mode must be 'json' or 'hash'")
    
    except Exception as e:
        print(f"\nError in workflow: {str(e)}")
        raise
    