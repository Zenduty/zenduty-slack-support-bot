from flask import Flask, request, Response, abort
from utils import (
    return_slack_pop_up,
    get_available_services,
    get_account_users,
    get_available_escalation_policies,
    create_incident,
    SLACK_SIGNING_SECRET,
    APP_PORT,
)
from slack_card import help_block
import json
import hashlib
import hmac
import time

app = Flask(__name__)


@app.before_request
def sign_verification():
    slack_signature = request.headers.get("X-Slack-Signature")
    request_body = request.get_data(as_text=True)
    timestamp = int(request.headers.get("X-Slack-Request-Timestamp"))
    current_time = int(time.time())

    if abs(current_time - timestamp) > 300:
        return abort(400, "Ignore this request.")

    slack_signing_secret = SLACK_SIGNING_SECRET
    if not slack_signing_secret:
        return abort(400, "Slack signing secret is empty.")

    sig_basestring = f"v0:{timestamp}:{request_body}"
    my_signature = (
        "v0="
        + hmac.new(
            bytes(slack_signing_secret, "utf-8"), msg=bytes(sig_basestring, "utf-8"), digestmod=hashlib.sha256
        ).hexdigest()
    )

    if hmac.compare_digest(my_signature.encode("utf-8"), slack_signature.encode("utf-8")):
        return None
    else:
        return abort(400, "Verification failed")


@app.route("/slash_command/", methods=["POST"])
def process_slash_command():
    data = dict(request.form)
    command = data.get("text", False)
    channel_id = data.get("channel_id", False)
    bot_token = data.get("token")
    trigger_id = data.get("trigger_id")
    response_url = data.get("response_url")
    user = data.get("user_name")

    if command not in ["create", "update services", "update users", "update escalations", "help"]:
        return "Invalid Command"
    if command == "help":
        return Response(
            json.dumps({"blocks": help_block}),
            content_type="application/json",
        )
    elif command == "create":
        return_slack_pop_up(channel_id, bot_token, trigger_id)
        message = ""
    elif command == "update services":
        get_available_services(refresh=True)
        message = f"services update triggered by {user}"
    elif command == "update users":
        get_account_users(refresh=True)
        message = f"user update triggered by {user}"
    elif command == "update escalations":
        get_available_escalation_policies(refresh=True)
        message = f"escalation update triggered by {user}"

    return message


@app.route("/interactive/", methods=["POST"])
def procees_submissions():
    payload = dict(request.form)["payload"]
    data = json.loads(payload)
    type = data.get("type")

    if type != "view_submission":
        return "invalid submission"
    callback = data["view"]["callback_id"]
    channel_id = data["view"]["private_metadata"]
    triggered_by = data["user"]["name"]
    triggered_by_id = data["user"]["id"]
    workspace = data["team"]["domain"]
    triggered_by_url = f"https://{workspace}.slack.com/team/{triggered_by_id}"

    if callback == "create_incident":
        values = data["view"]["state"]["values"]
        # assigned_to_id = values["assigned_to_id"]["assigned_to_id"]["selected_option"]["value"]  # noqa
        service = values["service_id"]["service_id"]["selected_option"]["value"]
        title = values["title"]["title"]["value"]
        summary = values["summary"]["summary"]["value"]
        summary += f"\n Triggered by {triggered_by}:{triggered_by_url}"
        urgency = int(values["urgency"]["urgency"]["selected_option"]["value"])
        escalation_policy = None
        assigned_to = None

        # if assigned_to_id:
        #     if "ep-" in assigned_to_id:
        #         escalation_policy = assigned_to_id[assigned_to_id.find("ep-") + 3 :]
        #     elif "user-" in assigned_to_id:
        #         assigned_to = assigned_to_id[assigned_to_id.find("user-") + 5 :]

        # if not escalation_policy and not assigned_to:
        #     return "invalid payload"

        incident_payload = {
            "title": title,
            "summary": summary,
            "user": None,
            "escalation_policy": None,
            "service": service,
            "urgency": urgency,
        }

        create_incident(incident_payload, channel_id, triggered_by)

        return Response(
            json.dumps(
                {
                    "response_action": "clear",
                }
            ),
            content_type="application/json",
        )


if __name__ == "__main__":
    app.run(port=APP_PORT, debug=True)
