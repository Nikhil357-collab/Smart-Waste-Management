import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv("config/.env")

CHANNEL_ID = os.getenv("CHANNEL_ID")
READ_API_KEY = os.getenv("READ_API_KEY")

def get_thingspeak_data(results=50):
    url = (
        f"https://api.thingspeak.com/channels/"
        f"{CHANNEL_ID}/feeds.json"
        f"?api_key={READ_API_KEY}"
        f"&results={results}"
    )

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(
            f"ThingSpeak Error: {response.status_code}"
        )

    data = response.json()

    feeds = data.get("feeds", [])

    if not feeds:
        return pd.DataFrame()

    df = pd.DataFrame(feeds)

    return df