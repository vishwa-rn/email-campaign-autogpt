# This should create a campaign by taking that information from the pickle file.
# For this, I will store the information which we need after the chain is built.

# 1. Call the API function and then figure out what to add.

from connectors.mailchimp.main import MailchimpConnector
from utils import get_value_from_pickle, update_pickle_file


def create_campaign_chain():
    connector = MailchimpConnector()
    list_id = get_value_from_pickle(key='list_id')
    email_body = get_value_from_pickle(key='email_body')
    email_subject = get_value_from_pickle(key="email_subject")
    from_name = get_value_from_pickle(key="from_name")
    user_objective = get_value_from_pickle(key="user_objective")
    update_pickle_file(key="campaign_title", value=user_objective)

    inputs = {
        "reply_to": {
            "question": "What is your REPLY TO mail?",
        }
    }
    answers = {}
    for key, value in inputs.items():
        answer = input(value['question'] + " ")
        answers[key] = answer

    update_pickle_file(key="reply_to", value=answers['reply_to'])

    campaign = connector.create_campaign(campaign_type="regular", list_id=list_id, campaign_title=user_objective,
                                         from_name=from_name, reply_to=answers["reply_to"], subject_line=email_subject)
    campaign_id = campaign['id']
    update_pickle_file(key="campaign_id", value=campaign_id)

    connector.update_campaign_body(
        body=email_body, campaign_id=campaign_id)
    return "Created an email campaign with the leads and the mail content."
