
# Function to generate the column setup
def create_column_setup(column_data):
    return {
        "type": "Column",
        "width": "auto",
        "items": [
            {
                "type": "Input.Toggle",
                "title": str(y),
                "id": str(y),
                "spacing": "None"
            }
            for y in column_data
        ]
    }


def present_card(chunked_list):
    columns_setup = [create_column_setup(column) for column in chunked_list]

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
                        {
                            "type": "ColumnSet",
                            "columns": [
                                columns_setup[0],
                                columns_setup[1],
                                columns_setup[2],
                                columns_setup[3],
                                columns_setup[4],
                            ],
                        }
                    ],
                },
                {
                    "type": "Container",
                    "items": [
                        {
                            "type": "ColumnSet",
                            "columns": [
                                {
                                    "type": "Column",
                                    "width": "stretch",
                                    "spacing": "None",
                                    "isVisible": False,
                                    "items": [
                                        {
                                            "type": "Input.Text",
                                            "isVisible": False,
                                            "id": "present_ses",
                                            "value": "present_ses",
                                            "spacing": "None",
                                        }
                                    ],
                                },
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
                        }
                    ],
                },
            ],
        },
    }
    return card
