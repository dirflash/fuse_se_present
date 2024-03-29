content = []


# Function to generate the column setup
def create_column_setup(column_data):
    return {
        "type": "Column",
        "width": "auto",
        "items": [
            {"type": "Input.Toggle", "title": str(y), "id": str(y), "spacing": "None"}
            for y in column_data
        ],
    }


def letter_list(first_letter_sets):
    # Now first_letter_sets contains a set of strings for each unique first letter
    for letter, string_set in first_letter_sets.items():
        print(f"Strings starting with {letter}: {sorted(string_set)}")

    print(f"a list of sets: {first_letter_sets['a']}")
    # convert the set to an ordered list
    a_list = sorted(list(first_letter_sets["a"]))
    # convert the list into a list of list
    a_list = [a_list]
    print(f"a list: {a_list}")


def present_card(chunked_list):
    """for x in chunked_list:
    content.append(create_column_setup(x))"""

    content = chunked_list
    # columns_setup = [create_column_setup(column) for column in chunked_list]

    # letter_lists = letter_list(first_letter_sets)
    # print(f"letter list: {letter_lists}")

    card = {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": {
            "type": "AdaptiveCard",
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.3",
            "body": [
                {
                    "type": "Container",
                    "items": [
                        *content,
                        {
                            "type": "TextBlock",
                            "text": " ",
                            "wrap": True,
                            "separator": True,
                            "spacing": "None",
                        },
                        {
                            "type": "Container",
                            "separator": False,
                        },
                        {
                            "type": "ColumnSet",
                            "columns": [
                                {
                                    "type": "Column",
                                    "width": "auto",
                                    "items": [
                                        {
                                            "type": "ActionSet",
                                            "actions": [
                                                {
                                                    "type": "Action.Submit",
                                                    "title": "Submit",
                                                    "associatedInputs": "auto",
                                                }
                                            ],
                                            "horizontalAlignment": "Left",
                                            "spacing": "None",
                                        }
                                    ],
                                    "spacing": "None",
                                },
                                {
                                    "type": "Column",
                                    "width": "auto",
                                    "spacing": "None",
                                    "isVisible": False,
                                },
                            ],
                            "spacing": "None",
                        },
                    ],
                },
            ],
        },
    }
    # print(card)
    return card
