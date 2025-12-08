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

#### A. Apify Token
1. Sign up at https://apify.com/
2. Go to Settings → Integrations
3. Copy your API token

#### B. Create Apify YouTube Task
1. Go to https://console.apify.com/actors/h7sDV53CddomktSi5/input
3. Click "Try for free"
4. Save as Task
5. Copy the Task ID (format: `username~taskname`)

#### C. Create Apify Genius Task
1. Go to https://console.apify.com/actors/Zutb7WV9AFZTYtv0F/input
2. Configure to scrape genius.com
3. Start your free trial
4. Save as Task
5. Copy the Task ID (format: `username~taskname`)

#### D. OpenRouter API Key
1. Go to https://openrouter.ai/
2. Sign in and get your API key

