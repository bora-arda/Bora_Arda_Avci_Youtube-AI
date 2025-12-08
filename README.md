# YouTube AI Scraping Agent

## Project Overview
This agent extracts artist information from YouTube, fetches their first album's songs using an LLM, scrapes lyrics from Genius.com, computes token metrics, and generates embeddings.

## Setup Instructions

### 1. Install Dependencies
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Get API Keys



# YouTube AI Scraping Agent

## Overview
This agent extracts artist information from YouTube, fetches their first album's songs using an LLM, scrapes lyrics from Genius.com, computes token metrics, and generates embeddings with hash output.

## Project Structure
```
.
├── .venv/                      # Virtual environment
├── src/
│   ├── __init__.py
│   ├── embedding.py            # Embedding model and hash computation
│   ├── genius_scraper.py       # Genius.com lyrics scraper
│   ├── llm_album_fetcher.py    # LLM for album information
│   ├── lyrics_processing.py    # Token counting and statistics
│   ├── main.py                 # Main workflow orchestration
│   ├── utils.py                # Utility functions (JSON parsing, MD5 hash)
│   └── youtube_scraper.py      # YouTube metadata extraction
├── .env                        # API keys (DO NOT COMMIT)
├── .gitignore                  # Git ignore file
├── Bora_Arda_Avci_YouTube_AI.py  # Entry point script
├── README.md                   # This file
└── requirements.txt            # Python dependencies
```

## Prerequisites
- Python 3.8 or higher
- pip package manager
- Internet connection for API calls

## Setup Instructions

### 1. Clone/Download the Project
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate it
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Note:** First run will download the embedding model (~500MB). This is cached for subsequent runs.

### 4. Set Up API Keys

Create a `.env` file in the project root directory with the following structure:

```env
APIFY_TOKEN=your_apify_token_here
APIFY_YOUTUBE_TASK_ID=your_youtube_task_id_here
APIFY_GENIUS_TASK_ID=your_genius_task_id_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

#### A. Apify Token
1. Sign up at https://apify.com/
2. Go to Settings → Integrations
3. Copy your API token
4. Paste it as `APIFY_TOKEN` in `.env`

#### B. Apify YouTube Scraper Task
1. Go to https://console.apify.com/actors/h7sDV53CddomktSi5/input
2. Click "Try for free" and configure the actor
3. Save as Task
4. Copy the Task ID (format: `username~taskname`)
5. Paste it as `APIFY_YOUTUBE_TASK_ID` in `.env`

#### C. Apify Genius Scraper Task

1. Go to https://console.apify.com/actors/Zutb7WV9AFZTYtv0F/input
2. Configure to scrape genius.com
3. Start your free trial
4. Save as Task
5. Copy the Task ID (format: `username~taskname`)
6. Paste it as `APIFY_GENIUS_TASK_ID` in `.env`

#### D. OpenRouter API Key
1. Go to https://openrouter.ai/
2. Sign in and get your API key
3. Create a new API key
4. Copy the key (starts with `sk-or-v1-`)
5. Paste it as `OPENROUTER_API_KEY` in `.env`

**Free model used:** `openai/gpt-4o-mini`

## Usage

### Command Format
```bash
python3 Bora_Arda_Avci_YouTube_AI.py <youtube_url> <mode>
```

**Modes:**
- `json` - Returns detailed JSON output with song statistics
- `hash` - Returns MD5 hash of the embedding vector

### Examples

#### Get JSON Output
```bash
python3 Bora_Arda_Avci_YouTube_AI.py "https://www.youtube.com/watch?v=rSaC-YbSDpo" json
```

**Expected Output:**
```json
{
  "artist": "Madonna",
  "album_name": "Madonna",
  "songs": [
    {
      "name": "Lucky Star",
      "lyrics_length_chars": 1234,
      "lyrics_length_words": 234,
      "lyrics_length_tokens": 345,
      "tokens_per_word": 1.47,
      "lyrics_hash": "abc123..."
    },
    ...
  ],
  "total_tokens_all_songs": 5047,
  "avg_tokens_per_song": 630.88
}
```

#### Get Hash Output
```bash
python3 Bora_Arda_Avci_YouTube_AI.py "https://www.youtube.com/watch?v=rSaC-YbSDpo" hash
```

**Expected Output:**
```
4ae6acfbd3ccc56d4a62b3f3a4f3eb1f
```

## How It Works

### Workflow Steps

1. **Extract Artist from YouTube**
   - Uses Apify YouTube Scraper to fetch video metadata
   - Extracts artist name from available fields (artist, channelName, author)

2. **Fetch First Album Information**
   - Queries LLM (via OpenRouter) to identify artist's first studio album
   - Retrieves complete track listing in original release order

3. **Scrape Lyrics from Genius.com**
   - For each song, constructs Genius URL slug
   - Uses Apify to scrape lyrics from Genius.com
   - Extracts raw text of lyrics

4. **Calculate Token Metrics**
   - Uses tiktoken with `cl100k_base` encoding
   - Computes:
     - Total token count
     - Character count
     - Word count
     - Tokens-per-word ratio
     - MD5 hash of raw lyrics

5. **Generate Embedding and Hash**
   - Concatenates token counts into a comma-separated string
   - Generates 768-dimensional embedding using `nomic-ai/nomic-embed-text-v1.5`
   - Formats each float to 10 decimal places
   - Computes MD5 hash of formatted embedding string

## Dependencies

- `apify-client==1.7.1` - Apify API client
- `python-dotenv==1.0.0` - Environment variable management
- `requests==2.31.0` - HTTP requests for LLM API
- `tiktoken==0.5.2` - Token counting (OpenAI tokenizer)
- `torch==2.1.2` - PyTorch for model operations
- `transformers==4.36.2` - Hugging Face transformers library
- `sentencepiece==0.1.99` - Tokenization support
- `protobuf==4.25.1` - Protocol buffers support

## Error Handling

The system includes comprehensive error handling:

- **API Failures:** Logged with detailed error messages
- **Missing Lyrics:** Songs that fail to scrape are skipped, processing continues
- **Invalid JSON:** LLM responses are parsed defensively with fallback mechanisms
- **Network Issues:** All API calls are wrapped in try-catch blocks

## Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'dotenv'"**
- Solution: Ensure virtual environment is activated
- Run: `pip install -r requirements.txt`

**"Could not extract artist name from YouTube metadata"**
- Solution: Verify YouTube Task ID is correct in `.env`
- Check that the task is properly configured in Apify

**"Lyrics not found for: [song name]"**
- Solution: Verify Genius Task ID is correct
- The song name might not match exactly on Genius.com
- Check Genius scraper configuration in Apify

**"Invalid API key" or "Unauthorized"**
- Solution: Double-check all API keys in `.env` file
- Ensure no extra spaces or quotes around values
- Verify API keys are still valid (not expired)

**"Rate limit exceeded"**
- Solution: Wait a few minutes before retrying
- Free tier APIs have usage limits
- Consider upgrading API plan if needed

**Windows: "python3: command not found"**
- Solution: Use `python` instead of `python3` on Windows
- Or add `python3.exe` alias (copy `python.exe` → `python3.exe`)

### Debug Mode

To see detailed logging, the script prints progress at each step:
- Step 1: Artist extraction
- Step 2: Album fetching
- Step 3: Individual song processing
- Step 4: Embedding computation

## Performance Notes

- **First Run:** ~2-5 minutes (includes model download)
- **Subsequent Runs:** ~30-60 seconds (model cached)
- **Processing Time:** Varies based on album length (typically 8-12 songs)
- **Network Dependency:** All steps require internet connectivity

## Disk Space

- **Virtual Environment:** ~500 MB
- **Embedding Model Cache:** ~500-800 MB
- **Total:** ~1-1.5 GB

Cache location (Windows): `C:\Users\<YourName>\AppData\Local\huggingface\`

To clean up after project completion:
```bash
# Delete virtual environment
rmdir /s .venv

# Delete model cache (Windows)
# Navigate to: %LOCALAPPDATA%\huggingface
# Delete the folder manually
```

## Testing

Test with the Madonna example from the specification:

```bash
python3 Bora_Arda_Avci_YouTube_AI.py "https://www.youtube.com/watch?v=rSaC-YbSDpo" json
```

**Expected Results:**
- Artist: Madonna
- Album: Madonna (first studio album, 1983)
- Songs: 8 tracks including "Lucky Star", "Borderline", "Holiday", etc.

## Important Notes

- **API Keys Security:** Never commit your `.env` file to version control
- **Deterministic Output:** Same input produces same output (with same APIs)
- **Free Tier Limits:** Be mindful of API rate limits on free accounts
- **Model Download:** First execution downloads ~500MB embedding model
- **Cross-Platform:** Works on Windows, macOS, and Linux

## Support

For issues related to:
- **Apify:** Check https://docs.apify.com/
- **OpenRouter:** Check https://openrouter.ai/docs
- **Transformers:** Check https://huggingface.co/docs/transformers/

## License

This project was created as a technical assessment for AIMultiple. The code and assessment content are proprietary to AIMultiple and should not be published or distributed.

## Author

Bora Arda Avcı

## Submission

Repository: [Private GitHub/Bitbucket repository]
Invited: github@aimultiple.com
Contact: hr@aimultiple.com, cem@aimultiple.com