import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    "Authorization": os.getenv("TOKEN")
}

class Gather:
    def __init__(self, guild_id, channel_id, author_id):
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.author_id = author_id

    def gather_messages(self, offset=0):
        url = (f"https://discord.com/api/v9/guilds/{self.guild_id}/messages/search?"
               f"author_id={self.author_id}&channel_id={self.channel_id}&offset={offset}")

        return requests.get(url, headers=HEADERS).json()

    def fetch(self, iterations=1, default_offset=0):
        offset = default_offset
        for i in range(iterations):
            res = self.gather_messages(offset=offset)
            rate_limit = res.get("retry_after")
            messages = res.get("messages")

            if rate_limit:
                print(f"Rate limited, trying after {rate_limit} seconds")
                time.sleep(float(rate_limit))

            elif messages and type(messages) == list:
                for message in messages:
                    self.save("\n\n" + message[0]["content"])
                print(f"Completed {offset / 25} iteration")

            elif messages == []:
                print("That's it for this channel.")
                return

            else:
                print(f"Unexpect error: {res}")
            offset += 25
        print("Saved all messages in messages2.txt")

    def save(self, text):
        file = open("messages2.txt", "a")
        file.write(text)
        file.close()

gather = Gather(807140294276415510, 963346820443041842, 791950104680071188)
gather.fetch(50, default_offset=500)
