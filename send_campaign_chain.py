from connectors.mailchimp.main import MailchimpConnector
import json
connector = MailchimpConnector()

print(json.dumps(connector.send_campaign(campaign_id="fa5d801dee")))

# all_campaigns = json.dumps(connector.get_campaigns())
# print(all_campaigns)
