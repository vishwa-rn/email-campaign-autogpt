from connectors.mailchimp.main import MailchimpConnector
import json
connector = MailchimpConnector()
print(json.dumps(connector.get_campaign_non_clickers("fa5d801dee")))
