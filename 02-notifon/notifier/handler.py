import os


def post_to_slack(event, context):
    print(event)
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
    print(slack_webhook_url)
    return 