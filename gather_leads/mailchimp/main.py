import requests
from dotenv import load_dotenv
import os


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

        # Create a new list that includes only the id and name of each list
        reduced_lists = [{'id': lst['id'], 'name': lst['name']}
                         for lst in mailing_lists]

        return reduced_lists


# if __name__ == "__main__":
#     # Create a connector object
#     connector = MailchimpConnector()

#     # Call get_lists on the connector object
#     lists = connector.get_lists()

#     # Do something with the lists. For example, print them:
#     print(lists)
