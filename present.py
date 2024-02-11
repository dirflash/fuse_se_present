import json

import requests

from cards import present_card as pc
from utils import preferences as p

se_list = []


def chunk_into_n(lst, n):
    # Calculate the length of each chunk
    chunk_size, remainder = divmod(len(lst), n)
    # Create the list of chunks with the calculated size
    chunks = [
        lst[
            i * chunk_size
            + min(i, remainder) : (i + 1) * chunk_size  # noqa: E203, W503
            + min(i + 1, remainder)  # noqa: W503
        ]
        for i in range(n)
    ]
    return chunks


for _ in range(1, 16):
    se_list.append(f"se{_:02}")
print(se_list)
# Sample se_list:
# ['se01', 'se02', 'se03', 'se04', 'se05', 'se06', 'se07', 'se08', 'se09', 'se10', 'se11,
# 'se12', 'se13', 'se14', 'se15']

chunked_list = chunk_into_n(se_list, 5)
print(chunked_list)
# Sample chunked_list:
# [['se01', 'se02', 'se03'], ['se04', 'se05', 'se06'], ['se07', 'se08', 'se09'],
# ['se10', 'se11', 'se12'], ['se13', 'se14', 'se15']]

post_msg_url = "https://webexapis.com/v1/messages/"
email = f"{p.test_person}@cisco.com"
card = pc.present_card(chunked_list)

headers = {
    "Authorization": p.test_webex_bearer,
    "Content-Type": "application/json",
}

payload = {
    "toPersonEmail": email,
    "markdown": "Adaptive card response. Open the message on a supported client to respond.",
    "attachments": card,
}

try:
    response = requests.request("POST", post_msg_url, headers=headers, data=json.dumps(payload))
    print(response.status_code)
except Exception as e:
    print(e)
    print("Error sending message to Webex")

"""
Sample response from submitting the card:
{
    "id": "XXXXXXX...",
    "type": "submit",
    "messageId": "XXXXXXX...",
    "inputs": {
        "present_ses": "present_ses",
        "se01": "true",
        "se02": "false",
        "se03": "true",
        "se04": "false",
        "se05": "true",
        "se06": "false",
        "se07": "false",
        "se08": "false",
        "se09": "false",
        "se10": "false",
        "se11": "true",
        "se12": "false",
        "se13": "true",
        "se14": "false",
        "se15": "true"
    },
    "personId": "XXXXXXX...",
    "roomId": "XXXXXXX...",
    "created": "2024-02-11T01:23:11.782Z"
}

Check boxes checked and submitted are 'true', unchecked are 'false'.

"""
