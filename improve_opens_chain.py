from connectors.mailchimp.main import MailchimpConnector
from content_creator_chain import get_subject_line_for_email_campaign
import json

connector = MailchimpConnector()
non_openers = json.dumps(connector.get_campaign_non_openers("fa5d801dee"))

segment = connector.create_segment(
    list_id="", segment_name="Not-opened", segment_conditions=non_openers)

# update the parameters after the memory problem is fixed.
new_subject_line = get_subject_line_for_email_campaign()

# update the parameters once the memory problem is solved.
new_campaign = connector.create_campaign_for_segment(
    subject_line=new_subject_line)

# update the parameters once the memory problem is solved.
connector.send_campaign()

# 1. Get the list of non-openers.
# 2. Create a segment for them.
# 3. Create a new subject line
# 4. Create a new campaign.
# 5. Send the campaign
