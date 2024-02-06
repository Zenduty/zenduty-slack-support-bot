# Zenduty SlackBot

Slash command Slack bot non-Zenduty users in an organization to declare an incident on Zenduty


## Create your slack bot application


## Prerequisites

- [Python](https://www.python.org/doc/versions/) version 3.8.10 or higher

```bash
# determine python version
python --version
```
- [Zenduty API KEY](https://docs.zenduty.com/api#generating-the-api-key)
- SlackBotToken(SLACK_BOT_TOKEN)
- SlackSigningSecret(SLACK_SIGNING_SECRET)


## Step 1: Creating the Slack Application

1. Go to [Slack Applications](https://api.slack.com/apps) in your web browser.

2. Click the **Create New App** button. 

3. Choose **Create an App From an app manifest**.

4. Open manifest.yml and replace with the copied ngrok url

4. Copy the manifest.yml paste the manifest code click on next and create

5. Your newly created app will appear in the apps list.

## Step 2: Copying Slack Tokens 
1. Go to **Basic Information** in the left side menu.
2. Under App Credentials copy the Signing Secret
3. Go to **OAuth & Permissions** in the left side menu.
4. Under OAuth Tokens for Your Workspace copy the Bot User OAuth Token


## Step 3: Installing the App to Your Workspace

1. Go to **Basic Information** in the left side menu.

2. Click **Install to Workspace**.

3. Click **Allow** to grant permissions for the app.

4. Once installed, the app will be visible in your Slack workspace.

## Additional Notes:
- Replace `[Your specified endpoint URL]/slash_command/` in Step 1, Command 4, with the URL where your bot's functionality is implemented.


## Step 4:  Running Bot Locally

1. If you're running in Docker, paste the copied API Key, Slackbot Token, and Slack Signing Secret in dev.env. If you're in a development environment, paste the keys in utils.py

2. Install required packages 

```
pip install -r requirements.txt
```
```
python app.py
```

#### Running Bot Locally With Docker

```
docker-compose up
```

## Testing the bot using ngrok

* Use ngrok to tunnel the exposed port (ngrok http 8002)
* Copy the ngrok url
* Please refer [Ngrok](https://ngrok.com/)

<img style="width:60%; height:auto;" alt="image" src="https://github.com/Zenduty/zenduty-slack-support-bot/assets/96110782/92f113c6-ef46-41a1-914c-b91b555f4d1f">


