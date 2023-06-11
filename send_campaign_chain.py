from connectors.mailchimp.main import MailchimpConnector
from utils import get_value_from_pickle
import json
connector = MailchimpConnector()


def send_campaign_chain():
    campaign_id = get_value_from_pickle(key="campaign_id")
    print(connector.send_campaign(campaign_id=campaign_id))
    return "Started the email campaign for this objective"
