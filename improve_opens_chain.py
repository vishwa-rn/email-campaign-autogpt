from connectors.mailchimp.main import MailchimpConnector
import json

connector = MailchimpConnector()
non_openers = json.dumps(connector.get_campaign_non_openers("fa5d801dee"))

segment = connector.create_segment(
    list_id="", segment_name="Not-opened", segment_conditions=non_openers)


# 1. Get the list of non-openers.
# 2. Create a segment for them.
# 3. Create a new subject line
# 4. Create a new campaign.
# 5. Send the campaign
