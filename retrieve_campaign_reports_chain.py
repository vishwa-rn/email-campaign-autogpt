from connectors.mailchimp.main import MailchimpConnector
import json


def retrieve_campaign_reports_chain(objective: str):
    connector = MailchimpConnector()
    report = connector.retrieve_campaign_report("fa5d801dee")
    report = {
        "emails_sent": report["emails_sent"],
        "opens": {
            "total": report["opens"]["opens_total"],
            "unique": report["opens"]["unique_opens"],
            "our_rate": report["opens"]["open_rate"],
            "industry_rate": report["industry_stats"]["open_rate"],
            "deviation_from_industry": report["industry_stats"]["open_rate"] - report["opens"]["open_rate"]
        },
        "clicks": {
            "total": report["clicks"]["clicks_total"],
            "unique": report["clicks"]["unique_clicks"],
            "our_rate": report["clicks"]["click_rate"],
            "industry_rate": report["industry_stats"]["click_rate"],
            "deviation_from_industry": report["industry_stats"]["click_rate"] - report["clicks"]["click_rate"]
        }
    }

    return f"""Deviation of opens from the industry is {round(report['opens']["deviation_from_industry"]*100, 2)}% and the deviation of clicks from the industry is {round(report['clicks']['deviation_from_industry']*100, 2)}%"""


# print(retrieve_campaign_reports_chain("test"))
