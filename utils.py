import os
import requests
import json
from slack_card import construct_slack_card

API_KEY = os.environ.get("ZENDUTY_API_KEY", "")
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET", "")
APP_PORT = os.environ.get("APP_PORT", 8002)

ZENDUTY_URL = "https://www.zenduty.com"

services_url = f"{ZENDUTY_URL}/api/account/available_incident_services/"
escalation_url = f"{ZENDUTY_URL}/api/account/available_account_eps/"
users_url = f"{ZENDUTY_URL}/api/account/users/"
incident_url = f"{ZENDUTY_URL}/api/incidents/"

headers = {"Authorization": f"token {API_KEY}"}
slack_headers = {
    "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
}


def check_file_exists(file_name):
    os.path.exists(file_name)


def write_into_json_file(file_name, data):
    with open(file_name, "w") as json_file:
        json.dump(data, json_file, indent=4)


def read_from_file(file_name):
    try:
        with open(file_name, "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return None


def fetch_and_cache_data(url, file_name, key_field, name_field):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data_cache = {}
        data = response.json()
        if file_name == "users.json":
            for item in data:
                data_cache[item["user"]["username"]] = f"{item['user']['first_name']} {item['user']['last_name']}"
        else:
            if isinstance(data, dict) and "escalations" in data:
                data = data["escalations"]
            for item in data:
                data_cache[item[key_field]] = item[name_field]
        write_into_json_file(file_name, data_cache)
        return data_cache
    else:
        raise Exception(f"Error fetching data from {url}")


def get_available_services(refresh=False):
    file_name = "services.json"
    data = read_from_file(file_name) if not refresh else None
    if data is None:
        return fetch_and_cache_data(services_url, file_name, "unique_id", "name")
    return data


def get_available_escalation_policies(refresh=False):
    file_name = "escalations.json"
    data = read_from_file(file_name) if not refresh else None
    if data is None:
        return fetch_and_cache_data(escalation_url, file_name, "unique_id", "name")
    return data


def get_account_users(refresh=False):
    file_name = "users.json"
    data = read_from_file(file_name) if not refresh else None
    if data is None:
        return fetch_and_cache_data(users_url, file_name, "unique_id", "name")
    return data


def get_slack_card(channel_id):
    services = get_available_services()
    # escalations = get_available_escalation_policies()
    # users = get_account_users()
    escalations = {}
    users = {}
    slack_card = construct_slack_card(channel_id, services, escalations, users)
    return slack_card


def return_slack_pop_up(channel_id, token, trigger_id):
    slack_card = get_slack_card(channel_id)
    json_body = {
        "token": SLACK_BOT_TOKEN,
        "trigger_id": trigger_id,
        "view": json.dumps(slack_card),
    }

    r = requests.post("https://slack.com/api/views.open", data=json_body)


def create_incident(payload, channel_id, username):
    response = requests.post(incident_url, headers=headers, json=payload)
    status_code = response.status_code
    if status_code == 201:
        data = response.json()
        incident_number = data["incident_number"]
        message = f"Incident created with incident number {incident_number}, triggered by {username}."
    elif response.status_code == 400:
        error = response.json()
        message = f"Incident creation failed error:- {error}, triggered by {username}."
    else:
        message = f"Incident creation failed with status code {status_code}, triggered by {username}."

    json_payload = {"text": message, "channel": channel_id}

    res = requests.post(
        "https://slack.com/api/chat.postMessage",
        json=json_payload,
        headers=slack_headers,
    )
