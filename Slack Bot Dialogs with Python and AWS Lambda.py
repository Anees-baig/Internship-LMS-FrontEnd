import os
import logging
import urllib
import boto3
from slackclient import SlackClient

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)

# Grab the Bot OAuth token from the environment + slack verification
BOT_TOKEN = os.environ["BOT_TOKEN"]
SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]
slack_client = SlackClient(BOT_TOKEN)

SLACK_URL = "https://slack.com/api/dialog.open"

def lambda_handler(data, context):
    ''' Entry point for API Gateway '''
    slack_event = data['event']

    if "bot_id" in slack_event:
        logging.warn("Ignore bot event")

    else:
        channel_id = slack_event["channel"]

        support_form = slack_client.api_call(
            "dialog.open",
            trigger_id = slack_event["trigger_id"],
            dialog = {
                "title": "AWS Support Ticket",
                "submit_label": "Submit",
                "callback_id": "support_form",
                "elements": [
                    {
                        "label": "Subject",
                        "type": "text",
                        "name": "subject",
                        "placeholder": "Support Case Subject"
                    },
                    {
                        "label": "Description",
                        "type": "textarea",
                        "name": "body",
                        "placeholder": "Describe the issue you would like to open a support case about"
                    },
                    {
                        "type": "select",
                        "label": "What is your issue type?",
                        "name": "issueType",
                        "options": [
                            {
                                "label": "Customer Service",
                                "value": "customerservice"
                            },
                            {
                                "label": "Technical",
                                "value": "technical"
                            }
                        ]
                    },
                    {
                        "label": "What is your severity level?",
                        "type": "select",
                        "name": "serverity",
                        "options": [
                            {
                                "label": "5 - General Guidance",
                                "value": "5"
                            },
                            {
                                "label": "4 - System Impaired",
                                "value": "4"
                            },
                            {
                                "label": "3 - Production System Impaired",
                                "value": "3"
                            },
                            {
                                "label": "2 - Production System Down",
                                "value": "2"
                            },
                            {
                                "label": "1 - Business-critical System Down",
                                "value": "1"
                            }
                        ]
                    },
                    {
                        "label": "Service Code",
                        "type": "text",
                        "name": "serviceCode"
                    },
                    {
                        "label": "Category Code",
                        "type": "text",
                        "name": "categoryCode"
                    },
                    {
                        "label": "Please choose your language",
                        "type": "select",
                        "name": "language",
                        "options": [
                            {
                                "label": "English",
                                "value": "english"
                            },
                            {
                                "label": "Japanese",
                                "value": "japanese"
                            }
                        ]
                    },
                    {
                        "label": "What is your attachement set id?",
                        "type": "text",
                        "name": "attachementSetId"
                    },
                    {
                        "label": "Please enter the emails you want cc'd on this case:",
                        "type": "textarea",
                        "name": "ccEmailAddresses"
                    }
                ]
            }
        })

        data = urllib.parse.urlencode(
            (
                ("token", BOT_TOKEN),
                ("channel", channel_id),
                ("dialog", support_form)
            )
        )

        # Construct the HTTP request that will be sent to the Slack API.
        request = urllib.request.Request(
            SLACK_URL, 
            data=data, 
            method="POST"
        )
        # Add a header mentioning that the text is URL-encoded.
        request.add_header(
            "Content-Type", 
            "application/x-www-form-urlencoded"
        )

        # Fire off the request!
        urllib.request.urlopen(request).read()

    # Everything went fine.
    return "200 OK"
