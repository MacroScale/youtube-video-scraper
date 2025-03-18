import os
import time 
import json 
import requests

import googleapiclient.discovery
from googleapiclient.errors import HttpError  # Import HttpError
from dotenv import load_dotenv

# need a list of CATEGORIES to get videos from
QUERIES = [
    "cats",
    "dogs",
    "cooking",
    "technology",
    "music",
    "travel",
    "gaming",
    "fitness",
    "news",
    "tutorials",
    "fashion",
    "beauty",
    "diy",
    "art",
    "photography",
    "movies",
    "books",
    "science",
    "history",
    "education",
    "finance",
    "business",
    "startups",
    "marketing",
    "programming",
    "design",
    "productivity",
    "motivation",
    "inspiration",
    "meditation",
    "yoga",
    "sports",
    "football",
    "basketball",
    "cricket",
    "racing",
    "cars",
    "motorcycles",
    "food",
    "restaurants",
    "recipes",
    "health",
    "wellness",
    "parenting",
    "relationships",
    "gardening",
    "home decor",
    "real estate",
    "investing",
    "crypto",
]

# total amount of videos to scrape across all categories
TOTAL_AMOUNT = 50000

# Constants
OUTPUT_DIR = "out"
PROGRESS_FILE = os.path.join(OUTPUT_DIR, "progress.json")
DATA_FILE = os.path.join(OUTPUT_DIR, "youtube_data.json")


def get_youtube_service(api_key):
    """Creates and returns a YouTube Data API service object."""
    return googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

def search_videos(youtube, search_query, max_results=50, page_token=None):
    """Searches YouTube videos based on the given query."""
    request = youtube.search().list(
        part="snippet",
        maxResults=max_results,
        q=search_query,
        type="video",
        pageToken=page_token
    )
    return request.execute()

def get_video_details_batch(youtube, video_ids):
    """Retrieves detailed metadata for a batch of videos."""
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=",".join(video_ids)
    )
    return request.execute()

# write data to json file
def write_data(filename: str, new_data: list):
    """Writes video data to a JSON file, handling existing data."""
    try:
        with open(filename, 'r') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []

    # Combine data
    updated_data = existing_data + new_data

    with open(filename, 'w') as f:
        json.dump(updated_data, f, indent=4)

def save_progress(progress):
    """Saves the progress of data collection."""
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)

def load_progress():
    """Loads the progress of data collection."""
    try:
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"query_index": 0, "page_token": None, "videos_collected": 0}


# email when complete
def email_alert(msg, testing: bool):

    if testing:
        print(msg)
        return

    API_KEY = os.getenv("MAILJET_KEY") or ""
    SECRET = os.getenv("MAILJET_SECRET") or ""

    url = "https://api.mailjet.com/v3.1/send" 
    data = {
            "Messages":[
                {
                    "From": {
                        "Email": "macroscale.cloud@gmail.com",
                        "Name": "Macroscale"
                        },
                    "To": [
                        {
                            "Email": "brandongill123@gmail.com",
                            "Name": "Brandon"
                            }
                        ],
                    "Subject": "Macroscale - Youtube Scraper",
                    "HTMLPart": f"<b>{msg}</b>",
                    }
                ]
            }

    headers = {"Content-Type": "application/json"}
    res = requests.post(url, json=data, headers=headers, auth=(API_KEY, SECRET))
    print(res.text)

def main():

    print("starting main.py")

    # if not os.path.exists(OUTPUT_DIR):
    #     print("creating output directory")
    #     os.makedirs(OUTPUT_DIR)
    # else:
    #     print("output dir found")
    #
    #
    # print("loading env file")
    # load_dotenv()
    # print("env loaded")
    # TESTING: bool = os.getenv("TESTING", "false").lower() in ("true", "1", "yes")
    # print(f"testing status: {TESTING}")
    #
    # try:
    #     YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
    #     serv = get_youtube_service(YOUTUBE_API_KEY)
    #
    #     progress = load_progress()
    #     query_index = progress["query_index"]
    #     next_page_token = progress["page_token"]
    #     videos_collected = progress["videos_collected"]
    #
    #     print(f"Starting from: query_index={query_index}, videos_collected={videos_collected}")  # Added
    #
    #     video_data = []
    #
    #     while videos_collected < TOTAL_AMOUNT:
    #         query = QUERIES[query_index]
    #         print(f"Processing query: {query}") 
    #
    #         try:
    #             search_response = search_videos(serv, query, page_token=next_page_token)
    #             video_ids = [item["id"]["videoId"] for item in search_response.get("items", []) if "videoId" in item["id"]]
    #
    #             if video_ids:
    #                 print(f"Found {len(video_ids)} videos in this batch.")
    #                 details_response = get_video_details_batch(serv, video_ids)
    #                 video_data.extend(details_response.get("items", []))
    #                 videos_collected += len(video_ids)
    #
    #             next_page_token = search_response.get("nextPageToken")
    #
    #             if not next_page_token:
    #                 query_index += 1
    #                 next_page_token = None
    #                 if query_index >= len(QUERIES):
    #                     query_index = 0 
    #             time.sleep(0.5)
    #
    #             if videos_collected % 1000 == 0:
    #                 print(f"Collected {videos_collected} videos.")
    #                 save_progress({"query_index": query_index, "page_token": next_page_token, "videos_collected": videos_collected})
    #
    #         except HttpError as e:
    #             if e.resp.status == 403 and "quotaExceeded" in str(e):
    #                 print("Quota exceeded. Retrying in 1 hour.")
    #                 time.sleep(3600) # wait one hour
    #             else:
    #                 print(f"An HTTP error occurred: {e}")
    #                 time.sleep(60) # wait one min on other errs
    #
    #         except Exception as e:
    #             print(f"An error occured: {e}")
    #             time.sleep(60) # wait one min on other errs
    #
    #     write_data(DATA_FILE, video_data)
    #     save_progress({"query_index": query_index, "page_token": next_page_token, "videos_collected": videos_collected})
    #
    #     msg = "The program has finished successfully, all data has been acquired"
    #     email_alert(msg, TESTING)
    #
    # except Exception as err:
    #     msg = f"There was an error that has caused the program to crash: {err}"
    #     email_alert(msg, TESTING)

if __name__ == "__main__":
    main()
