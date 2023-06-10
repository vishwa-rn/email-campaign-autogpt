import tkinter as tk
from tkinter import filedialog
from user_details import user_details
from langchain.base_language import BaseLanguageModel
import csv
import json
from connectors.mailchimp.main import MailchimpConnector


def select_file():
    # Create a root window and immediately withdraw it
    # We do this because we only want the file dialog to show up
    root = tk.Tk()
    root.withdraw()

    # Show an "Open" dialog box and return the path of the selected file
    filepath = filedialog.askopenfilename()

    return filepath


def read_file(filepath, connector, list_id):
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        emails = [row['email'] for row in reader]
        for email in emails:
            response = connector.add_member_to_list(
                list_id=list_id, email_address=email)
            print(response)

        csvFile = csv.reader(file)
        for lines in csvFile:
            print(lines)
    return csvFile


def upload_leads_excel_chain(memory: dict):
    inputs = {
        "list_name": {
            "question": "What is the list name?"
        },
        "from_name": {
            "question": "What is the FROM NAME for your campaign?",
        },
        "from_email": {
            "question": "What is your FROM EMAIL?",
        }
    }

    answers = {}

    for key, value in inputs.items():
        answer = input(value['question'] + " ")
        answers[key] = answer

    data = {
        "name": answers["list_name"],
        "contact": user_details['contact'],
        "campaign_defaults": {
            "from_name": answers['from_name'],
            "from_email": answers['from_email'],
            "subject": "",
            "language": "en"
        },
        "permission_reminder": user_details["permission_reminder"],
        "email_type_option": True
    }

    connector = MailchimpConnector()
    response = connector.create_list(data=data)
    new_list = json.loads(response)

    memory["mailchimp_leads_list_id"] = new_list["id"]
    filepath = select_file()
    contents = []
    if filepath:
        contents = read_file(filepath, connector=connector,
                             list_id=memory["mailchimp_leads_list_id"])
        print(contents)
    else:
        print("No file selected.")

    print(response)


# with open('connectors/mailchimp/data/testing.csv', 'r') as file:
#     csvFile = csv.reader(file)
#     reader = csv.DictReader(file)
#     emails = [row['email'] for row in reader]
#     for email in emails:
#         response = connector.add_member_to_list(
#             list_id=memory["mailchimp_leads_list_id"], email_address=email)
#         print(response)

# print(connector.get_lists())


# def main():
#     filepath = select_file()
#     contents = []
#     if filepath:
#         contents = read_file(filepath, contents)
#         print(contents)
#     else:
#         print("No file selected.")


# if __name__ == "__main__":
#     main()
