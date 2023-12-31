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
        # return mailing_lists

        # Create a new list that includes only the id and name of each list
        reduced_lists = [{'id': lst['id'], 'name': lst['name']}
                         for lst in mailing_lists]

        return reduced_lists

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

    def create_campaign(self, campaign_type: str, list_id: str, campaign_title: str, from_name: str, reply_to: str, subject_line: str):
        url = f"{self.base_url}/campaigns"
        headers = {"Content-Type": "application/json"}
        data = {
            "type": campaign_type,
            "recipients": {
                "list_id": list_id
            },
            "settings": {
                "subject_line": subject_line,
                "title": campaign_title,
                "from_name": from_name,
                "reply_to": reply_to
            }
        }

        response = requests.post(url, auth=(
            "anystring", self.api_key), headers=headers, data=json.dumps(data))  # type: ignore
        return response.json()

    def get_campaigns(self):
        url = f"{self.base_url}/campaigns"
        headers = {"Content-Type": "application/json"}

        response = requests.get(url, auth=(
            "anystring", self.api_key), headers=headers)  # type: ignore

        campaigns = response.json()['campaigns']

        reduced_lists = [{'id': campaign['id'], 'name': campaign['name']}
                         for campaign in campaigns]

        return reduced_lists

    def update_campaign_body(self, body, campaign_id):
        url = f'{self.base_url}/campaigns/{campaign_id}/content'
        headers = {"Content-Type": "application/json"}

        data = {
            'html': body
        }

        response = requests.put(url, auth=(
            "anystring", self.api_key), headers=headers, data=json.dumps(data))  # type: ignore

        print(response.json())

        if response.status_code == 200:
            print('Content added successfully')
        else:
            print(f'Error: {response.json()}')

    def send_campaign(self, campaign_id):
        url = f"{self.base_url}/campaigns/{campaign_id}/actions/send"
        response = requests.post(url, auth=(
            "anystring", self.api_key))  # type: ignore
        return response.status_code == 204

    def retrieve_campaign_report(self, campaign_id):
        url = f"{self.base_url}/reports/{campaign_id}"
        headers = {"Content-Type": "application/json"}

        response = requests.get(url, auth=(
            "anystring", self.api_key), headers=headers)  # type: ignore
        return response.json()

    def get_campaign_non_openers(self, campaign_id):
        url = f"{self.base_url}/reports/{campaign_id}/email-activity"
        headers = {"Content-Type": "application/json"}

        response = requests.get(url, auth=(
            "anystring", self.api_key), headers=headers)  # type: ignore
        email_activity = response.json()
        non_openers = []
        for record in email_activity['emails']:
            actions = record['activity']
            if not any(action['action'] == 'open' for action in actions):
                non_openers.append(record['email_address'])

        print(non_openers)
        return non_openers

    def get_campaign_non_clickers(self, campaign_id):
        url = f"{self.base_url}/reports/{campaign_id}/email-activity"
        headers = {"Content-Type": "application/json"}

        response = requests.get(url, auth=(
            "anystring", self.api_key), headers=headers)  # type: ignore
        email_activity = response.json()

        non_clickers = []
        for record in email_activity['emails']:
            actions = record['activity']
            if not any(action['action'] == 'click' for action in actions):
                non_clickers.append(record['email_address'])

        print(non_clickers)
        return non_clickers

    def create_segment(self, list_id, segment_name, segment_conditions):
        url = f"{self.base_url}/lists/{list_id}/segments"
        headers = {"Content-Type": "application/json"}
        data = {
            "name": segment_name,
            "static_segment": segment_conditions
        }

        response = requests.post(url, auth=(
            "anystring", self.api_key), headers=headers, data=json.dumps(data))  # type: ignore
        return response.json()

    def create_campaign_for_segment(self, campaign_type: str, list_id: str, segment_id: int, campaign_title: str, from_name: str, reply_to: str, subject_line: str):
        url = f"{self.base_url}/campaigns"
        headers = {"Content-Type": "application/json"}
        data = {
            "type": campaign_type,
            "recipients": {
                "list_id": list_id,
                "segment_opts": {
                    "saved_segment_id": segment_id
                }
            },
            "settings": {
                "subject_line": subject_line,
                "title": campaign_title,
                "from_name": from_name,
                "reply_to": reply_to
            }
        }

        response = requests.post(url, auth=(
            "anystring", self.api_key), headers=headers, data=json.dumps(data))  # type: ignore
        return response.json()
