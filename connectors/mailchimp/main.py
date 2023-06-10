import requests
from dotenv import load_dotenv
import os
import json


class MailchimpConnector:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('MAILCHIMP_API_KEY')
        if self.api_key is None:
            raise ValueError(
                "MAILCHIMP_API_KEY not found in environment variables")

        self.server = os.getenv("MAILCHIMP_SERVER")
        self.base_url = f"https://{self.server}.api.mailchimp.com/3.0"

    # this returns the list ids and their names.
    def get_lists(self):
        url = f"{self.base_url}/lists"
        response = requests.get(url, auth=(
            "anystring", self.api_key))  # type: ignore

        response = response.json()

        # Extract the mailing lists
        mailing_lists = response['lists']
        return mailing_lists

        # Create a new list that includes only the id and name of each list
        # reduced_lists = [{'id': lst['id'], 'name': lst['name']}
        #                  for lst in mailing_lists]

        # return reduced_lists

    #  data = {
    #         "name": list_name,
    #         "contact": {
    #             "company": "Your Company",  # Add actual company name
    #             "address1": "Address Line 1",  # Add actual address
    #             "city": "City",  # Add actual city
    #             "state": "State",  # Add actual state
    #             "zip": "ZIP",  # Add actual zip code
    #             "country": "Country"  # Add actual country
    #         },
    #         # Add actual permission reminder
    #         "permission_reminder": "You're receiving this email because you signed up for updates from Our Company.",
    #         "campaign_defaults": {
    #             "from_name": "From Name",  # Add actual from name
    #             "from_email": "from@email.com",  # Add actual from email
    #             "subject": "",
    #             "language": "en"
    #         },
    #         "email_type_option": True
    #     }

    def create_list(self, data):
        url = f"{self.base_url}/lists"
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, auth=(
            "anystring", self.api_key), headers=headers, data=json.dumps(data))  # type: ignore
        # Handle potential errors here
        return response.json()

    def add_member_to_list(self, list_id, email_address, status='subscribed', merge_fields=None):
        url = f"{self.base_url}/lists/{list_id}/members"
        headers = {"Content-Type": "application/json"}
        data = {
            "email_address": email_address,
            "status": status,  # "subscribed", "unsubscribed", "cleaned", "pending"
            "merge_fields": merge_fields or {}
        }
        response = requests.post(url, auth=(
            "anystring", self.api_key), headers=headers, data=json.dumps(data))  # type: ignore
        # Handle potential errors here
        return response.json()


# if __name__ == "__main__":
#     # Create a connector object
#     connector = MailchimpConnector()

#     # Call get_lists on the connector object
#     lists = connector.get_lists()

#     # Do something with the lists. For example, print them:
#     print(lists)
