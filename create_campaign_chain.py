# This should create a campaign by taking that information from the pickle file.
# For this, I will store the information which we need after the chain is built.

# 1. Call the API function and then figure out what to add.

from connectors.mailchimp.main import MailchimpConnector
import json
connector = MailchimpConnector()

# print(json.dumps(connector.create_campaign(campaign_type="regular", list_id="4401609701", campaign_title="AutoMakeIt test",
#                                            from_name="Gopal", reply_to="gopal@pixis.ai", subject_line="Hello world")))


print(json.dumps(connector.update_campaign_body(
    body="Body for the mails", campaign_id="fa5d801dee")))

# print(connector.get_lists())

# all_campaigns = json.dumps(connector.get_campaigns())
# print(all_campaigns)
