# YouTube Video Scraper

This script scrapes metadata from YouTube videos across a wide range of categories.

## Features

* Searches 50 predefined topics
* Rotates through multiple API keys to manage quota limits
* Automatically saves progress and can resume scraping
* Optional email alerts via Mailjet upon completion

## Setup

1. **Install dependencies**

```bash
uv sync
```

2. **Set up environment variables**

Create a `.env` file in the project root:

```dotenv
YOUTUBE_API_KEY_1=your_key_1
YOUTUBE_API_KEY_2=your_key_2
...

MAILJET_KEY=your_mailjet_key
MAILJET_SECRET=your_mailjet_secret
TESTING=true  # Set to false to enable email alerts
```

3. **Run the scraper**

```bash
uv run main.py
```

## Output

* `out/youtube_data.json`: Incremental results
* `out/all_youtube_data.json`: Final data dump
* `out/progress.json`: Tracks progress for resuming

## Notes

* The script automatically saves progress and can be safely 
interrupted and resumed.
* Email notifications are optional and disabled when `TESTING=true`.
