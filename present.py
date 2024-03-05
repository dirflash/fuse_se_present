"""
Obtain a set of SE's from MongoDB that have accepted an invitation to attend a FUSE session.
It then creates a list of first letters from the SE names.
Chunks the list into a dictionary of first letters to SE names.
Formats a Webex App card to display the names as a multi-select grouped by first letters.
Sends the formatted card to the FUSE administrator with the purpose of selecting actual
attendees to be paired.
"""

import json
from typing import Any, Dict, List

import requests

from cards import present_card as pc
from utils import preferences as p

FUSE_DATE = "2/9/2024"

# Get attendees from cwa_attendees Mongo collection
attendees: Dict[Any, Any] = p.cwa_attendees.find_one(
    {"date": FUSE_DATE}, {"_id": 0}
)  # type: ignore

se_set = sorted(
    set(attendees["accepted"] + attendees["no_response"] + attendees["tentative"])
)

card_body: List[Dict] = []

# unique first letters in se_set
unique_first_letters = sorted({x[0] for x in se_set})
print(f"Unique first letters in se_set: {unique_first_letters}")

# Create a dictionary where each key is a first letter and each value is an empty list
first_letter_lists: dict = {letter: [] for letter in unique_first_letters}

# Populate the lists with strings from se_set that start with the corresponding letter
for item in se_set:
    if item:  # make sure the string is not empty
        first_letter = item[0]  # get the first character of the string
        first_letter_lists[first_letter].append(
            item
        )  # add the string to the correct list

# --> Now first_letter_lists contains a list of strings for each unique first letter
# for letter, string_list in first_letter_lists.items():
#     print(f"Strings starting with {letter}: {sorted(string_list)}")

# Chunking the lists
N = 3  # This is the number of items in the main lists
chunked_lists_dict = {}

for letter, string_list in first_letter_lists.items():
    if len(string_list) >= N:  # only create chunked lists if there are N or more items
        chunked_lists = []
        for i in range(N):
            temp = []
            for j in range(i, len(string_list) - (len(string_list) % N), N):
                temp.append(string_list[j])
            chunked_lists.append(temp)

        # Adding remaining items to the lists
        for i in range(len(string_list) - (len(string_list) % N), len(string_list)):
            chunked_lists[i % N].append(string_list[i])

        chunked_lists_dict[letter] = chunked_lists
    else:  # if there are less than N items, create a separate list for each item
        chunked_lists_dict[letter] = [[item] for item in string_list]

# Now chunked_lists_dict contains chunked lists for each unique first letter
for letter, chunked_lists in chunked_lists_dict.items():
    print(f"Chunked lists for strings starting with {letter}: {chunked_lists}")

card_first_letter = []

for x in unique_first_letters:
    # Append the header for the first letter
    card_first_letter.append(
        {"spacing": "None", "text": x.upper(), "type": "TextBlock", "separator": True}
    )
    # Initialize the column set for the current first letter
    column_set: Dict[str, Any] = {"type": "ColumnSet", "columns": []}

    # Add columns to the column set for the current first letter
    for z in chunked_lists_dict[x]:
        column_items = []
        for y in z:
            column_items.append(
                {"type": "Input.Toggle", "title": y, "id": y, "spacing": "None"}
            )

        column_set["columns"].append(
            {
                "type": "Column",
                "width": "stretch",
                "items": column_items,
            }
        )

    # If there are fewer than 'N' columns, pad with empty columns
    while len(column_set["columns"]) < N:
        column_set["columns"].append(
            {
                "type": "Column",
                "width": "stretch",
                "items": [{"type": "TextBlock", "isVisible": False}],
            }
        )

    # Append the fully constructed column set to the card
    card_first_letter.append(column_set)

POST_MSG_URL = "https://webexapis.com/v1/messages/"


email = f"{p.test_person}@cisco.com"
card = pc.present_card(card_first_letter)

headers = {
    "Authorization": p.test_webex_bearer,
    "Content-Type": "application/json",
}

payload = {
    "toPersonEmail": email,
    "markdown": "Adaptive card response. Open the message on a supported client to respond.",
    "attachments": card,
}

response = requests.request(
    "POST", POST_MSG_URL, headers=headers, data=json.dumps(payload), timeout=10
)
