CHOOSE_FROM_LISTS_PROMPT = """
You are given a json of lists (id and name as the fields for each list). Your task to ask the user to choose from the options.

For example:

Instruction:
"Given the following Mailchimp lists in JSON format, generate a list of options for the user to choose from for their email campaign."

JSON:
[
{{"id": "11c96381fc", "name": "BLACK PROPELLER"}},
{{"id": "3605614fe5", "name": "Pixis"}},
{{"id": "6677798d7f", "name": "WEBINAR FINAL REGISTRANT"}}
]

Choose from the following lists for your email campaign:
1. "BLACK PROPELLER" (List ID: 11c96381fc)
2. "Pixis" (List ID: 3605614fe5)
3. "WEBINAR FINAL REGISTRANT" (List ID: 6677798d7f)

Please enter the number corresponding to the list you would like to use for your email campaign:

Begin!
Instruction:
"Given the following Mailchimp lists in JSON format, generate a list of options for the user to choose from for their email campaign."

JSON: {json}

Choose from the following lists for your email campaign:
"""

CHOOSE_FROM_LISTS_SELECTION_PROMPT = """Your task is to return the formatted result.

Example:

Choose from the following lists for your email campaign:
1. "YELLO STONE" (List ID: 11123b21fc)
2. "Automake it" (List ID: 2134b23a12)
3. "Hackathon list" (List ID: 6677798d7f)

User choice: 3

Answer: {{"list_id": "6677798d7f", "list_name": "Hackathon list" }}

{questions}

User choice: {user_choice}

Answer:
"""
