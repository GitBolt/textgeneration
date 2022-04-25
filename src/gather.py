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
                print(f"Completed {offset / 25} iteration [offset {offset}]")

            elif messages == []:
                print(f"That's it for this channel: {self.channel_id}")
                return
            elif res.get("code") == 50001:
                print("Access not there, skipping channel")
                return
            else:
                print(f"Unexpect error: {res}")
            offset += 25
        print("Saved all messages in messages2.txt")

    def save(self, text):
        file = open("kash_messages.txt", "a")
        file.write(text)
        file.close()

lst = [888684613097107508, 890515045367291914, 890513602044366868, 935188442059518022, 890513750690496532, 863987156405977129, 894872542312013864, 924214318701088768, 902193964361347072, 965617555194646618, 890513695283740714, 857091161612484632, 890513647330295848, 904984710571233290, 965624096538898542, 912623997508804628, 965630092564889640, 961194371141754960, 932559247483502612, 965632887007346751, 965171139708092436, 908526102316732469, 961562518432645140, 890514079578484776, 912638543870951464, 940270866674106408, 913423600005042227, 952868607686230026, 922095818746503258, 966697345217626174, 967356632222814218, 897006782101192734, 955419355087245312, 955423704463048745, 920989699017965568, 902481959387803690, 921077233337139301, 941266840963919902, 944600196178915360, 946372605760376842, 946432322020999208, 953248072052404256, 956243987348484197, 958333641774231622, 937288648880189501, 937425213392572517, 937288786897940580, 939139119458693120, 940148023588163614, 940192998648602644, 941307902201843802, 897627725383213147, 896977574184501308, 931523932538949632, 888684613097107509, 894869026088554526, 966033825161445416, 894868183578722314, 894868805585616917, 935214763259072532, 951396554412027914, 942801570834305064, 918158775519703051, 958302952991383562, 900236437394432030, 935555013940478004, 927584541328158761, 930006232289382400, 925039142885290065, 907828746457853982, 916982748097429526, 920743443356069968, 917343587774103592, 897666131991593082, 900441728216092673]
for i in lst:
    gather = Gather(857091160295866388, i, 355979301750833162)
    gather.fetch(100, default_offset=0)
