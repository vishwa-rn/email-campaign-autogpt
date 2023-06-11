from connectors.mailchimp.main import MailchimpConnector
from content_creator_chain import get_subject_line_for_email_campaign
from utils import get_value_from_pickle, update_pickle_file
import json


def improve_opens_chain():
    connector = MailchimpConnector()
    campaign_id = get_value_from_pickle(key="campaign_id")
    list_id = get_value_from_pickle(key="list_id")
    campaign_title = get_value_from_pickle(key="campaign_title")
    from_name = get_value_from_pickle(key="from_name")
    reply_to = get_value_from_pickle(key="reply_to")

    non_openers = json.dumps(
        connector.get_campaign_non_openers(campaign_id=campaign_id))

    not_opened_segment = connector.create_segment(
        list_id=list_id, segment_name="Not-opened", segment_conditions=non_openers)
    not_opened_segment_id = not_opened_segment['id']
    update_pickle_file("not_opened_segment_id", not_opened_segment_id)

    retry_subject_line = get_subject_line_for_email_campaign()

    retry_campaign_title = "Retry: " + campaign_title
    update_pickle_file(key='retry_campaign_title', value=retry_campaign_title)

    # update the parameters once the memory problem is solved.
    retry_campaign = connector.create_campaign_for_segment(
        campaign_type="REGULAR", list_id=list_id, segment_id=not_opened_segment_id, campaign_title=retry_campaign_title, from_name=from_name, reply_to=reply_to, subject_line=retry_subject_line)

    update_pickle_file("retry_campaign_id", retry_campaign['id'])

    print(connector.send_campaign(campaign_id=retry_campaign['id']))
    return "Started a new campaign with changes to improve opens."

# 1. Get the list of non-openers.
# 2. Create a segment for them.
# 3. Create a new subject line
# 4. Create a new campaign.
# 5. Send the campaign
