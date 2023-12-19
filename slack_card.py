def construct_slack_card(channel_id, services: dict, escalations: dict, users: dict):
    trimmed_services = {k: services[k] for i, k in enumerate(services) if i < 100}

    slack_card = {
        "private_metadata": channel_id,
        "callback_id": "create_incident",
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Create an incident",
            "emoji": True,
        },
        "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
        "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
        "blocks": [
            {
                "block_id": "service_id",
                "type": "input",
                "label": {
                    "type": "plain_text",
                    "text": "Select your Service",
                    "emoji": True,
                },
                "element": {
                    "type": "static_select",
                    "action_id": "service_id",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": service_name,
                                "emoji": True,
                            },
                            "value": str(service_id),
                        }
                        for service_id, service_name in trimmed_services.items()
                    ],
                },
            },
            {
                "block_id": "urgency",
                "type": "input",
                "label": {
                    "type": "plain_text",
                    "text": "Select Urgency",
                    "emoji": True,
                },
                "element": {
                    "type": "static_select",
                    "action_id": "urgency",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select urgency",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "High",
                                "emoji": True,
                            },
                            "value": "1",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Low",
                                "emoji": True,
                            },
                            "value": "0",
                        },
                    ],
                },
            },
            # {
            #     "block_id": "assigned_to_id",
            #     "type": "input",
            #     "label": {
            #         "type": "plain_text",
            #         "text": "Assign To",
            #         "emoji": True,
            #     },
            #     "element": {
            #         "type": "static_select",
            #         "action_id": "assigned_to_id",
            #         "placeholder": {
            #             "type": "plain_text",
            #             "text": "Select assignee",
            #             "emoji": True,
            #         },
            #         "options": [
            #             {
            #                 "text": {
            #                     "type": "plain_text",
            #                     "text": f"{ep_name}",
            #                     "emoji": True,
            #                 },
            #                 "value": f"ep-{ep_id}",
            #             }
            #             for ep_id, ep_name in escalations.items()
            #         ]
            #         + [
            #             {
            #                 "text": {
            #                     "type": "plain_text",
            #                     "text": f"{fullname}",
            #                     "emoji": True,
            #                 },
            #                 "value": f"user-{username}",
            #             }
            #             for username, fullname in users.items()
            #         ],
            #     },
            # },
            {
                "block_id": "title",
                "type": "input",
                "label": {
                    "type": "plain_text",
                    "text": "Incident Title",
                    "emoji": True,
                },
                "element": {
                    "action_id": "title",
                    "type": "plain_text_input",
                    "multiline": False,
                },
            },
            {
                "block_id": "summary",
                "type": "input",
                "label": {
                    "type": "plain_text",
                    "text": "Summary",
                    "emoji": True,
                },
                "element": {
                    "action_id": "summary",
                    "type": "plain_text_input",
                    "multiline": True,
                },
            },
        ],
    }

    return slack_card


help_block = [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Hey there 👋 I'm the Zenduty bot. I'm here to help you create incidents",
        },
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*1️⃣ Use the `/zenduty-bot create` command* and I'll ask for the incidents details in a dialog. Try it out by using the `/zenduty create` command in this channel.",  # noqa
        },
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*2️⃣ Use the `/zenduty-bot update services` command* and I'll fetch the services to create incidents",  # noqa
        },
    },
]
